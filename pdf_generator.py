import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Paleta Verde Institucional FOSSO
COLOR_FOSSO_OSCURO = colors.HexColor("#10371E")  # Verde oscuro cabecera
COLOR_FOSSO_VERDE = colors.HexColor("#1B4D2E")   # Verde corporativo
COLOR_FOSSO_CLARO = colors.HexColor("#F1F8F3")   # Verde tenue alterno
COLOR_LINEA = colors.HexColor("#CBE3D1")

def pie_corporativo(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(36, 25, "FOSSO food and services solutions — Sistema de Gestión Operativa Integral")
    canvas.drawRightString(landscape(letter)[0] - 36, 25, f"Página {doc.page}")
    canvas.setStrokeColor(COLOR_FOSSO_VERDE)
    canvas.setLineWidth(0.8)
    canvas.line(36, 35, landscape(letter)[0] - 36, 35)
    canvas.restoreState()

def encabezado_estandar(titulo_principal: str, subtitulo: str, td_style, header_title_style, header_subtitle_style):
    logo_path = os.path.join("assets", "logo_fosso.png")
    if os.path.exists(logo_path):
        img_logo = RLImage(logo_path, width=80, height=35)
        bloque_logo = [
            img_logo,
            Paragraph("<font size=6 color='#555'><b>FOSSO</b><br/>Food Services Solution</font>", td_style)
        ]
    else:
        bloque_logo = [Paragraph("<b>FOSSO</b><br/><font size=6 color='#555'>Food Services Solution</font>", td_style)]

    bloque_titulos = [
        Paragraph(titulo_principal, header_title_style),
        Spacer(1, 2),
        Paragraph(subtitulo, header_subtitle_style)
    ]

    header_table = Table([[bloque_logo, bloque_titulos]], colWidths=[120, landscape(letter)[0] - 192])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    return header_table

def generar_pdf_calidad(registros: list, nota_gerencia: str, ruta_salida: str):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=45)
    styles = getSampleStyleSheet()
    
    header_title_style = ParagraphStyle('HTitle', parent=styles['Heading1'], fontSize=13, leading=16, textColor=COLOR_FOSSO_OSCURO, alignment=1, fontName="Helvetica-Bold")
    header_subtitle_style = ParagraphStyle('HSub', parent=styles['Normal'], fontSize=9, leading=11, textColor=COLOR_FOSSO_VERDE, alignment=1, fontName="Helvetica-Bold")
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.white, alignment=1, fontName="Helvetica-Bold")
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.HexColor("#222222"))
    td_estado = ParagraphStyle('TDE', parent=styles['Normal'], fontSize=7, leading=9, textColor=COLOR_FOSSO_VERDE, fontName="Helvetica-Bold", alignment=1)

    elementos = [
        encabezado_estandar("REPORTE DE OBSERVACIONES LEVANTADAS Y PLAN DE ACCIÓN", "SEGUIMIENTO DE OBSERVACIONES Y EVIDENCIA DE LEVANTAMIENTO", td_style, header_title_style, header_subtitle_style),
        Spacer(1, 6)
    ]

    headers = [
        Paragraph("ITEM", th_style), Paragraph("FOTO DEL<br/>HALLAZGO", th_style),
        Paragraph("DESCRIPCIÓN DEL HALLAZGO /<br/>OBSERVACIÓN", th_style),
        Paragraph("FOTO<br/>LEVANTADA", th_style), Paragraph("ACCIÓN CORRECTIVA /<br/>OBS. LEVANTADA", th_style),
        Paragraph("RESPONSABLE", th_style), Paragraph("FECHA<br/>HALLAZGO", th_style),
        Paragraph("FECHA<br/>LEVANT.", th_style), Paragraph("ESTADO", th_style),
    ]
    filas = [headers]

    for reg in registros:
        img_antes = RLImage(reg["foto_antes"], width=65, height=50) if reg.get("foto_antes") and os.path.exists(reg["foto_antes"]) else ""
        img_desp = RLImage(reg["foto_despues"], width=65, height=50) if reg.get("foto_despues") and os.path.exists(reg["foto_despues"]) else ""
        filas.append([
            Paragraph(str(reg.get("item", 1)), td_style), img_antes, Paragraph(reg.get("hallazgo", ""), td_style),
            img_desp, Paragraph(reg.get("accion_correctiva", "") or "-", td_style), Paragraph("<b>FOSSO</b>", td_style),
            Paragraph(str(reg.get("fecha_hallazgo", "")), td_style), Paragraph(str(reg.get("fecha_levantamiento", "") or "-"), td_style),
            Paragraph(reg.get("estado", "PENDIENTE"), td_estado if reg.get("estado") == "LEVANTADA" else td_style)
        ])

    tabla = Table(filas, colWidths=[30, 70, 160, 70, 160, 60, 60, 60, 60])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_FOSSO_OSCURO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_LINEA),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FOSSO_CLARO]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla)

    if nota_gerencia and nota_gerencia.strip():
        elementos.append(Spacer(1, 10))
        caja_nota = Table([[Paragraph(f"<b>DIRECTIVA DE GERENCIA:</b> {nota_gerencia}", td_style)]], colWidths=[landscape(letter)[0] - 72])
        caja_nota.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_FOSSO_CLARO),
            ('BOX', (0,0), (-1,-1), 1, COLOR_FOSSO_VERDE),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        elementos.append(KeepTogether([caja_nota]))

    doc.build(elementos, onFirstPage=pie_corporativo, onLaterPages=pie_corporativo)
    return ruta_salida

