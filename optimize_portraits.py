import os
from PIL import Image, ImageEnhance, ImageFilter

def detect_vertical_crop(img, black_threshold=15):
    """Detects upper and lower black bars in mobile screenshots."""
    grayscale = img.convert("L")
    w, h = grayscale.size
    
    # Scan from top
    crop_top = 0
    for y in range(h):
        sample_pixels = [grayscale.getpixel((x, y)) for x in range(0, w, 10)]
        if (sum(sample_pixels) / len(sample_pixels)) > black_threshold:
            crop_top = y
            break
            
    # Scan from bottom
    crop_bottom = h
    for y in range(h - 1, -1, -1):
        sample_pixels = [grayscale.getpixel((x, y)) for x in range(0, w, 10)]
        if (sum(sample_pixels) / len(sample_pixels)) > black_threshold:
            crop_bottom = y + 1
            break
            
    # If bands detected (> 5% of height), apply crop
    if crop_top > int(h * 0.05) or (h - crop_bottom) > int(h * 0.05):
        print(f"[*] Bandas negras detectadas: Superior={crop_top}px ({crop_top/h:.1%}), Inferior={h-crop_bottom}px ({(h-crop_bottom)/h:.1%})")
        return crop_top, crop_bottom
    return 0, h

def process_portrait_fire(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"[-] No se encontró: {input_path}")
        return
    
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    
    # 1. Recorte de franjas negras superior e inferior de captura móvil
    crop_top, crop_bottom = detect_vertical_crop(img)
    if crop_top == 0 and crop_bottom == height:
        # Fallback al 22% predeterminado
        crop_top = int(height * 0.22)
        crop_bottom = int(height * 0.78)
        
    cropped = img.crop((0, crop_top, width, crop_bottom))
    print(f"[+] Recorte aplicado: {width}x{height} -> {cropped.size}")
    
    # 2. Restauración de microdetalle dérmico y capilar (Unsharp Mask)
    enhanced = cropped.filter(ImageFilter.UnsharpMask(radius=1.6, percent=140, threshold=3))
    
    # 3. Ajuste de contraste óptico cinemático (Sony A1 emulation)
    enhancer_contrast = ImageEnhance.Contrast(enhanced)
    contrasted = enhancer_contrast.enhance(1.06)
    
    enhancer_color = ImageEnhance.Color(contrasted)
    final_img = enhancer_color.enhance(1.04)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path, quality=95, optimize=True)
    print(f"[+] Retrato Fuego optimizado: {output_path} ({final_img.size})")

def process_portrait_studio(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"[-] No se encontró: {input_path}")
        return
    
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    
    # Comprobar si tiene bandas negras
    crop_top, crop_bottom = detect_vertical_crop(img)
    if crop_top > 0 or crop_bottom < height:
        cropped = img.crop((0, crop_top, width, crop_bottom))
    else:
        cropped = img
        
    # Recuperación de textura y microdetalle
    enhanced = cropped.filter(ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=3))
    enhancer_contrast = ImageEnhance.Contrast(enhanced)
    contrasted = enhancer_contrast.enhance(1.05)
    
    enhancer_color = ImageEnhance.Color(contrasted)
    final_img = enhancer_color.enhance(1.03)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path, quality=95, optimize=True)
    print(f"[+] Retrato Estudio optimizado: {output_path} ({final_img.size})")

if __name__ == "__main__":
    os.makedirs("assets/images", exist_ok=True)
    
    input_hero = "Screenshot_20261025_151030_Gallery.jpg"
    input_bio = "Screenshot_20261025_151102_Gallery.jpg"
    
    output_hero = "assets/images/hero_portrait_optimized.jpg"
    output_bio = "assets/images/bio_portrait_optimized.jpg"
    
    print("--- INICIANDO PROCESAMIENTO Y OPTIMIZACIÓN DE RETRATOS ---")
    process_portrait_fire(input_hero, output_hero)
    process_portrait_studio(input_bio, output_bio)
    print("--- PROCESAMIENTO COMPLETADO EXITOSAMENTE ---")
