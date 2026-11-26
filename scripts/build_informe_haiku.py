from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUT = Path(r"C:\Users\USUARIO\Downloads\U3FSOS\Informe_Haiku_VirtualBox.docx")


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color="D9D9D9", size="6"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def keep_row_together(row):
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            paragraph.paragraph_format.keep_together = True


def set_run_font(run, name="Arial", size=None, bold=None, color=None, italic=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    if italic is not None:
        run.italic = italic


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Página ")
    set_run_font(run, size=9, color="666666")
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.page_break_before = False
    r = p.add_run(text)
    return p


def add_body(doc, text, bold_lead=None):
    p = doc.add_paragraph(style="Body Text")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.keep_together = False
    p.paragraph_format.widow_control = True
    if bold_lead and text.startswith(bold_lead):
        lead = p.add_run(bold_lead)
        set_run_font(lead, bold=True)
        p.add_run(text[len(bold_lead):])
    else:
        p.add_run(text)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.keep_together = True
        p.paragraph_format.space_after = Pt(3)
        p.add_run(item)


def add_numbered(doc, items):
    for index, item in enumerate(items, start=1):
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Inches(0.28)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        p.paragraph_format.keep_together = True
        p.paragraph_format.space_after = Pt(3)
        p.add_run(f"{index}. {item}")


def add_code(doc, lines):
    for line in lines:
        p = doc.add_paragraph(style="Code")
        p.paragraph_format.keep_together = True
        p.add_run(line)


def add_table(doc, headers, rows, widths=None, font_size=9.2):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    header = table.rows[0]
    set_repeat_table_header(header)
    for i, value in enumerate(headers):
        cell = header.cells[i]
        set_cell_shading(cell, "1F4E78")
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(value)
        set_run_font(run, size=font_size, bold=True, color="FFFFFF")
        if widths:
            cell.width = Inches(widths[i])
    for row_index, values in enumerate(rows):
        row = table.add_row()
        keep_row_together(row)
        for i, value in enumerate(values):
            cell = row.cells[i]
            if row_index % 2 == 1:
                set_cell_shading(cell, "EEF4F8")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths:
                cell.width = Inches(widths[i])
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(value))
            set_run_font(run, size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


doc = Document()
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(0.72)
section.bottom_margin = Inches(0.67)
section.left_margin = Inches(0.82)
section.right_margin = Inches(0.82)
section.header_distance = Inches(0.3)
section.footer_distance = Inches(0.32)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Arial"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
normal.font.size = Pt(10.8)

body = styles["Body Text"]
body.font.name = "Arial"
body._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
body._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
body.font.size = Pt(10.8)
body.paragraph_format.line_spacing = 1.13
body.paragraph_format.space_after = Pt(5.5)

title = styles["Title"]
title.font.name = "Arial"
title._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
title._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
title.font.size = Pt(24)
title.font.bold = True
title.font.color.rgb = RGBColor(0, 0, 0)
title.paragraph_format.space_after = Pt(14)
title_ppr = title._element.get_or_add_pPr()
title_border = title_ppr.find(qn("w:pBdr"))
if title_border is not None:
    title_ppr.remove(title_border)

for name, size, before, after in (("Heading 1", 15, 9, 5), ("Heading 2", 11.8, 7, 3)):
    style = styles[name]
    style.font.name = "Arial"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(after)
    style.paragraph_format.keep_with_next = True

for name in ("List Bullet", "List Number"):
    style = styles[name]
    style.font.name = "Arial"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    style.font.size = Pt(10.6)
    style.paragraph_format.left_indent = Inches(0.25)
    style.paragraph_format.first_line_indent = Inches(-0.16)
    style.paragraph_format.space_after = Pt(3)

code = styles.add_style("Code", 1)
code.font.name = "Consolas"
code._element.rPr.rFonts.set(qn("w:ascii"), "Consolas")
code._element.rPr.rFonts.set(qn("w:hAnsi"), "Consolas")
code.font.size = Pt(8.6)
code.paragraph_format.left_indent = Inches(0.28)
code.paragraph_format.space_after = Pt(1)
code.paragraph_format.line_spacing = 1.0

footer = section.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
add_page_number(fp)

# Portada
doc.add_paragraph().paragraph_format.space_after = Pt(38)
p = doc.add_paragraph(style="Title")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Instalación de Haiku en VirtualBox y preparación de un entorno de desarrollo")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Informe técnico de práctica")
set_run_font(r, size=14, bold=True, color="444444")
p.paragraph_format.space_after = Pt(42)

