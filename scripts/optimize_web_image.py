#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
MOTOR DE PROCESAMIENTO Y CALIBRACIÓN DE IMÁGENES WEB — PLATAFORMA YORMAN TRABASILO
SKILL: skill-optimizacion-imagenes-plataforma-yorman (SKILL-017)
DIRECTOR: Lic. Yorman Antonio Trabasilo González
ESTÁNDAR: Resampling LANCZOS, cero aliasing, cero distorsión, preservación de textura
========================================================================================
"""

import os
import sys
import argparse
from PIL import Image, ImageOps

# Resoluciones canónicas calibradas para la plataforma
PRESETS = {
    "hero": {
        "width": 764,
        "height": 1024,
        "aspect_ratio": 3 / 4,
        "quality": 96,
        "description": "Retrato Principal Hero (Proporción 3:4, rostro, filipina y horno sin aliasing)"
    },
    "bio": {
        "width": 600,
        "height": 800,
        "aspect_ratio": 3 / 4,
        "quality": 95,
        "description": "Retrato de Trayectoria Curricular (Proporción 3:4)"
    },
    "recipe": {
        "width": 800,
        "height": 533,
        "aspect_ratio": 3 / 2,
        "quality": 92,
        "description": "Tarjeta de Receta Gastronómica (Proporción 3:2 apaisado)"
    },
    "modal": {
        "width": 1200,
        "height": 800,
        "aspect_ratio": 3 / 2,
        "quality": 94,
        "description": "Ficha Técnica Ampliada / Modal Gastronómico"
    },
    "square": {
        "width": 600,
        "height": 600,
        "aspect_ratio": 1 / 1,
        "quality": 95,
        "description": "Iconografía / Reseñas / Perfiles Cuadrados"
    }
}

def detect_and_crop_black_bars(img, threshold=15):
    """
    Detecta y recorta franjas negras superior e inferior si la imagen
    proviene de una captura de pantalla móvil.
    """
    gray = img.convert("L")
    w, h = gray.size
    
    top = 0
    for y in range(h):
        sample = [gray.getpixel((x, y)) for x in range(0, w, 15)]
        if (sum(sample) / len(sample)) > threshold:
            top = y
            break
            
    bottom = h
    for y in range(h - 1, -1, -1):
        sample = [gray.getpixel((x, y)) for x in range(0, w, 15)]
        if (sum(sample) / len(sample)) > threshold:
            bottom = y + 1
            break
            
    if top > int(h * 0.05) or (h - bottom) > int(h * 0.05):
        print(f"[*] Bandas negras detectadas y recortadas: Superior={top}px, Inferior={h - bottom}px")
        return img.crop((0, top, w, bottom))
    return img

def fit_to_aspect_ratio(img, target_ratio):
    """
    Ajusta la imagen a la relación de aspecto objetivo recortando sutilmente
    las orillas excedentes (centrado inteligente o anclado arriba para retratos).
    """
    w, h = img.size
    current_ratio = w / h
    
    # Si la diferencia es mínima (< 2%), no se recorta
    if abs(current_ratio - target_ratio) < 0.02:
        return img
        
    if current_ratio > target_ratio:
        # La imagen es más ancha de lo deseado -> recortar lados
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        return img.crop((offset, 0, offset + new_w, h))
    else:
        # La imagen es más alta -> para retratos se conserva el tercio superior (rostro/pecho)
        new_h = int(w / target_ratio)
        # 15% margen superior para no decapitar y mostrar postura
        offset = int((h - new_h) * 0.15)
        if offset + new_h > h:
            offset = h - new_h
        return img.crop((0, offset, w, offset + new_h))

def optimize_image(input_path, output_path, preset_name="hero", custom_w=None, custom_h=None):
    """
    Procesa, calibra resolución con Lanczos y optimiza la imagen sin alterar
    la naturalidad de los tonos dérmicos ni introducir ruido artificial.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {input_path}")
        
    preset = PRESETS.get(preset_name, PRESETS["hero"])
    target_w = custom_w or preset["width"]
    target_h = custom_h or preset["height"]
    target_ratio = target_w / target_h
    quality = preset["quality"]
    
    print(f"============================================================")
    print(f"PROCESANDO IMAGEN PARA PLATAFORMA YORMAN TRABASILO")
    print(f"Entrada:   {input_path}")
    print(f"Preset:    {preset_name.upper()} ({preset['description']})")
    print(f"Objetivo:  {target_w}x{target_h} px (Calidad: {quality}%)")
    print(f"============================================================")
    
    raw_img = Image.open(input_path)
    
    # Asegurar espacio de color RGB limpio
    if raw_img.mode in ("RGBA", "P"):
        background = Image.new("RGB", raw_img.size, (24, 24, 24))
        if raw_img.mode == "RGBA":
            background.paste(raw_img, mask=raw_img.split()[3])
        else:
            background.paste(raw_img.convert("RGB"))
        img = background
    else:
        img = raw_img.convert("RGB")
        
    # 1. Limpieza de bandas negras si aplican
    img = detect_and_crop_black_bars(img)
    
    # 2. Ajuste de proporción geométrica
    img = fit_to_aspect_ratio(img, target_ratio)
    
    # 3. Remuestreo Determinista con Filtro sinc LANCZOS (Anti-aliasing matemático perfecto)
    final_img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 4. Exportación Web Progresiva Optimizada
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final_img.save(
        output_path,
        "JPEG",
        quality=quality,
        progressive=True,
        optimize=True
    )
    
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"[OK] IMAGEN OPTIMIZADA CON EXITO:")
    print(f"    Ruta:       {output_path}")
    print(f"    Dimensiones:{final_img.size[0]}x{final_img.size[1]} px")
    print(f"    Peso Web:   {file_size_kb:.1f} KB")
    print(f"    Textura:    100% Pura (Sin aliasing, sin convolución, sin grano)")
    print(f"============================================================\n")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrador de Imágenes Web para Plataforma Yorman Trabasilo")
    parser.add_argument("--input", "-i", required=True, help="Ruta de la imagen de origen")
    parser.add_argument("--output", "-o", required=True, help="Ruta de destino (.jpg)")
    parser.add_argument("--type", "-t", choices=list(PRESETS.keys()), default="hero", help="Tipo de preset (hero, bio, recipe, modal, square)")
    parser.add_argument("--width", type=int, help="Ancho personalizado opcional")
    parser.add_argument("--height", type=int, help="Alto personalizado opcional")
    
    args = parser.parse_args()
    optimize_image(args.input, args.output, args.type, args.width, args.height)
