# app.py
import streamlit as st
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping

from experta import *
from reglas import SistemaEducativo, EXPLICACION
from hechos import Perfil, UU, VV
from engine_utils import preparar_engine
from resumen import generar_resumen_significados
from recomendaciones import generar_recomendaciones_conversacionales
from troncales import cargar_materias_troncales
from horarios import filtrar_materias_segun_hechos
from significados import SIGNIFICADOS
from datetime import datetime
import base64
from io import BytesIO
import re
import base64

def load_image_base64(path):
    """Carga una imagen local y la convierte a base64 para usarla en HTML."""
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
logo_base64 = base64.b64encode(open("logo.png", "rb").read()).decode()

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# ========== CONFIGURACIÓN DE LA PÁGINA ==========
st.set_page_config(
    page_title="Sistema Experto UNJu",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== ESTILOS CSS PERSONALIZADOS ==========
st.markdown("""
<style>
    /* Fondo con imagen y overlay */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), 
                          url('https://img.freepik.com/foto-gratis/antecedentes-tecnologicos-gradiente_23-2151895872.jpg?semt=ais_hybrid&w=740&q=80');/*imagen de todo el fondo*/
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Tarjetas con efecto glassmorphism mejorado */
    .card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Títulos con efecto neón */
    .neon-title {
        color: #fff;
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 0 0 10px #fff, 0 0 20px #4CAF50, 0 0 30px #4CAF50;
        margin-bottom: 30px;
    }
    
    /* Subtítulos */
    .subtitle {
        color: #fff;
        text-align: center;
        font-size: 1.5em;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Botones personalizados */
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border-radius: 25px;
        padding: 12px 35px;
        border: none;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(76, 175, 80, 0.6);
    }
    
    /* Radio buttons personalizados */
    .stRadio > label {
        color: white !important;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
    }
    
    /* Inputs personalizados */
    .stTextInput > label {
        color: white !important;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] {
    background-image: url("https://img.freepik.com/vector-gratis/vector-tecnologia-red-futurista-azul_53876-151537.jpg");/*imagen de menu*/
    background-size: cover;
    background-position: center;
}

    
    [data-testid="stSidebar"] .element-container {
        color: white !important;
    }
    
    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    }
    
    /* Alertas personalizadas */
    .success-box {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: white;
    }
    
    .info-box {
        background: rgba(33, 150, 243, 0.2);
        border-left: 4px solid #2196F3;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: white;
    }
    
    /* Expander personalizado */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white !important;
        font-weight: bold;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    }
    
    /* Markdown text in white */
    .stMarkdown {
        color: white;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Botones del sidebar sin caja rara */
    [data-testid="stSidebar"] button {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px !important;
        font-weight: bold !important;
        backdrop-filter: blur(10px);
    }

    [data-testid="stSidebar"] button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: scale(1.02);
        transition: 0.2s;
    }
    /* ===== ESTILO SIDEBAR TIPO YOUTUBE ===== */

    /* Contenedor del menú lateral */
    [data-testid="stSidebar"] .element-container {
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }

    /* Texto del menú: estilo YouTube */
    [data-testid="stSidebar"] button {
        background: transparent !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        text-align: left !important;
        padding: 10px 14px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    /* Ícono + texto alineados como en YouTube */
    [data-testid="stSidebar"] button div {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }

    /* Efecto hover tipo YouTube */
    [data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.15) !important;
    }

    /* Estado seleccionado del menú */
    [data-testid="stSidebar"] button:focus,
    [data-testid="stSidebar"] button:active {
        background: rgba(255,255,255,0.25) !important;
    }

    /* Separador suave tipo YouTube */
    .sidebar-separator {
        height: 1px;
        background: rgba(255,255,255,0.2);
        margin: 8px 0;
    }

</style>
""", unsafe_allow_html=True)

# ========== FUNCIONES AUXILIARES ==========
def obtener_saludo():
    h = datetime.now().hour
    if 6 <= h < 12:
        return "¡Buen día! ☀️"
    elif 12 <= h < 18:
        return "¡Buenas tardes! 🌤️"
    elif 18 <= h < 24:
        return "¡Buenas noches! 🌙"
    else:
        return "Wow, estás conectado a la madrugada 😴"

def inicializar_session_state():
    """Inicializa las variables de sesión"""
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "generar_recomendaciones"
    if 'nombre' not in st.session_state:
        st.session_state.nombre = ""
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    if 'resultados' not in st.session_state:
        st.session_state.resultados = None
    if 'formulario_completado' not in st.session_state:
        st.session_state.formulario_completado = False

def generar_pdf(nombre, resumen, hechos_usuario):
    """Genera un PDF con los resultados"""
    if not REPORTLAB_AVAILABLE:
        return None
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#4CAF50',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#2196F3',
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # Título
    story.append(Paragraph(f"Recomendaciones Académicas para {nombre}", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Fecha
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<i>Generado el: {fecha}</i>", normal_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Hechos Finales
    
    story.append(Paragraph("Perfil del Estudiante", heading_style))
    perfil = hechos_usuario  # esto ya lo generás antes

    # Mapa para imprimir bonito
    mapa_perfil = {
        "trabaja": "Situación laboral",
        "turno_trabajo": "Turno de trabajo",
        "cursa_todas": "Cursa todas las materias",
        "retoma_estudios": "Retoma estudios",
        "doble_carrera": "Estudia doble carrera",
        "dif_teorica": "Dificultad teórica",
        "dif_practica": "Dificultad práctica"
    }

    for clave, etiqueta in mapa_perfil.items():
        if clave in perfil:
            valor = perfil[clave]
            if isinstance(valor, bool):
                valor = "Sí" if valor else "No"
            story.append(Paragraph(f"• <b>{etiqueta}:</b> {valor}", normal_style))

    
    # Recomendaciones
    story.append(Paragraph("Recomendaciones Personalizadas", heading_style))
    recs = generar_recomendaciones_conversacionales(resumen['finales_ids'], hechos_usuario)
    # Filtrar el mensaje introductorio
    recs_filtradas = [rec for rec in recs[1:] if rec and len(rec.strip()) > 20]
    for i, rec in enumerate(recs_filtradas, 1):
        story.append(Paragraph(f"<b>{i}.</b> {rec}", normal_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Materias Troncales
    from reportlab.platypus import LongTable as Table, TableStyle

    from reportlab.lib import colors

    if resumen['troncales']:
        #story.append(PageBreak())
        story.append(Paragraph("Materias Troncales", heading_style))

        data = [[Paragraph(m, normal_style)] for m in resumen['troncales']]

        table = Table(data, colWidths=[450])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))

        story.append(table)

    
    # Horarios
    from reportlab.platypus import KeepTogether, Table, TableStyle
    from reportlab.lib import colors
    if resumen.get('materias_filtradas'):
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("Horarios Disponibles", heading_style))
        story.append(Spacer(1, 0.15*inch))

        for materia_info in resumen['materias_filtradas']:
            # Crear el título localmente (no lo agregues en otro lugar)
            titulo = Paragraph(f"<b>{materia_info['materia']}</b>", normal_style)

            # Crear tabla de horarios
            data = []
            for h in materia_info['horarios']:
                tipo = "Virtual" if h.get('virtual') else "Presencial"
                row = [
                    h.get('dia', ''),
                    f"{h.get('inicio','')} - {h.get('fin','')}",
                    tipo,
                    h.get('tipo_clase', '')
                ]
                data.append(row)

            # Si no hay filas, igual mostrar encabezado vacío (opcional)
            table = Table(
                [["Día", "Horario", "Modalidad", "Tipo"]] + data,
                colWidths=[80, 120, 100, 120]
            )
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('TEXTCOLOR',(0,0),(-1,0), colors.black),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('BOX',(0,0),(-1,-1),1,colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                ('PADDING',(0,0),(-1,-1),6),
            ]))

            # Agrupar Título + Tabla juntos para que no se separen entre páginas
            bloque_materia = [titulo, Spacer(1, 0.05*inch), table, Spacer(1, 0.2*inch)]
            story.append(KeepTogether(bloque_materia))
            
    # --- ESTAS TRES LÍNEAS SON OBLIGATORIAS ---
    doc.build(story)
    buffer.seek(0)
    return buffer