meta = add_table(
    doc,
    ["Dato", "Información"],
    [
        ["Estudiante", "________________________________________"],
        ["Curso", "________________________________________"],
        ["Docente", "________________________________________"],
        ["Institución", "________________________________________"],
        ["Fecha", "22 de noviembre de 2026"],
    ],
    widths=[1.55, 4.65],
    font_size=10,
)
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Haiku R1 beta 6 de 64 bits sobre Oracle VM VirtualBox en Windows")
set_run_font(r, size=11, italic=True, color="444444")
page_break(doc)

# Página 2
add_heading(doc, "1 Resumen", 1)
add_body(doc, "Este informe documenta la instalación de Haiku R1 beta 6 en una máquina virtual de VirtualBox y su preparación como entorno de desarrollo con Git, Python y Java. La máquina usa 4 GB de memoria, 1 CPU, un disco VDI de 25 GB con Be File System y red NAT con reenvío del puerto 8080 de Windows al 8000 de Haiku. La instalación y las pruebas se realizaron entre el 19 y el 22 de noviembre de 2026.")
add_body(doc, "Resultados obtenidos: Haiku arranca desde el disco sin la ISO; la red NAT asigna 10.0.2.15; se instalaron Git 2.54.0, Python 3.14.7, OpenJDK 17.0.14 con javac y Genio 6.0.2-3. Python imprimió Cuaderno: 3 x S/ 5 = S/ 15, Java compiló y ejecutó Total Java: S/ 20, Git registró dos commits con árbol de trabajo limpio y Windows recibió HTTP 200 del servidor de Haiku por 127.0.0.1:8080. Genio abrió el proyecto practica y mostró la rama master con los archivos creados.")

add_heading(doc, "2 Objetivos", 1)
add_heading(doc, "2 1 Objetivo general", 2)
add_body(doc, "Configurar un escritorio Haiku virtualizado donde se pueda versionar, programar y ejecutar código en Python y Java, y consultar desde Windows un servicio web ejecutado dentro de la máquina virtual.")
add_heading(doc, "2 2 Objetivos específicos", 2)
add_bullets(doc, [
    "Crear una máquina virtual compatible con Haiku y completar la instalación en un volumen BFS.",
    "Configurar idioma, red y repositorios de paquetes.",
    "Instalar Git, Python, el JDK de Java y el IDE Genio mediante pkgman.",
    "Verificar control de versiones, ejecución de ambos lenguajes y comunicación entre invitado y anfitrión.",
    "Generar una copia exportable de la máquina para que otra persona continúe el trabajo.",
])

add_heading(doc, "3 Alcance", 1)
add_body(doc, "El trabajo cubre la instalación local en VirtualBox, la preparación del entorno y pruebas de programas académicos sencillos. No incluye C# o .NET dentro de Haiku ni presupone disponibilidad oficial de Visual Studio Code, IntelliJ, Claude Code o Codex en el sistema invitado. El trabajo remoto con Git se muestra con repositorios locales; la publicación en un servicio remoto queda como extensión.")
page_break(doc)

# Página 3
add_heading(doc, "4 Fundamentos técnicos", 1)
add_heading(doc, "4 1 Sistema operativo Haiku", 2)
add_body(doc, "Haiku es un sistema operativo independiente inspirado en BeOS. Su núcleo deriva de NewOS y no es Linux. Ofrece compatibilidad con interfaces y herramientas POSIX, por lo que Terminal, Git, compiladores e intérpretes funcionan de forma familiar.")
add_heading(doc, "4 2 Sistema de archivos y paquetes", 2)
add_body(doc, "La partición de instalación usa Be File System (BFS). Las aplicaciones se distribuyen como paquetes HPKG, administrados desde HaikuDepot o con pkgman. Se usaron los repositorios oficiales de Haiku y HaikuPorts.")
add_heading(doc, "4 3 Virtualización y red", 2)
add_body(doc, "VirtualBox actúa como hipervisor sobre Windows. La red NAT da acceso a Internet sin exponer la máquina a la red física. El reenvío TCP de 127.0.0.1:8080 hacia el puerto 8000 del invitado permite abrir en Windows el servidor HTTP que corre en Haiku.")

