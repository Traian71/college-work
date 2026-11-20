# Decupeaza capturile brute (Retina, 2 px / punct) pentru PDF. Coordonatele sunt in puncte ale ferestrei.
from pathlib import Path
from PIL import Image
D = Path(__file__).resolve().parent
B, C = D / "capturi_brute", D / "capturi"
T = {  # nume: (fisier brut, x0, y0, x1, y1)
    "topologie_ex1":   ("topologie_ex1.png", 110, 205, 890, 665),
    "topologie_ex2":   ("topologie_ex2.png", 110, 205, 890, 665),
    "pc01_fara_ruta":  ("pc01_ping_pc11_fara_ruta.png", 26, 112, 330, 535),
    "pc11_fara_ruta":  ("pc11_ping_r2_fara_ruta.png", 26, 112, 330, 535),
    "r1_rute":         ("r1_ruta_show.png", 26, 526, 420, 948),
    "r2_rute":         ("r2_ruta_show.png", 26, 676, 420, 948),
    "pc01_cu_ruta":    ("pc01_ping_retea2.png", 26, 522, 330, 815),
    "pc11_cu_ruta":    ("pc11_ping_retea1.png", 26, 522, 330, 815),
    "pc02_ex2":        ("pc02_ex2.png", 26, 112, 330, 515),
    "pc13_ex2":        ("pc13_ex2.png", 26, 112, 330, 515),
}
for n, (f, *box) in T.items():
    im = Image.open(B / f)
    k = im.width / (1390 if "topologie" in f else 900)
    im.crop(tuple(round(v * k) for v in box)).save(C / f"{n}.png")
    print(n, im.size)
