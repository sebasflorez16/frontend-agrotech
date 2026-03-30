#!/usr/bin/env python3
"""
Test script para generar un artículo de ejemplo automáticamente.
Simula la entrada interactiva del generate_article.py
"""

import os
import sys
import json
import random
import re
import subprocess
from datetime import date
from urllib.parse import quote

# Importar las funciones del generador
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_article import (
    search_pexels,
    download_and_optimize_image,
    generate_html,
    parse_content_sections,
    TEMPLATES,
    TEMPLATE_NAMES,
    BLOG_DIR,
    POSTS_JSON,
    _load_existing_posts,
    _update_posts_json,
)

# ============================================================================
# DATOS DEL ARTÍCULO DE PRUEBA
# ============================================================================

ARTICLE_DATA = {
    "slug": "riego-eficiente-colombia",
    "title": "Riego Eficiente en Colombia: Cómo Ahorrar Agua y Aumentar su Cosecha con Datos",
    "description": "Descubra cómo el riego basado en datos satelitales puede reducir el desperdicio de agua hasta un 40% y mejorar el rendimiento de sus cultivos en las condiciones climáticas de Colombia.",
    "author": "Ing. Sofía Martínez",
    "tags": ["Riego", "Tecnología", "Eficiencia", "Colombia"],
}

SEARCH_KEYWORDS = "riego campo cultivo tropical"

CONTENT_TEXT = """INTRO: El agua es el recurso más preciado en la agricultura colombiana. Cada gota cuenta, y sin embargo, la mayoría de los agricultores riegan de forma uniforme sin saber que están desperdiciando hasta un 40% del agua. Hoy le mostramos cómo los datos pueden cambiar eso para siempre.

## El problema del riego a ciegas

Imagínese encender la bomba de riego cada vez que el sol aprieta fuerte, sin saber realmente si su cultivo lo necesita. Es lo que hace la mayoría. Se riega por costumbre, por calendario o simplemente "porque hace calor".

Pero la realidad es que el suelo no es uniforme. Hay zonas de su finca que retienen humedad durante días y otras que se secan en horas. Regar todo por igual significa:

- **Desperdiciar agua** en zonas que aún tienen humedad suficiente
- **Dejar zonas sedientas** donde el cultivo más lo necesita
- **Aumentar costos de energía** innecesariamente con bombeo excesivo
- **Favorecer enfermedades** por exceso de humedad en ciertas áreas

El resultado: más gasto, menos rendimiento y un cultivo que no alcanza su potencial real.

## La solución: riego de precisión con datos satelitales

La tecnología satelital puede medir la humedad del suelo y el estrés hídrico de sus plantas **antes** de que usted note cualquier síntoma a simple vista. Es como tener un sensor en cada metro cuadrado de su finca, pero sin necesidad de instalar nada.

El satélite detecta cambios en la reflectancia de las hojas que indican cuánta agua está usando la planta. Cuando una zona empieza a sufrir estrés hídrico, la señal cambia inmediatamente, días antes de que la hoja se marchite.

Con esta información, usted puede:

- **Regar solo donde se necesita**, ahorrando agua y energía
- **Programar el riego en el momento óptimo**, ni antes ni después
- **Identificar problemas de drenaje** que causan encharcamiento
- **Reducir el riesgo de enfermedades** asociadas al exceso de humedad

## Caso real: ahorro del 35% en agua en los Llanos Orientales

Un productor de arroz en Casanare implementó riego basado en mapas de humedad satelital durante dos ciclos consecutivos. Los resultados fueron contundentes:

- **35% menos consumo de agua** comparado con el riego tradicional
- **12% más de rendimiento** por hectárea
- **Reducción significativa** en costos de bombeo y energía
- **Menor incidencia de enfermedades** fungosas por exceso de humedad

La clave no fue una tecnología costosa ni compleja. Fue simplemente **saber dónde y cuándo regar**, algo que los datos satelitales revelan con una precisión que el ojo humano no puede alcanzar.

## Cómo empezar: tres pasos simples

No necesita ser experto en tecnología para beneficiarse del riego de precisión. El proceso es más sencillo de lo que imagina:

- **Paso 1:** Comparta la ubicación de su finca con nuestro equipo
- **Paso 2:** Reciba un informe inicial de humedad y zonas de riesgo
- **Paso 3:** Ajuste su programa de riego según las recomendaciones

En AgroTech nos encargamos de toda la parte técnica. Usted solo necesita tomar mejores decisiones con la información que le entregamos, en un formato claro y práctico que puede leer desde su celular.

## Reflexión final: cada gota cuenta

En un país como Colombia, donde el agua parece abundante pero los patrones de lluvia son cada vez más impredecibles, aprender a regar con inteligencia no es un lujo, es una necesidad.

La diferencia entre un agricultor que riega a ciegas y uno que riega con datos no es el tamaño de la finca ni el presupuesto disponible. Es la disposición a tomar decisiones basadas en información real.

El futuro del riego no está en bombas más grandes ni en pozos más profundos. Está en usar cada gota exactamente donde y cuando se necesita. Y esa información ya está disponible."""


