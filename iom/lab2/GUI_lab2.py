# Interfata pentru calculul parametrilor de timp scurt (pornind de la GUI-ul din laboratorul 1)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
from scipy.io import wavfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def energie(x):
    return np.sum(x**2)

def treceri_zero(x):
    return np.sum(np.abs(np.diff(np.sign(x)))) / (2 * len(x))

def autocorelatie(x):
    N = len(x)
    R = np.zeros(N)
    for k in range(N):
        R[k] = np.sum(x[0:N-k] * x[k:N])
    return R

def ton_fundamental(R, fs):
    # cautam maximul autocorelatiei pentru perioade corespunzatoare lui F0 intre 60 si 400 Hz
    kmin = int(fs / 400)
    kmax = min(int(fs / 60), len(R) - 1)
    k = kmin + np.argmax(R[kmin:kmax + 1])
    return fs / k

def categorie(F0):
    if F0 < 165:
        return "barbat"
    elif F0 < 255:
        return "femeie"
    else:
        return "copil"


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Parametri de timp scurt")
        self.geometry("950x750")
        self.semnal = None
        self.fs = None

        cadru = ttk.Frame(self, padding=10)
        cadru.pack(fill="both", expand=True)

        rand = ttk.Frame(cadru)
        rand.pack(fill="x", pady=3)
        ttk.Label(rand, text="Fișier .wav:").pack(side="left")
        self.var_cale = tk.StringVar()
        ttk.Entry(rand, textvariable=self.var_cale, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(rand, text="Caută...", command=self.cauta_fisier).pack(side="left")

        self.var_fs = self._camp(cadru, "Frecvență de eșantionare (Hz):", readonly=True)
        self.var_durata = self._camp(cadru, "Durata ferestrei (ms):", "20")
        self.var_start_a = self._camp(cadru, "Eșantion start „a”:", "9600")
        self.var_start_s = self._camp(cadru, "Eșantion start „s”:", "10960")

        ttk.Button(cadru, text="Calculează", command=self.calculeaza).pack(anchor="w", pady=5)

        self.var_rez_a = tk.StringVar()
        self.var_rez_s = tk.StringVar()
        self.var_vorbitor = tk.StringVar()
        ttk.Label(cadru, textvariable=self.var_rez_a).pack(anchor="w")
        ttk.Label(cadru, textvariable=self.var_rez_s).pack(anchor="w")
        ttk.Label(cadru, textvariable=self.var_vorbitor, font=("", 10, "bold")).pack(anchor="w")

        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=cadru)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))

    def _camp(self, parinte, text, valoare="", readonly=False):
        rand = ttk.Frame(parinte)
        rand.pack(fill="x", pady=3)
        ttk.Label(rand, text=text, width=32).pack(side="left")
        var = tk.StringVar(value=valoare)
        ttk.Entry(rand, textvariable=var, width=15, state="readonly" if readonly else "normal").pack(side="left")
        return var

    def cauta_fisier(self):
        cale = filedialog.askopenfilename(filetypes=[("Fișiere WAV", "*.wav")])
        if not cale:
            return
        self.fs, data = wavfile.read(cale)
        if data.ndim > 1:             # stereo -> pastram primul canal
            data = data[:, 0]
        self.semnal = data / max(abs(data))
        self.var_cale.set(cale)
        self.var_fs.set(str(self.fs))

    def calculeaza(self):
        if self.semnal is None:
            messagebox.showwarning("Atenție", "Alegeți mai întâi un fișier WAV.")
            return
        try:
            N = int(self.fs * float(self.var_durata.get()) / 1000)
            start_a = int(self.var_start_a.get())
            start_s = int(self.var_start_s.get())
        except ValueError:
            messagebox.showerror("Eroare", "Durata și eșantioanele de start trebuie să fie numere.")
            return

        cadru_a = self.semnal[start_a:start_a + N]
        cadru_s = self.semnal[start_s:start_s + N]

        Ra = autocorelatie(cadru_a)
        Rs = autocorelatie(cadru_s)
        F0 = ton_fundamental(Ra, self.fs)

        self.var_rez_a.set(f"„a”: E = {energie(cadru_a):.3f}   Z = {treceri_zero(cadru_a):.3f}   "
                           f"R(k)/R(0) = {Ra[round(self.fs / F0)] / Ra[0]:.2f}   F0 = {F0:.0f} Hz")
        self.var_rez_s.set(f"„s”: E = {energie(cadru_s):.3f}   Z = {treceri_zero(cadru_s):.3f}")
        self.var_vorbitor.set(f"Vorbitor: {categorie(F0)}")

        self.fig.clear()
        ax1 = self.fig.add_subplot(211)
        ax1.plot(self.semnal, linewidth=0.5)
        ax1.axvspan(start_a, start_a + N, color="orange", alpha=0.5)
        ax1.axvspan(start_s, start_s + N, color="green", alpha=0.5)
        ax1.set_title("Semnal")
        ax2 = self.fig.add_subplot(223)
        ax2.plot(cadru_a, color="orange")
        ax2.set_title("Cadrul „a”")
        ax3 = self.fig.add_subplot(224)
        ax3.plot(cadru_s, color="green")
        ax3.set_title("Cadrul „s”")
        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    App().mainloop()
