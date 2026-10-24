import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import wave

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def energie(x):
    E = 0
    for m in range(len(x)):
        E = E + x[m]**2
    return E

def treceri_zero(x):
    Z = 0
    for m in range(1, len(x)):
        Z = Z + abs(np.sign(x[m]) - np.sign(x[m-1]))
    return Z / (2 * len(x))

def autocorelatie(x):
    N = len(x)
    R = np.zeros(N)
    for k in range(N):
        for m in range(N - k):
            R[k] = R[k] + x[m] * x[m+k]
    return R


class WavApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Parametri de timp scurt")
        self.geometry("900x800")

        self.semnal = None
        self.fs = None

        self._construieste_interfata()

    def _construieste_interfata(self):
        cadru = ttk.Frame(self, padding=10)
        cadru.pack(fill="both", expand=True)

        rand1 = ttk.Frame(cadru)
        rand1.pack(fill="x", pady=3)
        ttk.Label(rand1, text="Fișier .wav:").pack(side="left")
        self.var_cale = tk.StringVar()
        ttk.Entry(rand1, textvariable=self.var_cale, state="readonly") \
            .pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(rand1, text="Caută...", command=self.cauta_fisier).pack(side="left")

        rand2 = ttk.Frame(cadru)
        rand2.pack(fill="x", pady=3)
        ttk.Label(rand2, text="Frecvență de eșantionare (Hz):", width=32).pack(side="left")
        self.var_fs = tk.StringVar()
        ttk.Entry(rand2, textvariable=self.var_fs, state="readonly", width=15).pack(side="left")

        rand3 = ttk.Frame(cadru)
        rand3.pack(fill="x", pady=3)
        ttk.Label(rand3, text="Durata ferestrei (ms):", width=32).pack(side="left")
        self.var_durata = tk.StringVar(value="20")
        ttk.Entry(rand3, textvariable=self.var_durata, width=15).pack(side="left")

        rand4 = ttk.Frame(cadru)
        rand4.pack(fill="x", pady=3)
        ttk.Label(rand4, text="Eșantion start „a”:", width=32).pack(side="left")
        self.var_start_a = tk.StringVar()
        ttk.Entry(rand4, textvariable=self.var_start_a, width=15).pack(side="left")

        rand5 = ttk.Frame(cadru)
        rand5.pack(fill="x", pady=3)
        ttk.Label(rand5, text="Eșantion start „s”:", width=32).pack(side="left")
        self.var_start_s = tk.StringVar()
        ttk.Entry(rand5, textvariable=self.var_start_s, width=15).pack(side="left")
        ttk.Button(rand5, text="Calculează", command=self.calculeaza).pack(side="left", padx=5)

        rand6 = ttk.Frame(cadru)
        rand6.pack(fill="x", pady=3)
        ttk.Label(rand6, text="Energie a / s:", width=32).pack(side="left")
        self.var_e = tk.StringVar()
        ttk.Entry(rand6, textvariable=self.var_e, state="readonly", width=30).pack(side="left")

        rand7 = ttk.Frame(cadru)
        rand7.pack(fill="x", pady=3)
        ttk.Label(rand7, text="Rata trecerilor prin zero a / s:", width=32).pack(side="left")
        self.var_z = tk.StringVar()
        ttk.Entry(rand7, textvariable=self.var_z, state="readonly", width=30).pack(side="left")

        rand8 = ttk.Frame(cadru)
        rand8.pack(fill="x", pady=3)
        ttk.Label(rand8, text="Ton fundamental (Hz):", width=32).pack(side="left")
        self.var_f0 = tk.StringVar()
        ttk.Entry(rand8, textvariable=self.var_f0, state="readonly", width=30).pack(side="left")

        rand9 = ttk.Frame(cadru)
        rand9.pack(fill="x", pady=3)
        ttk.Label(rand9, text="Vorbitor:", width=32).pack(side="left")
        self.var_vorbitor = tk.StringVar()
        ttk.Entry(rand9, textvariable=self.var_vorbitor, state="readonly", width=30).pack(side="left")

        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=cadru)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))

    def cauta_fisier(self):
        cale = filedialog.askopenfilename(
            title="Alege un fișier WAV",
            filetypes=[("Fișiere WAV", "*.wav"), ("Toate fișierele", "*.*")],
        )
        if not cale:
            return

        try:
            self.semnal, self.fs = self._citeste_wav(cale)
        except Exception as e:
            messagebox.showerror("Eroare", f"Nu s-a putut citi fișierul:\n{e}")
            return

        self.var_cale.set(cale)
        self.var_fs.set(str(self.fs))

    @staticmethod
    def _citeste_wav(cale):
        with wave.open(cale, "rb") as w:
            canale = w.getnchannels()
            latime = w.getsampwidth()
            fs = w.getframerate()
            brut = w.readframes(w.getnframes())

        if latime == 1:
            date = np.frombuffer(brut, dtype=np.uint8).astype(np.float32) - 128
        elif latime == 2:
            date = np.frombuffer(brut, dtype=np.int16).astype(np.float32)
        elif latime == 4:
            date = np.frombuffer(brut, dtype=np.int32).astype(np.float32)
        else:
            raise ValueError(f"Lățime eșantion nesuportată: {latime} octeți")

        if canale > 1:
            date = date[::canale]

        date = date / max(abs(date))
        return date, fs

    def calculeaza(self):
        if self.semnal is None:
            messagebox.showwarning("Atenție", "Încărcați mai întâi un fișier WAV.")
            return

        try:
            durata_ms = float(self.var_durata.get())
            start_a = int(self.var_start_a.get())
            start_s = int(self.var_start_s.get())
        except ValueError:
            messagebox.showerror("Eroare", "Durata și eșantioanele de start trebuie să fie numere.")
            return

        N = int(self.fs * durata_ms / 1000)
        a = self.semnal[start_a:start_a + N]
        s = self.semnal[start_s:start_s + N]

        Ra = autocorelatie(a)
        Rs = autocorelatie(s)

        kmin = int(self.fs / 500)
        kmax = int(self.fs / 60)
        k = kmin + np.argmax(Ra[kmin:kmax])
        F0 = self.fs / k

        if F0 < 165:
            vorbitor = "sex masculin"
        elif F0 <= 255:
            vorbitor = "sex feminin"
        else:
            vorbitor = "copil"

        self.var_e.set(f"{energie(a):.3f} / {energie(s):.3f}")
        self.var_z.set(f"{treceri_zero(a):.3f} / {treceri_zero(s):.3f}")
        self.var_f0.set(f"{F0:.1f}")
        self.var_vorbitor.set(vorbitor)

        self._deseneaza(a, s, Ra, Rs)

    def _deseneaza(self, a, s, Ra, Rs):
        self.fig.clear()

        ax1 = self.fig.add_subplot(221)
        ax1.plot(a)
        ax1.set_title("Cadrul a")

        ax2 = self.fig.add_subplot(222)
        ax2.plot(s)
        ax2.set_title("Cadrul s")

        ax3 = self.fig.add_subplot(223)
        ax3.plot(Ra)
        ax3.set_title("Autocorelație a")

        ax4 = self.fig.add_subplot(224)
        ax4.plot(Rs)
        ax4.set_title("Autocorelație s")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    WavApp().mainloop()
