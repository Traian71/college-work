# =============================================================================
# Interfață tkinter pentru analiza unui fișier WAV
#   - caută un fișier .wav și îl încarcă
#   - afișează forma de undă și frecvența de eșantionare (în câmpuri separate)
#   - permite introducerea duratei ferestrei de analiză (în ms)
#   - calculează numărul de eșantioane dintr-o fereastră
#   - redesenează graficul între doi indici de eșantion (capete incluse)
# =============================================================================

# --- Importuri ---------------------------------------------------------------
import tkinter as tk                              # biblioteca grafică standard
from tkinter import ttk, filedialog, messagebox   # widgeturi moderne, dialog de fișier, ferestre de mesaj
import wave                                       # citirea fișierelor .wav (modul standard Python)

import numpy as np                                # calcule numerice pe vectori
from matplotlib.figure import Figure              # figura matplotlib (fără pyplot, ca să o putem integra în tkinter)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # puntea matplotlib -> tkinter


# --- Clasa aplicației --------------------------------------------------------
# WavApp moștenește tk.Tk, deci obiectul WavApp este chiar fereastra principală.
class WavApp(tk.Tk):

    def __init__(self):
        # Apelăm constructorul clasei părinte (tk.Tk): creează fereastra propriu-zisă.
        # Trebuie făcut primul, înainte să folosim self.title(), self.geometry() etc.
        super().__init__()

        self.title("Analiză fișier WAV")   # titlul ferestrei
        self.geometry("850x600")           # dimensiunea inițială (lățime x înălțime, în pixeli)

        # Atributele care rețin starea aplicației.
        # Pornesc ca None pentru că nu am încărcat încă niciun fișier.
        self.semnal = None   # vectorul de eșantioane (numpy array)
        self.fs = None       # frecvența de eșantionare, în Hz
        self.primul_esantion = 0
        self.ultimul_esantion = 0

        # Creăm toate widgeturile (etichete, câmpuri, butoane, grafic)
        self._construieste_interfata()

    # -------------------------------------------------------------------------
    # Construirea interfeței grafice
    # -------------------------------------------------------------------------
    def _construieste_interfata(self):
        # Containerul principal: un Frame cu margine interioară de 10 px.
        # fill="both" + expand=True îl face să umple fereastra și să se
        # redimensioneze odată cu ea.
        cadru = ttk.Frame(self, padding=10)
        cadru.pack(fill="both", expand=True)

        # ---------- Rândul 1: selecția fișierului ----------
        # Fiecare rând este un Frame separat; în interiorul lui, widgeturile
        # sunt puse unul lângă altul (side="left").
        rand1 = ttk.Frame(cadru)
        rand1.pack(fill="x", pady=3)              # fill="x": se întinde pe orizontală; pady: spațiu vertical

        ttk.Label(rand1, text="Fișier .wav:").pack(side="left")

        # StringVar = variabilă tkinter legată de un widget.
        # Dacă îi schimbăm valoarea cu .set(), textul din câmp se actualizează automat.
        self.var_cale = tk.StringVar()
        # state="readonly": utilizatorul nu poate scrie în câmp, doar programul.
        # expand=True: câmpul ocupă tot spațiul orizontal rămas liber.
        ttk.Entry(rand1, textvariable=self.var_cale, state="readonly") \
            .pack(side="left", fill="x", expand=True, padx=5)

        # command=... : funcția apelată când se apasă butonul
        ttk.Button(rand1, text="Caută...", command=self.cauta_fisier).pack(side="left")

        # ---------- Rândul 2: frecvența de eșantionare ----------
        rand2 = ttk.Frame(cadru)
        rand2.pack(fill="x", pady=3)
        # width=32 la etichete -> toate etichetele au aceeași lățime,
        # deci câmpurile de lângă ele se aliniază pe verticală.
        ttk.Label(rand2, text="Frecvență de eșantionare (Hz):", width=32).pack(side="left")
        self.var_fs = tk.StringVar()
        ttk.Entry(rand2, textvariable=self.var_fs, state="readonly", width=15).pack(side="left")

        # ---------- Rândul 3: durata ferestrei de analiză ----------
        rand3 = ttk.Frame(cadru)
        rand3.pack(fill="x", pady=3)
        ttk.Label(rand3, text="Durata ferestrei (ms):", width=32).pack(side="left")
        # aici utilizatorul scrie, deci câmpul NU este readonly
        self.var_durata = tk.StringVar(value="20")
        ttk.Entry(rand3, textvariable=self.var_durata, width=15).pack(side="left")
        ttk.Button(rand3, text="Calculează", command=self.calculeaza).pack(side="left", padx=5)

        # ---------- Rândul 4: numărul de eșantioane dintr-o fereastră ----------
        rand4 = ttk.Frame(cadru)
        rand4.pack(fill="x", pady=3)
        ttk.Label(rand4, text="Nr. eșantioane într-o fereastră:", width=32).pack(side="left")
        self.var_nr = tk.StringVar()
        ttk.Entry(rand4, textvariable=self.var_nr, state="readonly", width=15).pack(side="left")

        # ---------- Rândul 5: intervalul afișat pe grafic ----------
        rand5 = ttk.Frame(cadru)
        rand5.pack(fill="x", pady=3)
        ttk.Label(rand5, text="Primul eșantion (de la 0):").pack(side="left")
        self.var_primul = tk.StringVar(value="0")
        ttk.Entry(rand5, textvariable=self.var_primul, width=10).pack(side="left", padx=(5, 12))
        ttk.Label(rand5, text="Ultimul eșantion:").pack(side="left")
        self.var_ultimul = tk.StringVar()
        ttk.Entry(rand5, textvariable=self.var_ultimul, width=10).pack(side="left", padx=5)
        ttk.Button(rand5, text="Redesenează graficul", command=self.redeseneaza_intervalul) \
            .pack(side="left", padx=5)

        # ---------- Graficul (forma de undă) ----------
        # Figure(figsize=(lățime, înălțime) în inci, dpi=pixeli pe inch)
        self.fig = Figure(figsize=(7, 4), dpi=100)
        # add_subplot(111) = un singur grafic (1 rând, 1 coloană, poziția 1).
        # self.ax este obiectul pe care desenăm.
        self.ax = self.fig.add_subplot(111)
        self._reseteaza_grafic()                  # setează titlul și axele

        # Integrăm figura matplotlib în fereastra tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=cadru)
        # get_tk_widget() returnează widgetul tkinter real, pe care îl plasăm în fereastră
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 0))

    def _reseteaza_grafic(self):
        """Șterge graficul curent și pune din nou titlul, etichetele axelor și grila."""
        self.ax.clear()
        self.ax.set_title("Forma de undă")
        self.ax.set_xlabel("Timp [s]")
        self.ax.set_ylabel("Amplitudine")
        self.ax.grid(True, alpha=0.3)             # alpha = transparența grilei

    # -------------------------------------------------------------------------
    # Logica aplicației
    # -------------------------------------------------------------------------
    def cauta_fisier(self):
        """Apelată la apăsarea butonului 'Caută...': alege și încarcă un fișier WAV."""
        # Deschide dialogul de selecție; returnează calea aleasă sau un șir gol la Cancel
        cale = filedialog.askopenfilename(
            title="Alege un fișier WAV",
            filetypes=[("Fișiere WAV", "*.wav"), ("Toate fișierele", "*.*")],
        )
        if not cale:        # utilizatorul a anulat -> nu facem nimic
            return

        # Încercăm să citim fișierul; dacă apare o eroare (fișier corupt,
        # format nesuportat) o prindem și afișăm un mesaj, fără ca programul să se închidă.
        try:
            self.semnal, self.fs = self._citeste_wav(cale)
        except Exception as e:
            messagebox.showerror("Eroare", f"Nu s-a putut citi fișierul:\n{e}")
            return

        # Actualizăm câmpurile din interfață
        self.var_cale.set(cale)                   # calea fișierului
        self.var_fs.set(str(self.fs))             # frecvența de eșantionare
        self.var_nr.set("")                       # golim rezultatul vechi (aparținea fișierului anterior)
        self.primul_esantion = 0
        self.ultimul_esantion = len(self.semnal) - 1
        self.var_primul.set("0")
        self.var_ultimul.set(str(self.ultimul_esantion))
        self._deseneaza()                         # desenăm forma de undă

    @staticmethod
    def _citeste_wav(cale):
        """Citește un fișier WAV și returnează (semnal, frecvență_de_eșantionare).

        @staticmethod: metoda nu folosește self, deci e o funcție obișnuită
        grupată în clasă pentru ordine.
        """
        # "rb" = citire binară; with închide automat fișierul la final
        with wave.open(cale, "rb") as w:
            canale = w.getnchannels()             # 1 = mono, 2 = stereo
            latime = w.getsampwidth()             # octeți per eșantion (1, 2 sau 4)
            fs = w.getframerate()                 # frecvența de eșantionare (Hz)
            brut = w.readframes(w.getnframes())   # toate datele audio, ca octeți bruți

        # Interpretăm octeții bruți în funcție de lățimea eșantionului:
        if latime == 1:
            # 8 biți: WAV folosește valori FĂRĂ semn (0..255), cu liniștea la 128.
            # Scădem 128 ca semnalul să fie centrat în 0.
            date = np.frombuffer(brut, dtype=np.uint8).astype(np.float32) - 128
        elif latime == 2:
            # 16 biți: valori cu semn (-32768..32767) - cel mai frecvent caz
            date = np.frombuffer(brut, dtype=np.int16).astype(np.float32)
        elif latime == 4:
            # 32 de biți: valori cu semn
            date = np.frombuffer(brut, dtype=np.int32).astype(np.float32)
        else:
            # de exemplu 24 de biți: nesuportat; eroarea e prinsă în cauta_fisier
            raise ValueError(f"Lățime eșantion nesuportată: {latime} octeți")

        # La stereo, eșantioanele sunt intercalate: stânga, dreapta, stânga, dreapta...
        # date[::canale] ia câte un eșantion din "canale" -> doar primul canal.
        if canale > 1:
            date = date[::canale]

        if len(date) == 0:
            raise ValueError("Fișierul WAV nu conține eșantioane.")

        return date, fs

    def calculeaza(self):
        """Apelată la apăsarea butonului 'Calculează': numărul de eșantioane dintr-o fereastră."""
        if self.semnal is None:
            messagebox.showwarning("Atenție", "Încărcați mai întâi un fișier WAV.")
            return

        try:
            durata_ms = float(self.var_durata.get())
        except ValueError:
            messagebox.showerror("Eroare", "Durata ferestrei trebuie să fie un număr.")
            return
        if durata_ms <= 0:
            messagebox.showerror("Eroare", "Durata ferestrei trebuie să fie pozitivă.")
            return

        # N = fs * durata; durata e în ms, deci împărțim la 1000 ca să fie în secunde
        nr = int(self.fs * durata_ms / 1000)
        self.var_nr.set(str(nr))
        self._deseneaza(durata_ms / 1000)         # evidențiem prima fereastră pe grafic

    def redeseneaza_intervalul(self):
        """Validează indicii introduși și afișează eșantioanele dintre ei."""
        if self.semnal is None:
            messagebox.showwarning("Atenție", "Încărcați mai întâi un fișier WAV.")
            return

        try:
            primul = int(self.var_primul.get())
            ultimul = int(self.var_ultimul.get())
        except ValueError:
            messagebox.showerror("Eroare", "Indicii eșantioanelor trebuie să fie numere întregi.")
            return

        if not 0 <= primul <= ultimul < len(self.semnal):
            messagebox.showerror(
                "Eroare",
                f"Introduceți un interval între 0 și {len(self.semnal) - 1}, "
                "cu primul eșantion cel mult egal cu ultimul.",
            )
            return

        self.primul_esantion = primul
        self.ultimul_esantion = ultimul
        self._deseneaza()

    def _deseneaza(self, durata_fereastra=None):
        """Desenează forma de undă. Dacă se dă durata ferestrei (în secunde),
        evidențiază pe grafic prima fereastră."""
        self._reseteaza_grafic()

        # Capătul din dreapta al feliei Python este exclus, de aceea adăugăm 1.
        indici = np.arange(self.primul_esantion, self.ultimul_esantion + 1)
        t = indici / self.fs
        self.ax.plot(t, self.semnal[self.primul_esantion:self.ultimul_esantion + 1],
                     linewidth=0.7,
                     marker="o" if self.primul_esantion == self.ultimul_esantion else None)

        if durata_fereastra is not None:
            # Evidențiem prima fereastră din intervalul afișat.
            inceput = self.primul_esantion / self.fs
            sfarsit = min(inceput + durata_fereastra,
                          self.ultimul_esantion / self.fs)
            self.ax.axvspan(inceput, sfarsit, color="orange", alpha=0.3,
                            label="Prima fereastră")
            self.ax.legend(loc="upper right")

        self.fig.tight_layout()    # ajustează marginile ca textul să nu fie tăiat
        self.canvas.draw()         # redesenează efectiv graficul în fereastră


# --- Punctul de intrare ------------------------------------------------------
# Blocul rulează doar când fișierul este pornit direct (nu când e importat).
if __name__ == "__main__":
    # Creăm fereastra; mainloop() pornește bucla de evenimente, care așteaptă
    # clickuri și taste până când utilizatorul închide fereastra.
    WavApp().mainloop()