def generar_pdf_mantenimiento(maquinarias: list, operacion: str, sede: str, nota_gerencia: str, ruta_salida: str):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=45)
    styles = getSampleStyleSheet()
    
    header_title_style = ParagraphStyle('HTM', parent=styles['Heading1'], fontSize=13, leading=16, textColor=COLOR_FOSSO_OSCURO, alignment=1, fontName="Helvetica-Bold")
    header_subtitle_style = ParagraphStyle('HSM', parent=styles['Normal'], fontSize=9, leading=11, textColor=COLOR_FOSSO_VERDE, alignment=1, fontName="Helvetica-Bold")
    th_style = ParagraphStyle('THM', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.white, alignment=1, fontName="Helvetica-Bold")
    td_style = ParagraphStyle('TDM', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#222222"))
    
    elementos = [
        encabezado_estandar("REPORTE OFICIAL DE ESTADO Y MANTENIMIENTO DE MAQUINARIAS", f"OPERACIÓN: {operacion} — SEDE: {sede}", td_style, header_title_style, header_subtitle_style),
        Spacer(1, 8)
    ]

    headers = [
        Paragraph("CÓDIGO / TAG", th_style), Paragraph("NOMBRE DEL EQUIPO", th_style),
        Paragraph("ÁREA OPERATIVA", th_style), Paragraph("ESTADO", th_style),
        Paragraph("FREC. (DÍAS)", th_style), Paragraph("ÚLTIMO MANT.", th_style),
        Paragraph("FOTO DE ESTADO", th_style), Paragraph("ANOMALÍA / OBSERVACIÓN", th_style)
    ]
    filas = [headers]

    for m in maquinarias:
        img_eq = RLImage(m["foto_estado"], width=60, height=45) if m.get("foto_estado") and os.path.exists(m["foto_estado"]) else "-"
        filas.append([
            Paragraph(m.get("codigo_tag", "-"), td_style), Paragraph(m.get("nombre_equipo", "-"), td_style),
            Paragraph(m.get("area_operativa", "-"), td_style), Paragraph(m.get("estado", "-"), td_style),
            Paragraph(str(m.get("frecuencia_dias", 30)), td_style), Paragraph(str(m.get("ultimo_mantenimiento", "-")), td_style),
            img_eq, Paragraph(m.get("anomalia", "-") or "Sin anomalías", td_style)
        ])

    tabla = Table(filas, colWidths=[65, 120, 100, 75, 60, 70, 75, 175])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_FOSSO_OSCURO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_LINEA),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FOSSO_CLARO]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)

    if nota_gerencia and nota_gerencia.strip():
        elementos.append(Spacer(1, 10))
        caja_nota = Table([[Paragraph(f"<b>DIRECTIVA DE GERENCIA:</b> {nota_gerencia}", td_style)]], colWidths=[landscape(letter)[0] - 72])
        caja_nota.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_FOSSO_CLARO),
            ('BOX', (0,0), (-1,-1), 1, COLOR_FOSSO_VERDE),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        elementos.append(KeepTogether([caja_nota]))

    doc.build(elementos, onFirstPage=pie_corporativo, onLaterPages=pie_corporativo)
    return ruta_salida

