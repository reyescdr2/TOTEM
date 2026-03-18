import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageSequence
from rembg import remove, new_session

# --- PROTOCOLO DE PRESERVACIÓN DE IDENTIDAD NATIVA v50.0 (Native Alpha Shield) ---
# Motor recalibrado para detectar automáticamente la transparencia original y evitar el "re-procesado" innecesario.

def process_gif(gif_file, remove_bg=True, precision="Estándar", erode_size=0, atomic_mode=True, super_clean=True, chroma_sensitivity=45):
    """
    Motor de Extracción de Alta Fidelidad v50.0.
    1. Native Alpha Detection: Si un GIF ya es transparente, NO se toca (Protocolo de Paso Directo).
    2. Smart Bypass: Solo activa la IA si se detecta un fondo sólido predominante.
    3. Integridad de Sincronía: Mantiene la secuencia de frames intacta.
    """
    img = Image.open(gif_file)
    frames_raw = []
    
    try:
        idx = 0
        while True:
            img.seek(idx)
            frames_raw.append(img.convert("RGBA").copy())
            idx += 1
    except EOFError:
        pass
    
    total_frames = len(frames_raw)
    frames_processed = []
    
    # --- DETECCIÓN DE TRANSPARENCIA GLOBAL ---
    # Escaneamos el primer fotograma para decidir si el activo es "Soberano Nativo" (ya transparente).
    first_frame_np = np.array(frames_raw[0])
    alpha_channel = first_frame_np[:, :, 3]
    transparent_pixels = np.sum(alpha_channel < 200)
    total_pixels = first_frame_np.shape[0] * first_frame_np.shape[1]
    
    # Si más del 5% del GIF es transparente, asumimos que ya está recortado y activamos el BYPASS.
    is_native_transparent = (transparent_pixels / total_pixels) > 0.05
    
    if is_native_transparent:
        st.success("💎 ACTIVO SOBERANO DETECTADO: El GIF ya cuenta con transparencia nativa. Procesando frames sin alteración de IA.")
        # Paso directo: solo unificación de canvas en unify_frames posterior.
        return frames_raw, img

    # Si NO tiene transparencia, procedemos con el reactor de purificación industrial.
    progress_bar = st.progress(0, text=f"⚔️ Protocolo v50.0: Procesando Activos ({total_frames} cuadros)...")
    
    try:
        session = new_session("isnet-anime")
    except:
        session = new_session("u2net")

    for i, frame in enumerate(frames_raw):
        frame_np = np.array(frame)
        h, w = frame_np.shape[:2]
        
        if not remove_bg:
            frames_processed.append(frame)
            continue

        # 1. SEGMENTACIÓN NEURONAL (Solo para GIFs con fondo)
        mask_res = remove(
            frame_np[:,:,:3], 
            session=session, 
            only_mask=True, 
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10
        )
        alpha_ia = np.array(mask_res).astype(np.uint8)
        
        # 2. PURGA CROMÁTICA PROTEGIDA
        img_lab = cv2.cvtColor(frame_np[:,:,:3], cv2.COLOR_RGB2LAB)
        
        # Muestreo periférico para detectar ambiente
        bg_samples = []
        for x in np.linspace(0, w-1, 40):
            bg_samples.append(img_lab[0, int(x)])
            bg_samples.append(img_lab[h-1, int(x)])
        bg_samples = np.array(bg_samples).astype(np.float32)

        if len(bg_samples) > 0:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
            _, _, bg_signatures = cv2.kmeans(bg_samples, 6, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            lab_dist_limit = 10 + (chroma_sensitivity * 1.5)
            chroma_mask = np.ones((h, w), dtype=np.uint8) * 255
            
            for signature in bg_signatures:
                dist_bg = np.sqrt(np.sum((img_lab - signature)**2, axis=2))
                chroma_mask[dist_bg < lab_dist_limit] = 0
            
            # Fusión
            alpha_ia = np.minimum(alpha_ia, chroma_mask)

        # 3. CONSOLIDACIÓN DE FOTOGRAMA
        result_np = frame_np.copy()
        result_np[:, :, 3] = alpha_ia
        frames_processed.append(Image.fromarray(result_np))
        
        progress_bar.progress((i + 1) / total_frames, text=f"Purificando Identidad: Cuadro {i+1}/{total_frames}")

    return frames_processed, img

def unify_frames(frames, size=256):
    """
    Sincronización de Canvas Industrial.
    Redimensiona y centra los frames (Incluso los nativos) para el formato 256px de Bedrock.
    """
    processed = []
    for img in frames:
        new_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        bbox = img.getbbox()
        if not bbox:
            processed.append(new_img)
            continue
            
        subject = img.crop(bbox)
        sw, sh = subject.size
        scale = (size - 10) / max(sw, sh)
        nw, nh = int(sw * scale), int(sh * scale)
        subject_res = subject.resize((nw, nh), Image.Resampling.LANCZOS)
        ox, oy = (size - nw) // 2, (size - nh) // 2
        new_img.paste(subject_res, (ox, oy), subject_res)
        processed.append(new_img)
    return processed
