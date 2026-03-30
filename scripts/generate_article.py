#!/usr/bin/env python3
"""
AgroTech Blog Article Generator
================================
Genera artículos HTML completos para el blog de AgroTech Colombia.

Funcionalidades:
1. Busca 3-4 imágenes relevantes en Pexels (contexto latino/agrícola)
2. Las descarga, redimensiona (500px) y convierte a WebP
3. Selecciona aleatoriamente 1 de 4 plantillas de estructura visual
4. Genera el HTML con SEO máximo (Schema.org, OG, Twitter, canonical, etc.)
5. Actualiza posts.json automáticamente

Uso:
  python3 scripts/generate_article.py

Se te pedirá interactivamente:
  - Slug del artículo (ej: riego-eficiente-colombia)
  - Título completo
  - Meta description
  - Nombre del autor
  - Tags (separados por coma)
  - Contenido del artículo (secciones con títulos H2)

Requisitos:
  pip install requests Pillow
"""

import os
import sys
import json
import random
import re
import subprocess
import textwrap
from datetime import date
from urllib.parse import quote

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

PEXELS_API_KEY = "qbQ194vpJ2SiokYivs9NGUOsVc0knowwsGywAjKQg98pWcSQX59SFadg"
SITE_URL = "https://agrotechcolombia.com"
WHATSAPP_NUMBER = "573223088873"

# Rutas del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(PROJECT_ROOT, "blog")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images", "blog")
POSTS_JSON = os.path.join(PROJECT_ROOT, "data", "posts.json")

# Términos de búsqueda preferidos para contexto latino/colombiano
LATIN_SEARCH_MODIFIERS = [
    "latin america",
    "colombia",
    "tropical agriculture",
    "south america farm",
    "hispanic farmer",
    "latin farmer field",
]

# Términos para imágenes sin personas (más universales)
LANDSCAPE_MODIFIERS = [
    "tropical crop field",
    "green plantation aerial",
    "agriculture technology",
    "farm landscape drone",
    "crop rows aerial view",
    "fertile soil planting",
]

# ============================================================================
# PEXELS API
# ============================================================================

