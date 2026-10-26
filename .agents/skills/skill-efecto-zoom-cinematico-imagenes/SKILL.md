---
name: skill-efecto-zoom-cinematico-imagenes
description: >-
  Protocolo determinista y motor de micro-zoom cinemático interactivo (Smooth Hover Focus) para imágenes, retratos y tarjetas visuales en la plataforma web oficial de Lic. Yorman Antonio Trabasilo González y proyectos gastronómicos afines. Aplica transformaciones de escala fluida (1.0x -> 1.08x), curvas de desaceleración cubic-bezier de alta gama, aceleración por hardware GPU (will-change: transform), confinamiento con overflow: hidden y halo perimetral dorado sin desbordamientos ni distorsiones.
---

# SKILL-019 — Motor de Micro-Zoom Cinemático Interactivo para Fotografía Web (V1.0.0 — CERTIFICADO OFICIAL)

```text
========================================================================================
DIRECTOR DEL PROYECTO: Lic. Yorman Antonio Trabasilo González
PLATAFORMA ASOCIADA:    Plataforma Web Oficial Yorman Trabasilo (v2.0) & ¡Qué Brutal!
ECOSISTEMA:            PROMASTER — Antigravity (V1.7.0)
IDENTIFICADOR:         SKILL-019 (SKILL-EFECTO-ZOOM-CINEMATICO-IMAGENES)
DOMINIO:               PM-FRONTEND-01 (Micro-interacciones UI/UX) & PM-MEDIA-03 (Animación)
VERSIÓN:               V1.0.0 (Escala 1.08x + Curva Cubic-Bezier + GPU Acceleration)
ESTADO:                VALIDADO Y CERTIFICADO OFICIALMENTE POR EL DIRECTOR
CLASES MAESTRAS:       .img-zoom-container, .img-zoom-target, .img-card-glow
========================================================================================
```

---

## 1. Fundamento Óptico y Experiencia de Usuario (UI/UX)

En plataformas gastronómicas y editoriales de alta gama, las fotografías estáticas pueden lucir inertes. El efecto de **Micro-Zoom Cinemático Interactivo** transforma la experiencia de navegación del comensale o cliente:

1. **Estado Reposo (Cursor fuera / Idle):**
   * La fotografía se muestra en su encuadre original canónico (`scale(1.0)`).
   * Mantiene el contexto espacial completo del plato, la cocina o el retrato del Chef.
2. **Estado Activo (Cursor arriba / Hover):**
   * Al posar el cursor, la imagen se acerca suavemente un **8% (`scale(1.08)`)** con una curva de desaceleración editorial (`cubic-bezier(0.25, 1, 0.5, 1)`).
   * Genera una sensación instantánea de **profundidad, foco y dinamismo tridimensional** (*focus cinematográfico*).
   * Un leve incremento de luminosidad y contraste (`brightness(1.03) contrast(1.02)`) aviva los colores de los ingredientes y el fuego.
3. **Confinamiento Inviolable (`overflow: hidden`):**
   * El zoom ocurre estrictamente dentro del contenedor redondeado (`rounded-2xl` o `rounded-xl`), garantizando que la imagen jamás desborde ni altere el flujo del layout ni desplace textos vecinos.

---

## 2. Especificación Técnica CSS Canónica

Toda imagen que deba exhibir el efecto de zoom debe regirse por estas tres clases utilitarias:

```css
/* ==========================================================================
   EFECTO ZOOM CINEMÁTICO INTERACTIVO (SMOOTH HOVER FOCUS) - SKILL-019
   ========================================================================== */

/* 1. Contenedor Maestro: confina la imagen y define el contexto de cursor */
.img-zoom-container {
  overflow: hidden !important;
  position: relative;
  cursor: pointer;
}

/* 2. Elemento Imagen: aceleración por GPU y curva suave de 0.7s */
.img-zoom-target {
  transform: scale(1);
  transition: transform 0.7s cubic-bezier(0.25, 1, 0.5, 1), filter 0.7s ease;
  will-change: transform;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transform-origin: center center;
}

/* 3. Disparador de Zoom: responde tanto al hover directo como al de la tarjeta contenedora */
.img-zoom-container:hover .img-zoom-target,
.group:hover .img-zoom-target,
.img-zoom-target:hover {
  transform: scale(1.08) !important;
  filter: brightness(1.03) contrast(1.02);
}

/* 4. Halo Dorado Perimetral en Tarjetas (Opcional para Tarjetas y Retratos) */
.img-card-glow {
  transition: border-color 0.4s ease, box-shadow 0.4s ease;
}
.img-card-glow:hover,
.group:hover .img-card-glow {
  border-color: rgba(197, 157, 95, 0.6) !important;
  box-shadow: 0 12px 35px -8px rgba(197, 157, 95, 0.22) !important;
}
```

---

## 3. Patrones de Integración en el HTML

### Patrón A: Retratos Editoriales (Hero y Bio)
```html
<div class="relative rounded-2xl overflow-hidden border border-brand-gold/40 shadow-2xl group img-card-glow">
  <div class="relative aspect-[3/4] w-full overflow-hidden img-zoom-container">
    <img src="assets/images/retrato.jpg" 
         alt="Lic. Yorman Trabasilo" 
         class="w-full h-full object-cover object-top cinematic-portrait img-zoom-target">
  </div>
</div>
```

### Patrón B: Tarjetas de Catálogo de Recetas
```html
<div class="recipe-card group img-card-glow bg-brand-card rounded-xl border border-neutral-800 overflow-hidden">
  <div class="relative h-52 overflow-hidden bg-neutral-900 img-zoom-container">
    <img src="assets/images/recetas/plato.jpg" 
         alt="Nombre del Plato" 
         class="w-full h-full object-cover img-zoom-target">
    <div class="absolute top-3 left-3 ...">Insignia</div>
  </div>
  <!-- Contenido y botón -->
</div>
```

### Patrón C: Artículos y Reseñas Históricas
```html
<article class="bg-brand-card rounded-2xl border border-neutral-800 overflow-hidden grid group img-card-glow">
  <div class="lg:col-span-5 h-72 lg:h-full min-h-[280px] overflow-hidden img-zoom-container">
    <img src="assets/images/historia.jpg" 
         alt="Artículo Histórico" 
         class="w-full h-full object-cover img-zoom-target">
  </div>
  <!-- Cuerpo del artículo -->
</article>
```

---

## 4. Reglas Inviolables de Rendimiento (Checklist de Calidad)

1. [x] **Aceleración por Hardware Obligatoria:** Toda imagen con zoom DEBE declarar `will-change: transform;` y `backface-visibility: hidden;` para delegar el renderizado al compositor de la GPU, previniendo caídas de FPS.
2. [x] **Curva de Desaceleración no Lineal:** Jamás usar `transition: linear` ni `ease-in`. La curva canónica es `cubic-bezier(0.25, 1, 0.5, 1)` (desaceleración suave, natural y elegante).
3. [x] **Factor de Escala Máximo 1.08x:** No exceder `1.08` (8%) en retratos o recetas para evitar recortes excesivos de los bordes o pixelación en monitores estándar.
4. [x] **Integración con SKILL-017:** Las imágenes deben estar previamente calibradas con Lanczos antialiasing antes de aplicar el efecto.

---
*Certificado y consolidado en el Ecosistema PROMASTER / Antigravity por Lic. Yorman Antonio Trabasilo González.*
