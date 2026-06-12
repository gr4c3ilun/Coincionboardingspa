"""
Genera workbook.pdf — Inducción COINCI SA de CV
Requiere: pip install reportlab
Uso:      python workbook.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import date

# ── COLORS ──────────────────────────────────────────
NAVY    = colors.HexColor('#0d1b4b')
ACCENT  = colors.HexColor('#4a90d9')
SUCCESS = colors.HexColor('#2ecc7a')
BONE    = colors.HexColor('#edeef0')
WHITE   = colors.white
LIGHT   = colors.HexColor('#f0f4ff')
MUTED   = colors.HexColor('#6b7280')
DANGER  = colors.HexColor('#e74c3c')

OUTPUT   = 'workbook.pdf'
LOGO     = os.path.join('assets', 'logo.png')
PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch


# ── HELPERS ─────────────────────────────────────────
def logo_img(w=1.8*inch, h=0.75*inch):
    if os.path.exists(LOGO):
        img = RLImage(LOGO, width=w, height=h)
        img.hAlign = 'CENTER'
        return img
    return Paragraph('<b>COINCI</b>', ParagraphStyle('lp', fontName='Helvetica-Bold',
        fontSize=18, textColor=WHITE, alignment=TA_CENTER))


def module_header(num, title):
    data = [[
        Paragraph(f'<font color="#4a90d9"><b>MÓDULO {num}</b></font>', ParagraphStyle(
            'mnum', fontName='Helvetica-Bold', fontSize=11, textColor=ACCENT, leading=13)),
        Paragraph(f'<b>{title}</b>', ParagraphStyle(
            'mtit', fontName='Helvetica-Bold', fontSize=17, textColor=WHITE, leading=20)),
    ]]
    t = Table(data, colWidths=[1.1*inch, PAGE_W - 2*MARGIN - 1.1*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (0,0), 16),
        ('LEFTPADDING', (1,0), (1,0), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    return t


def section_title(text):
    return Paragraph(f'<b>{text}</b>', ParagraphStyle(
        'st', fontName='Helvetica-Bold', fontSize=11, textColor=NAVY,
        spaceBefore=14, spaceAfter=5))


def body_text(text):
    return Paragraph(text, ParagraphStyle(
        'bt', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#374151'),
        leading=15, spaceAfter=4))


def bullet(text):
    return Paragraph(f'<bullet>•</bullet>{text}', ParagraphStyle(
        'bl', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#374151'),
        leading=15, leftIndent=14, spaceAfter=3))


def notes_block(lines=5):
    items = []
    items.append(section_title('Notas'))
    for _ in range(lines):
        items.append(HRFlowable(width='100%', thickness=0.5,
                                color=colors.HexColor('#c8cdd6'), dash=(2,3),
                                spaceAfter=14))
    return items


def key_takeaways(points):
    rows = []
    for p in points:
        rows.append([
            Paragraph(f'✔ {p}', ParagraphStyle(
                'kt', fontName='Helvetica', fontSize=10,
                textColor=colors.HexColor('#374151'), leading=14))
        ])
    t = Table(rows, colWidths=[PAGE_W - 2*MARGIN - 0.15*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LINEBEFORE',    (0,0), (0,-1), 4, SUCCESS),
        ('ROWBACKGROUNDS',(0,0), (-1,-1), [colors.HexColor('#f0fdf4'), colors.HexColor('#e8faf0')]),
    ]))
    return [
        section_title('Key Takeaways'),
        t,
    ]


# ── DOCUMENT SETUP ──────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title='Workbook de Inducción — COINCI SA de CV',
        author='COINCI SA de CV',
    )

    story = []

    # ── COVER PAGE ──────────────────────────────────
    cover_logo = logo_img(2.2*inch, 0.9*inch)
    story.append(Spacer(1, 1.2*inch))
    story.append(cover_logo)
    story.append(Spacer(1, 0.4*inch))

    # colored stripe
    stripe = Table([['']], colWidths=[PAGE_W - 2*MARGIN], rowHeights=[5])
    stripe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT),
    ]))
    story.append(stripe)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph('Workbook de Inducción', ParagraphStyle(
        'ct', fontName='Helvetica-Bold', fontSize=28, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph('Programa de Inducción para Nuevos Empleados', ParagraphStyle(
        'cs', fontName='Helvetica', fontSize=13, textColor=MUTED, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.6*inch))

    # name & date fields
    fields = [
        ['Nombre del empleado:', '__________________________________________________'],
        ['Fecha de inicio:',     '__________________________________________________'],
        ['Supervisor:',          '__________________________________________________'],
    ]
    ft = Table(fields, colWidths=[1.7*inch, PAGE_W - 2*MARGIN - 1.7*inch])
    ft.setStyle(TableStyle([
        ('FONTNAME',  (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',  (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE',  (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), NAVY),
        ('TEXTCOLOR', (1,0), (1,-1), MUTED),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.5*inch))

    # index
    story.append(Paragraph('Contenido', ParagraphStyle(
        'idx', fontName='Helvetica-Bold', fontSize=13, textColor=NAVY, spaceAfter=10)))

    modules = [
        ('Módulo 1', 'Bienvenida a COINCI'),
        ('Módulo 2', 'Código de Ética'),
        ('Módulo 3', 'Reglas del Lugar de Trabajo'),
        ('Módulo 4', 'Seguridad Ocupacional'),
    ]
    for num, title in modules:
        row = Table(
            [[Paragraph(f'<b>{num}</b>', ParagraphStyle('in', fontName='Helvetica-Bold',
                fontSize=10, textColor=ACCENT)),
              Paragraph(title, ParagraphStyle('it', fontName='Helvetica',
                fontSize=10, textColor=colors.HexColor('#374151')))]],
            colWidths=[0.9*inch, PAGE_W - 2*MARGIN - 0.9*inch]
        )
        row.setStyle(TableStyle([
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ]))
        story.append(row)

    story.append(PageBreak())

    # ── MODULE 1 ────────────────────────────────────
    story.append(module_header(1, 'Bienvenida a COINCI'))
    story.append(Spacer(1, 0.2*inch))

    story.append(section_title('¿Quiénes somos?'))
    story.append(body_text(
        'COINCI SA de CV es una empresa salvadoreña especializada en proyectos de '
        '<b>construcción civil, eléctrica y mecánica</b>, comprometida con la calidad '
        'y el desarrollo del país.'))

    story.append(section_title('Misión'))
    story.append(body_text(
        'Ofrecer las mejores soluciones con <b>calidad, eficiencia y precios competitivos</b>, '
        'superando las expectativas de los clientes.'))

    story.append(section_title('Visión'))
    story.append(body_text(
        'Ser <b>líderes nacionales</b> en la industria de la construcción, reconocidos por '
        'calidad, confiabilidad y satisfacción plena del cliente.'))

    story.append(section_title('Valores'))
    for v, d in [
        ('Honestidad', 'Transparencia en todas nuestras acciones.'),
        ('Respeto',    'Valoramos la diversidad de opiniones y personas.'),
        ('Compromiso', 'Cumplimos nuestras responsabilidades siempre.'),
    ]:
        story.append(bullet(f'<b>{v}:</b> {d}'))

    story.extend(notes_block(5))
    story.extend(key_takeaways([
        'COINCI opera en construcción civil, eléctrica y mecánica.',
        'Nuestra misión se centra en calidad y precios competitivos.',
        'Honestidad, Respeto y Compromiso son los valores centrales.',
        'La visión es el liderazgo nacional en construcción.',
    ]))
    story.append(PageBreak())

    # ── MODULE 2 ────────────────────────────────────
    story.append(module_header(2, 'Código de Ética'))
    story.append(Spacer(1, 0.2*inch))

    story.append(section_title('Objetivo'))
    story.append(body_text(
        'Armonizar los <b>principios morales con las leyes y regulaciones</b> aplicables, '
        'definiendo los estándares de conducta esperados de cada colaborador.'))

    story.append(section_title('Principios'))
    for p in ['Máxima calidad en el servicio prestado.',
              'Atención al cliente con cortesía y profesionalismo.',
              'Integridad en todas las relaciones laborales y comerciales.']:
        story.append(bullet(p))

    story.append(section_title('Conflicto de intereses'))
    for p in ['Prohibido aceptar regalos o beneficios de proveedores o clientes.',
              'No favorecer a terceros con recursos de la empresa.',
              'Reportar toda situación de conflicto al supervisor inmediato.']:
        story.append(bullet(p))

    story.append(section_title('No nepotismo'))
    story.append(body_text(
        'Los familiares de empleados <b>no pueden participar</b> en licitaciones ni '
        'contrataciones donde el empleado tenga influencia directa.'))

    story.append(section_title('Conductas prohibidas — consecuencia: despido inmediato'))
    for p in [
        'Falsificación o alteración de documentos.',
        'Bajo desempeño reiterado sin justificación.',
        'Divulgar información confidencial de la empresa o clientes.',
        'Irrespetar a compañeros de trabajo o jefes.',
        'Presentarse bajo efectos de alcohol o drogas.',
        'Dañar materiales, equipos o instalaciones.',
        'Cualquier forma de acoso (laboral, sexual u otros).',
        'Ausencias injustificadas por 2 días consecutivos.',
        'Revelar ofertas de proveedores a terceros.',
    ]:
        story.append(bullet(p))

    story.extend(notes_block(5))
    story.extend(key_takeaways([
        'El código armoniza la ética con el marco legal de la empresa.',
        'Nunca aceptes regalos ni favorezcas a terceros.',
        'Dos ausencias injustificadas consecutivas = despido inmediato.',
        'Cualquier conflicto de interés debe reportarse al supervisor.',
    ]))
    story.append(PageBreak())

    # ── MODULE 3 ────────────────────────────────────
    story.append(module_header(3, 'Reglas del Lugar de Trabajo'))
    story.append(Spacer(1, 0.2*inch))

    story.append(section_title('Puntualidad y asistencia'))
    for p in ['Llegar puntual al inicio de la jornada laboral.',
              'Avisar al supervisor ante cualquier ausencia y justificarla.',
              'Dos faltas injustificadas consecutivas son causal de despido.']:
        story.append(bullet(p))

    story.append(section_title('Conducta'))
    for p in ['Mantener trato respetuoso con compañeros, superiores y clientes.',
              'Prohibido presentarse bajo efectos de alcohol o drogas.',
              'Evitar discusiones o conflictos en el área de trabajo.']:
        story.append(bullet(p))

    story.append(section_title('Limpieza y orden'))
    for p in ['Mantener el área de trabajo limpia y ordenada.',
              'Depositar residuos en los lugares indicados.',
              'Reportar condiciones insalubres al supervisor.']:
        story.append(bullet(p))

    story.append(section_title('Cuidado de equipos'))
    for p in ['Devolver equipos y herramientas en el mismo estado recibido.',
              'Reportar de inmediato cualquier daño o avería.',
              'No usar equipos de la empresa para fines personales sin autorización.']:
        story.append(bullet(p))

    story.append(section_title('Confidencialidad'))
    story.append(body_text(
        'No compartir <b>información de proyectos, presupuestos ni datos de clientes</b> '
        'con personas externas ni publicarla en ningún medio.'))

    story.append(section_title('Comunicación'))
    story.append(body_text(
        'Ante cualquier problema, el primer paso es <b>comunicarse con el supervisor '
        'inmediato</b> de forma respetuosa y directa.'))

    story.extend(notes_block(5))
    story.extend(key_takeaways([
        'La puntualidad y asistencia son responsabilidad de cada empleado.',
        'Reporta inmediatamente cualquier daño a equipos o materiales.',
        'La confidencialidad de proyectos y clientes es obligatoria.',
        'Ante un problema, habla siempre con tu supervisor.',
    ]))
    story.append(PageBreak())

    # ── MODULE 4 ────────────────────────────────────
    story.append(module_header(4, 'Seguridad Ocupacional'))
    story.append(Spacer(1, 0.2*inch))

    story.append(section_title('EPP obligatorio en todo momento'))
    epp = [
        'Casco de seguridad', 'Lentes protectores', 'Guantes de trabajo',
        'Botas punta de acero', 'Chaleco reflectivo', 'Mascarilla',
    ]
    # 2-column grid for EPP
    epp_rows = []
    for i in range(0, len(epp), 2):
        row = [bullet(f'<b>{epp[i]}</b>')]
        if i+1 < len(epp):
            row.append(bullet(f'<b>{epp[i+1]}</b>'))
        else:
            row.append(Paragraph('', ParagraphStyle('_')))
        epp_rows.append(row)

    epp_t = Table(epp_rows, colWidths=[(PAGE_W - 2*MARGIN)/2]*2)
    epp_t.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(epp_t)

    story.append(section_title('Uso seguro de maquinaria'))
    for p in ['Solo operar maquinaria para la que tienes capacitación y autorización.',
              'Inspeccionar el equipo antes de cada uso.',
              'Nunca desactivar dispositivos de seguridad de las máquinas.',
              'Reportar cualquier anomalía antes de continuar operando.']:
        story.append(bullet(p))

    story.append(section_title('Uniformes y vestimenta'))
    for p in ['Usar el uniforme completo de COINCI durante toda la jornada.',
              'Evitar ropa suelta o holgada que pueda engancharse en maquinaria.',
              'No usar accesorios (aretes, pulseras, collares) con riesgo de atrapamiento.']:
        story.append(bullet(p))

    story.append(section_title('Procedimiento en emergencias'))
    for p in ['Detener el trabajo de inmediato ante cualquier incidente.',
              'Avisar al supervisor sin demora.',
              'No mover al lesionado salvo riesgo inminente mayor.',
              'Conocer la ubicación del botiquín y del extintor más cercano.',
              'Seguir instrucciones del supervisor hasta el cierre del incidente.']:
        story.append(bullet(p))

    story.extend(notes_block(5))
    story.extend(key_takeaways([
        'El EPP es obligatorio: casco, lentes, guantes, botas, chaleco y mascarilla.',
        'Solo opera maquinaria para la que fuiste capacitado.',
        'Ante un accidente: para, avisa al supervisor, no muevas al lesionado.',
        'Conoce la ubicación del botiquín y extintor antes de comenzar a trabajar.',
    ]))
    story.append(PageBreak())

    # ── CLOSING PAGE ────────────────────────────────
    story.append(Spacer(1, 1.4*inch))
    story.append(logo_img(2*inch, 0.8*inch))
    story.append(Spacer(1, 0.4*inch))

    stripe2 = Table([['']], colWidths=[PAGE_W - 2*MARGIN], rowHeights=[4])
    stripe2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), SUCCESS)]))
    story.append(stripe2)
    story.append(Spacer(1, 0.35*inch))

    story.append(Paragraph('¡Listo para comenzar!', ParagraphStyle(
        'cl', fontName='Helvetica-Bold', fontSize=26, textColor=NAVY, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        'Regresa al entrenamiento en línea para completar los módulos interactivos y obtener tu diploma.',
        ParagraphStyle('cs2', fontName='Helvetica', fontSize=12, textColor=MUTED,
                       alignment=TA_CENTER, leading=18)))
    story.append(Spacer(1, 0.4*inch))

    story.append(Paragraph(
        'Abre el archivo <b>index.html</b> en tu navegador para continuar.',
        ParagraphStyle('co', fontName='Helvetica', fontSize=11,
                       textColor=colors.HexColor('#374151'), alignment=TA_CENTER)))

    story.append(Spacer(1, 1.2*inch))
    story.append(Paragraph(
        f'COINCI SA de CV &nbsp;&bull;&nbsp; Workbook generado el {date.today().strftime("%d/%m/%Y")}',
        ParagraphStyle('ft', fontName='Helvetica', fontSize=8, textColor=MUTED, alignment=TA_CENTER)))

    # ── BUILD ────────────────────────────────────────
    doc.build(story)
    print(f'PDF generado: {OUTPUT}')


if __name__ == '__main__':
    build()
