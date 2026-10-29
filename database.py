import sqlite3
import os
import hashlib
from datetime import datetime
from PIL import Image

DB_PATH = os.path.join("data", "fosso_gestion.db")
FOTOS_DIR = os.path.join("data", "fotos")

os.makedirs(FOTOS_DIR, exist_ok=True)

def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def comprimir_y_guardar_foto(uploaded_file, prefijo: str) -> str:
    if uploaded_file is None:
        return ""
    try:
        img = Image.open(uploaded_file)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        max_dim = 1200
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        
        nombre_archivo = f"{prefijo}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        ruta_completa = os.path.join(FOTOS_DIR, nombre_archivo)
        img.save(ruta_completa, "JPEG", optimize=True, quality=75)
        return ruta_completa
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return ""

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Usuarios con los 3 cargos autorizados
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cargo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        es_liderazgo INTEGER NOT NULL DEFAULT 0
    )
    """)

    # 2. Notas de Gerencia
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notas_gerencia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operacion TEXT NOT NULL,
        sub_sede TEXT NOT NULL,
        modulo TEXT NOT NULL,
        texto_nota TEXT NOT NULL,
        autor TEXT NOT NULL,
        cargo TEXT NOT NULL,
        fecha_hora TEXT NOT NULL
    )
    """)

    # 3. Validación y creación de Calidad & 5S
    cur.execute("PRAGMA table_info(calidad_5s)")
    cols_existentes_5s = [col[1] for col in cur.fetchall()]
    cols_req_5s = {"item", "operacion", "sub_sede", "hallazgo", "foto_antes", "accion_correctiva", "foto_despues", "responsable", "estado", "fecha_hallazgo", "fecha_levantamiento"}
    if cols_existentes_5s and not cols_req_5s.issubset(set(cols_existentes_5s)):
        cur.execute("DROP TABLE calidad_5s")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS calidad_5s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item INTEGER NOT NULL DEFAULT 1,
        operacion TEXT NOT NULL,
        sub_sede TEXT NOT NULL,
        hallazgo TEXT NOT NULL,
        foto_antes TEXT,
        accion_correctiva TEXT,
        foto_despues TEXT,
        responsable TEXT NOT NULL DEFAULT 'FOSSO',
        estado TEXT NOT NULL DEFAULT 'PENDIENTE',
        fecha_hallazgo TEXT NOT NULL,
        fecha_levantamiento TEXT
    )
    """)

    # 4. Validación y creación de Inventario Maquinarias (Mantenimiento)
    cur.execute("PRAGMA table_info(inventario_maquinarias)")
    cols_existentes_maq = [col[1] for col in cur.fetchall()]
    cols_req_maq = {"operacion", "sub_sede", "codigo_tag", "nombre_equipo", "area_operativa", "frecuencia_dias", "ultimo_mantenimiento", "estado", "anomalia", "foto_estado"}
    if cols_existentes_maq and not cols_req_maq.issubset(set(cols_existentes_maq)):
        cur.execute("DROP TABLE inventario_maquinarias")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventario_maquinarias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operacion TEXT NOT NULL,
        sub_sede TEXT NOT NULL,
        codigo_tag TEXT NOT NULL,
        nombre_equipo TEXT NOT NULL,
        area_operativa TEXT NOT NULL,
        frecuencia_dias INTEGER DEFAULT 30,
        ultimo_mantenimiento TEXT,
        estado TEXT NOT NULL DEFAULT 'Operativo',
        anomalia TEXT,
        foto_estado TEXT
    )
    """)

    # 5. Validación y creación de SSOMA Condiciones
    cur.execute("PRAGMA table_info(ssoma_condiciones)")
    cols_existentes_ssoma = [col[1] for col in cur.fetchall()]
    cols_req_ssoma = {"operacion", "sub_sede", "descripcion_riesgo", "nivel_criticidad", "ubicacion", "foto_evidencia", "fecha_registro", "registrado_por"}
    if cols_existentes_ssoma and not cols_req_ssoma.issubset(set(cols_existentes_ssoma)):
        cur.execute("DROP TABLE ssoma_condiciones")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ssoma_condiciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operacion TEXT NOT NULL,
        sub_sede TEXT NOT NULL,
        descripcion_riesgo TEXT NOT NULL,
        nivel_criticidad TEXT NOT NULL,
        ubicacion TEXT NOT NULL,
        foto_evidencia TEXT,
        fecha_registro TEXT NOT NULL,
        registrado_por TEXT NOT NULL
    )
    """)

    # 6. Validación y creación de SSOMA Checklists
    cur.execute("PRAGMA table_info(ssoma_checklists)")
    cols_existentes_chk = [col[1] for col in cur.fetchall()]
    cols_req_chk = {"operacion", "sub_sede", "tipo_checklist", "sub_area", "turno", "fecha", "total_conformes", "total_items", "observaciones", "registrado_por"}
    if cols_existentes_chk and not cols_req_chk.issubset(set(cols_existentes_chk)):
        cur.execute("DROP TABLE ssoma_checklists")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ssoma_checklists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operacion TEXT NOT NULL,
        sub_sede TEXT NOT NULL,
        tipo_checklist TEXT NOT NULL,
        sub_area TEXT NOT NULL,
        turno TEXT NOT NULL,
        fecha TEXT NOT NULL,
        total_conformes INTEGER NOT NULL,
        total_items INTEGER NOT NULL,
        observaciones TEXT,
        registrado_por TEXT NOT NULL
    )
    """)

    # 7. Validación y creación de Charlas 5 Minutos
    cur.execute("PRAGMA table_info(charlas_5min)")
    cols_existentes_ch = [col[1] for col in cur.fetchall()]
    cols_req_ch = {"operacion", "sub_sede", "fecha", "hora", "tema", "instructor", "num_asistentes", "foto_evidencia", "foto_asistencia"}
    if cols_existentes_ch and not cols_req_ch.issubset(set(cols_existentes_ch)):
        cur.execute("DROP TABLE charlas_5min")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS charlas_5min (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operacion TEXT NOT NULL,
        sub_sede TEXT NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        tema TEXT NOT NULL,
        instructor TEXT NOT NULL,
        num_asistentes INTEGER NOT NULL,
        foto_evidencia TEXT NOT NULL,
        foto_asistencia TEXT NOT NULL
    )
    """)

    # Credenciales base para los 3 cargos
    usuarios_base = [
        ("GERENCIA", "Dirección y Gerencia Operativa", hash_pass("admin123"), 1),
        ("SUPERVISIÓN", "Supervisión de Calidad y Operaciones", hash_pass("super123"), 1),
        ("ASISTENTE", "Asistente Operativo / Administrativo", hash_pass("asist123"), 0)
    ]

    for cargo, nombre, p_hash, es_lider in usuarios_base:
        cur.execute("""
        INSERT INTO usuarios (cargo, nombre, password_hash, es_liderazgo)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(cargo) DO UPDATE SET password_hash=excluded.password_hash, es_liderazgo=excluded.es_liderazgo
        """, (cargo, nombre, p_hash, es_lider))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos y tablas de todos los módulos sincronizadas correctamente.")