import streamlit as st
import os
import base64
import importlib
from datetime import datetime, date
import database as db
import auth
import pdf_generator as pdf_gen

# Recarga limpia de módulos
importlib.reload(pdf_gen)

# Enlace directo del icono oficial en GitHub
URL_ICONO_RAW = "https://raw.githubusercontent.com/guaniloantonio7-ai/fosso-app/main/assets/icono_app.png"

# Detección de ruta local como respaldo
ruta_logo_local = os.path.join("assets", "icono_app.png")
if not os.path.exists(ruta_logo_local):
    ruta_logo_local = os.path.join("assets", "logo_fosso.png")

# Configurar icono oficial en la pestaña del navegador
st.set_page_config(
    page_title="FOSSO | Gestión Operativa",
    page_icon=ruta_logo_local if os.path.exists(ruta_logo_local) else URL_ICONO_RAW,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Base de Datos
db.init_db()

# Función para codificar imagen a base64
def obtener_imagen_base64(ruta_imagen):
    if os.path.exists(ruta_imagen):
        with open(ruta_imagen, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

b64_ico = obtener_imagen_base64(ruta_logo_local)
tag_ico = f"data:image/png;base64,{b64_ico}" if b64_ico else URL_ICONO_RAW

# Inyección de Metadatos PWA y Estilos visuales
st.markdown(f"""
    <head>
        <title>FOSSO</title>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="FOSSO">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#10371E">
        <link rel="apple-touch-icon" href="{URL_ICONO_RAW}">
        <link rel="apple-touch-icon-precomposed" href="{URL_ICONO_RAW}">
        <link rel="icon" type="image/png" href="{URL_ICONO_RAW}">
        <link rel="shortcut icon" type="image/png" href="{URL_ICONO_RAW}">
    </head>
    <style>
        /* 1. FLECHA DEL MENÚ LATERAL (ABRIR Y CERRAR) SIEMPRE VISIBLE Y EN PRIMER PLANO */
        [data-testid="collapsedControl"] {{
            display: block !important;
            visibility: visible !important;
            z-index: 999999 !important;
            color: #10371E !important;
            top: 15px !important;
            left: 15px !important;
        }}
        [data-testid="collapsedControl"] button,
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebarCollapseButton"] {{
            visibility: visible !important;
            display: inline-flex !important;
            color: #10371E !important;
            background-color: rgba(255, 255, 255, 0.85) !important;
            border-radius: 8px !important;
            z-index: 999999 !important;
        }}

        /* 2. ELIMINAR "Hosted with Streamlit" Y EL BOTÓN "Manage app" EN PC Y MÓVIL */
        .viewerBadge_container__1QSob,
        div[class*="viewerBadge"],
        a[class*="viewerBadge"],
        div[class*="manageApp"],
        button[class*="manageApp"],
        div[class*="ManageApp"],
        #manage-app-button,
        [data-testid="stStatusWidget"],
        [data-testid="stConnectionStatus"],
        footer {{
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            width: 0px !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}

        /* 3. ELIMINAR HERRAMIENTAS DE DESARROLLO (GitHub, Share, Fork, Lápiz) */
        [data-testid="stToolbarActions"],
        [data-testid="stToolbar"] > div:first-child,
        [data-testid="stAppDeployButton"],
        .stToolbarActionButton,
        button[title="View app in GitHub"],
        button[title="Edit app in GitHub"],
        button[title="Fork this app"] {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* 4. Cabecera invisible para despejar la pantalla */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* 5. Fondo general de la barra lateral */
        section[data-testid="stSidebar"] {{
            background-color: #10371E !important;
        }}
        
        /* 6. Textos, títulos y etiquetas en blanco en sidebar */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span:not([data-baseweb="select"] span),
        section[data-testid="stSidebar"] label {{
            color: #FFFFFF !important;
        }}

        /* 7. Cajas de selección: Fondo blanco con texto negro nítido */
        section[data-testid="stSidebar"] [data-baseweb="select"] {{
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
        }}
        section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            border: 2px solid #2E7D32 !important;
            min-height: 42px !important;
        }}
        section[data-testid="stSidebar"] [data-baseweb="select"] div,
        section[data-testid="stSidebar"] [data-baseweb="select"] span,
        section[data-testid="stSidebar"] [data-baseweb="select"] input {{
            color: #111111 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            -webkit-text-fill-color: #111111 !important;
        }}
        section[data-testid="stSidebar"] [data-baseweb="select"] svg {{
            fill: #1B4D2E !important;
            color: #1B4D2E !important;
        }}

        /* 8. Menú desplegable emergente al hacer clic */
        [data-baseweb="popover"], [data-baseweb="menu"], ul[role="listbox"] {{
            background-color: #FFFFFF !important;
        }}
        [data-baseweb="menu"] li, ul[role="listbox"] li {{
            background-color: #FFFFFF !important;
            color: #111111 !important;
            font-weight: 600 !important;
        }}
        [data-baseweb="menu"] li:hover, ul[role="listbox"] li[aria-selected="true"] {{
            background-color: #E8F5E9 !important;
            color: #1B4D2E !important;
        }}

        /* 9. Botones corporativos */
        .stButton>button {{
            background-color: #1B4D2E;
            color: white !important;
            border-radius: 6px;
            font-weight: 600;
            border: 1px solid #2E7D32;
        }}
        .stButton>button:hover {{
            background-color: #2E7D32;
            color: white !important;
        }}
    </style>
""", unsafe_allow_html=True)

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

def pie_autoria():
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #555555; font-size: 0.85em; font-weight: bold;'>"
        "DESARROLLADO POR: ING. ANTONIO GUANILO GONZALES"
        "</p>",
        unsafe_allow_html=True
    )

if not st.session_state["autenticado"]:
    auth.login_ui()
    pie_autoria()
    st.stop()

# ==============================================================================
# BARRA LATERAL CON LOGOS, USUARIO Y SELECTOR DE TEMA
# ==============================================================================
usuario = st.session_state["usuario"]

logo_fosso = os.path.join("assets", "logo_fosso.png")
if not os.path.exists(logo_fosso):
    logo_fosso = os.path.join("assets", "icono_app.png")

if os.path.exists(logo_fosso):
    b64_logo = obtener_imagen_base64(logo_fosso)
    st.sidebar.markdown(
        f"""
        <div style="
            background-color: #FFFFFF;
            padding: 12px 10px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            margin-bottom: 18px;
        ">
            <img src="data:image/png;base64,{b64_logo}" style="max-width: 90%; height: auto; display: block; margin: 0 auto;" />
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.image(URL_ICONO_RAW, use_container_width=True)

st.sidebar.markdown(f"**Usuario:** <span style='color: #FFFFFF;'>{usuario['nombre']}</span>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Cargo:** <span style='color: #A3E4D7; font-weight: bold;'>{usuario['cargo']}</span>", unsafe_allow_html=True)

if st.sidebar.button("Cerrar Sesión", use_container_width=True):
    st.session_state["autenticado"] = False
    st.session_state["usuario"] = None
    st.rerun()

st.sidebar.markdown("---")

# Selector de Tema Visual
tema_elegido = st.sidebar.selectbox(
    "🎨 Tema Visual:",
    ["Sistema / Claro", "Oscuro", "Claro"],
    index=0
)

if tema_elegido == "Oscuro":
    st.markdown("""
        <style>
            .stApp {
                background-color: #0E1117 !important;
                color: #FAFAFA !important;
            }
            .stMarkdown, p, span, label, h1, h2, h3, h4 {
                color: #FAFAFA !important;
            }
            [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
                color: #FAFAFA !important;
            }
            .stTextInput>div>div>input, .stTextArea textarea {
                background-color: #262730 !important;
                color: #FFFFFF !important;
            }
        </style>
    """, unsafe_allow_html=True)
elif tema_elegido == "Claro":
    st.markdown("""
        <style>
            .stApp {
                background-color: #F8F9FA !important;
                color: #111111 !important;
            }
        </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Selección de Sede")

op_seleccionada = st.sidebar.selectbox("Operación:", ["UNIFRUTTI", "AGROLMOS"])

logo_unifrutti = os.path.join("assets", "logo_unifrutti.png")
logo_agrolmos = os.path.join("assets", "logo_agrolmos.png")

if op_seleccionada == "UNIFRUTTI":
    fundos = ["Bomarea", "Mosqueta", "Hefei", "Pirona"]
    sub_sede = st.sidebar.selectbox("Fundo:", fundos)
    nombre_pantalla_sede = f"UNIFRUTTI - {sub_sede}"
    if os.path.exists(logo_unifrutti):
        st.sidebar.image(logo_unifrutti, caption=f"Fundo {sub_sede}", width=150)
else:
    sub_sede = "AGROLMOS"
    nombre_pantalla_sede = "AGROLMOS"
    if os.path.exists(logo_agrolmos):
        st.sidebar.image(logo_agrolmos, width=150)

modulo = st.sidebar.radio(
    "Módulo:",
    ["📊 Dashboard KPIs", "📋 Calidad & 5S", "🛠️ Mantenimiento", "🦺 SSOMA & Inocuidad", "⏱️ Capacitaciones 5 Min"]
)

# Helper para Notas Gerenciales
def seccion_notas_gerencia(mod_nombre: str):
    st.markdown("---")
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT texto_nota, autor, cargo, fecha_hora 
        FROM notas_gerencia 
        WHERE operacion = ? AND sub_sede = ? AND modulo = ? 
        ORDER BY id DESC LIMIT 1
    """, (op_seleccionada, sub_sede, mod_nombre))
    nota = cur.fetchone()
    conn.close()

    texto_nota_actual = nota["texto_nota"] if nota else ""
    if nota:
        st.info(f"**Directiva Vigente ({nota['fecha_hora']} - {nota['autor']}):**\n\n{nota['texto_nota']}")

    if usuario["es_liderazgo"]:
        with st.expander("📝 Registrar / Modificar Directiva Gerencial"):
            nueva_nota = st.text_area("Directiva para este módulo:", value=texto_nota_actual)
            if st.button("Guardar Directiva", key=f"btn_nota_{mod_nombre}"):
                if nueva_nota.strip():
                    conn = db.get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO notas_gerencia (operacion, sub_sede, modulo, texto_nota, autor, cargo, fecha_hora)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (op_seleccionada, sub_sede, mod_nombre, nueva_nota.strip(), usuario["nombre"], usuario["cargo"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    st.success("Directiva registrada con éxito.")
                    st.rerun()
    return texto_nota_actual

# ==============================================================================
# VISTA 1: DASHBOARD KPIS
# ==============================================================================
if modulo == "📊 Dashboard KPIs":
    st.title(f"Centro de Control: {nombre_pantalla_sede}")
    hoy_str = date.today().isoformat()
    
    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as total FROM calidad_5s WHERE operacion = ? AND sub_sede = ?", (op_seleccionada, sub_sede))
    tot_5s = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) as cerradas FROM calidad_5s WHERE operacion = ? AND sub_sede = ? AND estado = 'LEVANTADA'", (op_seleccionada, sub_sede))
    cerr_5s = cur.fetchone()["cerradas"]
    kpi_5s = round((cerr_5s / tot_5s * 100), 1) if tot_5s > 0 else 100.0

    cur.execute("SELECT COUNT(*) as total FROM inventario_maquinarias WHERE operacion = ? AND sub_sede = ?", (op_seleccionada, sub_sede))
    tot_maq = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) as operativas FROM inventario_maquinarias WHERE operacion = ? AND sub_sede = ? AND estado = 'Operativo'", (op_seleccionada, sub_sede))
    op_maq = cur.fetchone()["operativas"]
    kpi_maq = round((op_maq / tot_maq * 100), 1) if tot_maq > 0 else 100.0

    cur.execute("SELECT COUNT(*) as conteo FROM charlas_5min WHERE operacion = ? AND sub_sede = ? AND fecha = ?", (op_seleccionada, sub_sede, hoy_str))
    charla_hoy = cur.fetchone()["conteo"]
    kpi_charla = 100.0 if charla_hoy > 0 else 0.0

    cur.execute("SELECT COUNT(*) as conteo FROM ssoma_checklists WHERE operacion = ? AND sub_sede = ? AND fecha = ?", (op_seleccionada, sub_sede, hoy_str))
    chk_hoy = cur.fetchone()["conteo"]
    kpi_chk = 100.0 if chk_hoy > 0 else 0.0

    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Levantamiento 5S", f"{kpi_5s}%", f"{cerr_5s}/{tot_5s} resueltas")
    col2.metric("🛠️ Disponibilidad Equipos", f"{kpi_maq}%", f"{op_maq}/{tot_maq} operativas")
    col3.metric("⏱️ Charla 5 Min (Hoy)", f"{kpi_charla}%", "Cumplido" if kpi_charla == 100 else "Pendiente")
    col4.metric("🦺 Checklist Operativo", f"{kpi_chk}%", "Registrado" if kpi_chk == 100 else "Pendiente")

# ==============================================================================
# VISTA 2: CALIDAD & 5S
# ==============================================================================
elif modulo == "📋 Calidad & 5S":
    c_tit, c_pdf = st.columns([3, 1])
    with c_tit:
        st.markdown(f"<h2 style='color: #1B4D2E; margin-bottom: 0;'>FOSSO - Calidad 5S ({nombre_pantalla_sede})</h2>", unsafe_allow_html=True)
        st.caption("Plan de Acción y Levantamiento")
    
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM calidad_5s WHERE operacion = ? AND sub_sede = ? ORDER BY id DESC", (op_seleccionada, sub_sede))
    registros = [dict(r) for r in cur.fetchall()]
    conn.close()

    nota_actual = seccion_notas_gerencia("CALIDAD")

    with c_pdf:
        if st.button("📕 Descargar PDF", use_container_width=True):
            ruta_pdf = os.path.join("data", f"Reporte_Calidad_{op_seleccionada}_{sub_sede}.pdf")
            pdf_gen.generar_pdf_calidad(registros, nota_actual, ruta_pdf)
            with open(ruta_pdf, "rb") as f:
                st.download_button("Guardar Documento", f, file_name=f"Reporte_Calidad_{sub_sede}.pdf", mime="application/pdf")

    st.markdown("### Registro de Observación en Campo")
    with st.form("form_calidad_movil"):
        col_it, col_est = st.columns(2)
        nuevo_item = col_it.number_input("Ítem:", min_value=1, value=len(registros) + 1, step=1)
        estado_obs = col_est.selectbox("Estado:", ["PENDIENTE", "LEVANTADA"])

        st.markdown("<b style='color: #C0392B;'>1. Hallazgo / Observación</b>", unsafe_allow_html=True)
        desc_hallazgo = st.text_area("Descripción de la observación en comedor, cocina, etc.:", label_visibility="collapsed")
        foto_antes = st.file_uploader("📁 Elegir Foto del Hallazgo (Antes)", type=["jpg", "png", "jpeg"], key="f_ant")

        st.markdown("<b style='color: #27AE60;'>2. Acción Correctiva / Levantamiento</b>", unsafe_allow_html=True)
        accion_corr = st.text_area("Acción realizada para subsanar...", label_visibility="collapsed")
        foto_desp = st.file_uploader("📁 Elegir Foto de Acción (Después)", type=["jpg", "png", "jpeg"], key="f_des")

        c_f1, c_f2 = st.columns(2)
        f_hall = c_f1.date_input("Fecha Hallazgo:", value=date.today())
        registrar_fecha_lev = c_f2.checkbox("Indicar Fecha de Levantamiento", value=(estado_obs == "LEVANTADA"))
        f_lev = c_f2.date_input("Fecha Levantamiento:", value=date.today()) if registrar_fecha_lev else None

        btn_guardar = st.form_submit_button("💾 Guardar Observación", use_container_width=True)

        if btn_guardar and desc_hallazgo:
            r_ant = db.comprimir_y_guardar_foto(foto_antes, "cal_ant")
            r_des = db.comprimir_y_guardar_foto(foto_desp, "cal_des")
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO calidad_5s (item, operacion, sub_sede, hallazgo, foto_antes, accion_correctiva, foto_despues, responsable, estado, fecha_hallazgo, fecha_levantamiento)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'FOSSO', ?, ?, ?)
            """, (nuevo_item, op_seleccionada, sub_sede, desc_hallazgo, r_ant, accion_corr, r_des, estado_obs, str(f_hall), str(f_lev) if f_lev else ""))
            conn.commit()
            conn.close()
            st.success("Observación registrada con éxito.")
            st.rerun()

    st.markdown("### Historial de Hallazgos")
    if registros:
        with st.expander("🗑️ Eliminar una Observación del Historial"):
            opciones_eliminar = {
                f"ID #{r['id']} | Ítem {r['item']} - {r['hallazgo'][:40]}... ({r['estado']})": r['id']
                for r in registros
            }
            obs_seleccionada = st.selectbox("Seleccione la observación a borrar:", list(opciones_eliminar.keys()))
            
            if st.button("Confirmar y Eliminar Registro", key="btn_eliminar_obs"):
                id_a_borrar = opciones_eliminar[obs_seleccionada]
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("SELECT foto_antes, foto_despues FROM calidad_5s WHERE id = ?", (id_a_borrar,))
                fila_foto = cur.fetchone()
                if fila_foto:
                    if fila_foto["foto_antes"] and os.path.exists(fila_foto["foto_antes"]):
                        try:
                            os.remove(fila_foto["foto_antes"])
                        except Exception:
                            pass
                    if fila_foto["foto_despues"] and os.path.exists(fila_foto["foto_despues"]):
                        try:
                            os.remove(fila_foto["foto_despues"])
                        except Exception:
                            pass

                cur.execute("DELETE FROM calidad_5s WHERE id = ?", (id_a_borrar,))
                conn.commit()
                conn.close()
                st.warning("Observación eliminada con éxito.")
                st.rerun()

    for r in registros:
        with st.container():
            st.markdown(f"**Ítem #{r['item']} | ID Base:** `{r['id']}` | **Estado:** `{r['estado']}` | **Responsable:** `FOSSO`")
            c1, c2 = st.columns(2)
            with c1:
                st.caption("Antes")
                if r["foto_antes"] and os.path.exists(r["foto_antes"]):
                    st.image(r["foto_antes"], use_container_width=True)
                st.write(r["hallazgo"])
                st.caption(f"Fecha Hallazgo: {r['fecha_hallazgo']}")
            with c2:
                st.caption("Después")
                if r["foto_despues"] and os.path.exists(r["foto_despues"]):
                    st.image(r["foto_despues"], use_container_width=True)
                st.write(r["accion_correctiva"] or "Sin acción registrada aún.")
                st.caption(f"Fecha Levantamiento: {r['fecha_levantamiento'] or 'Pendiente'}")
            st.markdown("---")

# ==============================================================================
# VISTA 3: MANTENIMIENTO
# ==============================================================================
elif modulo == "🛠️ Mantenimiento":
    st.markdown(f"<h2 style='color: #1B4D2E;'>Sistema de Gestión de Mantenimiento ({nombre_pantalla_sede})</h2>", unsafe_allow_html=True)
    
    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.markdown("#### Registro / Actualización de Equipos")
        with st.form("form_mant_eq"):
            cod_maq = st.text_input("Código de Máquina:")
            nom_eq = st.text_input("Nombre del Equipo:")
            area_op = st.text_input("Área Operativa:")
            frec_mant = st.number_input("Frecuencia Mant. (Días):", min_value=1, value=30)
            ult_mant = st.date_input("Último Mantenimiento:", value=date.today())
            est_op = st.selectbox("Estado Operativo:", ["Operativo", "En Observación", "Inoperativo"])
            anomalia = st.text_area("Anomalía Detectada:")
            foto_eq_estado = st.file_uploader("📷 Cargar Foto de Estado", type=["jpg", "png", "jpeg"])
            
            submit_eq = st.form_submit_button("💾 Guardar / Actualizar Equipo", use_container_width=True)

            if submit_eq and nom_eq:
                r_foto = db.comprimir_y_guardar_foto(foto_eq_estado, "mant_eq")
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO inventario_maquinarias (operacion, sub_sede, codigo_tag, nombre_equipo, area_operativa, frecuencia_dias, ultimo_mantenimiento, estado, anomalia, foto_estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (op_seleccionada, sub_sede, cod_maq, nom_eq, area_op, frec_mant, str(ult_mant), est_op, anomalia, r_foto))
                conn.commit()
                conn.close()
                st.success("Equipo guardado en el catálogo.")
                st.rerun()

    with col_der:
        st.markdown("#### Catálogo e Historial de Equipos")
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventario_maquinarias WHERE operacion = ? AND sub_sede = ? ORDER BY id DESC", (op_seleccionada, sub_sede))
        lista_maq = [dict(m) for m in cur.fetchall()]
        conn.close()

        nota_mant = seccion_notas_gerencia("MANTENIMIENTO")

        if st.button("📄 GENERAR REPORTE DE MANTENIMIENTO (PDF)", use_container_width=True):
            ruta_pdf_mant = os.path.join("data", f"Reporte_Mantenimiento_{op_seleccionada}_{sub_sede}.pdf")
            pdf_gen.generar_pdf_mantenimiento(lista_maq, op_seleccionada, sub_sede, nota_mant, ruta_pdf_mant)
            with open(ruta_pdf_mant, "rb") as f:
                st.download_button("Descargar Reporte de Maquinarias", f, file_name=f"Reporte_Mantenimiento_{sub_sede}.pdf", mime="application/pdf")

        if lista_maq:
            tabla_vista = []
            for m in lista_maq:
                tabla_vista.append({
                    "Código": m["codigo_tag"],
                    "Equipo": m["nombre_equipo"],
                    "Área": m["area_operativa"],
                    "Estado": m["estado"],
                    "Último Mant.": m["ultimo_mantenimiento"]
                })
            st.dataframe(tabla_vista, use_container_width=True)

            maq_elim = st.selectbox("Seleccionar para eliminar:", [f"#{m['id']} - {m['nombre_equipo']}" for m in lista_maq])
            if st.button("🗑️ Eliminar Equipo Seleccionado", use_container_width=True):
                id_elim = int(maq_elim.split(" - ")[0].replace("#", ""))
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM inventario_maquinarias WHERE id = ?", (id_elim,))
                conn.commit()
                conn.close()
                st.warning("Equipo eliminado del catálogo.")
                st.rerun()

# ==============================================================================
# VISTA 4: SSOMA & INOCUIDAD
# ==============================================================================
elif modulo == "🦺 SSOMA & Inocuidad":
    st.markdown(f"<h2 style='color: #1B4D2E;'>SSOMA, Inocuidad & Seguridad ({nombre_pantalla_sede})</h2>", unsafe_allow_html=True)
    
    tipo_gestion = st.radio("Seleccione Función SSOMA:", ["📋 Checklists Operativos (BPM / POES / Limpieza)", "⚠️ Reporte de Infraestructura y Condiciones Peligrosas"], horizontal=True)

    if tipo_gestion == "📋 Checklists Operativos (BPM / POES / Limpieza)":
        col_sel, col_pdf_chk = st.columns([3, 1])
        with col_sel:
            formato_seleccionado = st.selectbox(
                "Seleccione el Checklist Oficial:",
                [
                    "CHECK LIST DE LIMPIEZA PROFUNDA (FSS-F-AC-01)",
                    "BPM Y POES - COMEDOR PRINCIPAL (FSS-AC-F-49)",
                    "BPM Y POES - COCINA (FSS-AC-F-49)",
                    "BPM - ALMACÉN (FSS-AC-F-49)",
                    "BPM Y POES - VAJILLA (FSS-AC-F-49)"
                ]
            )
        
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ssoma_checklists WHERE operacion = ? AND sub_sede = ? ORDER BY id DESC", (op_seleccionada, sub_sede))
        historial_checklists = [dict(c) for c in cur.fetchall()]
        conn.close()

        with col_pdf_chk:
            if st.button("📄 Exportar Reporte Checklists PDF", use_container_width=True):
                ruta_pdf_chk = os.path.join("data", f"Reporte_Checklists_{op_seleccionada}_{sub_sede}.pdf")
                pdf_gen.generar_pdf_ssoma_checklists(historial_checklists, op_seleccionada, sub_sede, ruta_pdf_chk)
                with open(ruta_pdf_chk, "rb") as f:
                    st.download_button("Guardar PDF Checklists", f, file_name=f"Reporte_Checklists_{sub_sede}.pdf", mime="application/pdf")

        items_checklist = []
        if "LIMPIEZA PROFUNDA" in formato_seleccionado:
            items_checklist = [
                "1.1 Cocina: Pisos limpios, secos, paredes y pediluvios sanitizados",
                "1.2 Cocina: Hornos limpios y libres de grasa acumulada",
                "1.3 Cocina: Cocinas industriales, sartenes y ollas desengrasadas",
                "1.4 Cocina: Artefactos eléctricos sin grasa o residuos (holding, licuadoras)",
                "1.5 Cocina: Tábolas de servido limpias y desinfectadas",
                "2.1 Vajilla: Pulverizadores rotulados, operativos y en su ubicación",
                "2.2 Vajilla: Área de recepción limpia, sin restos orgánicos",
                "2.3 Vajilla: Pisos secos, paredes limpias y maniluvio operativo",
                "3.1 Almacén: Pisos secos, anaqueles limpios y rotulados",
                "3.2 Almacén: Equipos de conservación limpios y en rango térmico",
                "4.1 Comedor: Línea caliente limpia, operativa y abastecida",
                "4.2 Comedor: Mesas, sillas limpias y basureros con bolsa plástica"
            ]
        elif "COMEDOR PRINCIPAL" in formato_seleccionado:
            items_checklist = [
                "1.1 Línea caliente limpia, ordenada y abastecida de agua",
                "1.2 Cubiertos, vajilla y bandejas higienizados y secos",
                "1.3 Dispensadores de ají y aderezos limpios y operativos",
                "2.1 Mesas y sillas del comedor higienizadas",
                "2.2 Baño María limpio, operativo y conectado",
                "2.3 Mesas del comedor con dispensadores de alcohol",
                "2.4 Refresqueras y hervidores con agua/refresco suficiente",
                "2.5 Mozos con uniforme reglamentario completo y limpio",
                "3.1 Pisos de salón y ventanas limpias",
                "3.2 Basureros con bolsa plástica, limpios y vacíos",
                "4.1 Toma de muestras de referencia del turno",
                "4.2 Control de temperaturas de línea de autoservicio"
            ]
        elif "COCINA" in formato_seleccionado:
            items_checklist = [
                "1.1 Solución desinfectante preparada para tablas, bowls y utensilios",
                "2.1 Cumplimiento del procedimiento de retiro de desechos",
                "2.2 Tachos limpios, rotulados y con bolsa interior",
                "3.1 Área de tránsito y pediluvios limpios",
                "4.1 Hornos y cocinas industriales desengrasados",
                "4.2 Cambros lavados después de cada servicio",
                "4.3 Artefactos eléctricos sin residuos",
                "5.1 Productos rotulados con fecha de apertura y vencimiento",
                "5.2 Cumplimiento de regla FIFO y ausencia de latas abolladas",
                "6.1 Formatos y registros BPM al día"
            ]
        elif "ALMACÉN" in formato_seleccionado:
            items_checklist = [
                "1.1 Área de recepción limpia y ordenada",
                "1.2 Estantes limpios, pintados y sin presencia de óxido",
                "2.1 Alimentos secos libres de polvo y separados de suelo",
                "2.2 Rotulación completa de productos congelados y frescos",
                "2.3 Ausencia de productos vencidos o alterados",
                "2.4 Productos químicos rigurosamente separados de víveres",
                "2.5 Aplicación correcta del sistema FIFO",
                "3.1 Verificación y registro térmico de cámaras de conservación"
            ]
        else: # VAJILLA
            items_checklist = [
                "1.1 Pulverizadores rotulados y con químicos autorizados",
                "2.1 Pozas de lavado limpias y desincrustadas de sarro",
                "3.1 Maniluvio limpio con jabón y desinfectante",
                "4.1 Menaje en general sin grasa y en óptimo estado",
                "5.1 Ausencia de menaje roto, quiñado o con bordes desgastados",
                "5.2 Vajilla y bandejas ordenadas por tamaño y material"
            ]

        with st.form("form_checklist_bpm"):
            c_t1, c_t2 = st.columns(2)
            turno = c_t1.selectbox("Turno de Verificación:", ["Desayuno", "Almuerzo", "Cena", "Limpieza Profunda"])
            fecha_chk = c_t2.date_input("Fecha de Inspección:", value=date.today())

            st.markdown("##### Verificación de Ítems Normativos:")
            respuestas = []
            for it in items_checklist:
                val = st.checkbox(it, value=True)
                respuestas.append(val)

            obs_bpm = st.text_area("Observaciones o Desviaciones Encontradas:")
            
            if st.form_submit_button("Guardar Checklist en Plataforma"):
                conformes = sum(1 for r in respuestas if r)
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO ssoma_checklists (operacion, sub_sede, tipo_checklist, sub_area, turno, fecha, total_conformes, total_items, observaciones, registrado_por)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (op_seleccionada, sub_sede, formato_seleccionado, "General", turno, str(fecha_chk), conformes, len(items_checklist), obs_bpm, usuario["nombre"]))
                conn.commit()
                conn.close()
                st.success(f"Checklist registrado: {conformes}/{len(items_checklist)} conformes ({round(conformes/len(items_checklist)*100, 1)}%).")
                st.rerun()

    else:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ssoma_condiciones WHERE operacion = ? AND sub_sede = ? ORDER BY id DESC", (op_seleccionada, sub_sede))
        historial_condiciones = [dict(cd) for cd in cur.fetchall()]
        conn.close()

        col_tit_riesgo, col_pdf_riesgo = st.columns([3, 1])
        with col_tit_riesgo:
            st.markdown("#### Reporte de Condiciones Inseguras / Riesgos Locativos")

        with col_pdf_riesgo:
            if st.button("📄 Exportar Reporte de Riesgos PDF", use_container_width=True):
                ruta_pdf_cond = os.path.join("data", f"Reporte_Riesgos_{op_seleccionada}_{sub_sede}.pdf")
                pdf_gen.generar_pdf_condiciones_riesgo(historial_condiciones, op_seleccionada, sub_sede, ruta_pdf_cond)
                with open(ruta_pdf_cond, "rb") as f:
                    st.download_button("Guardar PDF de Riesgos", f, file_name=f"Reporte_Riesgos_{sub_sede}.pdf", mime="application/pdf")

        with st.form("form_cond_inseguras", clear_on_submit=True):
            c_u, c_c = st.columns(2)
            ubic = c_u.text_input("Ubicación exacta del riesgo (ej. Piso de cocina, cableado expuesto):")
            nivel_riesgo_sel = c_c.selectbox("Nivel de Riesgo:", ["BAJO", "MEDIO", "ALTO / INMEDIATO"])
            det_riesgo = st.text_area("Descripción de la Condición Insegura o Deterioro:")
            foto_peligro = st.file_uploader("📷 Foto de la Condición Peligrosa:", type=["jpg", "png", "jpeg"])

            btn_reg_peligro = st.form_submit_button("💾 Registrar Reporte de Peligro", use_container_width=True)

            if btn_reg_peligro and det_riesgo.strip():
                r_pel = db.comprimir_y_guardar_foto(foto_peligro, "peligro_ssoma")
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO ssoma_condiciones (operacion, sub_sede, descripcion_riesgo, nivel_criticidad, ubicacion, foto_evidencia, fecha_registro, registrado_por)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (op_seleccionada, sub_sede, det_riesgo.strip(), nivel_riesgo_sel, ubic.strip(), r_pel, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), usuario["nombre"]))
                conn.commit()
                conn.close()
                st.success("Reporte de peligro registrado exitosamente.")
                st.rerun()

        st.markdown("### Historial de Condiciones Inseguras Reportadas")
        
        if historial_condiciones:
            with st.expander("🗑️ Eliminar un Reporte de Riesgo del Historial"):
                opciones_riesgos = {
                    f"ID #{cd['id']} | {cd['fecha_registro'][:10]} - [{cd['nivel_criticidad']}] {cd['ubicacion']}": cd['id']
                    for cd in historial_condiciones
                }
                riesgo_sel = st.selectbox("Seleccione el registro a eliminar:", list(opciones_riesgos.keys()))
                
                if st.button("Confirmar y Eliminar Registro", key="btn_eliminar_riesgo"):
                    id_borrar_r = opciones_riesgos[riesgo_sel]
                    conn = db.get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT foto_evidencia FROM ssoma_condiciones WHERE id = ?", (id_borrar_r,))
                    fila_fr = cur.fetchone()
                    if fila_fr and fila_fr["foto_evidencia"] and os.path.exists(fila_fr["foto_evidencia"]):
                        try:
                            os.remove(fila_fr["foto_evidencia"])
                        except Exception:
                            pass
                    cur.execute("DELETE FROM ssoma_condiciones WHERE id = ?", (id_borrar_r,))
                    conn.commit()
                    conn.close()
                    st.warning("Reporte de riesgo eliminado correctamente.")
                    st.rerun()

            for cd in historial_condiciones:
                with st.container():
                    st.markdown(f"**Registro ID #{cd['id']}** | **Fecha:** `{cd['fecha_registro']}` | **Reportado por:** `{cd['registrado_por']}`")
                    c_col1, c_col2 = st.columns([1, 2])
                    with c_col1:
                        if cd["foto_evidencia"] and os.path.exists(cd["foto_evidencia"]):
                            st.image(cd["foto_evidencia"], use_container_width=True)
                        else:
                            st.info("Sin evidencia fotográfica")
                    with c_col2:
                        riesgo_val = cd['nivel_criticidad']
                        if "ALTO" in riesgo_val:
                            st.error(f"🚨 **Nivel de Riesgo:** {riesgo_val}")
                        elif "MEDIO" in riesgo_val:
                            st.warning(f"⚠️ **Nivel de Riesgo:** {riesgo_val}")
                        else:
                            st.success(f"✅ **Nivel de Riesgo:** {riesgo_val}")
                        
                        st.markdown(f"**Ubicación:** {cd['ubicacion']}")
                        st.markdown(f"**Descripción del Deterioro / Riesgo:**\n\n{cd['descripcion_riesgo']}")
                    st.markdown("---")
        else:
            st.info("No hay condiciones inseguras registradas actualmente para esta sede.")

    seccion_notas_gerencia("SSOMA")