def search_pexels(query, count=4, orientation="landscape"):
    """Busca imágenes en Pexels con contexto latino/agrícola."""
    import requests

    headers = {"Authorization": PEXELS_API_KEY}
    all_photos = []

    # Estrategia: buscar con varios modificadores para variedad
    search_queries = []

    # 1. Búsqueda directa con contexto
    search_queries.append(f"{query} agriculture")

    # 2. Agregar modificador latino aleatorio
    latin_mod = random.choice(LATIN_SEARCH_MODIFIERS)
    search_queries.append(f"{query} {latin_mod}")

    # 3. Agregar paisaje agrícola
    landscape_mod = random.choice(LANDSCAPE_MODIFIERS)
    search_queries.append(f"{landscape_mod} {query}")

    for sq in search_queries:
        if len(all_photos) >= count:
            break

        params = {
            "query": sq,
            "per_page": 5,
            "orientation": orientation,
            "locale": "es-ES",
        }

        try:
            resp = requests.get(
                "https://api.pexels.com/v1/search",
                headers=headers,
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            for photo in data.get("photos", []):
                # Evitar duplicados
                if photo["id"] not in [p["id"] for p in all_photos]:
                    all_photos.append(photo)
                    if len(all_photos) >= count:
                        break
        except Exception as e:
            print(f"  ⚠️  Error buscando '{sq}': {e}")
            continue

    if not all_photos:
        print("  ❌ No se encontraron imágenes. Intenta con otras palabras clave.")
        return []

    print(f"  ✅ Encontradas {len(all_photos)} imágenes")
    return all_photos[:count]


def download_and_optimize_image(photo, slug, index):
    """Descarga una imagen de Pexels, la redimensiona y convierte a WebP."""
    import requests

    # URL de tamaño mediano (ya pre-redimensionada ~1280px)
    url = photo["src"]["large"]
    photographer = photo["photographer"]
    pexels_id = photo["id"]

    # Nombre SEO-friendly
    filename = f"{slug}-{index + 1}"
    webp_path = os.path.join(IMAGES_DIR, f"{filename}.webp")
    temp_path = os.path.join(IMAGES_DIR, f"{filename}_temp.jpg")

    print(f"  📥 Descargando imagen {index + 1} (Pexels ID: {pexels_id}, by {photographer})...")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        with open(temp_path, "wb") as f:
            f.write(resp.content)

        # Redimensionar a 500px de ancho máximo con sips
        subprocess.run(
            ["sips", "-Z", "500", temp_path, "--out", temp_path],
            capture_output=True,
            check=True,
        )

        # Convertir a WebP con cwebp
        result = subprocess.run(
            ["cwebp", "-q", "75", temp_path, "-o", webp_path],
            capture_output=True,
        )

        if result.returncode != 0:
            # Fallback: intentar con sips a png y luego cwebp
            png_temp = temp_path.replace(".jpg", ".png")
            subprocess.run(["sips", "-s", "format", "png", temp_path, "--out", png_temp], capture_output=True)
            subprocess.run(["cwebp", "-q", "75", png_temp, "-o", webp_path], capture_output=True)
            if os.path.exists(png_temp):
                os.remove(png_temp)

        # Limpiar temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if os.path.exists(webp_path):
            size_kb = os.path.getsize(webp_path) / 1024
            print(f"  ✅ {filename}.webp ({size_kb:.0f} KB)")
            return {
                "filename": f"{filename}.webp",
                "path": f"/images/blog/{filename}.webp",
                "full_url": f"{SITE_URL}/images/blog/{filename}.webp",
                "photographer": photographer,
                "pexels_id": pexels_id,
            }
        else:
            print(f"  ❌ Error al convertir imagen {index + 1}")
            return None

    except Exception as e:
        print(f"  ❌ Error descargando imagen {index + 1}: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None


# ============================================================================
# PLANTILLAS DE ESTRUCTURA
# ============================================================================

def template_A(sections, images):
    """
    Template A: Hero + imagen derecha + imagen izquierda + imagen derecha
    Distribución: texto-img | img-texto | texto-img
    """
    html_parts = []
    img_idx = 1  # imagen 0 es hero

    for i, section in enumerate(sections):
        if i == 0:
            # Primera sección: solo texto (intro)
            html_parts.append(section["html"])
        elif img_idx < len(images) and section.get("is_h2"):
            img = images[img_idx]
            if img_idx % 2 == 1:
                # Imagen a la derecha
                html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row">
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                    </div>''')
            else:
                # Imagen a la izquierda (reverse)
                html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row reverse">
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                    </div>''')
            img_idx += 1
        else:
            # Sección sin imagen
            if section.get("is_h2"):
                html_parts.append(f'<h2 class="blog-section-title">{section["title"]}</h2>')
            html_parts.append(section["html"])

    return "\n".join(html_parts)


def template_B(sections, images):
    """
    Template B: Hero + 2 imágenes a la derecha + imagen full-width
    """
    html_parts = []
    img_idx = 1

    for i, section in enumerate(sections):
        if i == 0:
            html_parts.append(section["html"])
        elif img_idx < len(images) and section.get("is_h2") and img_idx <= 2:
            img = images[img_idx]
            html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row">
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                    </div>''')
            img_idx += 1
        elif img_idx < len(images) and section.get("is_h2") and img_idx == 3:
            img = images[img_idx]
            html_parts.append(f'<h2 class="blog-section-title">{section["title"]}</h2>')
            html_parts.append(f'''
                    <img src="{img['path']}" alt="{section['title']}" loading="lazy" class="blog-full-image" width="800" height="450">
                    <p class="image-caption" style="text-align:center; margin-bottom: var(--spacing-md);">{img.get('caption', '')}</p>''')
            html_parts.append(section["html"])
            img_idx += 1
        else:
            if section.get("is_h2"):
                html_parts.append(f'<h2 class="blog-section-title">{section["title"]}</h2>')
            html_parts.append(section["html"])

    return "\n".join(html_parts)


def template_C(sections, images):
    """
    Template C: Hero + imagen izquierda + full-width + imagen derecha
    """
    html_parts = []
    img_idx = 1

    for i, section in enumerate(sections):
        if i == 0:
            html_parts.append(section["html"])
        elif img_idx < len(images) and section.get("is_h2") and img_idx == 1:
            img = images[img_idx]
            html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row reverse">
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                    </div>''')
            img_idx += 1
        elif img_idx < len(images) and section.get("is_h2") and img_idx == 2:
            img = images[img_idx]
            html_parts.append(f'<h2 class="blog-section-title">{section["title"]}</h2>')
            html_parts.append(section["html"])
            html_parts.append(f'''
                    <img src="{img['path']}" alt="{section['title']}" loading="lazy" class="blog-full-image" width="800" height="450">
                    <p class="image-caption" style="text-align:center; margin-bottom: var(--spacing-md);">{img.get('caption', '')}</p>''')
            img_idx += 1
        elif img_idx < len(images) and section.get("is_h2") and img_idx == 3:
            img = images[img_idx]
            html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row">
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                    </div>''')
            img_idx += 1
        else:
            if section.get("is_h2"):
                html_parts.append(f'<h2 class="blog-section-title">{section["title"]}</h2>')
            html_parts.append(section["html"])

    return "\n".join(html_parts)


def template_D(sections, images):
    """
    Template D: Hero + imagen derecha grande + secciones limpias + imagen derecha al final
    Minimalista: solo 2 imágenes dentro del cuerpo, más limpio.
    """
    html_parts = []
    img_idx = 1
    used_images = 0

    for i, section in enumerate(sections):
        if i == 0:
            html_parts.append(section["html"])
        elif section.get("is_h2") and used_images == 0 and img_idx < len(images):
            img = images[img_idx]
            html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row">
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                    </div>''')
            img_idx += 1
            used_images += 1
        elif section.get("is_h2") and i == len(sections) - 1 and img_idx < len(images):
            # Última sección con imagen
            img = images[img_idx]
            html_parts.append(f'''
                    <h2 class="blog-section-title">{section["title"]}</h2>
                    <div class="blog-row reverse">
                        <div class="blog-col-image">
                            <img src="{img['path']}" alt="{section['title']}" loading="lazy" width="350" height="233">
                            <p class="image-caption">{img.get('caption', '')}</p>
                        </div>
                        <div class="blog-col-text">
                            {section["html"]}
                        </div>
                    </div>''')
            img_idx += 1
            used_images += 1
        else:
            if section.get("is_h2"):
                html_parts.append(f'<h2 class="blog-section-title">{section["title"]}</h2>')
            html_parts.append(section["html"])

    return "\n".join(html_parts)