add_table(doc, ["Decisión", "Valor", "Justificación"], [
    ["Memoria", "4096 MB", "Evita una configuración insuficiente para navegador, IDE y compiladores."],
    ["Procesador", "1 CPU", "Reduce problemas durante la instalación inicial."],
    ["Disco", "VDI dinámico de 25 GB", "Reserva capacidad sin ocupar todo el espacio desde el inicio."],
    ["Firmware", "BIOS", "Opción indicada para esta instalación; EFI desactivado."],
    ["Vídeo", "VMSVGA y 64 MB", "Salida compatible; aceleración 3D desactivada."],
    ["Red", "NAT", "Acceso a Internet y reenvío de puertos."],
], widths=[1.2, 1.55, 3.65], font_size=8.8)

add_heading(doc, "4 4 Interpretación y compilación", 2)
add_body(doc, "Python ejecuta el fuente con el intérprete instalado. Java requiere javac para producir bytecode y java para ejecutarlo. Ambas formas de ejecución se probaron en el mismo sistema.")
page_break(doc)

# Página 4
add_heading(doc, "5 Configuración de la máquina virtual", 1)
add_table(doc, ["Opción", "Configuración"], [
    ["Nombre", "Haiku-Desarrollo"],
    ["ISO", "haiku-r1beta6-x86_64-anyboot.iso"],
    ["Tipo", "Other Unknown de 64 bits"],
    ["RAM y CPU", "4096 MB y 1 procesador"],
    ["Disco", "VDI dinámico de 25 GB"],
    ["Pantalla", "VMSVGA, 64 MB y 3D desactivado"],
    ["Red", "NAT, cable conectado e Intel PRO 1000 MT Desktop"],
    ["Puertos", "127.0.0.1:8080 hacia el puerto 8000 del invitado"],
], widths=[1.55, 4.85], font_size=9.2)

add_heading(doc, "6 Instalación de Haiku", 1)
add_numbered(doc, [
    "Iniciar la máquina desde la ISO, elegir español y abrir Instalar Haiku.",
    "Abrir DriveSetup y confirmar que el destino es el disco virtual vacío de 25 GB.",
    "Inicializar el disco con Intel Partition Map y crear una partición que ocupe todo el espacio.",
    "Marcarla como activa y formatearla en BFS con el nombre Haiku.",
    "Volver al instalador, elegir la ISO como origen y el volumen Haiku como destino.",
    "Iniciar la copia, apagar la máquina al terminar y retirar la ISO.",
    "Encender de nuevo y comprobar el arranque desde el disco virtual.",
])

add_heading(doc, "6 1 Control de seguridad durante el particionado", 2)
add_body(doc, "DriveSetup mostró el disco virtual de 25 GB; identificarlo por tamaño evita operar sobre otro medio. La partición activa y el sector de arranque permiten iniciar sin la ISO.")

add_heading(doc, "6 2 Resultado obtenido", 2)
add_body(doc, "El instalador confirmó la copia y la escritura del sector de arranque. Tras retirar la ISO, la máquina arrancó desde el disco, mostró el asistente de bienvenida y llegó al escritorio en español.")
page_break(doc)

# Página 5
add_heading(doc, "7 Configuración inicial y herramientas", 1)
add_body(doc, "En el primer inicio se eligió español y se entró al escritorio. La interfaz Intel PRO/1000 obtuvo la dirección 10.0.2.15 por DHCP y pkgman list-repos confirmó los repositorios oficiales de Haiku y HaikuPorts. Las herramientas se instalaron con pkgman desde Terminal.")

add_table(doc, ["Paquete", "Función", "Resultado verificado"], [
    ["git", "Control de versiones", "Git 2.54.0"],
    ["python3.14", "Intérprete de Python", "Python 3.14.7"],
    ["openjdk17 y openjdk17_default", "JDK para Java", "OpenJDK y javac 17.0.14"],
    ["genio", "IDE nativo de Haiku", "Genio 6.0.2-3; proyecto abierto"],
], widths=[1.9, 2.1, 2.4], font_size=8.9)

add_heading(doc, "7 1 Preparación del proyecto", 2)
add_body(doc, "Los archivos se guardan en una carpeta persistente del directorio personal. La Terminal permite crearla y confirmar las herramientas.")
add_code(doc, [
    "pkgman install git python3.14",
    "pkgman install openjdk17 openjdk17_default",
    "git version; python3.14 --version; javac -version",
    "mkdir -p /boot/home/Desarrollo/practica",
    "cd /boot/home/Desarrollo/practica",
])

