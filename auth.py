import streamlit as st
import os
import base64
from database import get_connection, hash_pass

def verificar_credenciales(cargo: str, password: str):
    """Valida el cargo y la clave contra la base de datos SQLite."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cargo, nombre, password_hash, es_liderazgo FROM usuarios WHERE cargo = ?", (cargo,))
    row = cur.fetchone()
    conn.close()

    if row and row["password_hash"] == hash_pass(password):
        return {
            "cargo": row["cargo"],
            "nombre": row["nombre"],
            "es_liderazgo": bool(row["es_liderazgo"])
        }
    return None

def login_ui():
    """Renderiza el inicio de sesión centrado con el logo FOSSO ampliado."""
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        logo_path = os.path.join("assets", "logo_fosso.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                b64_logo = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 5px;">
                    <img src="data:image/png;base64,{b64_logo}" style="width: 320px; max-width: 90%; height: auto; display: block; margin: 0 auto;" />
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 25px;'>
                <p style='color: #2E7D32; font-size: 1.15em; font-weight: 600; letter-spacing: 0.5px; margin-top: 5px;'>
                    Plataforma de Gestión Operativa
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        with st.form("form_login"):
            cargo_seleccionado = st.selectbox("Seleccione su Cargo:", ["GERENCIA", "SUPERVISIÓN", "ASISTENTE"])
            password_ingresado = st.text_input("Contraseña:", type="password", placeholder="Ingrese su clave de acceso")
            submit = st.form_submit_button("Ingresar a la Plataforma", use_container_width=True)

            if submit:
                usuario = verificar_credenciales(cargo_seleccionado, password_ingresado)
                if usuario:
                    st.session_state["autenticado"] = True
                    st.session_state["usuario"] = usuario
                    st.success(f"Sesión iniciada como {usuario['cargo']}.")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas para el perfil seleccionado.")