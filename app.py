import streamlit as st
from docx import Document
from docx.shared import Inches
import pandas as pd
import io

# Configuración inicial
st.set_page_config(page_title="Endalia Fast Doc", layout="wide")

st.title("⚡ Generador Instantáneo de Documentación")

# --- COLUMNAS PRINCIPALES ---
col_in, col_pre = st.columns([1, 1])

with col_in:
    st.subheader("1. Entrada de Datos")
    
    # Subida de PBIs (Excel o CSV)
    file_pbi = st.file_uploader("Adjuntar archivo de PBIs (Excel/CSV)", type=['xlsx', 'csv'])
    
    pbi_content = ""
    if file_pbi:
        try:
            if file_pbi.name.endswith('.xlsx'):
                df = pd.read_excel(file_pbi)
                pbi_content = df.to_string() # Convertimos el Excel a texto para la IA
            else:
                df = pd.read_csv(file_pbi)
                pbi_content = df.to_string()
            st.success("✅ Archivo de PBI leído.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    # Capturas de pantalla
    capturas = st.file_uploader("Subir Capturas", type=['png', 'jpg'], accept_multiple_files=True)
    
    # Datos de formato
    seccion = st.text_input("Sección de destino", value="7.2.X Nueva Funcionalidad")
    num_img_start = st.number_input("Empezar en Imagen nº:", value=98)

    btn_generar = st.button("🪄 Generar Borrador")

# --- LÓGICA DE PREVISUALIZACIÓN ---
if "borrador" not in st.session_state:
    st.session_state.borrador = ""

if btn_generar:
    # Aquí la IA redactaría usando pbi_content. 
    # Para el ejemplo, generamos una estructura estándar de Endalia:
    st.session_state.borrador = f"""### {seccion}

**Definición:**
A partir de los requisitos del backlog, se implementa la funcionalidad para gestionar...

**Configuración:**
El administrador podrá habilitar esta opción desde el menú de políticas.

**[Image {num_img_start}]**
"""

with col_pre:
    st.subheader("2. Previsualización")
    if st.session_state.borrador:
        texto_final = st.text_area("Edita antes de exportar:", value=st.session_state.borrador, height=300)
        
        st.markdown("---")
        st.markdown("#### Vista previa:")
        st.markdown(texto_final)
        
        # BOTÓN DE DESCARGA INSTANTÁNEA
        # No va a GitHub, genera el archivo en el momento en tu RAM
        doc = Document()
        doc.add_heading(seccion, level=2)
        doc.add_paragraph(texto_final)
        
        # Añadir imágenes si existen
        if capturas:
            for i, img in enumerate(capturas):
                doc.add_paragraph(f"\n[Image {num_img_start + i}]")
                doc.add_picture(img, width=Inches(5))

        # Preparar para descarga
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="📥 Descargar Word Ahora (Instantáneo)",
            data=buffer,
            file_name=f"Update_{seccion.replace('.', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