add_heading(doc, "7 2 Criterios de aceptación y observaciones", 2)
add_bullets(doc, [
    "Haiku reconoce la red por DHCP y descarga paquetes por HTTPS: cumplido.",
    "Python, Java, javac y Git responden desde Terminal: cumplido.",
    "pkgman search no listó Genio, pero pkgman install genio sí resolvió el paquete; conviene probar la instalación directa.",
    "Una descarga de Genio fue rechazada por el servidor al 71 %; se reanudó reutilizando los paquetes ya descargados.",
])
page_break(doc)

# Página 6
add_heading(doc, "8 Prueba funcional en Python", 1)
add_body(doc, "El archivo presupuesto.py define un artículo, calcula el total y lo imprime. Con tres cuadernos a S/ 5 el total de control es 3 x 5 = S/ 15. Después se sirvió la carpeta por HTTP para comprobar la comunicación con Windows.")

add_heading(doc, "8 1 Ejecución", 2)
add_code(doc, [
    "cd /boot/home/Desarrollo/practica",
    "python3.14 presupuesto.py",
    "python3.14 -m http.server 8000 --bind 0.0.0.0",
])
add_body(doc, "La salida fue Cuaderno: 3 x S/ 5 = S/ 15. Con el servidor activo, Windows solicitó http://127.0.0.1:8080 y recibió HTTP 200; el registro del servidor en Haiku mostró la petición.")

add_table(doc, ["Prueba", "Resultado esperado", "Resultado obtenido"], [
    ["Salida de Python", "Cuaderno: 3 x S/ 5 = S/ 15", "Coincide"],
    ["Servidor en Haiku", "Escucha en 0.0.0.0:8000", "Activo"],
    ["Acceso desde Windows", "HTTP 200 en 127.0.0.1:8080", "HTTP 200"],
], widths=[1.8, 2.5, 2.1], font_size=9.3)

add_heading(doc, "8 2 Interpretación de la prueba", 2)
add_body(doc, "La salida demuestra el intérprete y el cálculo. La respuesta HTTP 200 por el puerto 8080 confirma que el reenvío NAT y el enlace a 0.0.0.0 funcionan, y que un servicio de Haiku es consultable desde Windows.")
page_break(doc)

# Página 7
add_heading(doc, "9 Prueba funcional en Java", 1)
add_body(doc, "Presupuesto.java multiplica 4 unidades por S/ 5 e imprime el total en consola. La prueba confirma que el JDK compila el fuente a bytecode y que la máquina virtual de Java lo ejecuta en Haiku.")

add_heading(doc, "9 1 Compilación y ejecución", 2)
add_code(doc, [
    "javac Presupuesto.java",
    "java Presupuesto",
])
add_table(doc, ["Paso", "Resultado esperado", "Resultado obtenido"], [
    ["javac", "Genera Presupuesto.class", "Archivo creado"],
    ["java", "Total Java: S/ 20", "Total Java: S/ 20"],
], widths=[1.4, 2.5, 2.5], font_size=9.2)

add_heading(doc, "9 2 Relación con Python", 2)
add_body(doc, "Ambos programas aplican la misma operación de precio por cantidad. Python se ejecuta directamente desde el fuente y Java necesita una compilación previa, lo que permite comparar los dos modelos de ejecución.")

add_heading(doc, "10 Control de versiones con Git", 1)
add_body(doc, "Se inicializó un repositorio en /boot/home/Desarrollo/practica, se configuró un usuario local y se hicieron dos commits: inicio, con README.md, presupuesto.py y Presupuesto.java, y resultados, con Presupuesto.class y resultado.html. Al final git status indicó que el árbol de trabajo estaba limpio.")
add_code(doc, [
    "git init",
    "git add README.md presupuesto.py Presupuesto.java",
    "git commit -m inicio",
    "git add Presupuesto.class resultado.html",
    "git commit -m resultados",
    "git status; git log --oneline",
])
add_body(doc, "Git funciona de forma local en Haiku. Para trabajo remoto bastaría agregar un servidor con git remote add origin y usar git push; no se probó en este informe.")
page_break(doc)

