# Construieste prezentarea (6 slide-uri) pentru tema de curs IOM. Ruleaza din radacina repo-ului:
#   uv run --no-project --with python-pptx --with scipy --with numpy --with matplotlib python arhiva/iom/tema-curs/sursa/build_slides.py [link]
# Fara link, slide-ul 1 are un loc gol pentru linkul inregistrarii.
import json, sys
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.io import wavfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SRC = 'arhiva/iom/tema-curs/sursa'
OUT = 'iom/tema-curs/Prezentare_IOM_FileMitita_Traian.pptx'
LINK = sys.argv[1] if len(sys.argv) > 1 else None

PLUM, ORANGE, MAGENTA = RGBColor(0x2A, 0x0F, 0x3D), RGBColor(0xF0, 0x7B, 0x3F), RGBColor(0xB6, 0x36, 0x79)
INK, MUTED, TINT, WHITE = RGBColor(0x1F, 0x1A, 0x24), RGBColor(0x6B, 0x64, 0x75), RGBColor(0xF6, 0xEF, 0xF4), RGBColor(0xFF, 0xFF, 0xFF)
HEAD, BODY = 'Cambria', 'Calibri'

# forma de unda a inregistrarii mele (cele 7 cuvinte), pentru slide-ul de titlu
fs, x = wavfile.read('iom/lab3-bonus/semnale/cuvinte.wav'); x = x / max(abs(x))
fig = plt.figure(figsize=(12, 1.6), dpi=150); ax = fig.add_axes([0, 0, 1, 1])
ax.plot(x[::4], color='#F07B3F', lw=0.6); ax.set_xlim(0, len(x[::4])); ax.set_ylim(-1.05, 1.05); ax.axis('off')
fig.savefig(f'{SRC}/unda.png', transparent=True); plt.close(fig)

script = json.load(open(f'{SRC}/script.json', encoding='utf-8'))
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]


def bg(slide, color):
    f = slide.background.fill; f.solid(); f.fore_color.rgb = color


def text(slide, x, y, w, h, runs, size=16, color=INK, font=BODY, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lines = runs if isinstance(runs, list) else [runs]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
        r.font.size, r.font.name, r.font.bold = Pt(size), font, bold
        r.font.color.rgb = color
    return tb


def box(slide, x, y, w, h, fill, line=None, radius=True):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                               Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line: s.line.color.rgb = line; s.line.width = Pt(1.25)
    else: s.line.fill.background()
    if radius: s.adjustments[0] = 0.12
    s.shadow.inherit = False
    return s


def arrow(slide, x, y, w=0.45, color=MUTED):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(0.32))
    a.fill.solid(); a.fill.fore_color.rgb = color; a.line.fill.background(); a.shadow.inherit = False


