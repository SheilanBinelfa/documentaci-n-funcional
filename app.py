import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# Configuración de estilo Endalia para la previsualización
st.set_page_config(page_title="Endalia Doc Tool", layout="wide")

st.title("🖋️ Editor y Previsualizador de Documentación")

# --- PANEL LATERAL: Configuración ---
st.sidebar.header("Configuración del Documento")
num_imagen = st.sidebar.number_input("Número de la primera imagen:", value=98)
seccion = st.sidebar.text_input("Sección/Título:", "7.2.6 Nueva Funcionalidad")

# --- CUERPO: Entrada de datos ---
col_in, col_pre = st.columns([1, 1])

with col_in:
    st.subheader("1. Datos de Entrada")
    pbi_input = st.text_area("Pega aquí los PBI del Backlog:", height=150)
    capturas = st.file_uploader("Sube las capturas de pantalla", type=['png', 'jpg'], accept_multiple_files=True)
    
    # Botón para que la IA trabaje
    generar_borrador = st.button("🪄 Generar Propuesta con IA")

# --- LÓGICA DE GENERACIÓN ---
if "borrador_texto" not in st.session_state:
    st.session_state.borrador_texto = ""

if generar_borrador:
    # Aquí iría la llamada a la API de OpenAI/Claude con tu estilo de Endalia
    # Simulamos la redacción profesional:
    texto_ia = f"""### {seccion}
**Definición:** A partir de los requisitos analizados, se implementa la capacidad de gestionar de forma automática los registros asociados a...

**Configuración:** Para la correcta visualización, se ha habilitado un nuevo check en el panel de administración, tal como se muestra en la **[Image {num_imagen}]**.
"""
    st.session_state.borrador_texto = texto_ia

# --- COLUMNA DE PREVISUALIZACIÓN ---
with col_pre:
    st.subheader("2. Previsualización del Documento")
    if st.session_state.borrador_texto:
        # Editamos en vivo
        contenido_final = st.text_area("Edita el borrador antes de exportar:", 
                                        value=st.session_state.borrador_texto, height=300)
        
        st.markdown("---")
        st.markdown("#### Vista previa de cómo quedaría:")
        # Renderizamos el contenido como se vería (Markdown simula bien el flujo de Word)
        st.markdown(contenido_final)
        
        if capturas:
            st.image(capturas[0], caption=f"Vista previa de [Image {num_imagen}]", width=400)
    else:
        st.info("Escribe los PBI y pulsa 'Generar' para ver la previsualización aquí.")

# --- EXPORTACIÓN ---
if st.session_state.borrador_texto:
    st.divider()
    if st.button("✅ Todo correcto, descargar Word"):
        doc = Document()
        # Aquí puedes añadir lógica para aplicar negritas y estilos de Endalia
        doc.add_heading(seccion, level=2)
        doc.add_paragraph(contenido_final.replace("### " + seccion, ""))
        
        current_img = num_imagen
        for img in capturas:
            doc.add_paragraph(f"\n[Image {current_img}]")
            doc.add_picture(img, width=Inches(5))
            current_img += 1
            
        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="📥 Descargar ahora",
            data=bio.getvalue(),
            file_name=f"Update_{seccion}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
