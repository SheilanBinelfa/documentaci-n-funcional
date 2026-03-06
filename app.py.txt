import streamlit as st
from github import Github
import openai

# Configuración de la página
st.set_page_config(page_title="Editor de Documentación Endalia", layout="wide")

# --- CONFIGURACIÓN DE SECRETOS (Configura esto en el panel de Streamlit) ---
# github_token = st.secrets["GITHUB_TOKEN"]
# openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title("📝 Editor Inteligente: Documentación Funcional")

# --- BARRA LATERAL: Selección de Ubicación ---
st.sidebar.header("Ubicación en el Documento")

# Simulamos el índice de tu Word de Endalia
indice_actual = [
    "5. Políticas de registro",
    "6.1 Planificación horaria",
    "6.1.4 Generación de turnos",
    "7.2 Registro de Jornada",
    "7.2.2 Registro diario",
    "Nueva Sección..."
]

seccion_seleccionada = st.sidebar.selectbox("¿Dónde quieres añadir la funcionalidad?", indice_actual)

if seccion_seleccionada == "Nueva Sección...":
    nueva_seccion = st.sidebar.text_input("Nombre y número de la nueva sección (ej: 7.2.5 Notificaciones)")

# --- CUERPO PRINCIPAL: Entrada de Datos ---
st.subheader("Entrada de Product Backlog Items (PBI)")
pbi_input = st.text_area("Pega aquí los items del backlog o criterios de aceptación:", height=200, 
                         placeholder="Ejemplo: El sistema debe permitir fichajes nocturnos que crucen la medianoche...")

if st.button("Generar Borrador para el Documento"):
    if pbi_input:
        with st.spinner("Redactando con el estilo de Endalia..."):
            # AQUÍ LLAMAMOS A LA IA
            # El prompt le indica que use tu estilo específico: negritas, estructura técnica, etc.
            prompt = f"""
            Actúa como un redactor técnico de software de RRHH. 
            Toma estos items de backlog: "{pbi_input}"
            Y redáctalos para incluirlos en la sección "{seccion_seleccionada}" del manual funcional.
            
            REGLAS DE ESTILO:
            1. Usa un tono formal y profesional.
            2. Usa negritas para elementos de la interfaz (botones, menús).
            3. Estructura el contenido con subapartados: 'Definición' y 'Configuración' si aplica.
            4. Inspírate en el formato de Endalia: claro, directo y con foco en el usuario.
            """
            
            # (Simulación de respuesta de IA - Aquí iría la llamada real a openai.ChatCompletion)
            borrador = f"### {seccion_seleccionada}\n\n**Definición:** Esta funcionalidad permite... [Texto generado basado en el PBI]\n\n**Configuración:** Para activar esta opción, el administrador deberá..."
            
            st.session_state['borrador'] = borrador
            st.success("¡Borrador generado!")

# --- EDICIÓN Y ENVÍO ---
if 'borrador' in st.session_state:
    st.subheader("Revisar y Editar Borrador")
    texto_final = st.text_area("Puedes modificar el texto antes de subirlo a GitHub:", 
                               value=st.session_state['borrador'], height=300)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Publicar en GitHub"):
            # Lógica para subir a GitHub usando PyGithub
            st.info("Conectando con GitHub para realizar el commit...")
            # repo.update_file(path, "Update doc", texto_final, contents.sha)
            st.success("¡Documentación actualizada en el repositorio!")
            
    with col2:
        if st.button("📥 Generar Word/PDF"):
            st.info("Generando archivo con Pandoc y tu plantilla...")
            # Aquí dispararías la descarga del archivo actualizado