def generar_pdf_ssoma_checklists(checklists: list, operacion: str, sede: str, ruta_salida: str):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=45)
    styles = getSampleStyleSheet()
    
    header_title_style = ParagraphStyle('HTS', parent=styles['Heading1'], fontSize=13, leading=16, textColor=COLOR_FOSSO_OSCURO, alignment=1, fontName="Helvetica-Bold")
    header_subtitle_style = ParagraphStyle('HSS', parent=styles['Normal'], fontSize=9, leading=11, textColor=COLOR_FOSSO_VERDE, alignment=1, fontName="Helvetica-Bold")
    th_style = ParagraphStyle('THS', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.white, alignment=1, fontName="Helvetica-Bold")
    td_style = ParagraphStyle('TDS', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#222222"))
    
    elementos = [
        encabezado_estandar("HISTORIAL DE CHECKLISTS OPERATIVOS SSOMA & INOCUIDAD", f"OPERACIÓN: {operacion} — SEDE: {sede}", td_style, header_title_style, header_subtitle_style),
        Spacer(1, 8)
    ]

    headers = [
        Paragraph("FECHA", th_style), Paragraph("TURNO", th_style),
        Paragraph("FORMATO / CHECKLIST", th_style), Paragraph("CONFORMIDAD", th_style),
        Paragraph("% CUMPLIMIENTO", th_style), Paragraph("OBSERVACIONES / DESVIACIONES", th_style),
        Paragraph("RESPONSABLE", th_style)
    ]
    filas = [headers]

    for c in checklists:
        porc = round((c['total_conformes'] / c['total_items'] * 100), 1) if c.get('total_items', 0) > 0 else 0
        filas.append([
            Paragraph(c.get("fecha", "-"), td_style), Paragraph(c.get("turno", "-"), td_style),
            Paragraph(c.get("tipo_checklist", "-"), td_style),
            Paragraph(f"{c.get('total_conformes', 0)} / {c.get('total_items', 0)}", td_style),
            Paragraph(f"<b>{porc}%</b>", td_style), Paragraph(c.get("observaciones", "-") or "Conforme", td_style),
            Paragraph(c.get("registrado_por", "-"), td_style)
        ])

    tabla = Table(filas, colWidths=[65, 60, 210, 75, 75, 160, 95])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_FOSSO_OSCURO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_LINEA),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FOSSO_CLARO]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=pie_corporativo, onLaterPages=pie_corporativo)
    return ruta_salida