def dot(slide, x, y, label, fill=ORANGE):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.52), Inches(0.52))
    c.fill.solid(); c.fill.fore_color.rgb = fill; c.line.fill.background(); c.shadow.inherit = False
    text(slide, x, y, 0.52, 0.52, label, size=15, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def title(slide, t):
    text(slide, 0.7, 0.45, 11.9, 0.9, t, size=36, font=HEAD, bold=True, color=PLUM)


def notes(slide, i):
    slide.notes_slide.notes_text_frame.text = script[i]


# 1. Titlu
s = prs.slides.add_slide(blank); bg(s, PLUM)
text(s, 0.8, 1.35, 11.7, 0.5, 'INTERFEȚE OM–MAȘINĂ · TEMĂ DE CURS', size=14, color=ORANGE, bold=True)
text(s, 0.8, 1.9, 11.7, 1.6, 'Recunoașterea automată a vorbirii', size=48, font=HEAD, bold=True, color=WHITE)
text(s, 0.8, 3.0, 11.7, 0.7, 'de la parametrii semnalului vocal la rețelele neuronale', size=24, color=RGBColor(0xE9, 0xD8, 0xE6))
s.shapes.add_picture(f'{SRC}/unda.png', Inches(0.8), Inches(3.95), Inches(11.7), Inches(1.0))
text(s, 0.8, 5.15, 11.7, 0.4, 'Forma de undă: cele 7 cuvinte-model înregistrate de mine (vin, merg, măr, casă, mâine, bun, nor)',
     size=12, color=RGBColor(0xB9, 0xA8, 0xC2))
text(s, 0.8, 5.95, 6.5, 0.5, 'FILE-MITIȚĂ Traian · grupa 441A', size=18, color=WHITE, bold=True)
text(s, 0.8, 6.45, 11.7, 0.45, 'Înregistrarea prezentării: ' + (LINK or '[link de adăugat]'), size=14,
     color=ORANGE if LINK else RGBColor(0xFF, 0xC8, 0x6B))
notes(s, 0)

# 2. Interfete vocale
s = prs.slides.add_slide(blank); bg(s, WHITE); title(s, 'Interfețele vocale sunt peste tot')
for i, (h, d) in enumerate([('Asistenți vocali', 'Siri, Google Assistant'), ('Dictare și subtitrări', 'telefon, YouTube, Teams'),
                            ('Comenzi în mașină', 'fără mâini pe telefon'), ('Accesibilitate', 'deficiențe de vedere / mobilitate')]):
    x = 0.7 + i * 3.02
    box(s, x, 1.65, 2.78, 1.55, TINT)
    text(s, x + 0.25, 1.85, 2.3, 0.5, h, size=18, bold=True, color=PLUM)
    text(s, x + 0.25, 2.4, 2.3, 0.7, d, size=14, color=MUTED)
text(s, 0.7, 3.75, 11.9, 0.5, 'Cum funcționează un asistent vocal', size=20, bold=True, color=INK)
lant = [('Cuvânt de\nactivare', '„Hey Siri”'), ('Recunoașterea\nvorbirii (ASR)', 'voce → text'),
        ('Înțelegerea\nlimbajului (NLU)', 'text → intenție'), ('Sinteză\nvocală (TTS)', 'text → voce')]
for i, (h, d) in enumerate(lant):
    x = 0.7 + i * 3.1
    hi = i == 1
    box(s, x, 4.4, 2.5, 1.75, PLUM if hi else WHITE, None if hi else PLUM)
    text(s, x + 0.2, 4.6, 2.1, 0.9, h.split('\n'), size=17, bold=True, color=WHITE if hi else PLUM, align=PP_ALIGN.CENTER)
    text(s, x + 0.2, 5.55, 2.1, 0.4, d, size=14, color=ORANGE if hi else MUTED, align=PP_ALIGN.CENTER)
    if i < 3: arrow(s, x + 2.58, 5.1)
text(s, 0.7, 6.5, 11.9, 0.4, 'Prezentarea se concentrează pe a doua verigă: recunoașterea vorbirii.', size=14, color=MUTED)
notes(s, 1)

# 3. Semnal -> parametri
s = prs.slides.add_slide(blank); bg(s, WHITE); title(s, 'De la semnal la parametri')
s.shapes.add_picture(f'{SRC}/fig_casa.png', Inches(0.7), Inches(1.75), Inches(7.4))
text(s, 0.7, 4.95, 7.4, 0.8, 'Spectrograma cuvântului „casă”, înregistrat de mine (lab 3, bonus): F1 ≈ 790 Hz, F2 ≈ 1290 Hz',
     size=13, color=MUTED)
for i, (h, d) in enumerate([('Cadre de 20–30 ms', 'fereastră Hamming, pas 10 ms'), ('Energie · ZCR · F0', 'parametri de timp scurt (lab 2)'),
                            ('Formanții F1, F2', 'deosebesc vocalele (lab 3)'), ('MFCC', 'spectrul pe scara Mel, 12–13 coeficienți')]):
    y = 1.75 + i * 1.22
    dot(s, 8.55, y + 0.05, str(i + 1), ORANGE if i < 3 else MAGENTA)
    text(s, 9.25, y, 3.6, 0.45, h, size=18, bold=True, color=PLUM)
    text(s, 9.25, y + 0.45, 3.6, 0.5, d, size=14, color=MUTED)
notes(s, 2)

# 4. Recunoasterea clasica
s = prs.slides.add_slide(blank); bg(s, WHITE); title(s, 'Recunoașterea clasică (1980–2010)')
box(s, 0.7, 1.75, 3.9, 4.6, TINT)
text(s, 1.0, 2.0, 3.3, 0.5, 'Șabloane + DTW', size=20, bold=True, color=PLUM)
for i, (h, d) in enumerate([('Șabloane', 'cuvinte înregistrate dinainte'), ('DTW', 'aliniere dinamică în timp'),
                            ('Limită', 'câteva zeci de comenzi, un vorbitor')]):
    y = 2.7 + i * 1.2
    text(s, 1.0, y, 3.3, 0.4, h, size=17, bold=True, color=MAGENTA)
    text(s, 1.0, y + 0.42, 3.3, 0.6, d, size=15, color=INK)
text(s, 5.1, 1.75, 4.0, 0.5, 'Modele Markov ascunse (HMM)', size=20, bold=True, color=PLUM)
for i, (h, d) in enumerate([('Model acustic', 'HMM-GMM pe vectori MFCC'), ('Dicționar de pronunție', 'cuvânt → foneme'),
                            ('Model de limbă', '„deschide ușa” > „deschide oușa”')]):
    y = 2.4 + i * 1.3
    box(s, 5.1, y, 4.3, 1.1, WHITE, PLUM)
    text(s, 5.35, y + 0.15, 3.9, 0.4, h, size=17, bold=True, color=PLUM)
    text(s, 5.35, y + 0.58, 3.9, 0.4, d, size=14, color=MUTED)
    arrow(s, 9.55, y + 0.4, 0.5)
box(s, 10.25, 3.35, 2.4, 1.6, PLUM)
text(s, 10.35, 3.55, 2.2, 1.2, ['Decodor Viterbi', '→ text'], size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
notes(s, 3)

# 5. Retele neuronale
s = prs.slides.add_slide(blank); bg(s, WHITE); title(s, 'Recunoașterea cu rețele neuronale')
box(s, 0.7, 1.75, 4.6, 3.1, PLUM)
text(s, 0.95, 2.0, 4.1, 1.1, '680.000 h', size=54, font=HEAD, bold=True, color=ORANGE)
text(s, 0.95, 3.15, 4.1, 1.5, ['audio folosit la antrenarea Whisper', '(OpenAI, 2022), ~100 de limbi,', 'inclusiv româna'],
     size=16, color=WHITE)
box(s, 0.7, 5.15, 4.6, 1.3, TINT)
text(s, 0.95, 5.3, 4.1, 0.5, 'WER = (S + D + I) / N', size=22, bold=True, color=PLUM, font=HEAD)
text(s, 0.95, 5.85, 4.1, 0.5, 'cuvinte înlocuite, șterse, inserate', size=14, color=MUTED)
for i, (an, h, d) in enumerate([('2006', 'CTC', 'antrenare fără aliniere cadru–literă'), ('2012', 'DNN-HMM', 'rețea în modelul acustic, ~⅓ mai puține erori'),
                                ('2016+', 'End-to-end', 'codor–decodor cu atenție, Transformer'), ('2022', 'Whisper', 'intrare: tot spectrograma Mel')]):
    y = 1.8 + i * 1.18
    dot(s, 5.95, y + 0.05, str(i + 1), MAGENTA if i < 3 else ORANGE)
    text(s, 6.7, y, 1.2, 0.45, an, size=18, bold=True, color=ORANGE)
    text(s, 7.9, y, 4.8, 0.45, h, size=18, bold=True, color=PLUM)
    text(s, 7.9, y + 0.45, 4.8, 0.5, d, size=14, color=MUTED)
notes(s, 4)

# 6. Provocari si concluzii
s = prs.slides.add_slide(blank); bg(s, PLUM)
text(s, 0.8, 0.6, 11.7, 0.9, 'Provocări și concluzii', size=36, font=HEAD, bold=True, color=WHITE)
chips = ['Zgomot și ecou', 'Accente, vorbire spontană', 'Limba română: puține date', 'Confidențialitate (cloud)', 'Întârziere < 1 s']
x = 0.8
for c in chips:
    w = 0.42 + len(c) * 0.115
    if x + w > 12.6: x = 0.8
    box(s, x, 1.8 if c in chips[:3] else 2.65, w, 0.6, RGBColor(0x44, 0x1F, 0x5C))
    text(s, x, 1.8 if c in chips[:3] else 2.65, w, 0.6, c, size=16, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += w + 0.25
    if c == chips[2]: x = 0.8
text(s, 0.8, 3.8, 11.7, 1.4, ['De la șabloane pentru câteva cuvinte la rețele antrenate pe sute de mii de ore,',
                              'baza a rămas aceeași: cadre, spectru, spectrogramă și formanți.'], size=22, color=WHITE)
text(s, 0.8, 5.7, 11.7, 0.9, 'Mulțumesc!', size=40, font=HEAD, bold=True, color=ORANGE)
notes(s, 5)

import datetime
cp = prs.core_properties
cp.author = cp.last_modified_by = 'Traian FILE-MITIȚĂ'
cp.title = 'Recunoașterea automată a vorbirii'
cp.comments = ''
cp.created = cp.modified = datetime.datetime.now()
prs.save(OUT)
print(OUT)