# Página 8
add_heading(doc, "11 Matriz de verificación", 1)
add_table(doc, ["Comprobación", "Criterio", "Estado"], [
    ["Arranque instalado", "Inicia desde el disco sin la ISO", "Cumplido"],
    ["Conectividad", "IP 10.0.2.15 y repositorios activos", "Cumplido"],
    ["Herramientas", "Git 2.54.0, Python 3.14.7, javac 17.0.14", "Cumplido"],
    ["Prueba Python", "Salida S/ 15 y HTTP 200 desde Windows", "Cumplido"],
    ["Prueba Java", "Compila y muestra S/ 20", "Cumplido"],
    ["Git", "Dos commits y árbol limpio", "Cumplido"],
    ["Genio", "Paquete 6.0.2-3 y proyecto abierto", "Cumplido"],
    ["Copia compartible", "Instantánea final y OVA validado de 655 MB", "Cumplido"],
], widths=[1.5, 3.85, 1.05], font_size=8.8)

add_heading(doc, "12 Problemas encontrados y solución", 1)
add_table(doc, ["Problema", "Acción correctiva"], [
    ["La VM vuelve al instalador", "Retirar la ISO y poner el disco duro primero en el arranque."],
    ["No aparece el disco destino", "Formatear la partición en BFS y reabrir el instalador."],
    ["pkgman search no muestra un paquete", "Probar pkgman install nombre y revisar pkgman list-repos."],
    ["Descarga rechazada por el servidor", "Repetir pkgman install; reutiliza los paquetes ya descargados."],
    ["Windows no abre el servidor", "Escuchar en 0.0.0.0 y revisar el reenvío 8080 hacia 8000."],
    ["javac no funciona", "Instalar también openjdk17_default."],
    ["Instantánea durante una actualización", "Hacerla con la VM estable y relanzar la instalación."],
], widths=[2.1, 4.3], font_size=8.7)
page_break(doc)

# Página 9
add_heading(doc, "13 Conclusiones", 1)
add_body(doc, "Haiku funciona en VirtualBox como entorno básico de desarrollo. Con 4 GB de RAM, un disco BFS de 25 GB y red NAT se obtuvo un sistema que arranca, descarga paquetes y ejecuta herramientas estándar sin recurrir a Linux.")
add_body(doc, "Las pruebas confirmaron los puntos clave: Python produjo S/ 15, Java compiló y produjo S/ 20, Git registró el historial sin cambios pendientes y Windows alcanzó el servidor de Haiku con HTTP 200. Las limitaciones son la ausencia de .NET, Visual Studio Code e IntelliJ oficiales y el uso de un repositorio Git solo local.")
add_body(doc, "Para continuar, la máquina se exportó como Haiku-Desarrollo-Listo.ova, un archivo validado de 655 MB, y se creó la instantánea Haiku listo para desarrollo. La copia permite repetir la práctica en otro equipo desde el estado funcional final.")

add_heading(doc, "14 Recomendaciones", 1)
add_bullets(doc, [
    "Usar la copia exportada para ensayar la demostración sin repetir la instalación.",
    "Probar Git remoto con un servicio como GitHub o Codeberg si el docente lo solicita.",
    "Evitar descargas o actualizaciones de último momento durante la exposición.",
    "Crear una instantánea antes de cada experimento y no tomarla durante una actualización.",
])

add_heading(doc, "15 Fuentes de consulta", 1)
sources = [
    "Haiku Project. Descargas de Haiku. https://download.haiku-os.org/",
    "Haiku Project. Notas de Haiku R1 beta 6. https://github.com/haiku/website/blob/master/content/get-haiku/r1beta6/release-notes.md",
    "Haiku User Guide. DriveSetup y Be File System. https://i18n.haiku-os.org/userguide/data/export/docs/userguide/en/applications/drivesetup.html",
    "Haiku User Guide. Instalación de aplicaciones y paquetes. https://i18n.haiku-os.org/userguide/data/export/docs/userguide/en/applications.html",
    "Genio. Repositorio oficial. https://codeberg.org/Genio/Genio",
    "Oracle. VirtualBox Downloads. https://www.virtualbox.org/wiki/Downloads",
]
for source in sources:
    p = doc.add_paragraph(style="Body Text")
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_after = Pt(3)
    p.add_run(source)

doc.core_properties.title = "Instalación de Haiku en VirtualBox y preparación de un entorno de desarrollo"
doc.core_properties.subject = "Informe técnico de práctica"
doc.core_properties.author = "Estudiante"
doc.core_properties.keywords = "Haiku, VirtualBox, Python, Java, Genio, BFS"

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(OUT)
