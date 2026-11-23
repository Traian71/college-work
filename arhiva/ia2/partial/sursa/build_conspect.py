# Construieste conspectul IA2: conspect_template.html + scheme SVG -> conspect.html -> PDF (Chrome headless, KaTeX din CDN).
# Rulare: python3 build_conspect.py
import subprocess, tempfile
from pathlib import Path
import scheme as S

D = Path(__file__).resolve().parent
OUT = D.parents[3] / "ia2/partial/Conspect_IA2_lucrare_curs.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IN, H, O = S.FILL_IN, S.FILL_H, S.FILL_O

retea_221 = S.retea(
    [[("x1", "x₁", IN, "= 2"), ("x2", "x₂", IN, "= −1")],
     [("h1", "h₁", H, "bias 0,5|ReLU"), ("h2", "h₂", H, "bias −0,5|ReLU")],
     [("y", "y", O, "bias −1")]],
    [("x1", "h1", "1", .35), ("x2", "h1", "0,5", .3), ("x1", "h2", "−0,5", .3), ("x2", "h2", "−1", .35),
     ("h1", "y", "0,5", .4), ("h2", "y", "−0,5", .4)],
    W=520, H=270, titluri=["intrare", "strat ascuns", "ieșire"])

v1p1 = S.retea(
    [[("I1", "I₁", IN, "= 10"), ("I2", "I₂", IN, "= 30"), ("I3", "I₃", IN, "= 20")],
     [("H1", "H₁", H, "sigmoid"), ("H2", "H₂", H, "sigmoid")],
     [("O1", "O₁", O, "ReLU"), ("O2", "O₂", O, "ReLU")]],
    [("I1", "H1", "0,2", .28), ("I1", "H2", "0,7", .2), ("I2", "H1", "−0,1", .22), ("I2", "H2", "−1,2", .22),
     ("I3", "H1", "0,4", .2), ("I3", "H2", "1,2", .28),
     ("H1", "O1", "1,1", .3), ("H1", "O2", "−3,1", .22), ("H2", "O1", "0,1", .22), ("H2", "O2", "1,17", .3)],
    W=560, H=350, titluri=["intrare", "strat ascuns", "ieșire"])

v2p1 = S.retea(
    [[("i1", "i₁", IN, "= 2"), ("i2", "i₂", IN, "= −1")],
     [("h1", "h₁", H, "b₁ = 0,5"), ("h2", "h₂", H, "b₂ = −0,5")],
     [("h3", "h₃", H, ""), ("h4", "h₄", H, "")],
     [("o1", "o₁", O, "b₃ = −1"), ("o2", "o₂", O, "b₄ = 0,5")]],
    [("i1", "h1", "w₁₁ = 1", .3), ("i1", "h2", "w₁₂ = −0,5", .22), ("i2", "h1", "w₂₁ = 0,5", .22), ("i2", "h2", "w₂₂ = −1", .3),
     ("h1", "h3", "ReLU", .5), ("h2", "h4", "ReLU", .5),
     ("h3", "o1", "w₃₁ = 0,5", .3), ("h3", "o2", "w₃₂ = −1", .22), ("h4", "o1", "w₄₁ = −0,5", .22), ("h4", "o2", "w₄₂ = 1", .3)],
    W=640, H=320, titluri=["intrare", "strat ascuns", "după ReLU", "ieșire"])

sub = {"NEURON": S.neuron(), "RETEA_221": retea_221, "GRAFICE": S.activari(), "GRADIENT": S.gradient(),
       "BACKPROP": S.backprop(), "V1P1": v1p1, "MATRICE": S.matrice_A(), "V2P1": v2p1, "OVERFIT": S.overfit(),
       "CONV": S.conv(), "POOL": S.pooling(), "PCA": S.pca()}
html = (D / "conspect_template.html").read_text(encoding="utf-8")
for k, v in sub.items():
    html = html.replace("{{" + k + "}}", v)
assert "{{" not in html
(D / "conspect.html").write_text(html, encoding="utf-8")

with tempfile.TemporaryDirectory() as t:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={t}/p", "--virtual-time-budget=15000",
                    "--no-pdf-header-footer", f"--print-to-pdf={OUT}", (D / "conspect.html").as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