def generar_pdf_condiciones_riesgo(condiciones: list, operacion: str, sede: str, ruta_salida: str):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=45)
    styles = getSampleStyleSheet()
    
    # Encabezados estrictamente en VERDE FOSSO
    header_title_style = ParagraphStyle('HTC', parent=styles['Heading1'], fontSize=13, leading=16, textColor=COLOR_FOSSO_OSCURO, alignment=1, fontName="Helvetica-Bold")
    header_subtitle_style = ParagraphStyle('HSC', parent=styles['Normal'], fontSize=9, leading=11, textColor=COLOR_FOSSO_VERDE, alignment=1, fontName="Helvetica-Bold")
    th_style = ParagraphStyle('THC', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.white, alignment=1, fontName="Helvetica-Bold")
    td_style = ParagraphStyle('TDC', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#222222"))
    
    # Estilos de texto exclusivos para la celda de NIVEL DE RIESGO
    style_alto = ParagraphStyle('CritAlto', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#78281F"), fontName="Helvetica-Bold", alignment=1)
    style_medio = ParagraphStyle('CritMedio', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#7D6608"), fontName="Helvetica-Bold", alignment=1)
    style_bajo = ParagraphStyle('CritBajo', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#1E8449"), fontName="Helvetica-Bold", alignment=1)

    elementos = [
        encabezado_estandar("REPORTE DE CONDICIONES INSEGURAS Y RIESGOS DE INFRAESTRUCTURA", f"OPERACIÓN: {operacion} — SEDE: {sede}", td_style, header_title_style, header_subtitle_style),
        Spacer(1, 8)
    ]

    # Nombre de columna corregido a "NIVEL DE RIESGO"
    headers = [
        Paragraph("ID", th_style), Paragraph("FECHA / REGISTRO", th_style),
        Paragraph("UBICACIÓN EXACTA", th_style), Paragraph("NIVEL DE RIESGO", th_style),
        Paragraph("EVIDENCIA FOTOGRÁFICA", th_style), Paragraph("DESCRIPCIÓN DE LA CONDICIÓN INSEGURA", th_style),
        Paragraph("REPORTADO POR", th_style)
    ]
    filas = [headers]

    # Cabecera verde oscuro y líneas verde suave
    estilos_tabla = [
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_FOSSO_OSCURO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_LINEA),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]

    for idx, cond in enumerate(condiciones, start=1):
        img_cond = RLImage(cond["foto_evidencia"], width=65, height=50) if cond.get("foto_evidencia") and os.path.exists(cond["foto_evidencia"]) else "-"
        
        # Lectura compatible tanto si el campo se llama nivel_riesgo como si viene de nivel_criticidad
        valor_riesgo = str(cond.get('nivel_riesgo') or cond.get('nivel_criticidad') or '').upper()

        if "ALTO" in valor_riesgo:
            p_riesgo = Paragraph(f"🚨 {valor_riesgo}", style_alto)
            bg_celda_riesgo = colors.HexColor("#FADBD8")  # Rojo suave
        elif "MEDIO" in valor_riesgo:
            p_riesgo = Paragraph(f"⚠️ {valor_riesgo}", style_medio)
            bg_celda_riesgo = colors.HexColor("#FCF3CF")  # Amarillo suave
        else:
            p_riesgo = Paragraph(f"✅ {valor_riesgo}", style_bajo)
            bg_celda_riesgo = colors.HexColor("#D5F5E3")  # Verde suave

        # Fondo general de la fila: blanco o verde corporativo clarito
        bg_fila = colors.white if idx % 2 != 0 else COLOR_FOSSO_CLARO
        estilos_tabla.append(('BACKGROUND', (0, idx), (-1, idx), bg_fila))
        
        # ÚNICAMENTE la celda de la columna índice 3 (NIVEL DE RIESGO) recibe el color de alerta
        estilos_tabla.append(('BACKGROUND', (3, idx), (3, idx), bg_celda_riesgo))

        filas.append([
            Paragraph(f"#{cond.get('id', '-')}", td_style),
            Paragraph(cond.get("fecha_registro", "-"), td_style),
            Paragraph(cond.get("ubicacion", "-"), td_style),
            p_riesgo,
            img_cond,
            Paragraph(cond.get("descripcion_riesgo", "-"), td_style),
            Paragraph(cond.get("registrado_por", "-"), td_style)
        ])

    tabla = Table(filas, colWidths=[30, 85, 110, 90, 75, 250, 100])
    tabla.setStyle(TableStyle(estilos_tabla))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=pie_corporativo, onLaterPages=pie_corporativo)
    return ruta_salida

def generar_pdf_charlas(charlas: list, operacion: str, sede: str, ruta_salida: str):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=45)
    styles = getSampleStyleSheet()
    
    header_title_style = ParagraphStyle('HTCH', parent=styles['Heading1'], fontSize=13, leading=16, textColor=COLOR_FOSSO_OSCURO, alignment=1, fontName="Helvetica-Bold")
    header_subtitle_style = ParagraphStyle('HSCH', parent=styles['Normal'], fontSize=9, leading=11, textColor=COLOR_FOSSO_VERDE, alignment=1, fontName="Helvetica-Bold")
    th_style = ParagraphStyle('THCH', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.white, alignment=1, fontName="Helvetica-Bold")
    td_style = ParagraphStyle('TDCH', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor("#222222"))
    
    elementos = [
        encabezado_estandar("HISTORIAL DE CAPACITACIONES Y CHARLAS DE 5 MINUTOS", f"OPERACIÓN: {operacion} — SEDE: {sede}", td_style, header_title_style, header_subtitle_style),
        Spacer(1, 8)
    ]

    headers = [
        Paragraph("FECHA / HORA", th_style), Paragraph("TEMA TRATADO", th_style),
        Paragraph("INSTRUCTOR", th_style), Paragraph("ASIST.", th_style),
        Paragraph("FOTO DEL EQUIPO", th_style), Paragraph("FICHA DE ASISTENCIA (FIRMAS)", th_style)
    ]
    filas = [headers]

    for ch in charlas:
        img_eq = RLImage(ch["foto_evidencia"], width=65, height=50) if ch.get("foto_evidencia") and os.path.exists(ch["foto_evidencia"]) else "-"
        img_asist = RLImage(ch["foto_asistencia"], width=65, height=50) if ch.get("foto_asistencia") and os.path.exists(ch["foto_asistencia"]) else "-"
        filas.append([
            Paragraph(f"{ch.get('fecha', '')}<br/>{ch.get('hora', '')}", td_style), Paragraph(ch.get("tema", ""), td_style),
            Paragraph(ch.get("instructor", ""), td_style), Paragraph(str(ch.get("num_asistentes", 0)), td_style),
            img_eq, img_asist
        ])

    tabla = Table(filas, colWidths=[80, 240, 120, 50, 125, 125])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_FOSSO_OSCURO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_LINEA),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FOSSO_CLARO]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)
    doc.build(elementos, onFirstPage=pie_corporativo, onLaterPages=pie_corporativo)
    return ruta_salida