# ==============================================================================
# VISTA 5: CAPACITACIONES 5 MINUTOS
# ==============================================================================
elif modulo == "⏱️ Capacitaciones 5 Min":
    col_t_ch, col_pdf_ch = st.columns([3, 1])
    with col_t_ch:
        st.markdown(f"<h2 style='color: #1B4D2E;'>Capacitaciones y Charlas Diarias ({nombre_pantalla_sede})</h2>", unsafe_allow_html=True)

    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM charlas_5min WHERE operacion = ? AND sub_sede = ? ORDER BY id DESC", (op_seleccionada, sub_sede))
    historial_charlas = [dict(ch) for ch in cur.fetchall()]
    
    hoy_str = date.today().isoformat()
    cur.execute("SELECT * FROM charlas_5min WHERE operacion = ? AND sub_sede = ? AND fecha = ? ORDER BY id DESC LIMIT 1", (op_seleccionada, sub_sede, hoy_str))
    charla_hoy = cur.fetchone()
    conn.close()

    with col_pdf_ch:
        if st.button("📄 Exportar Reporte de Charlas PDF", use_container_width=True):
            ruta_pdf_ch = os.path.join("data", f"Reporte_Charlas_{op_seleccionada}_{sub_sede}.pdf")
            pdf_gen.generar_pdf_charlas(historial_charlas, op_seleccionada, sub_sede, ruta_pdf_ch)
            with open(ruta_pdf_ch, "rb") as f:
                st.download_button("Guardar PDF Charlas", f, file_name=f"Reporte_Charlas_{sub_sede}.pdf", mime="application/pdf")

    if historial_charlas:
        with st.expander("🗑️ Eliminar una Charla del Historial"):
            opciones_charlas = {
                f"ID #{c['id']} | {c['fecha']} {c['hora']} - {c['tema'][:35]} (Inst: {c['instructor']})": c['id']
                for c in historial_charlas
            }
            charla_seleccionada = st.selectbox("Seleccione la charla a eliminar:", list(opciones_charlas.keys()))
            
            if st.button("Confirmar y Eliminar Charla", key="btn_eliminar_charla"):
                id_ch_borrar = opciones_charlas[charla_seleccionada]
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("SELECT foto_evidencia, foto_asistencia FROM charlas_5min WHERE id = ?", (id_ch_borrar,))
                fila_f = cur.fetchone()
                if fila_f:
                    if fila_f["foto_evidencia"] and os.path.exists(fila_f["foto_evidencia"]):
                        try:
                            os.remove(fila_f["foto_evidencia"])
                        except Exception:
                            pass
                    if fila_f["foto_asistencia"] and os.path.exists(fila_f["foto_asistencia"]):
                        try:
                            os.remove(fila_f["foto_asistencia"])
                        except Exception:
                            pass
                
                cur.execute("DELETE FROM charlas_5min WHERE id = ?", (id_ch_borrar,))
                conn.commit()
                conn.close()
                st.warning("Charla de 5 minutos eliminada con éxito.")
                st.rerun()

    if charla_hoy:
        st.success(f"Charla del día completada ({charla_hoy['fecha']} {charla_hoy['hora']}).")
        st.write(f"**Tema:** {charla_hoy['tema']} | **Instructor:** {charla_hoy['instructor']} | **Asistentes:** {charla_hoy['num_asistentes']}")
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.caption("Evidencia 1: Equipo Reunido en Charla")
            if charla_hoy["foto_evidencia"] and os.path.exists(charla_hoy["foto_evidencia"]):
                st.image(charla_hoy["foto_evidencia"], use_container_width=True)
        with c_f2:
            st.caption("Evidencia 2: Ficha de Firmas / Asistencia")
            if charla_hoy["foto_asistencia"] and os.path.exists(charla_hoy["foto_asistencia"]):
                st.image(charla_hoy["foto_asistencia"], use_container_width=True)
    else:
        st.warning("⚠️ Pendiente: No se ha cargado la charla ni la ficha de asistencia del día de hoy.")
        with st.form("form_charla_doble"):
            tema = st.text_input("Tema Tratado (ej. Uso de EPP, Prevención de Cortes, Ergonomía):")
            inst = st.text_input("Instructor / Responsable:", value=usuario["nombre"])
            num_asist = st.number_input("Número de Participantes:", min_value=1, value=6)
            
            c_u1, c_u2 = st.columns(2)
            f_equipo = c_u1.file_uploader("📷 Evidencia 1: Foto del Equipo Reunido", type=["jpg", "png", "jpeg"])
            f_hoja = c_u2.file_uploader("📄 Evidencia 2: Foto de Ficha de Firmas", type=["jpg", "png", "jpeg"])

            if st.form_submit_button("Registrar Charla y Asistencia") and tema and f_equipo and f_hoja:
                r1 = db.comprimir_y_guardar_foto(f_equipo, "charla_equipo")
                r2 = db.comprimir_y_guardar_foto(f_hoja, "charla_firmas")
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO charlas_5min (operacion, sub_sede, fecha, hora, tema, instructor, num_asistentes, foto_evidencia, foto_asistencia)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (op_seleccionada, sub_sede, hoy_str, datetime.now().strftime("%H:%M:%S"), tema, inst, num_asist, r1, r2))
                conn.commit()
                conn.close()
                st.success("Charla y formato de firmas guardados correctamente.")
                st.rerun()

    seccion_notas_gerencia("CHARLAS")

pie_autoria()