TEMPLATES = [template_A, template_B, template_C, template_D]
TEMPLATE_NAMES = ["A (alternado izq/der)", "B (derecha + full-width)", "C (izq + full + der)", "D (minimalista)"]


# ============================================================================
# GENERADOR HTML
# ============================================================================

def generate_html(article_data, images, article_body_html):
    """Genera el HTML completo del artículo con SEO máximo."""

    slug = article_data["slug"]
    title = article_data["title"]
    description = article_data["description"]
    author = article_data["author"]
    tags = article_data["tags"]
    today = date.today().isoformat()
    today_display = date.today().strftime("%-d de %B de %Y").replace(
        "January", "enero").replace("February", "febrero").replace(
        "March", "marzo").replace("April", "abril").replace(
        "May", "mayo").replace("June", "junio").replace(
        "July", "julio").replace("August", "agosto").replace(
        "September", "septiembre").replace("October", "octubre").replace(
        "November", "noviembre").replace("December", "diciembre")

    hero_image = images[0] if images else {"path": "", "full_url": ""}
    canonical = f"{SITE_URL}/blog/{slug}.html"

    # Article tags para OG
    og_tags = "\n".join([f'    <meta property="article:tag" content="{t}">' for t in tags])

    # Keywords
    keywords = ", ".join(tags + ["agricultura Colombia", "AgroTech", "tecnología agrícola"])

    # Encoded URLs para compartir
    encoded_title = quote(title)
    encoded_url = quote(canonical)

    # Related posts (los existentes)
    existing_posts = _load_existing_posts()
    related_html = _generate_related_posts(existing_posts, slug)

    # WhatsApp CTA
    wa_text = quote(f"Hola, leí su artículo '{title}' y quisiera más información")

    html = f'''<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AgroTech Colombia</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="{author}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="es-CO" href="{canonical}">

    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="AgroTech Colombia">
    <meta property="og:locale" content="es_CO">
    <meta property="og:image" content="{hero_image['full_url']}">
    <meta property="og:image:alt" content="{title}">
    <meta property="article:published_time" content="{today}">
    <meta property="article:modified_time" content="{today}">
    <meta property="article:author" content="{author}">
    <meta property="article:section" content="Tecnología Agrícola">
{og_tags}

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{hero_image['full_url']}">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico?v=3">
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png?v=3">
    <link rel="icon" type="image/png" sizes="192x192" href="/images/favicon-192x192.png?v=3">
    <link rel="icon" type="image/png" sizes="512x512" href="/images/favicon-512x512.png?v=3">
    <link rel="apple-touch-icon" href="/images/apple-touch-icon.png?v=3">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#4CAF50">

    <!-- Fonts & CSS - Async loading -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
        rel="stylesheet" media="print" onload="this.media='all'">
    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"></noscript>
    <link rel="stylesheet" href="../css/landing.css">
    <link rel="stylesheet" href="../css/blog-article.css">

    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{SITE_URL}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{SITE_URL}/blog.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "{title}" }}
      ]
    }}
    </script>

    <!-- Article Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{description}",
      "image": "{hero_image['full_url']}",
      "datePublished": "{today}",
      "dateModified": "{today}",
      "author": {{
        "@type": "Person",
        "name": "{author}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "AgroTech Colombia",
        "logo": {{
          "@type": "ImageObject",
          "url": "{SITE_URL}/images/agrotech-logo.webp"
        }}
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{canonical}"
      }},
      "keywords": {json.dumps(tags + ["agricultura", "Colombia"], ensure_ascii=False)}
    }}
    </script>
</head>

<body>
    <!-- Header -->
    <header class="header" id="header">
        <div class="container">
            <nav class="nav" aria-label="Navegación principal">
                <a href="/index.html" class="nav-logo">
                    <img src="/images/agrotech-logo.webp" alt="AgroTech Colombia - Inicio" class="nav-logo-image" width="40" height="40" loading="eager">
                    <span>agrotech.</span>
                </a>
                <ul class="nav-links" id="navLinks">
                    <li><a href="/blog.html">← Volver al Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <!-- Article Header -->
        <section class="section article-header">
            <div class="container article-container">
                <span class="section-badge">Blog AgroTech</span>
                <h1>{title}</h1>
                <div class="article-meta">
                    <time datetime="{today}">{today_display}</time> · por <span style="color: var(--brand-green);">{author}</span>
                </div>
            </div>
        </section>

        <!-- Hero Image -->
        <div class="container article-container" style="margin-top: var(--spacing-md); margin-bottom: var(--spacing-md);">
            <img src="{hero_image['path']}" alt="{title}" class="blog-hero-image" width="800" height="450" loading="eager" style="width: 100%; max-width: 800px; margin: 0 auto; display: block; border-radius: 12px; aspect-ratio: 16/9; object-fit: cover;">
        </div>

        <!-- Article Content -->
        <article class="section" style="padding-top: 0;">
            <div class="container article-container">
                <div class="article-content">
                    {article_body_html}

                    <div style="text-align: center; margin-top: 60px; margin-bottom: 40px; padding: 40px; background: rgba(76, 175, 80, 0.05); border-radius: 12px;">
                        <h3 style="color: var(--brand-green); margin-bottom: 15px;">¿Le gustaría saber más sobre cómo la tecnología puede ayudarle?</h3>
                        <p style="font-size: 1.1em; margin-bottom: 30px; color: var(--text-secondary); max-width: 700px; margin-left: auto; margin-right: auto;">Permítanos mostrarle cómo los datos satelitales pueden transformar la rentabilidad de su finca. Sin compromiso.</p>
                        <a href="https://wa.me/{WHATSAPP_NUMBER}?text={wa_text}" class="neuro-button neuro-button-primary" target="_blank" rel="noopener noreferrer" aria-label="Solicitar información por WhatsApp" style="font-size: 1.1em; padding: 15px 30px;">Solicitar Información</a>
                    </div>
                </div>

                <!-- Share Buttons -->
                <div class="share-section">
                    <h3>📢 ¿Le pareció útil? Compártalo con otros agricultores</h3>
                    <p>Ayude a que más productores tomen mejores decisiones</p>
                    <div class="share-buttons">
                        <a href="https://api.whatsapp.com/send?text={encoded_title}%20%E2%80%93%20{encoded_url}" class="share-btn share-btn--whatsapp" target="_blank" rel="noopener noreferrer" aria-label="Compartir en WhatsApp">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                            WhatsApp
                        </a>
                        <a href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" class="share-btn share-btn--facebook" target="_blank" rel="noopener noreferrer" aria-label="Compartir en Facebook">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                            Facebook
                        </a>
                        <a href="https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}" class="share-btn share-btn--twitter" target="_blank" rel="noopener noreferrer" aria-label="Compartir en X (Twitter)">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                            X
                        </a>
                        <a href="https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}" class="share-btn share-btn--linkedin" target="_blank" rel="noopener noreferrer" aria-label="Compartir en LinkedIn">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                            LinkedIn
                        </a>
                        <button class="share-btn share-btn--copy" onclick="copyArticleLink(this)" aria-label="Copiar enlace del artículo">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
                            Copiar enlace
                        </button>
                    </div>
                </div>

                <!-- Related Posts -->
                <div style="margin-top: var(--spacing-xl); border-top: 1px solid rgba(255,255,255,0.1); padding-top: var(--spacing-lg);">
                    <h3 style="margin-bottom: var(--spacing-md); color: var(--text-primary);">También le puede interesar</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--spacing-md);">
                        {related_html}
                    </div>
                </div>

                <div style="margin-top: var(--spacing-xl); text-align: center;">
                    <a href="/blog.html" class="neuro-button neuro-button-primary">Volver al Blog</a>
                </div>
            </div>
        </article>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; <script>document.write(new Date().getFullYear())</script> Agrotech Digital.</p>
            </div>
        </div>
    </footer>

    <script>
    function copyArticleLink(btn) {{
        var url = window.location.href;
        var originalHTML = btn.innerHTML;
        function onCopied() {{
            btn.classList.add('copied');
            btn.innerHTML = '✓ ¡Enlace copiado!';
            setTimeout(function() {{
                btn.classList.remove('copied');
                btn.innerHTML = originalHTML;
            }}, 2500);
        }}
        if (navigator.clipboard) {{
            navigator.clipboard.writeText(url).then(onCopied);
        }} else {{
            var input = document.createElement('input');
            input.value = url;
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy');
            document.body.removeChild(input);
            onCopied();
        }}
    }}
    </script>
</body>

</html>'''

    return html


