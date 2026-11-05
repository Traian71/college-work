import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import wave  # modul standard pentru citirea fișierelor .wav

import numpy as np
# Figure + FigureCanvasTkAgg = graficul matplotlib pus direct în fereastra Tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Energia de timp scurt a unui cadru: E = suma x[m]^2
# Mare pentru vocale (ex. „a”), mică pentru consoane surde (ex. „s”) și liniște.
def energie(x):
    E = 0
    for m in range(len(x)):
        E = E + x[m]**2
    return E

# Rata trecerilor prin zero: Z = 1/(2N) * suma |sgn(x[m]) - sgn(x[m-1])|
# Când semnalul își schimbă semnul, diferența semnelor e 2 (de la -1 la 1 sau invers),
# de aceea se împarte la 2. Împărțirea la N dă o rată (treceri pe eșantion).
# Mică pentru „a” (semnal periodic, lent), mare pentru „s” (seamănă cu zgomotul).
def treceri_zero(x):
    Z = 0
    for m in range(1, len(x)):
        Z = Z + abs(np.sign(x[m]) - np.sign(x[m-1]))
    return Z / (2 * len(x))

# Autocorelația: R[k] = suma x[m] * x[m+k], adică semnalul înmulțit cu el însuși
# decalat cu k eșantioane. Dacă semnalul e periodic cu perioada T,
# R[k] are un maxim când k = T, de aici aflăm tonul fundamental.
def autocorelatie(x):
    N = len(x)
    R = np.zeros(N)
    for k in range(N):              # pentru fiecare decalaj k
        for m in range(N - k):      # până la N-k ca să nu ieșim din cadru
            R[k] = R[k] + x[m] * x[m+k]
    return R


