import streamlit as st
from docx import Document
import pandas as pd
import io
import re

st.set_page_config(page_title="Endalia Doc Tool v3", layout="wide")

# --- FUNCIONES DE SOPORTE ---
@st.cache_data
def procesar_word_maestro(file):
    doc = Document(file)
    secciones = {}
    titulo_actual = "Inicio / Portada"
    contenido = []
    patron = re.compile(r'^(\d+\.[\d\.]*)\s*(.*)')

    for para in doc.paragraphs:
        texto = para.text.strip()
        if not texto: continue
        if para.style.name.startswith('Heading') or patron.match(texto):
            secciones[titulo_actual] = "\n".join(contenido)
            titulo_actual = texto
            contenido = []
        else:
            contenido.append(texto)
    secciones[titulo_actual] = "\n".join(contenido)
    return secciones

def leer_pbi_archivo(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        return file.read().decode("utf-8")

# --- INTERFAZ ---
st.title("🚀 Sistema de Documentación Inteligente")

# 1. Carga del Word Maestro (Solo una vez)
archivo_word = st.sidebar.file_uploader("1. Sube el Word de Endalia (Base)", type=['docx'])

if archivo_word:
    dict_secciones = procesar_word_maestro(archivo_word)
    
    # 2. Navegación y Lectura
    st.sidebar.divider()
    busqueda = st.sidebar.text_input("🔍 Buscar en el índice:")
    titulos = [t for t in dict_secciones.keys() if busqueda.lower() in t.lower()]
    seleccion = st.sidebar.selectbox("Sección actual para referencia:", titulos)

    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.subheader("📖 Referencia Actual")
        st.info(f"Viendo: {seleccion}")
        st.markdown(dict_secciones[seleccion])

    with col_der:
        st.subheader("🛠️ Nueva Funcionalidad")
        
        # OPCIÓN DE ADJUNTAR PBIs
        tipo_entrada = st.radio("Método de entrada de PBI:", ["Subir Archivo (Excel/CSV/TXT)", "Copiar y Pegar"])
        
        datos_pbi = ""
        if tipo_entrada == "Subir Archivo (Excel/CSV/TXT)":
            file_pbi = st.file_uploader("Adjunta el backlog de la funcionalidad:", type=['xlsx', 'csv', 'txt'])
            if file_pbi:
                datos_pbi = leer_pbi_archivo(file_pbi)
                st.success("Archivo de PBI cargado correctamente.")
        else:
            datos_pbi = st.text_area("Pega aquí los detalles del desarrollo:")

        capturas = st.file_uploader("Adjunta las capturas (Images)", type=['png', 'jpg'], accept_multiple_files=True)
        
        if st.button("🪄 Redactar Propuesta"):
            # Aquí la IA tomaría 'dict_secciones[seleccion]' como base de estilo
            # y 'datos_pbi' como el nuevo contenido.
            st.session_state.propuesta_ia = f"### [BORRADOR] {seleccion}\n\n**Definición:** Basado en el archivo adjunto, se integra la nueva lógica de... \n\n**Configuración:** Se añade el nuevo check en la pantalla de administración..."

    # 3. Previsualización y Descarga
    if "propuesta_ia" in st.session_state:
        st.divider()
        st.subheader("👁️ Previsualización del cambio")
        texto_editable = st.text_area("Edita la redacción final:", value=st.session_state.propuesta_ia, height=250)
        
        if st.button("📥 Generar Word para Drive"):
            # Lógica de creación de .docx igual a la anterior
            st.write("Generando archivo...")
else:
    st.warning("Primero sube el Word 'Endalia - Planificación y registro horario' en el menú lateral.")
