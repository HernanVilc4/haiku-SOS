from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


SOURCE = Path(r"C:\Users\USUARIO\Downloads\U3FSOS\Guia_Companero_Haiku_Git_Programacion.md")
OUT = Path(r"C:\Users\USUARIO\Downloads\U3FSOS\Guia_Companero_Haiku_Git_Programacion.docx")


def font(run, name="Arial", size=None, bold=None, color=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_page_field(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Página ")
    font(run, size=9, color="666666")
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, end])


def add_inline(paragraph, text):
    parts = re.split(r"(`[^`]+`|\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            r = paragraph.add_run(part[1:-1])
            font(r, name="Consolas", size=9.3, color="1F4E78")
        elif part.startswith("**") and part.endswith("**"):
            r = paragraph.add_run(part[2:-2])
            font(r, bold=True)
        else:
            paragraph.add_run(part)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def borders(table):
    tbl_pr = table._tbl.tblPr
    node = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "6")
        e.set(qn("w:color"), "D9D9D9")
        node.append(e)
    tbl_pr.append(node)


def margins(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for side, value in (("top", 90), ("start", 110), ("bottom", 90), ("end", 110)):
        n = OxmlElement(f"w:{side}")
        n.set(qn("w:w"), str(value))
        n.set(qn("w:type"), "dxa")
        tc_mar.append(n)
    tc_pr.append(tc_mar)


doc = Document()
sec = doc.sections[0]
sec.page_width = Inches(8.5)
sec.page_height = Inches(11)
sec.top_margin = Inches(0.68)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.78)
sec.right_margin = Inches(0.78)
add_page_field(sec.footer.paragraphs[0])

styles = doc.styles
for style_name in ("Normal", "Body Text", "List Bullet", "List Number"):
    s = styles[style_name]
    s.font.name = "Arial"
    s._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    s._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    s.font.size = Pt(10.5)
    s.paragraph_format.space_after = Pt(4)

title = styles["Title"]
title.font.name = "Arial"
title._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
title._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
title.font.size = Pt(23)
title.font.bold = True
title.font.color.rgb = RGBColor(0, 0, 0)
title.paragraph_format.space_after = Pt(8)
title_ppr = title._element.get_or_add_pPr()
title_border = title_ppr.find(qn("w:pBdr"))
if title_border is not None:
    title_ppr.remove(title_border)

for name, size in (("Heading 1", 15), ("Heading 2", 12)):
    s = styles[name]
    s.font.name = "Arial"
    s._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    s._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = RGBColor(0, 0, 0)
    s.paragraph_format.space_before = Pt(8)
    s.paragraph_format.space_after = Pt(4)
    s.paragraph_format.keep_with_next = True

code_style = styles.add_style("Código", 1)
code_style.font.name = "Consolas"
code_style._element.rPr.rFonts.set(qn("w:ascii"), "Consolas")
code_style._element.rPr.rFonts.set(qn("w:hAnsi"), "Consolas")
code_style.font.size = Pt(8.6)
code_style.paragraph_format.left_indent = Inches(0.28)
code_style.paragraph_format.right_indent = Inches(0.15)
code_style.paragraph_format.space_after = Pt(1)

lines = SOURCE.read_text(encoding="utf-8").splitlines()
i = 0
in_code = False
first_body = True
while i < len(lines):
    line = lines[i]
    if line.startswith("```"):
        in_code = not in_code
        i += 1
        continue
    if in_code:
        p = doc.add_paragraph(style="Código")
        p.paragraph_format.keep_together = True
        p.add_run(line or " ")
        i += 1
        continue
    if not line.strip():
        i += 1
        continue
    if line.startswith("# "):
        p = doc.add_paragraph(style="Title")
        p.add_run(line[2:])
        meta = doc.add_paragraph()
        meta.paragraph_format.space_after = Pt(10)
        r = meta.add_run("Manual práctico para estudiantes · Haiku R1 Beta 6 · VirtualBox")
        font(r, size=10.5, color="555555")
    elif line.startswith("## "):
        p = doc.add_paragraph(style="Heading 1")
        p.add_run(line[3:])
    elif line.startswith("### "):
        p = doc.add_paragraph(style="Heading 2")
        p.add_run(line[4:])
    elif line.startswith("| "):
        table_lines = []
        while i < len(lines) and lines[i].startswith("|"):
            table_lines.append(lines[i])
            i += 1
        rows = [[c.strip() for c in row.strip("|").split("|")] for row in table_lines]
        rows = [rows[0]] + rows[2:]
        table = doc.add_table(rows=1, cols=len(rows[0]))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True
        borders(table)
        for c, value in zip(table.rows[0].cells, rows[0]):
            shade(c, "1F4E78")
            margins(c)
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            r = c.paragraphs[0].add_run(value)
            font(r, size=9, bold=True, color="FFFFFF")
        for n, values in enumerate(rows[1:]):
            row = table.add_row()
            for c, value in zip(row.cells, values):
                margins(c)
                c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                if n % 2:
                    shade(c, "EEF4F8")
                p = c.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                add_inline(p, value)
        i -= 1
    elif re.match(r"^\d+\. ", line):
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Inches(0.24)
        p.paragraph_format.first_line_indent = Inches(-0.18)
        p.paragraph_format.keep_together = True
        add_inline(p, line)
    elif line.startswith("- [ ] "):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.keep_together = True
        add_inline(p, "☐ " + line[6:])
    elif line.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.keep_together = True
        add_inline(p, line[2:])
    else:
        p = doc.add_paragraph(style="Body Text")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.widow_control = True
        add_inline(p, line)
        if first_body:
            p.paragraph_format.space_after = Pt(8)
            first_body = False
    i += 1

doc.core_properties.title = "Guía de Haiku en VirtualBox para Git Python y Java"
doc.core_properties.subject = "Instalación y prácticas de programación"
doc.core_properties.author = ""
doc.save(OUT)
print(OUT)
