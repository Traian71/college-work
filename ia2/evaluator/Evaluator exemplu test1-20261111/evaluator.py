#!/usr/bin/env python3
"""AI2 evaluator: extracts notebook definitions, grades preprocessing, model and performance.

Required shared files in the same directory as this script:
  train1.npz, test1.npz, expected_train1.npz, expected_test1.npz
  train2.npz, test2.npz, expected_train2.npz, expected_test2.npz
Each student subfolder:
  S1.ipynb, S2.ipynb, model1.pth, model2.pth

Run: python evaluator.py [--device cpu|cuda|auto] [--preprocess-timeout 60]
Defaults: S1 atol=1e-1, S2 atol=1e-2, rtol=0.
Only the preprocessing subprocess has a timeout; model/accuracy are untimed.
Output: evaluator_checks.csv, one row per student; scores + short failure reasons.

Notebooks are parsed using AST; training loops are not executed. Student code
is still untrusted Python: subprocess timeouts are NOT a security sandbox.
Use OS/container isolation for untrusted submissions.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


DATA_FILES = (
    "train1.npz", "test1.npz", "train2.npz", "test2.npz",
    "expected_train1.npz", "expected_test1.npz",
    "expected_train2.npz", "expected_test2.npz",
)
STUDENT_FILES = ("S1.ipynb", "S2.ipynb", "model1.pth", "model2.pth")
PROBE_MARKER = "__AI2_CHECK_RESULT__="


def is_literal_assignment(node: ast.stmt) -> bool:
    if isinstance(node, ast.Assign):
        if not all(isinstance(target, ast.Name) for target in node.targets):
            return False
    elif isinstance(node, ast.AnnAssign):
        if not isinstance(node.target, ast.Name) or node.value is None:
            return False
    else:
        return False
    try:
        ast.literal_eval(node.value)
    except (ValueError, TypeError, SyntaxError, RecursionError):
        return False
    return True


def clean_cell(source: str) -> str:
    """Remove standalone notebook shell commands and magic commands."""
    lines = source.splitlines(keepends=True)
    if any(line.lstrip().startswith("%%") for line in lines):
        return ""
    cleaned = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(("%", "!", "?")) or stripped.startswith(
            ("get_ipython().run_line_magic(", "get_ipython().system(")
        ):
            cleaned.append("\n")
        else:
            cleaned.append(line)
    return "".join(cleaned)


def extract_notebook(notebook_path: Path, output_path: Path) -> dict[str, Any]:
    """Keep imports, top-level functions/classes (including helpers), constants.

    Cell bodies outside those definitions are never executed by this function.
    Top-level training code, dataset loads, and model saving are omitted.
    """
    with notebook_path.open("r", encoding="utf-8") as f:
        notebook = json.load(f)
    if not isinstance(notebook.get("cells"), list):
        raise ValueError("Missing/invalid notebook cells")

    retained: list[ast.stmt] = []
    defined: set[str] = set()
    omitted = 0

    for idx, cell in enumerate(notebook["cells"], start=1):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        if not isinstance(source, str):
            raise ValueError(f"Cell {idx}: source is not a string")
        source = clean_cell(source)
        if not source.strip():
            continue
        try:
            tree = ast.parse(source, filename=f"{notebook_path.name}:cell{idx}")
        except SyntaxError as exc:
            raise SyntaxError(f"Cell {idx}, line {exc.lineno}: {exc.msg}") from exc

        for node in tree.body:
            if isinstance(node, (
                ast.Import, ast.ImportFrom,
                ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
            )):
                retained.append(node)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    defined.add(node.name)
            elif is_literal_assignment(node):
                retained.append(node)
            else:
                omitted += 1

    future = [n for n in retained if isinstance(n, ast.ImportFrom) and n.module == "__future__"]
    retained = future + [n for n in retained if n not in future]
    module = ast.fix_missing_locations(ast.Module(body=retained, type_ignores=[]))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "# Extracted from " + notebook_path.name + " (training code omitted).\n\n"
        + ast.unparse(module) + "\n", encoding="utf-8"
    )
    return {
        "omitted_statements": omitted,
        "preprocess_defined": "preprocess" in defined,
        "Model_defined": "Model" in defined,
    }


# Executed in a new Python interpreter, NOT in the evaluator process.
# Imports the extracted module, then optionally invokes preprocess() once.
# Expected datasets are read in the same process so no large arrays need to
# be serialized over the subprocess boundary.
WORKER = r'''
import importlib.util
import inspect
import json
import sys
import traceback
from pathlib import Path

import numpy as np
import torch

MARKER = "__AI2_CHECK_RESULT__="


def emit(data):
    print(MARKER + json.dumps(data, allow_nan=False), flush=True)


def to_numpy(value, name):
    """Support numpy, CPU/CUDA torch tensors, or lists/tuples of either."""
    if isinstance(value, torch.Tensor):
        arr = value.detach().cpu().numpy()
    elif isinstance(value, np.ndarray):
        arr = value
        if arr.dtype == object:
            # A numpy object array can also be a list of individual images.
            arr = np.stack([to_numpy(v, name) for v in arr], axis=0)
    elif isinstance(value, (list, tuple)):
        if not value:
            arr = np.asarray(value)
        elif all(isinstance(v, torch.Tensor) for v in value):
            arr = torch.stack([v.detach().cpu() for v in value]).numpy()
        elif any(isinstance(v, (torch.Tensor, np.ndarray)) for v in value):
            arr = np.stack([to_numpy(v, name) for v in value], axis=0)
        else:
            arr = np.asarray(value)
    else:
        raise TypeError(f"{name}: expected ndarray/tensor/list, got {type(value).__name__}")

    if arr.dtype.kind not in "biuf":
        raise TypeError(f"{name}: non-numeric array dtype {arr.dtype}")
    return arr


def unpack_preprocess(value):
    """Starter notebook uses ((X_train,y_train),(X_test,y_test)); accept flat 4 too."""
    if not isinstance(value, (tuple, list)):
        raise TypeError("preprocess must return two (X,y) pairs or four values")
    if len(value) == 2:
        train, test = value
        if not isinstance(train, (tuple, list)) or len(train) != 2:
            raise ValueError("First return element must be (X_train, y_train)")
        if not isinstance(test, (tuple, list)) or len(test) != 2:
            raise ValueError("Second return element must be (X_test, y_test)")
        return train[0], train[1], test[0], test[1]
    if len(value) == 4:
        return value[0], value[1], value[2], value[3]
    raise ValueError("preprocess must return two (X,y) pairs or four values")


def exact_labels(actual, expected):
    return actual.shape == expected.shape and bool(np.array_equal(actual, expected))


def near(actual, expected, atol):
    """Absolute tolerance only: rtol=0. Chunked to avoid giant temporaries."""
    if actual.shape != expected.shape:
        return False
    if actual.dtype.kind not in "biuf" or expected.dtype.kind not in "biuf":
        return False
    if actual.ndim == 0:
        return bool(np.isfinite(actual) and np.isfinite(expected)
                    and np.abs(actual - expected) <= atol)
    for i in range(0, len(actual), 512):
        a = np.asarray(actual[i:i+512], dtype=np.float64)
        b = np.asarray(expected[i:i+512], dtype=np.float64)
        if not np.allclose(a, b, atol=atol, rtol=0.0, equal_nan=False):
            return False
    return True


def shape(value):
    return "x".join(str(v) for v in value.shape)


def load_reference(path):
    with np.load(path, allow_pickle=False) as file:
        if "X" not in file or "y" not in file:
            raise ValueError(f"{path.name} must contain 'X' and 'y'")
        return file["X"], file["y"]


def s1_signs(actual, expected):
    """PCA eigenvector signs are mathematically arbitrary.

    Compute signs ON TRAINING, then apply those SAME signs to test features.
    Does not accept arbitrary feature permutations or unrelated projections.
    """
    if actual.shape != expected.shape or actual.ndim != 2:
        return None
    # At most 32 components; avoids a second 1600x32 array.
    correlations = np.einsum("ij,ij->j", actual, expected, dtype=np.float64)
    return np.where(correlations < 0, -1.0, 1.0)


def signed_near(actual, reference, signs, atol):
    if signs is None or actual.shape != reference.shape:
        return False
    if actual.ndim != 2 or actual.shape[1] != len(signs):
        return False
    for i in range(0, len(actual), 512):
        a = np.asarray(actual[i:i+512], dtype=np.float64)
        b = np.asarray(reference[i:i+512], dtype=np.float64)
        if not np.allclose(a * signs, b, atol=atol, rtol=0.0, equal_nan=False):
            return False
    return True


def standardize_raw(raw, mean, std):
    return (np.asarray(raw, dtype=np.float64) - mean) / std


def grade_s1(Xtr, ytr, Xte, yte, root, atol):
    Etr, eytr = load_reference(root / "expected_train1.npz")
    Ete, eyte = load_reference(root / "expected_test1.npz")
    labels_train = exact_labels(ytr, eytr)
    labels_test = exact_labels(yte, eyte)

    # Full PCA-whitened output; allow component-wise sign flips.
    signs = s1_signs(Xtr, Etr)
    train_final = signed_near(Xtr, Etr, signs, atol) and labels_train
    test_final = signed_near(Xte, Ete, signs, atol) and labels_test

    # If student stopped after standardization (216 original features), we
    # can still award its 1 point; also test transfer point if appropriate.
    train_standardized = False
    test_standardized = False
    if Xtr.ndim == 2 and Xtr.shape[1] != Etr.shape[1]:
        with np.load(root / "train1.npz", allow_pickle=False) as f:
            raw_train = f["X"]
        if raw_train.shape == Xtr.shape:
            raw_train = raw_train.astype(np.float64)
            mean, std = raw_train.mean(axis=0), raw_train.std(axis=0)
            std[std == 0] = 1.0
            train_standardized = near(Xtr, standardize_raw(raw_train, mean, std), atol) and labels_train
            if train_standardized:
                with np.load(root / "test1.npz", allow_pickle=False) as f:
                    raw_test = f["X"]
                if raw_test.shape == Xte.shape:
                    test_standardized = (
                        near(Xte, standardize_raw(raw_test, mean, std), atol)
                        and labels_test
                    )

    standardized_point = bool(train_final or train_standardized)
    pca_points = 2 if train_final else 0
    test_point = bool((train_final and test_final) or (train_standardized and test_standardized))
    return {
        "normalize_ok": standardized_point,
        "pca_whitening_ok": bool(train_final),
        "test_transform_ok": test_point,
        "train_labels_ok": labels_train,
        "test_labels_ok": labels_test,
        "train_shape": shape(Xtr),
        "test_shape": shape(Xte),
        "train_matches_expected": train_final,
        "test_matches_expected": bool(train_final and test_final),
        "points": int(standardized_point) + pca_points + int(test_point),
        "max_points": 4,
        "details": "PCA columns may differ in sign; test uses the training-derived signs",
    }


def spatial_images(x):
    """View NCHW/NHWC/NHW grayscale images as NHW (for resize point)."""
    if x.ndim == 3:
        return x
    if x.ndim == 4 and x.shape[1] == 1:
        return x[:, 0, :, :]
    if x.ndim == 4 and x.shape[-1] == 1:
        return x[:, :, :, 0]
    return None


def resize_matches(actual, expected, atol):
    a, e = spatial_images(actual), spatial_images(expected)
    if a is None or e is None or a.shape != e.shape:
        return False
    if a.shape[-2:] != (32, 32):
        return False
    # Allow student to return 0..255 images when only bilinear resize is done.
    # Expected files are normalized to 0..1; use one global scale (not per image).
    scale = 255.0 if float(np.max(a)) > 1.0 + atol else 1.0
    if scale == 1.0:
        return near(a, e, atol)
    for i in range(0, len(a), 512):
        aa = np.asarray(a[i:i+512], dtype=np.float64) / scale
        ee = np.asarray(e[i:i+512], dtype=np.float64)
        if not np.allclose(aa, ee, atol=atol, rtol=0.0, equal_nan=False):
            return False
    return True


def grade_s2(Xtr, ytr, Xte, yte, root, atol):
    Etr, eytr = load_reference(root / "expected_train2.npz")
    Ete, eyte = load_reference(root / "expected_test2.npz")
    labels_train = exact_labels(ytr, eytr)
    labels_test = exact_labels(yte, eyte)

    resize_ok = (
        labels_train and labels_test
        and resize_matches(Xtr, Etr, atol)
        and resize_matches(Xte, Ete, atol)
    )
    # Normalization + channel must match the expected NCHW tensor layout.
    norm_ok = (
        resize_ok
        and Xtr.shape == Etr.shape and Xte.shape == Ete.shape
        and Xtr.ndim == 4 and Xtr.shape[1] == 1
        and np.isfinite(Xtr).all() and np.isfinite(Xte).all()
        and float(np.min(Xtr)) >= -atol and float(np.max(Xtr)) <= 1 + atol
        and float(np.min(Xte)) >= -atol and float(np.max(Xte)) <= 1 + atol
        and near(Xtr, Etr, atol) and near(Xte, Ete, atol)
    )
    return {
        "bilinear_resize_ok": bool(resize_ok),
        "normalize_channel_ok": bool(norm_ok),
        "train_labels_ok": labels_train,
        "test_labels_ok": labels_test,
        "train_shape": shape(Xtr),
        "test_shape": shape(Xte),
        "train_matches_expected": bool(norm_ok),
        "test_matches_expected": bool(norm_ok),
        "points": int(resize_ok) + int(norm_ok),
        "max_points": 2,
        "details": "Resize accepts NHW/NCHW/NHWC and 0..1 or 0..255; full solution needs NCHW in 0..1",
    }




def issue_from_preprocess(grading, subject):
    issues = []
    if not grading.get('train_labels_ok') or not grading.get('test_labels_ok'):
        issues.append('wrong labels')
    if subject == 1:
        if not grading['normalize_ok']:
            issues.append('normalization mismatch')
        if not grading['pca_whitening_ok']:
            issues.append('PCA: wrong shape / atol exceeded')
        if not grading['test_transform_ok']:
            issues.append('test: wrong shape / atol exceeded')
    else:
        if not grading['bilinear_resize_ok']:
            issues.append('resize: wrong shape / atol exceeded')
        if not grading['normalize_channel_ok']:
            issues.append('normalization/channel mismatch')
    return ', '.join(issues) if issues else ''


def issue_from_exception(exc):
    if isinstance(exc, (ValueError, TypeError, IndexError, KeyError)):
        msg = str(exc).replace('\n', ' ')
        if len(msg) > 120:
            msg = msg[:117] + '...'
        return 'wrong return: ' + msg
    return type(exc).__name__ + ': ' + str(exc).replace('\n', ' ')[:120]


def grade_model(model_class, subject, device):
    max_points = 4 if subject == 1 else 5
    if not inspect.isclass(model_class):
        return None, {'points': 0, 'max_points': max_points, 'reason': 'missing Model class'}
    try:
        model = model_class()
        if not isinstance(model, torch.nn.Module):
            raise TypeError('Model() must be a torch.nn.Module')
        model = model.to(device)
        model.eval()
        with torch.inference_mode():
            probe = torch.zeros((2, 32) if subject == 1 else (2, 1, 32, 32),
                                dtype=torch.float32, device=device)
            logits = model(probe)
            if not isinstance(logits, torch.Tensor) or logits.ndim != 2 or logits.shape[0] != 2 or logits.shape[1] < 10:
                raise ValueError('wrong forward output shape: expected (batch, >=10)')
            if not bool(torch.isfinite(logits).all().item()):
                raise ValueError('forward output contains NaN/inf')
        linear = [m for m in model.modules() if isinstance(m, torch.nn.Linear)]
        conv = [m for m in model.modules() if isinstance(m, torch.nn.Conv2d)]
        nparams = sum(p.numel() for p in model.parameters() if p.requires_grad)
        if subject == 1:
            # Only modules can be reliably checked by static inspection.
            activation_types = (
                torch.nn.ReLU, torch.nn.ReLU6, torch.nn.LeakyReLU,
                torch.nn.ELU, torch.nn.SELU, torch.nn.CELU,
                torch.nn.GELU, torch.nn.Sigmoid, torch.nn.Tanh,
                torch.nn.SiLU, torch.nn.Mish, torch.nn.Softplus,
                torch.nn.Softsign, torch.nn.Hardtanh, torch.nn.Hardsigmoid,
                torch.nn.Hardswish, torch.nn.PReLU, torch.nn.RReLU,
                torch.nn.Softmax, torch.nn.LogSoftmax, torch.nn.GLU,
            )
            activation_names = {type(m).__name__.lower() for m in model.modules()
                                if isinstance(m, activation_types)}
            # Also credit activations written as F.relu(x), torch.tanh(x), etc.
            # Static inspection of the Model class avoids running student helpers.
            try:
                import ast
                import textwrap
                class_tree = ast.parse(textwrap.dedent(inspect.getsource(model_class)))
                functional_names = {
                    'relu', 'relu6', 'leaky_relu', 'elu', 'selu', 'celu',
                    'gelu', 'sigmoid', 'tanh', 'silu', 'mish', 'softplus',
                    'softsign', 'hardtanh', 'hardsigmoid', 'hardswish',
                    'prelu', 'rrelu', 'softmax', 'log_softmax', 'glu',
                }
                for call in ast.walk(class_tree):
                    if isinstance(call, ast.Call):
                        fn = call.func
                        name = (fn.attr if isinstance(fn, ast.Attribute) else
                                fn.id if isinstance(fn, ast.Name) else '')
                        if name.lower() in functional_names:
                            activation_names.add(name.lower().replace('_', ''))
            except (OSError, TypeError, SyntaxError):
                pass
            criteria = [
                ('<3 linear', len(linear) >= 3),
                ('<2 activation types', len(activation_names) >= 2),
                ('no expanding linear', any(m.out_features > m.in_features for m in linear)),
                ('>20000 params', nparams <= 20000),
            ]
        else:
            criteria = [
                ('<2 linear', len(linear) >= 2),
                ('<2 conv', len(conv) >= 2),
                ('no halving linear', any(2*m.out_features == m.in_features for m in linear)),
                ('no equal-channel conv', any(m.in_channels == m.out_channels for m in conv)),
                ('>200000 params', nparams <= 200000),
            ]
        points = sum(int(passed) for _, passed in criteria)
        reasons = [reason for reason, passed in criteria if not passed]
        return model, {
            'points': points, 'max_points': max_points,
            'reason': ', '.join(reasons), 'parameters': nparams,
            'linear_count': len(linear), 'conv_count': len(conv),
        }
    except BaseException as exc:
        return None, {'points': 0, 'max_points': max_points,
                      'reason': 'Model/forward failed: ' + issue_from_exception(exc)}


def evaluate_accuracy(model, weights_path, X_test, y_test, device, batch_size):
    if not weights_path.is_file():
        raise FileNotFoundError('missing model weights')
    # weights_only=True avoids loading arbitrary pickled Python objects.
    state = torch.load(str(weights_path), map_location='cpu', weights_only=True)
    if isinstance(state, dict) and 'model_state_dict' in state:
        state = state['model_state_dict']
    elif isinstance(state, dict) and 'state_dict' in state:
        state = state['state_dict']
    if not isinstance(state, dict):
        raise TypeError('model weights must contain a state_dict')
    model.load_state_dict(state, strict=True)
    model.eval()

    if y_test.ndim != 1 or len(y_test) != len(X_test):
        raise ValueError('wrong test label shape')
    correct, total = 0, 0
    with torch.inference_mode():
        for start in range(0, len(X_test), batch_size):
            x = torch.as_tensor(np.asarray(X_test[start:start+batch_size]),
                                dtype=torch.float32, device=device)
            y = torch.as_tensor(np.asarray(y_test[start:start+batch_size]),
                                dtype=torch.long, device=device)
            out = model(x)
            if not isinstance(out, torch.Tensor) or out.ndim != 2 or out.shape[0] != len(y):
                raise ValueError('wrong forward output shape')
            loss = torch.nn.functional.cross_entropy(out, y)
            if not torch.isfinite(loss).item():
                raise ValueError('test loss is not finite')
            correct += (out.argmax(dim=1) == y).sum().item()
            total += len(y)
    if not total:
        raise ValueError('empty test set')
    return correct / total


def main():
    stage = sys.argv[1]
    module_path = Path(sys.argv[2])
    root = Path(sys.argv[3])
    subject = int(sys.argv[4])
    atol = float(sys.argv[5])
    student_dir = Path(sys.argv[6])
    weights_path = Path(sys.argv[7])
    requested_device = sys.argv[8]
    batch_size = int(sys.argv[9])
    cache_path = Path(sys.argv[10])
    preprocess_full = sys.argv[11] == '1'
    sys.path.insert(0, str(student_dir))

    if stage not in ('preprocess', 'model'):
        raise ValueError('Unknown worker stage')
    if requested_device == 'auto':
        requested_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if requested_device == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA requested but unavailable')
    device = torch.device(requested_device)

    maximum = (4 if subject == 1 else 2) if stage == 'preprocess' else (4 if subject == 1 else 5)
    result_key = 'preprocess' if stage == 'preprocess' else 'model'
    probe = {
        'import_ok': False,
        result_key: {'points': 0, 'max_points': maximum, 'reason': 'not run'},
    }
    if stage == 'model':
        probe['performance'] = {
            'points': 0, 'max_points': 2 if subject == 1 else 3,
            'reason': 'not eligible',
        }

    try:
        spec = importlib.util.spec_from_file_location('_ai2_submission', module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        probe['import_ok'] = True
    except BaseException as exc:
        probe[result_key]['reason'] = 'import failed: ' + issue_from_exception(exc)
        emit(probe)
        return

    if stage == 'preprocess':
        preprocess = getattr(module, 'preprocess', None)
        if not callable(preprocess):
            probe['preprocess']['reason'] = 'missing preprocess function'
        else:
            try:
                value = preprocess(str(root / f'train{subject}.npz'), str(root / f'test{subject}.npz'))
                Xtr, ytr, Xte, yte = unpack_preprocess(value)
                Xtr = to_numpy(Xtr, 'X_train')
                ytr = to_numpy(ytr, 'y_train')
                Xte = to_numpy(Xte, 'X_test')
                yte = to_numpy(yte, 'y_test')
                if Xtr.ndim < 2 or Xte.ndim < 2:
                    raise ValueError('X must have at least 2 dimensions')
                grading = (grade_s1(Xtr, ytr, Xte, yte, root, atol)
                           if subject == 1 else grade_s2(Xtr, ytr, Xte, yte, root, atol))
                probe['preprocess'] = {
                    'points': grading['points'], 'max_points': grading['max_points'],
                    'reason': issue_from_preprocess(grading, subject),
                }
                # The model stage must use the student's features, not the
                # reference ones (PCA component signs can be different).
                if grading['points'] == grading['max_points']:
                    np.savez(cache_path, X=Xte, y=yte)
            except BaseException as exc:
                probe['preprocess']['reason'] = issue_from_exception(exc)
        emit(probe)
        return

    # Entirely separate process: this runs even if preprocessing times out.
    model, mg = grade_model(getattr(module, 'Model', None), subject, device)
    probe['model'] = mg
    if preprocess_full and mg['points'] == mg['max_points']:
        try:
            with np.load(cache_path, allow_pickle=False) as file:
                X_test, y_test = file['X'], file['y']
            accuracy = evaluate_accuracy(model, weights_path, X_test, y_test, device, batch_size)
            thresholds = (0.90, 0.95) if subject == 1 else (0.90, 0.94, 0.98)
            perf_points = sum(accuracy + 1e-12 >= threshold for threshold in thresholds)
            probe['performance'] = {
                'points': perf_points, 'max_points': len(thresholds),
                'accuracy': round(accuracy * 100, 4),
                'reason': '' if perf_points == len(thresholds) else 'accuracy below threshold',
            }
        except BaseException as exc:
            probe['performance']['reason'] = 'test failed: ' + issue_from_exception(exc)
    emit(probe)

try:
    main()
except BaseException as exc:
    emit({'import_ok': False, 'error': issue_from_exception(exc)})
'''


def run_worker(stage, extracted_path, root, student, subject, weights, cache_path, args, working_dir, preprocess_full=False):
    atol = args.atol_s1 if subject == 1 else args.atol_s2
    if args.atol is not None:
        atol = args.atol   # Backward-compatible override for both subjects.
    cmd = [
        sys.executable, '-I', '-B', '-c', WORKER,
        stage, str(extracted_path), str(root), str(subject), str(atol),
        str(student), str(weights), args.device, str(args.batch_size),
        str(cache_path), '1' if preprocess_full else '0',
    ]
    env = os.environ.copy()
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[name] = str(args.threads)
    timeout = args.preprocess_timeout if stage == 'preprocess' else None
    try:
        result = subprocess.run(
            cmd, cwd=working_dir, capture_output=True, text=True, env=env,
            errors='replace', timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return None, f'timeout ({timeout}s)'
    except OSError as exc:
        return None, f'worker failed: {exc}'

    for line in reversed(result.stdout.splitlines()):
        if line.startswith(PROBE_MARKER):
            try:
                payload = json.loads(line[len(PROBE_MARKER):])
            except json.JSONDecodeError:
                return None, 'invalid worker result'
            if result.returncode:
                return None, f'worker exited {result.returncode}: {result.stderr[-180:]}'
            return payload, ''
    return None, ('no worker result: ' + (result.stderr or result.stdout)[-200:]).replace('\n', ' ')


def list_students(root, all_subdirs):
    ignored = {'__pycache__', '.ipynb_checkpoints', '_evaluator_extracted',
               'sample_data', '_tmp', '.git'}
    return [
        folder for folder in sorted(root.iterdir(), key=lambda p: p.name.lower())
        if folder.is_dir() and folder.name not in ignored
        and not folder.name.startswith('.')
        and (all_subdirs or any((folder / name).is_file() for name in STUDENT_FILES))
    ]


def empty_result(points, reason):
    return {'points': 0, 'max_points': points, 'reason': reason}


def shorten(text, limit=85):
    text = ' '.join(str(text).split())
    return text[:limit - 3] + '...' if len(text) > limit else text


def format_score(data):
    score = int(data['points'])
    maximum = int(data['max_points'])
    reason = shorten(data.get('reason', ''))
    if 'accuracy' in data:
        acc = f"{float(data['accuracy']):.2f}%"
        reason = (acc + ('; ' + reason if reason else ''))
    return f'{score}/{maximum}' + (f' ({reason})' if reason else '')


def check_subject(student, subject, root, tmp, args):
    maximum_prep = 4 if subject == 1 else 2
    maximum_model = 4 if subject == 1 else 5
    maximum_perf = 2 if subject == 1 else 3
    notebook = student / f'S{subject}.ipynb'
    weights = student / f'model{subject}.pth'
    result = {
        'preprocess': empty_result(maximum_prep, 'not evaluated'),
        'model': empty_result(maximum_model, 'not evaluated'),
        'performance': empty_result(maximum_perf, 'not eligible'),
    }
    if not notebook.is_file():
        result['preprocess']['reason'] = 'missing S' + str(subject) + '.ipynb'
        result['model']['reason'] = 'missing S' + str(subject) + '.ipynb'
        return result

    missing_data = [fn for fn in (f'train{subject}.npz', f'test{subject}.npz',
                                   f'expected_train{subject}.npz', f'expected_test{subject}.npz')
                    if not (root / fn).is_file()]

    extracted = tmp / student.name / f'S{subject}_extracted.py'
    working_dir = tmp / student.name / f'S{subject}'
    working_dir.mkdir(parents=True, exist_ok=True)
    cache_path = working_dir / 'preprocessed_test.npz'
    try:
        extract_notebook(notebook, extracted)
        if args.keep_extracted:
            target = root / '_evaluator_extracted' / student.name / extracted.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(extracted, target)
    except Exception as exc:
        message = 'extraction failed: ' + shorten(f'{type(exc).__name__}: {exc}', 120)
        result['preprocess']['reason'] = message
        result['model']['reason'] = message
        return result

    # Preprocessing has its own 60-second subprocess deadline.
    if missing_data:
        result['preprocess'] = empty_result(maximum_prep, 'missing shared data')
    else:
        prep_payload, prep_error = run_worker(
            'preprocess', extracted, root, student, subject, weights, cache_path,
            args, working_dir,
        )
        if prep_error:
            result['preprocess'] = empty_result(maximum_prep, prep_error)
        elif prep_payload and isinstance(prep_payload.get('preprocess'), dict):
            result['preprocess'] = prep_payload['preprocess']
        else:
            result['preprocess'] = empty_result(
                maximum_prep, shorten((prep_payload or {}).get('error', 'preprocess import failed'), 150))

    prep_full = (
        result['preprocess']['points'] == maximum_prep and cache_path.is_file()
    )
    # Model structure is always graded, even when preprocess timed out or failed.
    model_payload, model_error = run_worker(
        'model', extracted, root, student, subject, weights, cache_path,
        args, working_dir, preprocess_full=prep_full,
    )
    if model_error:
        result['model'] = empty_result(maximum_model, model_error)
        result['performance'] = empty_result(maximum_perf, model_error)
    elif model_payload and isinstance(model_payload.get('model'), dict):
        result['model'] = model_payload['model']
        if isinstance(model_payload.get('performance'), dict):
            result['performance'] = model_payload['performance']
    else:
        result['model'] = empty_result(
            maximum_model, shorten((model_payload or {}).get('error', 'model import failed'), 150))
    if missing_data:
        result['performance'] = empty_result(maximum_perf, 'missing shared data')
    return result


def main():
    parser = argparse.ArgumentParser(description='AI2 grading: preprocessing, model structure, test accuracy')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--report', type=Path, default=None)
    parser.add_argument('--atol-s1', type=float, default=1e-1)
    parser.add_argument('--atol-s2', type=float, default=1e-2)
    parser.add_argument('--atol', type=float, default=None,
                        help='Optional override of both subject tolerances')
    parser.add_argument('--device', choices=['auto', 'cpu', 'cuda'], default='auto')
    parser.add_argument('--batch-size', type=int, default=256)
    parser.add_argument('--threads', type=int, default=2, help='CPU threads per worker')
    parser.add_argument('--preprocess-timeout', type=int, default=60,
                        help='Maximum seconds for preprocessing and its comparison, per subject')
    parser.add_argument('--keep-extracted', action='store_true')
    parser.add_argument('--all-subdirs', action='store_true')
    args = parser.parse_args()
    if (args.atol_s1 < 0 or args.atol_s2 < 0 or
        (args.atol is not None and args.atol < 0) or
        args.batch_size <= 0 or args.preprocess_timeout <= 0 or args.threads <= 0):
        parser.error('tolerances must be nonnegative; batch size, threads and preprocessing timeout must be positive')
    root = args.root.resolve()
    if not root.is_dir():
        parser.error('Root directory does not exist: ' + str(root))
    report = args.report or root / 'evaluator_checks.csv'
    if not report.is_absolute():
        report = (Path.cwd() / report).resolve()

    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('AI2 evaluator -- full grading')
    print(f'Root: {root} | device: {args.device} (auto={device})')
    t1, t2 = ((args.atol, args.atol) if args.atol is not None else (args.atol_s1, args.atol_s2))
    print(f'Tolerance: S1 atol={t1:g}, S2 atol={t2:g}, rtol=0 | preprocess timeout={args.preprocess_timeout}s')
    missing = [name for name in DATA_FILES if not (root / name).is_file()]
    if missing:
        print('WARNING: missing shared files: ' + ', '.join(missing))
    students = list_students(root, args.all_subdirs)
    print(f'Student folders: {len(students)}')
    if not students:
        print('No student folders found')
        return 1

    rows = []
    with tempfile.TemporaryDirectory(prefix='ai2_eval_') as td:
        for student in students:
            print(f'\n{student.name}')
            row = {'student': student.name}
            total = 0
            for subject in (1, 2):
                results = check_subject(student, subject, root, Path(td), args)
                sub_total = sum(int(info['points']) for info in results.values())
                total += sub_total
                for part in ('preprocess', 'model', 'performance'):
                    label = 'perf' if part == 'performance' else part
                    row[f'S{subject}_{label}'] = format_score(results[part])
                    print(f'  S{subject} {label:<10} {row[f"S{subject}_{label}"]}')
                row[f'S{subject}_total'] = f'{sub_total}/10'
                print(f'  S{subject} TOTAL      {sub_total}/10')
            row['total'] = f'{total}/20'
            print('  OVERALL       ' + row['total'])
            rows.append(row)

    columns = ['student', 'S1_preprocess', 'S1_model', 'S1_perf', 'S1_total',
               'S2_preprocess', 'S2_model', 'S2_perf', 'S2_total', 'total']
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print('\nSaved: ' + str(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
