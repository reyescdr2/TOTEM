import io
import os
import streamlit as st
import traceback

# PROTOCOLO DE TRANSCODIFICACIÓN INDUSTRIAL v6.0 (FFMPEG Resilience)
# Motor recalibrado para asegurar la compatibilidad universal del activo de audio.

try:
    from pydub import AudioSegment
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths() 
    except: pass
except ImportError:
    AudioSegment = None

def convert_audio_to_ogg(audio_file):
    """
    Motor de Transcodificación de Proximidad v6.0.
    Normaliza el recurso de audio para cumplimiento estricto con el motor de Bedrock.
    """
    if AudioSegment is None:
        st.error("REACTOR DE SONIDO DESACTIVADO: La librería Pydub o FFMPEG no se detectaron.")
        return None
    try:
        # Puntero al inicio del búfer para evitar lecturas nulas.
        audio_file.seek(0)
        
        # Ingesta del activo original (MP3/WAV/etc.)
        audio = AudioSegment.from_file(audio_file)
        
        # NORMALIZACIÓN INDUSTRIAL SOVEREIGN:
        # 1. Monoaural (1 canal): Requerido para posicionamiento espacial 3D in-game.
        # 2. 44100 Hz: Frecuencia de muestreo estándar para fidelidad de audio.
        audio = audio.set_channels(1).set_frame_rate(44100)
        
        # Reactor de exportación a OGG Vorbis
        # Utilizamos libvorbis para asegurar la compatibilidad con el cliente de Minecraft.
        buffer = io.BytesIO()
        audio.export(buffer, format="ogg", codec="libvorbis", parameters=["-q", "5"])
        
        # Retorno de la matriz sonora purificada
        return buffer.getvalue()
    except Exception as e:
        # Informe de falla técnica detallado para el operador
        error_msg = f"FALLO DE TRANSCODIFICACIÓN: {str(e)}"
        st.error(error_msg)
        print(f"[AUDIO_ENGINE_ERROR] {error_msg}")
        return None