# ========== PANTALLA DE BIENVENIDA Y CUESTIONARIO ==========
def pagina_generar_recomendaciones():
    #st.markdown('<h1 class="neon-title">🎓 Sistema Experto UNJu</h1>', unsafe_allow_html=True)
    st.markdown(
    f"""
    <div style="display:flex; justify-content:center; align-items:center; gap:20px; width:100%;">
        <h1 class="neon-title" style="margin:0;">🎓 Sistema Experto UNJu</h1>
        <img src="data:image/png;base64,{logo_base64}" style="height:80px;">
    </div>
    """,
    unsafe_allow_html=True
)



    st.markdown(f'<p class="subtitle">{obtener_saludo()}</p>', unsafe_allow_html=True)
    
    if not st.session_state.formulario_completado:
        # Usar casi todo el ancho de la pantalla
        col1, col2, col3 = st.columns([0.5, 10, 0.5])
        with col2:
            st.markdown("""
            <div class="card">
                <h2 style="color: white; text-align: center;">Bienvenido/a 👋</h2>
                <p style="color: white; text-align: center; font-size: 1.1em;">
                    Soy tu asistente de la <b>Facultad de Ingeniería (UNJu)</b>
                </p>
                <p style="color: white; text-align: center;">
                    Completa el siguiente cuestionario para recibir recomendaciones 
                    personalizadas sobre tu cursada universitaria.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        
            
            # Formulario único
            
            st.markdown("### 📝 Información Personal")
            nombre = st.text_input("✍️ ¿Cómo te llamas?", placeholder="Ingresa tu nombre aquí...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💼 Situación Laboral")
            trabaja = st.radio(
                "¿Trabajás actualmente?",
                ["Sí", "No"],
                key="trabaja_radio",
                index=None  # Sin opción marcada por defecto
            )
            
            # Mostrar pregunta del turno SOLO si trabaja es "Sí"
            turno = None
            if trabaja == "Sí":
                turno = st.radio(
                    "¿En qué turno trabajás?",
                    ["🌅 Mañana", "☀️ Tarde", "🌙 Noche"],
                    key="turno_radio",
                    index=None  # Sin opción marcada por defecto
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📚 Situación Académica")
            
            cursa_todas = st.radio(
                "¿Vas a cursar todas las materias del año?",
                ["Sí", "No"],
                key="cursa_radio",
                index=None  # Sin opción marcada por defecto
            )
            
            retoma = st.radio(
                "¿Estás retomando los estudios después de un tiempo?",
                ["Sí", "No"],
                key="retoma_radio",
                index=None  # Sin opción marcada por defecto
            )
            
            doble = st.radio(
                "¿Estás estudiando dos carreras a la vez?",
                ["Sí", "No"],
                key="doble_radio",
                index=None  # Sin opción marcada por defecto
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📖 Dificultades Académicas")
            
            dif_teorica = st.radio(
                "¿Tenés dificultad en la parte teórica?",
                ["Sí", "No"],
                key="dif_teorica_radio",
                index=None  # Sin opción marcada por defecto
            )
            
            dif_practica = st.radio(
                "¿Tenés dificultad en la parte práctica?",
                ["Sí", "No"],
                key="dif_practica_radio",
                index=None  # Sin opción marcada por defecto
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
                
            # ===========================
            # BOTÓN FINAL
            # ===========================
            if st.button("✨ Generar Recomendaciones", use_container_width=True):

                # 🔍 Validaciones
                if not nombre or not nombre.strip():
                    st.error("⚠️ Por favor, ingresa tu nombre para continuar")
                elif trabaja is None:
                    st.error("⚠️ Por favor, indica si trabajas actualmente")
                elif trabaja == "Sí" and turno is None:
                    st.error("⚠️ Por favor, selecciona tu turno de trabajo")
                elif cursa_todas is None:
                    st.error("⚠️ Por favor, indica si vas a cursar todas las materias")
                elif retoma is None:
                    st.error("⚠️ Por favor, indica si estás retomando los estudios")
                elif doble is None:
                    st.error("⚠️ Por favor, indica si estás estudiando dos carreras")
                elif dif_teorica is None:
                    st.error("⚠️ Por favor, indica si tenés dificultad en la parte teórica")
                elif dif_practica is None:
                    st.error("⚠️ Por favor, indica si tenés dificultad en la parte práctica")
                else:
                    # Guardar respuestas en session_state
                    st.session_state.nombre = nombre.strip()
                    st.session_state.respuestas = {}

                    # Situación laboral
                    st.session_state.respuestas['trabaja'] = (trabaja == "Sí")

                    if trabaja == "Sí":
                        turno_map = {
                            "🌅 Mañana": "AC",
                            "☀️ Tarde": "AD",
                            "🌙 Noche": "AE"
                        }
                        st.session_state.respuestas['turno_trabajo'] = turno_map[turno]

                    # Situación académica
                    st.session_state.respuestas['cursa_todas'] = (cursa_todas == "Sí")
                    st.session_state.respuestas['retoma_estudios'] = (retoma == "Sí")
                    st.session_state.respuestas['doble_carrera'] = (doble == "Sí")

                    # Dificultades académicas
                    st.session_state.respuestas['dif_teorica'] = (dif_teorica == "Sí")
                    st.session_state.respuestas['dif_practica'] = (dif_practica == "Sí")

                    # Procesar resultados
                    with st.spinner("🔄 Procesando tu perfil..."):
                        procesar_resultados()

                    st.session_state.formulario_completado = True
                    st.rerun()
    
    else:
        # Mostrar resultados
        mostrar_resultados()

def procesar_resultados():
    """Procesa las respuestas y genera recomendaciones"""
    # Primero ejecutar el motor con las respuestas básicas
    engine, hechos_usuario = preparar_engine(
        st.session_state.respuestas,
        SistemaEducativo,
        Perfil
    )
    
    # Agregar las dificultades académicas si corresponde
    if st.session_state.respuestas.get('dif_teorica', False):
        engine.declare(UU())
    
    if st.session_state.respuestas.get('dif_practica', False):
        engine.declare(VV())
    
    # Ejecutar inferencia secundaria
    engine.run()
    
    # Generar resumen
    resumen = generar_resumen_significados(engine, "reglas.py")
    
    st.session_state.resultados = {
        'engine': engine,
        'hechos_usuario': hechos_usuario,
        'resumen': resumen
    }

def mostrar_resultados():
    """Muestra los resultados de las recomendaciones"""
    st.markdown(f'<h1 class="neon-title">Resultados para {st.session_state.nombre} 🎉</h1>', unsafe_allow_html=True)
    
    resultados = st.session_state.resultados
    resumen = resultados['resumen']
    
    # Botón para exportar PDF
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if REPORTLAB_AVAILABLE:
            pdf_buffer = generar_pdf(st.session_state.nombre, resumen, resultados['hechos_usuario'])
            if pdf_buffer:
                st.download_button(
                    label="📄 Descargar Recomendaciones en PDF",
                    data=pdf_buffer,
                    file_name=f"recomendaciones_{st.session_state.nombre.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("📦 Instala reportlab para habilitar la exportación a PDF: pip install reportlab")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
   # ===============================
    # 📌 TABS CON CONTROL DE TRONCALES
    # ===============================

    # Lista base de tabs (reco, horarios, trazabilidad)
    tab_labels = ["💡 Recomendaciones"]

    # Agregamos la pestaña de troncales SOLO si existe información
    mostrar_troncales = bool(resumen.get("troncales"))
    if mostrar_troncales:
        tab_labels.append("📖 Materias Troncales")

    # Agregamos el resto (estos siempre van)
    tab_labels += ["🕐 Horarios Disponibles", "🔍 Trazabilidad"]

    # Crear tabs finales
    tabs = st.tabs(tab_labels)

    # Asignar cada tab a variables
    idx = 0
    tab1 = tabs[idx]; idx += 1

    if mostrar_troncales:
        tab2 = tabs[idx]; idx += 1
    else:
        tab2 = None  # No existe la pestaña

    tab3 = tabs[idx]; idx += 1
    tab4 = tabs[idx]

    
    with tab1:
        st.markdown("### 💡 Recomendaciones")
        recs = generar_recomendaciones_conversacionales(
            resumen['finales_ids'],
            resultados['hechos_usuario']
        )
        
        # Filtrar la primera "recomendación" si es solo un mensaje introductorio
        recs_filtradas = [rec for rec in recs[1:] if rec and len(rec.strip()) > 20]
        
        # Invertir el orden de las recomendaciones (última primero)
        recs_filtradas = list(reversed(recs_filtradas))
        
        for i, rec in enumerate(recs_filtradas, 1):
            with st.expander(f"📌 Recomendación {i}", expanded=(i == 1)):
                st.markdown(f"<div class='card' style='color: white;'>{rec}</div>", unsafe_allow_html=True)
    
    # Mostrar tab2 SOLO si existe
    if tab2 is not None:
        with tab2:
            st.markdown("### 📖 Materias Troncales y Sus Correlativas")
            for mat in resumen['troncales']:
                st.markdown(f"<div class='info-box'>{mat}</div>", unsafe_allow_html=True)

    
    with tab3:
        if resumen['materias_filtradas']:
            st.markdown("### 🕐 Horarios Disponibles Según Tu Perfil")
            for materia_info in resumen['materias_filtradas']:
                with st.expander(f"📚 {materia_info['materia']}", expanded=False):
                    for horario in materia_info['horarios']:
                        tipo = "🌐 Virtual" if horario['virtual'] else "🏫 Presencial"
                        st.markdown(f"""
                        <div class='info-box' style='color: white; margin-bottom: 10px;'>
                            <strong>📅 {horario['dia']}</strong><br>
                            🕐 <strong>Horario:</strong> {horario['inicio']} - {horario['fin']}<br>
                            📍 <strong>Modalidad:</strong> {tipo}<br>
                            📖 <strong>Tipo:</strong> {horario['tipo_clase']}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No hay horarios específicos para mostrar según tu perfil")
    
    with tab4:
        st.markdown("### 🔍 Trazabilidad del Razonamiento")
        if EXPLICACION:
            for i, paso in enumerate(EXPLICACION, 1):
                with st.expander(f"🔸 Paso {i}: {paso.get('regla', 'sin_nombre')}", expanded=False):
                    antecedentes = paso.get('antecedentes', [])
                    consecuentes = paso.get('consecuentes', [])
                    
                    st.markdown("**Condiciones que se cumplieron:**")
                    if antecedentes:
                        for ant in antecedentes:
                            # Extraer código limpio
                            codigo = ant.split('=')[0] if '=' in ant else ant
                            if "(" in codigo:
                                match = re.search(r'\((.*?)\)', codigo)
                                if match:
                                    codigo = match.group(1).split("=")[0]
                            codigo = codigo.strip()
                            significado = SIGNIFICADOS.get(codigo, ant)
                            st.markdown(f"• {significado}")
                    
                    st.markdown("**Conclusiones inferidas:**")
                    if consecuentes:
                        for cons in consecuentes:
                            significado = SIGNIFICADOS.get(cons, cons)
                            st.markdown(f"✓ {significado}")
        else:
            st.info("No hay trazabilidad registrada")
    
    # Botón para nueva consulta
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Realizar Nueva Consulta", use_container_width=True):
            st.session_state.formulario_completado = False
            st.session_state.respuestas = {}
            st.session_state.resultados = None
            st.session_state.nombre = ""
            # Limpiar EXPLICACION para nueva consulta
            EXPLICACION.clear()
            st.rerun()

# ========== PÁGINA DEL PLAN DE ESTUDIOS ==========
def pagina_plan_estudios():
    st.markdown("""
        <h1 style="text-align:left; width:100%; margin-bottom:20px;">
            📋 Plan de Estudios
        </h1>
    """, unsafe_allow_html=True)

    # Card descriptiva
    st.markdown("""
        <div class="card" style="width:100%;">
            <h2 style="color:white; text-align:left;">Plan de Estudios - Ingeniería en Informática</h2>
            <p style="color:white; text-align:left;">
                Aquí puedes consultar el plan de estudios completo de la carrera.
            </p>
        </div>
        <br>
    """, unsafe_allow_html=True)

    # === ID del archivo en Google Drive ===
    file_id = "1ZZwkgc8-kSPG33Q87GO-wxpbXtzFMduz"

    # === URL para visualizar ===
    pdf_preview_url = f"https://drive.google.com/file/d/{file_id}/preview"

    # === URL para descargar ===
    pdf_download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Mostrar PDF a ancho completo
    st.markdown(f"""
        <iframe src="{pdf_preview_url}"
                width="100%"
                height="900px"
                style="border:none;">
        </iframe>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Botón para descargar exactamente el PDF mostrado
    st.markdown(f"""
        <a href="{pdf_download_url}" target="_blank" download>
            <button style="
                background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
                color: white;
                border-radius: 25px;
                padding: 12px 35px;
                border: none;
                font-weight: bold;
                font-size: 1.1em;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            ">
                📥 Descargar PDF
            </button>
        </a>
    """, unsafe_allow_html=True)

# ========== PÁGINA DEL PLAN DE ESTUDIOS ==========
def pagina_Horario():
    st.markdown("""
        <h1 style="text-align:left; width:100%; margin-bottom:20px;">
            📋 Horario
        </h1>
    """, unsafe_allow_html=True)

    # Card descriptiva
    st.markdown("""
        <div class="card" style="width:100%;">
            <h2 style="color:white; text-align:left;">Plan de Estudios - Ingeniería en Informática</h2>
            <p style="color:white; text-align:left;">
                Aquí puedes consultar el plan de estudios completo de la carrera.
            </p>
        </div>
        <br>
    """, unsafe_allow_html=True)

    # === ID del archivo en Google Drive ===
    file_id = "1ZZwkgc8-kSPG33Q87GO-wxpbXtzFMduz"

    # === URL para visualizar ===
    pdf_preview_url = f"https://drive.google.com/file/d/{file_id}/preview"

    # === URL para descargar ===
    pdf_download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Mostrar PDF a ancho completo
    st.markdown(f"""
        <iframe src="{pdf_preview_url}"
                width="100%"
                height="900px"
                style="border:none;">
        </iframe>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Botón para descargar exactamente el PDF mostrado
    st.markdown(f"""
        <a href="{pdf_download_url}" target="_blank" download>
            <button style="
                background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
                color: white;
                border-radius: 25px;
                padding: 12px 35px;
                border: none;
                font-weight: bold;
                font-size: 1.1em;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            ">
                📥 Descargar PDF
            </button>
        </a>
    """, unsafe_allow_html=True)
    
    
# ========== SIDEBAR ==========
def mostrar_sidebar():
    with st.sidebar:
        st.markdown("### Menú Principal")

        if st.button("Generar Recomendaciones", use_container_width=True):
            st.session_state.pagina = "generar_recomendaciones"

        if st.button("Plan de Estudios", use_container_width=True):
            st.session_state.pagina = "plan_estudios"

        if st.button("Horarios", use_container_width=True):
            st.session_state.pagina = "Horario"
        st.button("Estadísticas", use_container_width=True)
        
        st.markdown("---")
        
        # Información del sistema
        st.info("Sistema experto de recomendación académica para la Facultad de Ingeniería (UNJu).")


# ========== MAIN ==========
def main():
    inicializar_session_state()
    mostrar_sidebar()
    
    # Navegación entre páginas
    if st.session_state.pagina == "generar_recomendaciones":
        pagina_generar_recomendaciones()
    elif st.session_state.pagina == "plan_estudios":
        pagina_plan_estudios()

if __name__ == "__main__":
    main()