# ============================================================================
# UTILIDADES
# ============================================================================

def _load_existing_posts():
    """Carga los posts existentes del JSON."""
    try:
        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _generate_related_posts(posts, current_slug, max_count=2):
    """Genera HTML de posts relacionados (excluyendo el actual)."""
    others = [p for p in posts if p["id"] != current_slug]
    selected = random.sample(others, min(max_count, len(others))) if others else []

    html_parts = []
    for p in selected:
        html_parts.append(f'''
                        <a href="/blog/{p['id']}.html" class="related-card">
                            <h4 style="color: var(--brand-green); font-size: 1.1rem; margin-bottom: var(--spacing-xs);">{p['title']}</h4>
                            <p style="color: var(--text-secondary); font-size: 0.9rem;">{p['summary'][:120]}...</p>
                        </a>''')

    return "\n".join(html_parts)


def _update_posts_json(article_data, hero_image_path):
    """Agrega el nuevo artículo al posts.json."""
    posts = _load_existing_posts()

    new_post = {
        "id": article_data["slug"],
        "title": article_data["title"],
        "summary": article_data["description"],
        "content": "",  # Se deja vacío — el HTML completo está en el archivo
        "date": date.today().isoformat(),
        "author": article_data["author"],
        "image": hero_image_path.lstrip("/"),
        "tags": article_data["tags"],
    }

    # Insertar al inicio (más reciente primero)
    posts.insert(0, new_post)

    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"  ✅ posts.json actualizado ({len(posts)} artículos)")


