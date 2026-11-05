import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import wave

import numpy as np
from scipy import fft, signal
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WavApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Analiza in frecventa")
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
        ttk.Label(rand3, text="Eșantion start cadru:", width=32).pack(side="left")
        self.var_start = tk.StringVar()
        ttk.Entry(rand3, textvariable=self.var_start, width=15).pack(side="left")

        rand4 = ttk.Frame(cadru)
        rand4.pack(fill="x", pady=3)
        ttk.Label(rand4, text="Eșantion stop cadru:", width=32).pack(side="left")
        self.var_stop = tk.StringVar()
        ttk.Entry(rand4, textvariable=self.var_stop, width=15).pack(side="left")

        rand5 = ttk.Frame(cadru)
        rand5.pack(fill="x", pady=3)
        ttk.Label(rand5, text="Fereastra spectrogramei (ms):", width=32).pack(side="left")
        self.var_durata = tk.StringVar(value="20")
        ttk.Entry(rand5, textvariable=self.var_durata, width=15).pack(side="left")
        ttk.Button(rand5, text="Calculează", command=self.calculeaza).pack(side="left", padx=5)

        rand6 = ttk.Frame(cadru)
        rand6.pack(fill="x", pady=3)
        ttk.Label(rand6, text="Număr puncte FFT (n):", width=32).pack(side="left")
        self.var_n = tk.StringVar()
        ttk.Entry(rand6, textvariable=self.var_n, state="readonly", width=15).pack(side="left")

        self.fig = Figure(figsize=(7, 5), dpi=100)
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
            start = int(self.var_start.get())
            stop = int(self.var_stop.get())
            durata_ms = float(self.var_durata.get())
        except ValueError:
            messagebox.showerror("Eroare", "Start, stop și durata ferestrei trebuie să fie numere.")
            return

        cadru_a = self.semnal[start:stop]
        L = int(self.fs * durata_ms / 1000)
        if len(cadru_a) < L:
            messagebox.showerror("Eroare", "Cadrul trebuie să fie cel puțin cât fereastra spectrogramei.")
            return

        n = 2
        while n < len(cadru_a):
            n = n * 2

        sp_a = fft.fft(cadru_a, n = n)
        frecv = fft.fftfreq(len(sp_a), 1/self.fs)

        w = signal.windows.hamming(L)
        f, t, sxx = signal.spectrogram(cadru_a, self.fs, w)

        self.var_n.set(str(n))
        self._deseneaza(cadru_a, frecv[:n//2], np.abs(sp_a[:n//2]), f, t, sxx)

    def _deseneaza(self, cadru_a, frecv, sp, f, t, sxx):
        self.fig.clear()

        ax1 = self.fig.add_subplot(221)
        ax1.plot(cadru_a)
        ax1.set_title("Cadrul de analiză")

        ax2 = self.fig.add_subplot(222)
        ax2.plot(frecv, sp)
        ax2.set_title("Spectrul de amplitudine")
        ax2.set_xlabel("Frecventa [Hz]")

        ax3 = self.fig.add_subplot(212)
        ax3.pcolormesh(t, f, sxx, shading="auto")
        ax3.set_title("Spectrograma")
        ax3.set_ylabel("Frecventa [Hz]")
        ax3.set_xlabel("Timp [s]")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    WavApp().mainloop()