def main():
    print("\n" + "=" * 60)
    print("  🧪 TEST: Generando artículo de prueba")
    print("=" * 60)

    slug = ARTICLE_DATA["slug"]
    output_path = os.path.join(BLOG_DIR, f"{slug}.html")

    # Si ya existe, eliminar para la prueba
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"  🗑️  Eliminado artículo previo: blog/{slug}.html")

    # Parsear contenido
    sections = parse_content_sections(CONTENT_TEXT)
    print(f"\n  📝 Secciones parseadas: {len(sections)}")
    for s in sections:
        if s.get("is_h2"):
            print(f"     - H2: {s['title']}")
        else:
            print(f"     - INTRO (sin título)")

    # Buscar imágenes en Pexels
    print(f"\n  🖼️  Buscando imágenes: '{SEARCH_KEYWORDS}'...")
    photos = search_pexels(SEARCH_KEYWORDS, count=4)

    if not photos:
        print("  ❌ No se encontraron imágenes. Abortando.")
        sys.exit(1)

    # Descargar y optimizar
    images = []
    for i, photo in enumerate(photos):
        img = download_and_optimize_image(photo, slug, i)
        if img:
            if i == 0:
                img["caption"] = ""
            else:
                h2_sections = [s for s in sections if s.get("is_h2")]
                if i - 1 < len(h2_sections):
                    img["caption"] = f"Imagen relacionada: {h2_sections[i-1]['title']}"
                else:
                    img["caption"] = f"Foto por {photo['photographer']} en Pexels"
            images.append(img)

    print(f"\n  ✅ Imágenes descargadas: {len(images)}")

    if not images:
        print("  ❌ No se pudieron descargar imágenes. Abortando.")
        sys.exit(1)

    # Seleccionar template
    template_idx = random.randint(0, len(TEMPLATES) - 1)
    template_fn = TEMPLATES[template_idx]
    print(f"  🎨 Template: {TEMPLATE_NAMES[template_idx]}")

    # Generar body
    article_body_html = template_fn(sections, images)

    # Generar HTML completo
    full_html = generate_html(ARTICLE_DATA, images, article_body_html)

    # Guardar
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"\n  ✅ Artículo generado: blog/{slug}.html")

    # Verificar tamaño del archivo
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  📄 Tamaño: {size_kb:.1f} KB")

    # Actualizar posts.json
    hero_path = images[0]["path"] if images else ""
    _update_posts_json(ARTICLE_DATA, hero_path)

    # Resumen
    print("\n" + "=" * 60)
    print("  ✅ TEST COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print(f"  📄 Archivo:    blog/{slug}.html ({size_kb:.1f} KB)")
    print(f"  🖼️  Imágenes:  {len(images)} WebP en images/blog/")
    print(f"  🎨 Template:   {TEMPLATE_NAMES[template_idx]}")
    print(f"  📊 posts.json: Actualizado")

    # Verificar que el HTML tenga las partes clave
    print("\n  🔍 VERIFICACIÓN DE CONTENIDO:")
    checks = {
        "Schema.org Article": '"@type": "Article"' in full_html,
        "Open Graph tags": 'property="og:title"' in full_html,
        "Twitter Card": 'name="twitter:card"' in full_html,
        "Canonical URL": 'rel="canonical"' in full_html,
        "Botones compartir": 'share-btn' in full_html,
        "CTA WhatsApp": 'wa.me' in full_html,
        "Related Posts": 'También le puede interesar' in full_html,
        "Blog-row (layout)": 'blog-row' in full_html,
        "Imágenes WebP": '.webp' in full_html,
        "Lazy loading": 'loading="lazy"' in full_html,
        "Breadcrumb Schema": 'BreadcrumbList' in full_html,
        "Meta description": 'meta name="description"' in full_html,
    }

    all_ok = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        if not passed:
            all_ok = False
        print(f"     {status} {check_name}")

    if all_ok:
        print(f"\n  🎉 ¡Todas las verificaciones pasaron! El artículo está listo.")
    else:
        print(f"\n  ⚠️  Algunas verificaciones fallaron. Revisa el HTML generado.")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