def parse_content_sections(content_text):
    """
    Parsea el contenido del artículo.
    Espera formato:

    INTRO: Párrafo introductorio...

    ## Título de sección 1
    Párrafo de contenido...
    - Punto de lista
    - Otro punto

    ## Título de sección 2
    Más contenido...
    """
    sections = []
    current_section = None
    lines = content_text.strip().split("\n")

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## "):
            # Guardar sección anterior
            if current_section:
                sections.append(current_section)

            title = stripped[3:].strip()
            current_section = {
                "title": title,
                "is_h2": True,
                "lines": [],
            }
        elif stripped.startswith("INTRO:"):
            intro_text = stripped[6:].strip()
            sections.append({
                "title": "",
                "is_h2": False,
                "html": f'<p class="blog-intro">{intro_text}</p>',
                "lines": [],
            })
        else:
            if current_section is None:
                # Texto antes de cualquier sección — tratar como intro
                if stripped:
                    sections.append({
                        "title": "",
                        "is_h2": False,
                        "html": f"<p>{stripped}</p>",
                        "lines": [],
                    })
            else:
                if stripped:
                    current_section["lines"].append(stripped)

    # Guardar última sección
    if current_section:
        sections.append(current_section)

    # Convertir líneas a HTML
    for section in sections:
        if "html" not in section or not section.get("html"):
            html_parts = []
            in_list = False
            for line in section.get("lines", []):
                if line.startswith("- ") or line.startswith("* "):
                    if not in_list:
                        html_parts.append("<ul>")
                        in_list = True
                    item = line[2:].strip()
                    # Soportar negritas con **texto**
                    item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                    html_parts.append(f"<li>{item}</li>")
                else:
                    if in_list:
                        html_parts.append("</ul>")
                        in_list = False
                    # Soportar negritas con **texto**
                    processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                    html_parts.append(f"<p>{processed}</p>")
            if in_list:
                html_parts.append("</ul>")
            section["html"] = "\n                    ".join(html_parts)

    return sections


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def _build_article(slug, title, description, author, tags, search_keywords, content_text):
    """
    Lógica central de generación de artículo.
    Recibe todos los datos ya procesados y genera el artículo completo.
    """

    # Verificar que no exista
    output_path = os.path.join(BLOG_DIR, f"{slug}.html")
    if os.path.exists(output_path):
        print(f"  ❌ Ya existe: blog/{slug}.html")
        sys.exit(1)

    # Parsear contenido
    sections = parse_content_sections(content_text)

    if len(sections) < 2:
        print("  ⚠️  Se necesitan al menos 2 secciones (intro + una sección H2)")
        sys.exit(1)

    print(f"\n  📝 Secciones detectadas: {len(sections)}")
    for s in sections:
        if s.get("is_h2"):
            print(f"     - H2: {s['title']}")
        else:
            print(f"     - INTRO")

    # --- Buscar y descargar imágenes ---
    if not search_keywords:
        search_keywords = " ".join(tags[:3]) + " agriculture"

    print(f"\n🖼️  BUSCANDO IMÁGENES EN PEXELS ({search_keywords})...\n")
    photos = search_pexels(search_keywords, count=4)

    images = []
    for i, photo in enumerate(photos):
        img = download_and_optimize_image(photo, slug, i)
        if img:
            # Asignar caption contextual
            if i == 0:
                img["caption"] = ""  # Hero no necesita caption visible
            else:
                # Usar el título de la sección correspondiente como contexto
                h2_sections = [s for s in sections if s.get("is_h2")]
                if i - 1 < len(h2_sections):
                    img["caption"] = f"{h2_sections[i-1]['title']} — Foto: {photo['photographer']}"
                else:
                    img["caption"] = f"Foto por {photo['photographer']} en Pexels"
            images.append(img)

    if not images:
        print("\n  ❌ No se pudieron descargar imágenes. Abortando.")
        sys.exit(1)

    # --- Seleccionar template ---
    template_idx = random.randint(0, len(TEMPLATES) - 1)
    template_fn = TEMPLATES[template_idx]
    print(f"\n🎨 Template seleccionado: {TEMPLATE_NAMES[template_idx]}")

    # --- Generar body del artículo con el template ---
    article_body_html = template_fn(sections, images)

    # --- Generar HTML completo ---
    article_data = {
        "slug": slug,
        "title": title,
        "description": description,
        "author": author,
        "tags": tags,
    }

    full_html = generate_html(article_data, images, article_body_html)

    # --- Guardar archivo ---
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"\n  ✅ Artículo generado: blog/{slug}.html")

    # --- Actualizar posts.json ---
    hero_path = images[0]["path"] if images else ""
    _update_posts_json(article_data, hero_path)

    # --- Resumen final ---
    size_kb = os.path.getsize(output_path) / 1024
    print("\n" + "=" * 60)
    print("  ✅ ¡ARTÍCULO GENERADO EXITOSAMENTE!")
    print("=" * 60)
    print(f"  📄 Archivo:    blog/{slug}.html ({size_kb:.1f} KB)")
    print(f"  🖼️  Imágenes:  {len(images)} WebP en images/blog/")
    print(f"  🎨 Template:   {TEMPLATE_NAMES[template_idx]}")
    print(f"  📊 posts.json: Actualizado")
    print(f"\n  👉 Próximos pasos:")
    print(f"     1. Revisa el artículo en el navegador")
    print(f"     2. git add -A && git commit -m 'blog: {slug}'")
    print(f"     3. git push origin main")
    print(f"     4. Solicita indexación en Google Search Console")
    print(f"     5. URL: {SITE_URL}/blog/{slug}.html")
    print("=" * 60 + "\n")


