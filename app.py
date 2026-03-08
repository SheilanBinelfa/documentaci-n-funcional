import streamlit as st
from docx import Document
import re
import io

st.set_page_config(page_title="Endalia Doc Explorer", layout="wide")

@st.cache_data
def leer_todo_el_word(file):
    doc = Document(file)
    secciones = {}
    titulo_actual = "Inicio / Portada"
    contenido_acumulado = []

    # Expresión regular para detectar títulos numerados (ej: 7.2.2 o 4.1)
    patron_titulo = re.compile(r'^(\d+\.[\d\.]*)\s*(.*)')

    for para in doc.paragraphs:
        texto = para.text.strip()
        if not texto: continue

        # Si el párrafo es un título por estilo O por numeración
        es_titulo = para.style.name.startswith('Heading') or patron_titulo.match(texto)
        
        if es_titulo:
            # Guardamos lo anterior antes de empezar sección nueva
            secciones[titulo_actual] = "\n".join(contenido_acumulado)
            titulo_actual = texto
            contenido_acumulado = []
        else:
            contenido_acumulado.append(texto)
            
    # Guardar la última sección
    secciones[titulo_actual] = "\n".join(contenido_acumulado)
    return secciones

st.title("📂 Explorador Completo de Documentación")

archivo = st.sidebar.file_uploader("Carga el Word de Endalia", type=['docx'])

if archivo:
    dict_docs = leer_todo_el_word(archivo)
    
    # Buscador de secciones para no perderte en el "kilométrico"
    busqueda = st.sidebar.text_input("🔍 Buscar sección (ej: 7.2):")
    titulos_filtrados = [t for t in dict_docs.keys() if busqueda.lower() in t.lower()]

    seleccion = st.sidebar.selectbox("Selecciona la sección a consultar:", titulos_filtrados)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📖 Contenido Original")
        if seleccion:
            st.markdown(f"### {seleccion}")
            st.write(dict_docs[seleccion])
        
    with col2:
        st.subheader("✍️ Añadir Nueva Funcionalidad")
        st.info("Escribe aquí lo nuevo. La IA usará el texto de la izquierda como referencia.")
        pbi = st.text_area("PBI / Notas del desarrollo:")
        
        if st.button("Generar propuesta"):
            # Aquí iría el prompt con el texto de la izquierda + tus notas
            st.success("Propuesta generada respetando el estilo de la sección actual.")

else:
    st.info("Sube el archivo 'Endalia - Planificación y registro horario...' para activar el visor.")
