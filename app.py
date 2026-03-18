import streamlit as st
import numpy as np
import cv2
import io
import os
from PIL import Image
from modules.core_processor import process_gif, unify_frames
from modules.pack_compiler import create_mcpack
from modules.audio_engine import convert_audio_to_ogg
# --- CONFIGURACIÓN DE ENTORNO ---
st.set_page_config(
    page_title="CDR Totems | Elite Asset Suite",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CAPA DE SEGURIDAD SOBERANA (ACCESS KEY) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("### 🔒 CDR Totems | Búfer de Identidad")
    auth_input = st.text_input("Introduzca la Clave Maestra de Acceso (Master Key):", type="password")
    if st.button("🔓 Desbloquear Reactor"):
        if auth_input == "REYES200705192058356683654688954686596":
            st.session_state.authenticated = True
            st.success("IDENTIDAD VERIFICADA: Acceso concedido.")
            st.rerun()
        else:
            st.error("BLOQUEO DE SISTEMA: Clave maestra incorrecta.")
    st.stop()

# --- ARQUITECTURA DE INTERFAZ (Visible tras autenticación) ---
st.title("CDR Totems")
st.subheader("Elite Visual Assets Compiling Suite | Cloud Architecture v13.0")

# NOTA DE DESPLIEGUE CLOUD 24/7
st.success("☁️ **ESTADO DEL REACTOR:** Operando en la Nube. Acceso global 24/7 activo y blindado.")

# NOTA DE OPTIMIZACIÓN TÉCNICA
st.info("💡 **TECHNICAL ADVISORY:** Para una extracción de grado quirúrgico con 'Cero Residuos', se recomienda recursos con fondos cromáticos uniformes. El motor CDR v10.0 incluye blindaje de audio (Mono/441kHz) y limpieza de metadatos industrial.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🧬 Ingesta de Recursos")
    gif_file = st.file_uploader("Recurso GIF de Entrada (Secuencia)", type=["gif"], help="Animación base para el activo.")
    if gif_file:
        if "last_gif" not in st.session_state or st.session_state.last_gif != gif_file.name:
            st.session_state.last_gif = gif_file.name
            if "processed_frames" in st.session_state: del st.session_state.processed_frames
            if "mcpack_data" in st.session_state: del st.session_state.mcpack_data
    
    audio_file = st.file_uploader("Búfer de Audio (Efecto de Uso)", type=["mp3", "wav", "ogg"], help="Sonido de activación del tótem.")
    icon_file = st.file_uploader("Identidad Visual del Pack (Icono)", type=["png", "jpg", "jpeg"], help="Imagen que se verá en el menú de packs de Minecraft.")

    with st.expander("⚙️ Parámetros de Inferencia"):
        remove_bg = st.checkbox("Aislamiento de Identidad (Multi-Pass)", value=True)
        atomic_mode = st.checkbox("Blindaje de Masa Crítica (Anti-Mutilation)", value=True)
        super_clean = st.checkbox("Purificación Profunda (Residue Purge)", value=True)
        precision = st.selectbox("Precisión de Segmentación", ["Alta", "Estándar", "Rápida"])
        chroma_sens = st.slider("Sensibilidad de Purificación Cromática", 0, 100, 55)
        erode_val = st.slider("Erosión Perimetral (Fringe Removal)", 0, 5, 0)
    
    # 🧬 VISTA DE INGESTA (Pre-procesamiento)
    if gif_file or icon_file:
        st.markdown("---")
        st.markdown("#### 👁️ Monitor de Ingesta")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            if gif_file: st.image(gif_file, caption="Animación Fuente", width=128)
        with v_col2:
            if icon_file: st.image(icon_file, caption="Identidad de Pack", width=128)

with col2:
    st.markdown("### � Configuración de Salida")
    p_name = st.text_input("Identificador del Pack (Nomenclatura)", value="CDR_Totem_Pack")
    p_desc = st.text_area("Descripción (Manifest)", value="Activo soberano procesado con CDR Totems v10.0.")

if st.button("🔧 EJECUTAR COMPILACIÓN DE ACTIVOS (MASTER SYNC)"):
    if not gif_file:
        st.error("ERROR CRÍTICO: Recurso GIF ausente.")
    else:
        with st.spinner("Procesando matriz visual y sincronizando frecuencias soberanas..."):
            # 1. PROCESAMIENTO VISUAL
            frames, _ = process_gif(gif_file, remove_bg, precision, erode_val, atomic_mode, super_clean, chroma_sens)
            unified = unify_frames(frames)
            st.session_state.processed_frames = unified
            
            # 2. PROCESAMIENTO DE AUDIO (Sello de Transcodificación)
            a_bytes = None
            if audio_file:
                audio_file.seek(0)
                if audio_file.name.endswith(".ogg"):
                    a_bytes = audio_file.read()
                else:
                    a_bytes = convert_audio_to_ogg(audio_file)
            
            # 3. PROCESAMIENTO DE ICONO (Fidelidad de Búfer)
            processed_icon = None
            if icon_file:
                try:
                    icon_file.seek(0)
                    icon_img = Image.open(icon_file).resize((128, 128), Image.Resampling.LANCZOS)
                    icon_img.info.clear() # Limpieza de metadatos
                    ic_bytes = io.BytesIO()
                    icon_img.save(ic_bytes, format="PNG")
                    processed_icon = ic_bytes.getvalue()
                except: pass

            # 4. CONSOLIDACIÓN DE CONTENEDOR .MCPACK
            mcpack_res = create_mcpack(p_name, p_desc, processed_icon, unified, a_bytes)
            
            st.session_state.processed_gif_bytes = io.BytesIO()
            unified[0].save(st.session_state.processed_gif_bytes, format="GIF", save_all=True, append_images=unified[1:], loop=0, duration=100, disposal=2)
            st.session_state.processed_audio = a_bytes
            st.session_state.mcpack_data = mcpack_res
            st.rerun()

# --- DASHBOARD DE RESULTADOS (Sovereign Output) ---
if "mcpack_data" in st.session_state:
    st.divider()
    
    st.markdown("### 📊 Dashboard de Análisis Visual")
    
    # 1. Visualización de la Secuencia Completa (Inspección de Frames)
    if "processed_frames" in st.session_state and st.session_state.processed_frames:
        st.write(f"🔍 Inspección Técnica: {len(st.session_state.processed_frames)} fotogramas sincronizados.")
        cols = st.columns(6)
        for idx, frame in enumerate(st.session_state.processed_frames):
            with cols[idx % 6]:
                st.image(frame, caption=f"Frame {idx+1}", use_container_width=True)
    
    st.divider()
    
    # 2. Comparativa de Identidad
    comp1, comp2 = st.columns(2)
    with comp1:
        if gif_file:
            st.markdown("### 🖼️ Recurso GIF Original")
            st.image(gif_file, width=256)
    with comp2:
        if "processed_gif_bytes" in st.session_state:
            st.markdown("### ⚔️ Simulación de Segmentación IA")
            st.image(st.session_state.processed_gif_bytes.getvalue(), width=256)

    st.divider()
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.success("✅ COMPILACIÓN COMPLETADA")
        st.write(f"📦 ACTIVO: `{p_name}.mcpack`")
        
        st.download_button(
            label="⬇️ DESCARGAR ACTIVO SOBERANO (.MCPACK)",
            data=st.session_state.mcpack_data,
            file_name=f"{p_name}.mcpack",
            mime="application/octet-stream"
        )
        
        st.markdown("---")
        if "processed_audio" in st.session_state and st.session_state.processed_audio:
            st.markdown("### 🔊 Monitor de Salida Sonora")
            st.info("👂 Reproduciendo el activo purificado (.OGG) que se incluirá en el pack.")
            st.audio(st.session_state.processed_audio, format="audio/ogg")
        else:
            st.warning("🔇 No se detectó flujo de audio procesado para este activo.")
        
        st.write("🔧 Sello de Integridad v11.0: Audio Mono/44.1kHz e Iconografía vinculada.")
    
    with res_col2:
        st.info("💡 **ESTADO SOBERANO:** El pack ha sido purificado de metadatos y está listo para su despliegue en Minecraft Bedrock.")