# Fereastra principală (moștenește tk.Tk, deci clasa ESTE fereastra)
class WavApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Parametri de timp scurt")
        self.geometry("900x800")

        # semnalul citit și frecvența de eșantionare, completate după ce alegem fișierul
        self.semnal = None
        self.fs = None

        self._construieste_interfata()

    def _construieste_interfata(self):
        # cadrul care conține tot, cu margine de 10 px
        cadru = ttk.Frame(self, padding=10)
        cadru.pack(fill="both", expand=True)

        # Fiecare „rand” e un Frame cu o etichetă + un câmp (și uneori un buton), puse de la stânga la dreapta.
        # Câmpurile sunt legate de un StringVar: cu .get() citim ce scrie, cu .set() scriem în el.
        # state="readonly" = câmp doar pentru afișare, utilizatorul nu poate scrie în el.

        # rândul 1: calea fișierului + butonul care deschide dialogul de căutare
        rand1 = ttk.Frame(cadru)
        rand1.pack(fill="x", pady=3)
        ttk.Label(rand1, text="Fișier .wav:").pack(side="left")
        self.var_cale = tk.StringVar()
        ttk.Entry(rand1, textvariable=self.var_cale, state="readonly") \
            .pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(rand1, text="Caută...", command=self.cauta_fisier).pack(side="left")

        # rândul 2: frecvența de eșantionare citită din fișier (doar afișare)
        rand2 = ttk.Frame(cadru)
        rand2.pack(fill="x", pady=3)
        ttk.Label(rand2, text="Frecvență de eșantionare (Hz):", width=32).pack(side="left")
        self.var_fs = tk.StringVar()
        ttk.Entry(rand2, textvariable=self.var_fs, state="readonly", width=15).pack(side="left")

        # rândul 3: durata ferestrei de analiză, implicit 20 ms (vorbirea e aprox. staționară pe 10-30 ms)
        rand3 = ttk.Frame(cadru)
        rand3.pack(fill="x", pady=3)
        ttk.Label(rand3, text="Durata ferestrei (ms):", width=32).pack(side="left")
        self.var_durata = tk.StringVar(value="20")
        ttk.Entry(rand3, textvariable=self.var_durata, width=15).pack(side="left")

        # rândul 4: de la ce eșantion începe cadrul din sunetul „a” (îl luăm din Audacity)
        rand4 = ttk.Frame(cadru)
        rand4.pack(fill="x", pady=3)
        ttk.Label(rand4, text="Eșantion start „a”:", width=32).pack(side="left")
        self.var_start_a = tk.StringVar()
        ttk.Entry(rand4, textvariable=self.var_start_a, width=15).pack(side="left")

        # rândul 5: de la ce eșantion începe cadrul din sunetul „s” + butonul Calculează
        rand5 = ttk.Frame(cadru)
        rand5.pack(fill="x", pady=3)
        ttk.Label(rand5, text="Eșantion start „s”:", width=32).pack(side="left")
        self.var_start_s = tk.StringVar()
        ttk.Entry(rand5, textvariable=self.var_start_s, width=15).pack(side="left")
        ttk.Button(rand5, text="Calculează", command=self.calculeaza).pack(side="left", padx=5)

        # rândurile 6-9: rezultatele (doar afișare)
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

        # zona de grafice: o figură matplotlib (7x4 inch) pusă sub câmpuri
        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=cadru)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))

    # apelată de butonul „Caută...”
    def cauta_fisier(self):
        # dialogul standard de deschidere fișier; întoarce calea sau "" dacă dăm Cancel
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

        # afișăm calea și frecvența de eșantionare în câmpuri
        self.var_cale.set(cale)
        self.var_fs.set(str(self.fs))

    # citește fișierul și întoarce (semnalul ca vector numpy, fs)
    @staticmethod
    def _citeste_wav(cale):
        with wave.open(cale, "rb") as w:
            canale = w.getnchannels()   # 1 = mono, 2 = stereo
            latime = w.getsampwidth()   # câți octeți are un eșantion (1, 2 sau 4)
            fs = w.getframerate()       # frecvența de eșantionare (ex. 16000 Hz)
            brut = w.readframes(w.getnframes())  # toate eșantioanele, ca octeți

        # transformăm octeții în numere, după lățimea eșantionului
        if latime == 1:
            # pe 8 biți eșantioanele sunt fără semn (0..255), scădem 128 ca să fie centrate în 0
            date = np.frombuffer(brut, dtype=np.uint8).astype(np.float32) - 128
        elif latime == 2:
            date = np.frombuffer(brut, dtype=np.int16).astype(np.float32)
        elif latime == 4:
            date = np.frombuffer(brut, dtype=np.int32).astype(np.float32)
        else:
            raise ValueError(f"Lățime eșantion nesuportată: {latime} octeți")

        # la stereo eșantioanele sunt intercalate (S D S D ...), păstrăm doar primul canal
        if canale > 1:
            date = date[::canale]

        # normalizare: împărțim la valoarea maximă ca semnalul să fie între -1 și 1
        date = date / max(abs(date))
        return date, fs

    # apelată de butonul „Calculează”
    def calculeaza(self):
        if self.semnal is None:
            messagebox.showwarning("Atenție", "Încărcați mai întâi un fișier WAV.")
            return

        # citim valorile introduse; dacă nu sunt numere, afișăm o eroare
        try:
            durata_ms = float(self.var_durata.get())
            start_a = int(self.var_start_a.get())
            start_s = int(self.var_start_s.get())
        except ValueError:
            messagebox.showerror("Eroare", "Durata și eșantioanele de start trebuie să fie numere.")
            return

        # câte eșantioane are fereastra: N = fs * durata (în secunde)
        # ex. 16000 Hz * 0.02 s = 320 eșantioane
        N = int(self.fs * durata_ms / 1000)
        # decupăm cele două cadre din semnal
        a = self.semnal[start_a:start_a + N]
        s = self.semnal[start_s:start_s + N]

        Ra = autocorelatie(a)
        Rs = autocorelatie(s)

        # Tonul fundamental din autocorelația lui „a” (vocală, deci sunet periodic).
        # Căutăm maximul doar pentru decalaje care corespund unor frecvențe între 60 și 500 Hz
        # (domeniul vocii): frecvența f înseamnă o perioadă de fs/f eșantioane.
        # Ignorăm k mici, pentru că R[0] e oricum maximul (semnalul cu el însuși).
        kmin = int(self.fs / 500)
        kmax = int(self.fs / 60)
        k = kmin + np.argmax(Ra[kmin:kmax])   # argmax dă poziția în bucată, adunăm kmin
        F0 = self.fs / k                       # perioada k (eșantioane) -> frecvență (Hz)

        # clasificarea vorbitorului după intervalele de F0 din fișa de lucru
        if F0 < 165:
            vorbitor = "sex masculin"
        elif F0 <= 255:
            vorbitor = "sex feminin"
        else:
            vorbitor = "copil"

        # scriem rezultatele în câmpuri (:.3f = 3 zecimale)
        self.var_e.set(f"{energie(a):.3f} / {energie(s):.3f}")
        self.var_z.set(f"{treceri_zero(a):.3f} / {treceri_zero(s):.3f}")
        self.var_f0.set(f"{F0:.1f}")
        self.var_vorbitor.set(vorbitor)

        self._deseneaza(a, s, Ra, Rs)

    # desenează 4 grafice într-o grilă 2x2
    def _deseneaza(self, a, s, Ra, Rs):
        self.fig.clear()   # ștergem graficele de la calculul anterior

        # 221 = grilă 2x2, poziția 1 (stânga sus); 222 dreapta sus etc.
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

        self.fig.tight_layout()   # spațiere automată ca titlurile să nu se suprapună
        self.canvas.draw()        # redesenăm figura în fereastră


# pornește aplicația doar dacă rulăm fișierul direct (nu când îl importăm)
if __name__ == "__main__":
    WavApp().mainloop()   # mainloop = bucla care așteaptă click-uri și le tratează
