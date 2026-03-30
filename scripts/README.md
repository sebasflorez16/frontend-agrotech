# 🌱 AgroTech Blog Article Generator

## Descripción

Sistema automatizado para generar artículos del blog de AgroTech Colombia con:

- **Imágenes de Pexels** (contexto latino/agrícola), descargadas y optimizadas a WebP
- **4 plantillas visuales** seleccionadas aleatoriamente para variedad
- **SEO máximo**: Schema.org, Open Graph, Twitter Card, canonical, breadcrumbs
- **Componentes sociales**: botones de compartir (WhatsApp, Facebook, X, LinkedIn, copiar link)
- **CTA de WhatsApp** integrado al final
- **Posts relacionados** automáticos desde `posts.json`
- **Hero image** visible al inicio del artículo
- **Actualización automática** de `posts.json`

## Requisitos

```bash
pip install requests Pillow
brew install webp  # para cwebp (macOS)
```

## Uso

### Modo 1: Interactivo (por consola)

```bash
cd frontend-agrotech
python3 scripts/generate_article.py
```

El script te pedirá:
1. **Slug** (ej: `riego-eficiente-colombia`)
2. **Título** completo
3. **Meta description** (max 160 caracteres)
4. **Autor** (ej: `Ing. Sofía Martínez`)
5. **Tags** separados por coma
6. **Palabras clave** para buscar imágenes
7. **Contenido** del artículo (escribir y terminar con `FIN`)

### Modo 2: Desde archivo JSON (automatizado)

```bash
cd frontend-agrotech
python3 scripts/generate_article.py --json scripts/ejemplo-articulo.json
```

#### Formato del JSON:

```json
{
  "slug": "riego-eficiente-colombia",
  "title": "Título completo del artículo",
  "description": "Meta description para SEO (max 160 chars)",
  "author": "Ing. Sofía Martínez",
  "tags": ["Riego", "Tecnología", "Colombia"],
  "search_keywords": "riego campo cultivo tropical",
  "content": "INTRO: Párrafo introductorio...\n\n## Título sección 1\n\nContenido...\n\n## Título sección 2\n\nMás contenido..."
}
```

#### Campos obligatorios:
- `slug` — URL del artículo (sin espacios, con guiones)
- `title` — Título SEO completo
- `description` — Meta description
- `content` — Contenido en formato markdown simple

#### Campos opcionales:
- `author` — Por defecto: "Equipo AgroTech"
- `tags` — Por defecto: ["Agricultura", "Tecnología"]
- `search_keywords` — Si vacío, se generan desde los tags

## Formato del contenido

```
INTRO: El párrafo introductorio se muestra destacado al inicio...

## Título de la primera sección

Párrafos de texto normal van así, uno por línea.

Otro párrafo separado por una línea en blanco.

- **Punto de lista en negrita:** con descripción
- Otro punto de lista
- Más puntos

## Título de la segunda sección

Más contenido. Puedes usar **negritas** con doble asterisco.

## Título de la tercera sección

Y así sucesivamente. Se recomienda tener entre 4-6 secciones H2.
```

## Plantillas visuales

El generador selecciona aleatoriamente entre 4 plantillas:

| Template | Estructura | Descripción |
|----------|-----------|-------------|
| **A** | texto-img / img-texto / texto-img | Alternado izquierda/derecha |
| **B** | img-derecha / img-derecha / img-fullwidth | Derecha + full-width |
| **C** | img-izquierda / fullwidth / img-derecha | Mixto variado |
| **D** | img-derecha (1ª sección) + img-izquierda (última) | Minimalista |

## ¿Qué genera?

Cuando ejecutas el script, se crean:

```
blog/
  └── {slug}.html          ← Artículo HTML completo (SEO, schema, social)
images/blog/
  ├── {slug}-1.webp         ← Hero image (eager loading)
  ├── {slug}-2.webp         ← Imagen sección 1 (lazy)
  ├── {slug}-3.webp         ← Imagen sección 2 (lazy)
  └── {slug}-4.webp         ← Imagen sección 3 (lazy)
data/
  └── posts.json            ← Actualizado con el nuevo artículo
```

## Después de generar

```bash
# 1. Revisar en navegador
open blog/{slug}.html

# 2. Commit y deploy
git add -A
git commit -m "blog: {slug}"
git push origin main

# 3. Solicitar indexación en Google Search Console
#    URL: https://agrotechcolombia.com/blog/{slug}.html
```

## Ejemplo completo de flujo

```bash
# Crear el JSON del nuevo artículo
cat > scripts/mi-articulo.json << 'EOF'
{
  "slug": "fertilizacion-variable-cafe",
  "title": "Fertilización Variable en Café: La Revolución Silenciosa del Agro Colombiano",
  "description": "Aprenda cómo la fertilización variable basada en datos satelitales puede ahorrarle hasta un 30% en insumos y mejorar la calidad de su café.",
  "author": "Ing. Carlos Rodríguez",
  "tags": ["Fertilización", "Café", "Tecnología", "Colombia"],
  "search_keywords": "coffee plantation colombia fertilizer",
  "content": "INTRO: La fertilización es uno de los costos más altos...\n\n## El problema de fertilizar a ciegas\n\nContenido...\n\n## La solución satelital\n\nMás contenido..."
}
EOF

# Generar
python3 scripts/generate_article.py --json scripts/mi-articulo.json

# Deploy
git add -A && git commit -m "blog: fertilizacion-variable-cafe" && git push
```

## Notas técnicas

- Las imágenes se descargan de Pexels (API key ya configurada)
- Se redimensionan a 500px de ancho máximo
- Se convierten a WebP con calidad 75 (~20-40 KB por imagen)
- Hero image usa `loading="eager"`, las demás `loading="lazy"`
- El HTML incluye Schema.org Article + BreadcrumbList
- Compatible con el tema dark del sitio
- Los botones de compartir incluyen WhatsApp, Facebook, X, LinkedIn y copiar enlace
