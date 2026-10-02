"""Merge Sort - implementare care urmeaza pas cu pas pseudocodul din README.md.

Indicii sunt 1-based (ca in pseudocod): A[0] nu se foloseste.

Rulare:
    python3 merge_sort.py                  # exemplul din README, cu trasare
    python3 merge_sort.py 5 2 9 1 7        # sir propriu, cu trasare
    python3 merge_sort.py --test           # teste automate
"""

import random
import sys


def merge_sort(A, st, dr, trace=None, nivel=0):
    """Sorteaza crescator subsecventa A[st..dr] (inclusiv)."""
    if trace is not None:
        trace.append(f"{'    ' * nivel}MergeSort(A, {st}, {dr})  {A[st:dr + 1]}")

    if st < dr:
        mij = (st + dr) // 2                                 # DIVIDE
        merge_sort(A, st, mij, trace, nivel + 1)             # STAPANESTE - stanga
        merge_sort(A, mij + 1, dr, trace, nivel + 1)         # STAPANESTE - dreapta
        interclasare(A, st, mij, dr, trace, nivel + 1)       # COMBINA
    elif trace is not None:
        trace[-1] += "  -> caz de baza"


def interclasare(A, st, mij, dr, trace=None, nivel=0):
    """Interclaseaza A[st..mij] si A[mij+1..dr], ambele deja sortate."""
    stanga, dreapta = A[st:mij + 1], A[mij + 1:dr + 1]

    B = [None]                       # B[1..dr-st+1]; B[0] nefolosit
    i, j = st, mij + 1
    while i <= mij and j <= dr:
        if A[i] <= A[j]:             # "<=" pastreaza stabilitatea
            B.append(A[i])
            i += 1
        else:
            B.append(A[j])
            j += 1
    while i <= mij:                  # restul din jumatatea stanga
        B.append(A[i])
        i += 1
    while j <= dr:                   # restul din jumatatea dreapta
        B.append(A[j])
        j += 1
    for p in range(1, len(B)):       # copiere inapoi in A[st..dr]
        A[st + p - 1] = B[p]

    if trace is not None:
        trace.append(f"{'    ' * nivel}Interclasare(A, {st}, {mij}, {dr})  "
                     f"{stanga} + {dreapta} -> {A[st:dr + 1]}")


def sorteaza(valori, trace=None):
    A = [None] + list(valori)
    merge_sort(A, 1, len(valori), trace)
    return A[1:]


def teste():
    assert sorteaza([]) == []
    assert sorteaza([7]) == [7]
    assert sorteaza([2, 1]) == [1, 2]
    assert sorteaza([5, 5, 5]) == [5, 5, 5]
    assert sorteaza([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert sorteaza([4, 3, 2, 1]) == [1, 2, 3, 4]
    assert sorteaza([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]

    # stabilitate: elementele egale isi pastreaza ordinea relativa
    class E:
        def __init__(self, cheie, eticheta):
            self.cheie, self.eticheta = cheie, eticheta

        def __le__(self, alt):
            return self.cheie <= alt.cheie

    elemente = [E(2, "a"), E(1, "b"), E(2, "c"), E(1, "d")]
    assert [e.eticheta for e in sorteaza(elemente)] == ["b", "d", "a", "c"]

    for _ in range(2000):
        v = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
        assert sorteaza(v) == sorted(v)

    print("Toate testele au trecut.")


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        teste()
    else:
        valori = [int(x) for x in sys.argv[1:]] or [38, 27, 43, 3, 9, 82, 10]
        trace = []
        rezultat = sorteaza(valori, trace)
        print("\n".join(trace))
        print(f"\nRezultat: {rezultat}")