def main_interactive():
    """Modo interactivo: pide datos por consola."""
    print("\n📝 DATOS DEL ARTÍCULO\n")

    slug = input("  Slug (ej: riego-eficiente-colombia): ").strip()
    if not slug:
        print("  ❌ Slug es obligatorio")
        sys.exit(1)

    title = input("  Título completo: ").strip()
    description = input("  Meta description (max 160 chars): ").strip()
    author = input("  Autor (ej: Ing. Sofía Martínez): ").strip() or "Equipo AgroTech"
    tags_input = input("  Tags separados por coma (ej: Tecnología, Riego, Colombia): ").strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    search_keywords = input("  Palabras clave para buscar imágenes (ej: riego campo cultivo): ").strip()

    print("\n📝 CONTENIDO DEL ARTÍCULO")
    print("  Escribe el contenido. Formato:")
    print("    INTRO: Párrafo introductorio...")
    print("    ## Título de sección")
    print("    Párrafo de texto...")
    print("    - Punto de lista")
    print("  ")
    print("  Cuando termines, escribe una línea con solo 'FIN'\n")

    content_lines = []
    while True:
        line = input()
        if line.strip() == "FIN":
            break
        content_lines.append(line)

    content_text = "\n".join(content_lines)

    _build_article(slug, title, description, author, tags, search_keywords, content_text)


