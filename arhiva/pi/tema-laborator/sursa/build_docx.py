# Face versiunile Word (.docx) ale testului si baremului din test.html / barem.html.
# Rulare: uv run --no-project --with python-docx python build_docx.py
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt

AICI = Path(__file__).parent
LIVRABIL = AICI.parents[3] / "pi" / "tema-laborator"


def bordura(p, laturi=("top", "left", "bottom", "right"), culoare="000000"):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:pBdr")
    for l in laturi:
        e = OxmlElement(f"w:{l}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "6")
        e.set(qn("w:space"), "4")
        e.set(qn("w:color"), culoare)
        b.append(e)
    pPr.append(b)


def fara_borduri(tabel):
    tblPr = tabel._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for l in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{l}")
        e.set(qn("w:val"), "nil")
        b.append(e)
    tblPr.append(b)


class Conv(HTMLParser):
    def __init__(self, doc, marime):
        super().__init__(convert_charrefs=True)
        self.doc, self.marime = doc, marime
        self.p = None              # paragraful curent
        self.fmt = []              # stiva de formatare inline
        self.liste = []            # [tip, contor]
        self.in_style = self.in_title = self.in_pre = False
        self.info = self.doc_sep = False
        self.matdiv = None         # [(eticheta, matrice)] pentru f0 = ..., f = ...
        self.mat = None
        self.celula = None
        self.eticheta = ""

    # ---------- paragrafe ----------
    def nou(self, stil=None, centrat=False, indent=0):
        self.p = self.doc.add_paragraph(style=stil)
        pf = self.p.paragraph_format
        pf.space_before, pf.space_after = Pt(0), Pt(3)
        if centrat:
            self.p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if indent:
            pf.left_indent = Mm(indent)
        return self.p

    def text(self, t):
        if self.p is None:
            self.nou()
        r = self.p.add_run(t)
        r.font.size = Pt(self.marime)
        for f in self.fmt:
            if f == "b":
                r.bold = True
            elif f == "i":
                r.italic = True
            elif f == "sub":
                r.font.subscript = True
            elif f == "sup":
                r.font.superscript = True
            elif f == "code":
                r.font.name = "Courier New"
                r.font.size = Pt(self.marime - 1.5)

    # ---------- taguri ----------
    def handle_starttag(self, tag, a):
        a = dict(a)
        cls = a.get("class", "")
        if tag == "style":
            self.in_style = True
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.nou(centrat=True)
            self.fmt.append("b")
            self.p.paragraph_format.space_after = Pt(2)
            self.h = "h1"
        elif tag == "h2":
            self.nou()
            pf = self.p.paragraph_format
            pf.space_before, pf.keep_with_next = Pt(10), True
            if self.doc_sep:
                bordura(self.p, ("top",))
            self.fmt.append("b")
        elif tag == "p":
            self.nou(centrat=(cls == "sub"))
        elif tag == "div":
            if cls == "info":
                self.info = True
                self.nou()
                bordura(self.p)
            elif cls == "doc":
                self.doc_sep = True
            else:
                self.matdiv = []
                self.eticheta = ""
        elif tag == "br":
            if self.info:
                self.nou()
                bordura(self.p)
            else:
                self.p.add_run().add_break()
        elif tag in ("ol", "ul"):
            self.liste.append([a.get("type", "1"), 0])
        elif tag == "li":
            l = self.liste[-1]
            l[1] += 1
            n = l[1]
            semn = f"{chr(96 + n)})" if l[0] == "a" else f"{n}."
            self.nou(indent=7 * len(self.liste))
            self.p.paragraph_format.first_line_indent = Mm(-6)
            self.text(semn + " ")
        elif tag == "table" and self.matdiv is not None:
            self.mat = []
        elif tag == "tr" and self.mat is not None:
            self.mat.append([])
        elif tag == "td" and self.mat is not None:
            self.mat[-1].append("")
        elif tag == "pre":
            self.in_pre = True
            self.buf = ""
        elif tag == "span" and cls == "pct":
            self.fmt.append("b")
        elif tag in ("b", "i", "sub", "sup", "code"):
            self.fmt.append(tag)
        elif tag == "span":
            self.fmt.append("")

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        elif tag == "title":
            self.in_title = False
        elif tag in ("h1", "h2"):
            self.fmt.pop()
            if tag == "h1":
                for r in self.p.runs:
                    r.font.size = Pt(self.marime + 3)
            else:
                for r in self.p.runs:
                    r.font.size = Pt(self.marime + 1)
            self.p = None
        elif tag in ("p", "li"):
            self.p = None
        elif tag == "div":
            if self.info:
                self.info = False
                self.p = None
            elif self.matdiv is not None:
                self.scrie_matrici()
                self.matdiv = None
        elif tag in ("ol", "ul"):
            self.liste.pop()
            self.p = None
        elif tag == "table" and self.mat is not None:
            self.matdiv.append((self.eticheta.strip(), self.mat))
            self.eticheta, self.mat = "", None
        elif tag == "pre":
            self.in_pre = False
            for linie in self.buf.split("\n"):
                p = self.nou(indent=3)
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(linie if linie else " ")
                r.font.name = "Courier New"
                r.font.size = Pt(8.5)
                bordura(p, culoare="999999")
            self.p = None
        elif tag in ("b", "i", "sub", "sup", "code", "span"):
            self.fmt.pop()

    def handle_data(self, d):
        if self.in_style or self.in_title:
            return
        if self.in_pre:
            self.buf += d
            return
        if self.mat is not None:
            if self.mat and self.mat[-1]:
                self.mat[-1][-1] += d.strip()
            return
        if self.matdiv is not None:
            # eticheta matricei: "f0 =" (cu indice)
            if d.strip():
                self.eticheta += ("_" if self.fmt and self.fmt[-1] == "sub" else "") + d.strip()
            return
        if not d.strip() and self.p is None:
            return
        d = re.sub(r"\s+", " ", d)
        if self.p is None or not self.p.runs:
            d = d.lstrip()
        if d:
            self.text(d)

    # ---------- f0 = [..]  f = [..] pe un rand ----------
    def scrie_matrici(self):
        ext = self.doc.add_table(rows=1, cols=2 * len(self.matdiv))
        fara_borduri(ext)
        ext.autofit = False
        for k, (et, m) in enumerate(self.matdiv):
            c = ext.rows[0].cells[2 * k]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            baza, _, ind = et.replace("=", "").strip().partition("_")
            r = p.add_run(baza)
            r.font.size = Pt(self.marime)
            if ind:
                r = p.add_run(ind)
                r.font.size = Pt(self.marime)
                r.font.subscript = True
            r = p.add_run(" =")
            r.font.size = Pt(self.marime)
            c.width = Mm(14)
            c2 = ext.rows[0].cells[2 * k + 1]
            c2.width = Mm(45)
            c2.vertical_alignment = 1  # centru
            c.vertical_alignment = 1
            t = c2.add_table(rows=len(m), cols=len(m[0]))
            t.style = "Table Grid"
            t.alignment = WD_TABLE_ALIGNMENT.LEFT
            for i, rand in enumerate(m):
                for j, v in enumerate(rand):
                    cc = t.cell(i, j)
                    cc.width = Mm(11)
                    pp = cc.paragraphs[0]
                    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    rr = pp.add_run(v)
                    rr.font.size = Pt(self.marime)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(0)


def fa(html, iesire, marime, margini):
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.top_margin, s.right_margin, s.bottom_margin, s.left_margin = (Mm(x) for x in margini)
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.font.size = Pt(marime)
    c = Conv(doc, marime)
    c.feed((AICI / html).read_text(encoding="utf-8"))
    doc.core_properties.author = "Traian File-Mitita"
    doc.core_properties.title = ""
    doc.save(iesire)
    print("scris", iesire)


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else LIVRABIL
    fa("test.html", dest / "Test_PIm_Masuri_calitate_FileMitita_Traian.docx", 12, (18, 18, 16, 18))
    fa("barem.html", dest / "Barem_PIm_Masuri_calitate_FileMitita_Traian.docx", 11, (15, 16, 14, 16))
