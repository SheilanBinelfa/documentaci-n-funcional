import streamlit as st
from docx import Document
from docx.shared import Inches
import io

st.set_page_config(page_title="Endalia Doc Intelligence", layout="wide")

# Función para extraer secciones del Word original
@st.cache_data
def extraer_secciones(file):
    doc = Document(file)
    secciones = {}
    current_section = None
    content = []
    
    for para in doc.paragraphs:
        # Detectamos si es un título (basado en estilo o numeración)
        if para.style.name.startswith('Heading') or (para.text and para.text[0].isdigit()):
            if current_section:
                secciones[current_section] = "\n".join(content)
            current_section = para.text
            content = []
        else:
            content.append(para.text)
    return secciones

st.title("📂 Consultor y Editor de Documentación")

# --- PASO 1: CARGAR EL DOCUMENTO MAESTRO ---
st.sidebar.header("1. Documento Base")
archivo_maestro = st.sidebar.file_uploader("Sube el Word actual (25Q4)", type=['docx'])

if archivo_maestro:
    dict_secciones = extraer_secciones(archivo_maestro)
    lista_titulos = list(dict_secciones.keys())
    
    # --- PASO 2: SELECCIÓN Y LECTURA ---
    st.sidebar.header("2. Navegación")
    opcion = st.sidebar.selectbox("Selecciona una funcionalidad para leer:", ["-- Seleccionar --"] + lista_titulos)
    
    col_lectura, col_edicion = st.columns(2)
    
    with col_lectura:
        st.subheader("📖 Contenido Actual")
        if opcion != "-- Seleccionar --":
            texto_actual = dict_secciones[opcion]
            st.info(f"Visualizando: {opcion}")
            st.markdown(texto_actual if texto_actual.strip() else "_Esta sección solo contiene imágenes o tablas en el original._")
        else:
            st.write("Selecciona una sección en el menú lateral para leer su contenido actual.")

    # --- PASO 3: AÑADIR NUEVA FUNCIONALIDAD ---
    with col_edicion:
        st.subheader("✍️ Añadir / Modificar")
        pbi_input = st.text_area("Pega los PBI para la nueva funcionalidad:", height=150)
        capturas = st.file_uploader("Adjuntar capturas", type=['png', 'jpg'], accept_multiple_files=True)
        
        if st.button("🪄 Generar Propuesta"):
            # Aquí la IA usaría el 'texto_actual' como contexto para no repetirse
            # y redactar con el mismo estilo.
            st.session_state.propuesta = f"""### {opcion} (Actualizado)
{texto_actual[:200]}... 

**Nueva Mejora:** Basado en los requisitos, se añade la capacidad de... [Redacción de la IA]
"""
            st.success("Propuesta generada combinando lo actual con lo nuevo.")

    # --- PREVISUALIZACIÓN FINAL Y EXPORTAR ---
    if "propuesta" in st.session_state:
        st.divider()
        st.subheader("👁️ Previsualización del nuevo fragmento")
        texto_final = st.text_area("Edita el resultado final:", value=st.session_state.propuesta, height=250)
        
        if st.button("📥 Descargar Word Actualizado"):
            # Lógica de descarga igual a la anterior...
            pass
else:
    st.warning("Por favor, sube el documento Word original en la barra lateral para empezar.")
