import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Configuración de página
st.set_page_config(
    page_title="Reconocimiento Óptico de Caracteres",
    page_icon="📷",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .camera-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .result-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .sidebar-section {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF0000;
        margin: 1rem 0;
    }
    .filter-option {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 2px solid #3B82F6;
    }
    .text-output {
        background-color: #1F2937;
        color: #10B981;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        border: 2px solid #10B981;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-title">📷 Reconocimiento Óptico de Caracteres</h1>', unsafe_allow_html=True)

# Sidebar mejorado
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🎛️ Opciones de Procesamiento**")
    filtro = st.radio(
        "Aplicar Filtro:",
        ('Con Filtro', 'Sin Filtro'),
        help="El filtro invierte los colores para mejorar la detección de texto"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**💡 Instrucciones**")
    st.write("""
    1. Toma una foto del texto
    2. Elige si aplicar filtro
    3. El texto detectado aparecerá abajo
    4. Funciona mejor con texto claro y buen contraste
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Sección de cámara
st.markdown('<div class="camera-container">', unsafe_allow_html=True)
st.markdown("### 📸 Captura de Imagen")
st.markdown("Toma una foto del texto que quieres reconocer")
img_file_buffer = st.camera_input("Haz clic en el ícono de la cámara para capturar")
st.markdown('</div>', unsafe_allow_html=True)

# Procesamiento de imagen
if img_file_buffer is not None:
    with st.spinner('🔍 Procesando imagen y reconociendo texto...'):
        # Leer y procesar imagen
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Aplicar filtro si está seleccionado
        if filtro == 'Con Filtro':
            cv2_img = cv2.bitwise_not(cv2_img)
            filter_status = "✅ Filtro aplicado"
        else:
            filter_status = "⏹️ Sin filtro"
        
        # Convertir a RGB para mostrar
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        
        # Reconocimiento de texto
        text = pytesseract.image_to_string(img_rgb)
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🖼️ Imagen Procesada")
            st.image(img_rgb, use_container_width=True, caption=filter_status)
        
        with col2:
            st.markdown("### 📝 Texto Reconocido")
            if text.strip():
                st.markdown('<div class="text-output">', unsafe_allow_html=True)
                st.text_area("", text, height=200, label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Estadísticas
                st.markdown("#### 📊 Estadísticas")
                col_stat1, col_stat2 = st.columns(2)
                with col_stat1:
                    st.metric("Caracteres reconocidos", len(text))
                with col_stat2:
                    st.metric("Líneas de texto", text.count('\n') + 1)
            else:
                st.markdown("""
                <div style='background-color: #FEF3C7; padding: 2rem; border-radius: 10px; border-left: 4px solid #F59E0B;'>
                <h4>⚠️ No se detectó texto</h4>
                <p>Intenta:</p>
                <ul>
                <li>Mejorar la iluminación</li>
                <li>Usar el filtro de inversión</li>
                <li>Asegurar que el texto esté enfocado</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer informativo
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280;'>
<p><strong>OCR App</strong> • Desarrollado con PyTesseract y Streamlit</p>
<p>Reconocimiento de texto en imágenes en tiempo real</p>
</div>
""", unsafe_allow_html=True)