def main_json(json_path):
    """
    Modo JSON: lee datos de un archivo JSON.

    Formato esperado del JSON:
    {
        "slug": "riego-eficiente-colombia",
        "title": "Riego Eficiente en Colombia...",
        "description": "Meta description...",
        "author": "Ing. Sofía Martínez",
        "tags": ["Riego", "Tecnología"],
        "search_keywords": "riego campo cultivo tropical",
        "content": "INTRO: Texto intro...\\n\\n## Sección 1\\nContenido...\\n\\n## Sección 2\\nMás contenido..."
    }
    """
    if not os.path.exists(json_path):
        print(f"  ❌ Archivo no encontrado: {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required = ["slug", "title", "description", "content"]
    for field in required:
        if field not in data:
            print(f"  ❌ Campo obligatorio faltante en JSON: '{field}'")
            sys.exit(1)

    slug = data["slug"]
    title = data["title"]
    description = data["description"]
    author = data.get("author", "Equipo AgroTech")
    tags = data.get("tags", ["Agricultura", "Tecnología"])
    search_keywords = data.get("search_keywords", "")
    content_text = data["content"]

    print(f"\n  📂 Cargado desde: {json_path}")

    _build_article(slug, title, description, author, tags, search_keywords, content_text)


def main():
    print("\n" + "=" * 60)
    print("  🌱 AgroTech Blog Article Generator")
    print("=" * 60)

    # Modo JSON: python generate_article.py --json articulo.json
    if len(sys.argv) >= 3 and sys.argv[1] == "--json":
        main_json(sys.argv[2])
    else:
        main_interactive()


if __name__ == "__main__":
    main()
