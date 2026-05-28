---
name: AgroTech Colombia
description: Historial satelital del lote, en español de Colombia, para el agricultor mediano-grande.
colors:
  brand-green: "#4CAF50"
  brand-green-dark: "#388E3C"
  brand-green-light: "#66BB6A"
  brand-orange: "#FF6F00"
  brand-orange-dark: "#E65100"
  brand-orange-light: "#FF8F00"
  dark-bg: "#1a1a1a"
  dark-bg-secondary: "#242424"
  dark-bg-tertiary: "#2d2d2d"
  dark-card: "#212121"
  dark-card-hover: "#2a2a2a"
  text-primary: "#ffffff"
  text-secondary: "#b0b0b0"
  text-muted: "#808080"
  accent-success: "#4CAF50"
  accent-warning: "#FF9800"
  accent-error: "#F44336"
  accent-info: "#2196F3"
  manifest-bg: "#0a0e13"
  legacy-neuro-green: "#2E8B57"
  legacy-neuro-orange: "#FF7A00"
  legacy-mobile-green: "#35B835"
typography:
  display:
    fontFamily: "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "clamp(2.5rem, 5vw, 4rem)"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "normal"
  headline:
    fontFamily: "Inter, 'Segoe UI', sans-serif"
    fontSize: "clamp(2rem, 4vw, 3rem)"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "Inter, 'Segoe UI', sans-serif"
    fontSize: "clamp(1.5rem, 3vw, 2rem)"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: "Inter, 'Segoe UI', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  body-lg-editorial:
    fontFamily: "Inter, 'Segoe UI', sans-serif"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.9
  label:
    fontFamily: "Inter, 'Segoe UI', sans-serif"
    fontSize: "0.85rem"
    fontWeight: 600
    letterSpacing: "0.05em"
rounded:
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  full: "50%"
spacing:
  xs: "0.5rem"
  sm: "1rem"
  md: "2rem"
  lg: "3rem"
  xl: "5rem"
components:
  button-primary:
    backgroundColor: "{colors.brand-green}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "1rem 2rem"
  button-primary-hover:
    backgroundColor: "{colors.brand-green-light}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "1rem 2rem"
  button-secondary:
    backgroundColor: "{colors.brand-orange}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "1rem 2rem"
  button-secondary-hover:
    backgroundColor: "{colors.brand-orange-light}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "1rem 2rem"
  card-neuro:
    backgroundColor: "{colors.dark-card}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
  card-pricing-recommended:
    backgroundColor: "{colors.dark-card}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
  input:
    backgroundColor: "{colors.dark-card}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  badge-section:
    backgroundColor: "{colors.dark-card}"
    textColor: "{colors.brand-green}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs} {spacing.sm}"
  bullet-check:
    textColor: "{colors.brand-green}"
    padding: "0"
---

# Design System: AgroTech Colombia

## 1. Overview

**Creative North Star: "El Cuaderno de Campo Satelital"**

AgroTech Colombia diseña como una **revista técnica agro impresa fundida con un cuaderno de campo del agrónomo**: tipografía cómoda, datos defendibles, fotografía honesta del campo colombiano, mapas NDVI con escala cromática técnica. La estética debe sentirse hecha por alguien que entiende de cultivos antes que de productos digitales. Trust-first absoluto: el primer scroll transmite solidez técnica y honestidad, no entusiasmo de pitch deck.

Este sistema **rechaza explícitamente**: Linear/Notion/Vercel/Fluence dark-purple SaaS, glassmorphism decorativo, gradient text, hero centrado sobre dark mesh, neomorphism iOS-2020, Material Design defaults, Awwwards scroll-jacking y agro-cliché verde fosforescente con tractor stock. Si dudamos entre "más diseñado" y "más legible", gana legible. Si dudamos entre "más rápido en 4G rural" y "más bonito en MacBook", gana 4G rural.

**Estado actual:** sistema dark neuromórfico Material-derivado, en proceso de migración hacia editorial trust-first. Documento generado el 28-may-2026 sobre la base de `PRODUCT.md` v1, después de los quick-wins 1 a 5 del audit. Tokens normativos viven en el frontmatter; la prosa es contexto de aplicación.

**Key Characteristics:**
- Voz: honesta, mecánica, llana, precisa, agro-tech.
- Audiencia primaria: agricultor 40-65a en Android gama media bajo 4G rural.
- Idioma: español-CO formal ("usted"), sin excepciones públicas.
- WhatsApp es producto, no soporte.
- LCP objetivo <2.5s en 4G simulado. Cualquier animación que cueste eso, se corta.
- `prefers-reduced-motion` respetado por contrato.

## 2. Colors

Paleta Material-derivada en transición hacia OKLCH tintado a la marca. Convive con **tres paletas legacy** que deben consolidarse (ver §sidecar deuda). Los HEX del frontmatter son la fuente de verdad actual; las equivalencias OKLCH listadas abajo son el destino de la próxima pasada `/impeccable colorize`.

### Primary
- **Verde Marca** (`#4CAF50` aprox `oklch(72% 0.17 145)`): ancla principal. Aparece en CTAs primarios, links activos, iconos de éxito, badges de plan, headings de sección H2 de artículos, focus ring. Usar <25% del viewport por encima del fold; nunca como gradient text.
- **Verde Oscuro** (`#388E3C` aprox `oklch(60% 0.16 145)`): hover y bordes activos de elementos verdes; segundo paso de gradient en botones.
- **Verde Claro** (`#66BB6A` aprox `oklch(78% 0.14 145)`): hover de links, segundo stop en gradients de pricing recomendado, microacento en illustrations.

### Secondary
- **Naranja Marca** (`#FF6F00` aprox `oklch(70% 0.20 50)`): acento de cosecha, badges de alerta moderada, segundo CTA del hero, headings H3 de artículos. Compite con el verde, limitar a <10% del viewport.
- **Naranja Oscuro** (`#E65100` aprox `oklch(58% 0.18 50)`): hover de naranja primario.
- **Naranja Claro** (`#FF8F00` aprox `oklch(75% 0.18 60)`): hover suave, hints visuales.

### Neutral (dark, untinted hoy. Destino: tintado verde chroma 0.005)
- **Page background** (`#1a1a1a`, destino `oklch(20% 0.005 145)`): fondo principal de landing y blog hub.
- **Surface secondary** (`#242424`): bandas alternadas, sub-secciones.
- **Surface tertiary** (`#2d2d2d`): sub-sub-secciones (poco uso).
- **Card** (`#212121`): cards neumórficas, article-content wrap.
- **Card hover** (`#2a2a2a`): estado hover de cards.
- **Text primary** (`#ffffff`, destino `oklch(98% 0.003 145)`): titulares y body en surfaces oscuras. **Bandera: `#fff` puro está vetado por skill, migrar.**
- **Text secondary** (`#b0b0b0` aprox `oklch(75% 0 0)`): párrafos largos, meta, captions.
- **Text muted** (`#808080`): timestamps, microcopy auxiliar.

### Semantic
- **Success** (`#4CAF50`): coincide con verde marca (potencial colisión semántica, `/colorize` debe separarlos).
- **Warning** (`#FF9800` aprox `oklch(76% 0.17 60)`): badges informativos amarillo-cálidos, fallos de contraste detectados en audit.
- **Error** (`#F44336` aprox `oklch(64% 0.21 27)`): errores de formulario, alertas críticas.
- **Info** (`#2196F3` aprox `oklch(65% 0.16 245)`): hints, reservado para NDMI/humedad en mapas científicos.

### Color strategy per surface
- **Landing (`index.html`):** Committed dark. Verde marca carga la identidad, naranja como segundo acento limitado. Estrategia actual heredada; viable si se ejecuta con restraint post quick-wins.
- **Blog hub + artículos:** Editorial sobre dark. Defectuoso para long-read en celular bajo sol. **Destino recomendado:** virar a light editorial (paper warm `oklch(98% 0.005 90)`), texto tinted verde-oscuro, acento marca solo en links y bullets.
- **Dashboard (`product` register, fuera de scope):** Restrained. Neutros tintados + un acento (verde) en datos relevantes.

### Contrast matrix (WCAG AA, fondo `#1a1a1a` salvo nota)
| Foreground | Background | Ratio | Estado |
|---|---|---|---|
| `#ffffff` text-primary | `#1a1a1a` | 17.4:1 | AAA |
| `#b0b0b0` text-secondary | `#1a1a1a` | 7.7:1 | AAA |
| `#b0b0b0` text-secondary | `#242424` | 6.9:1 | AAA |
| `#b0b0b0` text-secondary | `#212121` card | 7.5:1 | AAA |
| `#808080` text-muted | `#1a1a1a` | 4.9:1 | AA (body), Fail (small) |
| `#4CAF50` brand-green | `#1a1a1a` | 7.5:1 | AAA (links OK) |
| `#FF9800` warning | `#1a1a1a` | 7.2:1 | AAA |
| `#FF9800` warning | `rgba(255,152,0,.15)` badge | ~3.1:1 | **FAIL para body 0.8rem** |
| `#66BB6A` brand-green-light | `#212121` | 6.6:1 | AAA |

### Named Rules
**The One Voice Rule.** El verde marca aparece en menos del 25% del viewport. El naranja en menos del 10%. Si conviven con info-blue del mismo elemento, perdimos: rediseñar la jerarquía cromática.

**The No Pure Black/White Rule.** `#000` y `#fff` quedan prohibidos por contrato. Cuando migremos a OKLCH, todos los neutros llevan chroma 0.003 a 0.01 hacia hue 145 (verde marca).

**The Manifest-Match Rule.** `site.webmanifest` declara `background_color:#0a0e13` mientras el CSS usa `#1a1a1a`. Próxima `/colorize` debe alinearlos a un único token.

## 3. Typography

**Display Font:** `Inter` (con fallback `'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif`)
**Body Font:** `Inter` (idéntico al display, **bandera roja**)
**Label/Mono Font:** sin definir.

**Character:** sistema mono-familia. `Inter` cumple su trabajo neutralmente pero no tiene carácter editorial. La skill `design-taste-frontend` lista `Inter` en el reflex-reject set; sin una display de contrapunto, el sitio se lee técnicamente correcto y visualmente genérico. La próxima `/impeccable typeset` debe agregar **una display de carácter** (candidatos serios: GT America Mono / Söhne Mono para metadata, o un serif editorial como Source Serif 4 para H1 del blog) y **una mono real** para cifras y badges técnicos.

### Hierarchy
- **Display H1** (800, `clamp(2.5rem, 5vw, 4rem)`, line-height 1.2): hero del landing, título de hub blog, headline del artículo. Hasta quick-win 1 llevaba gradient text; ahora es color sólido.
- **Headline H2** (700, `clamp(2rem, 4vw, 3rem)`, 1.2): inicio de sección landing y sección de artículo. En artículos viste verde marca por defecto, debe migrar a color de texto principal (mayor jerarquía por escala, no por color).
- **Title H3** (700, `clamp(1.5rem, 3vw, 2rem)`, 1.3): sub-secciones, títulos de card.
- **Body** (400, `1rem`, 1.6): párrafos del landing, copy de pricing, footer.
- **Body large editorial** (400, `1.15rem`, **1.9**): cuerpo del artículo. La line-height 1.9 es excesiva incluso para long-read editorial. Destino: 1.6.
- **Label** (600, `0.85rem`, letter-spacing 0.05em): badges de sección, plan-tags, metadata.

### Reading column
Artículos sirven hoy con `max-width:100%` dentro de `.article-container` (1200px). Para editorial real: **65 a 75ch** (aprox 700px) sobre fondo claro. Fuera de ese rango la lectura de 1.700 palabras se vuelve hostil en pantalla amplia.

### Named Rules
**The Solid Heading Rule.** H1 a H4 son color sólido. Nunca `background-clip:text` con gradiente. Énfasis por peso y tamaño únicamente.

**The Editorial Column Rule.** En `/blog/*` el `<article>` no excede 70ch. Imágenes y tablas pueden romper al bleed full, el texto no.

**The Two-Family Minimum (destino).** Cuerpo conserva sans neutra. H1 y H2 reciben una display con personalidad. Cifras y metadata van en mono. Sin estas tres familias, el sitio se ve hecho a la carrera.

## 4. Elevation

Sistema **neuromórfico dark** con doble sombra paralela (light + dark) que simula relieve 3D. Funciona estéticamente pero comunica más "estilo iOS 2020" que "revista técnica agro". La próxima `/impeccable distill` debe **bajar el peso de las sombras a la mitad** (de `16px` blur a `6 a 8px`) o reemplazarlas por tonal layering (cambios sutiles de luminosidad entre superficies adyacentes).

### Shadow Vocabulary
- **Card resting** (`8px 8px 16px rgba(0,0,0,.5), -8px -8px 16px rgba(255,255,255,.05)`): cards neumórficas, article-content wrap.
- **Card hover** (`12px 12px 24px rgba(0,0,0,.5), -12px -12px 24px rgba(255,255,255,.05)`): hover de cards.
- **Button resting** (`6px 6px 12px rgba(0,0,0,.5), -6px -6px 12px rgba(255,255,255,.05)`): botones primarios y secundarios.
- **Button pressed (inset)** (`inset 6px 6px 12px rgba(0,0,0,.3), inset -6px -6px 12px rgba(255,255,255,.03)`): estado active.
- **Input sunken (inset)** (`inset 8px 8px 16px rgba(0,0,0,.3), inset -8px -8px 16px rgba(255,255,255,.03)`): campos de formulario.

### Border Radius scale
`8px -> 16px -> 24px -> 32px -> 50%`. La escala es ancha; el uso real en cards y botones es `24px` (radius-lg), exceso para B2B trust-first. Destino editorial: `4 a 8px` en superficies de lectura, `12 a 16px` en CTAs, `999px` solo en pills.

### Named Rules
**The Half-Shadow Rule (destino).** Reducir todos los blurs neuromórficos a 50%. Mantener el sistema dual pero más sutil.

**The Editorial Has No Shadow Rule.** El `.article-content` no debe llevar sombra. Texto largo sobre card flotante distrae del flujo de lectura.

## 5. Components

### Buttons
- **Shape:** radius-lg (24px). Padding 1rem 2rem.
- **Primary (`.btn-cta`, `.neuro-button` con gradient verde):** `linear-gradient(135deg, brand-green, brand-green-dark)` + shadow neuro. Hover invierte gradient hacia más claro. Usar para CTAs comerciales: "Ver demo", "Solicitar informe", "Hablar por WhatsApp".
- **Secondary (gradient naranja):** mismo patrón con naranja. Para acción secundaria del hero (p. ej. "Ver ejemplo de informe").
- **Ghost (no implementado consistentemente):** pendiente, útil para "Cancelar", "Más información".
- **Estados:** resting, hover (sombra +50%, gradient invertido), active (inset), focus (pendiente, definir focus ring visible). Disabled (pendiente).
- **Bandera:** los gradients suaves en botón son aceptables porque sirven a affordance 3D, no son decoración text-clip.

### Cards
- **`.neuro-card` (genérica):** background `dark-card`, radius-lg, padding md, doble sombra. Aparece en features, pricing, gallery, blog cards, FAQ: uso excesivo. La próxima `/distill` debe diferenciar al menos 2 variantes: card-data (más compacta, padding sm) y card-feature (presentación, padding lg).
- **`.pricing-card.recommended`:** mismo container con borde verde 1px + label "RECOMENDADO" (no `estrella` desde quick-win 5). Sin `transform:scale(1.03)` post-fix.
- **`.blog-card`:** hereda `.neuro-card` con `font-size:1.25rem` en título. Audit detectó que es **demasiado pequeño** para hub editorial; destino 1.6 a 2rem para feature y 1.35rem para secundarios.
- **Anti-rule:** prohibido anidar `.neuro-card` dentro de `.neuro-card`. Si una card necesita sub-zonas, usar separadores tipográficos (border-top sutil, divisores `--text-muted`).

### Badges
- **`.section-badge`:** label uppercase 0.85rem letter-spacing 0.05em sobre fondo `dark-card` o `transparent`, color `brand-green`. Eyebrow de sección. **Anti-rule (de audit):** el badge no debe repetir las primeras palabras del H1 siguiente.
- **`.plan-badge` "EMPRESARIAL":** naranja `#FF9800` sobre `rgba(255,152,0,.15)`: **contraste fallido** detectado en audit. Fix pendiente.
- **`.pricing-badge "RECOMENDADO"`:** texto plano post quick-win 5, sin emoji estrella.

### Inputs
- **Shape:** radius-md (16px). Padding sm md.
- **Style:** sunken inset shadows sobre `dark-card`. Color de texto `text-primary`.
- **Estados:** focus (pendiente, debe agregar ring verde 2px offset 2px), error (pendiente), disabled (pendiente).
- **Bandera:** estados de formulario incompletos. `/impeccable harden` debe cerrar el set.

### Navigation
- **`.header`:** sticky top con `backdrop-filter:blur(20px)` sobre `dark-bg`, único uso justificable de glass: navegación. Padding sm vertical.
- **`.nav-burger`:** 3 spans 25x3px, gap 5px. Audit: área tocable borderline 40px, target 44x44. Fix pendiente.
- **Active state:** sin indicador claro de sección activa en scroll. Definir en `/impeccable layout`.

### Pricing
- **Layout:** 3 cards `repeat(auto-fit, minmax(...))`. Recommended con borde verde 1px y `RECOMENDADO` label superior.
- **Bullet `.check`:** `<span class="check" aria-hidden="true">›</span>`, color brand-green, font-weight 700, margin-right 0.5rem, width 1ch. Reemplazó los emoji check en quick-win 5.

### Blog editorial
- **`.blog-intro`:** font-size 1.35rem, weight 500, color text-secondary. Sin border-left desde quick-win 3.
- **`.blog-pullquote`:** italic + color brand-green + comilla decorativa absolute. **Pendiente refactor por `/impeccable typeset`**, el patrón Medium-AI clásico debe migrarse a comilla pequeña tipográfica, sin italic, color de cuerpo bold.
- **`.article-content`:** wrap completo con neuro card. **Pendiente eliminación** por `/distill` (Impeccable: "don't wrap everything in a container").
- **`.blog-row`:** layout text+image 60/40, alterna con `.reverse`. **Anti-rule (Taste Zigzag Cap):** máximo 2 zigzags consecutivos.

### WhatsApp CTA / Footer
- Botones de WhatsApp viven en CTAs principales y burbuja sticky (pendiente verificar). Tono y color: verde-WhatsApp `#25D366` puede colisionar con brand-green: decisión: usar brand-green para no introducir cuarto color.

### Named Rules
**The No Card-in-Card Rule.** Si vas a anidar `.neuro-card`, no anides. Usa tipografía o divisores.

**The Editorial No-Wrap Rule.** En `/blog/*`, el `<article>` fluye sobre el background de página directamente.

**The Pricing No-Star Rule.** Plan recomendado se destaca por borde y label tipográfico, no por estrella amarilla ni `transform:scale`.

## 6. Do's and Don'ts

### Do
- Usar `var(--brand-green)` para acción primaria y links activos. Nada más le compete.
- Definir cada cifra con su unidad: `200 ha`, `$1.100.000 COP`, `+60% vs promedio dep.`, `1 a 3 días`.
- Citar fuente al lado de cada estadística pública: Sentinel-2, IDEAM, FNA, Fedearroz, DANE.
- Usar tap targets `min-width:44px; min-height:44px` para todo control en mobile.
- Self-host de Inter (woff2 subset latin) en próxima pasada: eliminar dependencia Google Fonts CDN.
- Respetar `prefers-reduced-motion: reduce` desactivando todas las animaciones que no sean entrada inicial.
- Escribir copy real, B2B agro CO, tono "usted", verbos de campo.
- Mantener `<time datetime="YYYY-MM-DD">` en posts y meta.
- Servir imágenes en `.webp` con `width` y `height` explícitos y `loading="lazy"` para below-the-fold.

### Don't
- **No** `background-clip:text` con gradient en ningún heading. Nunca.
- **No** `border-left: 4px solid var(--brand-green)` como acento de callout/intro. Side-stripe vetado.
- **No** `#000` ni `#fff` puros. Tintar neutros hacia hue 145.
- **No** hero centrado sobre dark mesh con gradient blur radial.
- **No** glassmorphism fuera del header sticky.
- **No** animaciones `infinite` sin propósito (cursor-glow, partículas, shimmer perpetuo, gradient border): cortadas en quick-win 2, no las reintroduzcas.
- **No** em-dashes en UI copy. Tampoco doble guion ASCII. Usar punto, coma, dos puntos, paréntesis.
- **No** emojis decorativos en pricing, headings de artículo o body. Excepción: telefono, sobre, globo en footer (icono funcional).
- **No** repetir las primeras 2 palabras del H1 en el eyebrow del mismo bloque.
- **No** stats grandes en hero ("3000+ / 3 años / 98%"). Si la cifra importa, contextualizarla en sección dedicada con metodología.
- **No** anidar `.neuro-card` dentro de `.neuro-card`.
- **No** 4+ secciones consecutivas con patrón `.blog-row` zigzag.
- **No** "98% precisión" sin metodología, "70% progreso" sin fuente. Fake-precise está vetado.
- **No** mezclar idiomas en `aria-label` (p. ej. "Toggle menu" en sitio español).
- **No** `<div onclick>` para botones. Usar `<button type="button">`.

---

## Sidecar: Deuda técnica de diseño priorizada

Estos no caben en el frontmatter de Stitch (limitado a 8 props por componente) pero son críticos para la próxima fase.

### P0 - Bloqueantes para `/impeccable colorize`
1. **Tres paletas coexisten.** `landing.css` (Material green `#4CAF50`), `agrotech-neomorphic.css` (SeaGreen `#2E8B57`, Orange `#FF7A00`), `mobile-clean-redesign.css` (bright `#35B835`). Decisión requerida: cuál es la marca real, las otras se eliminan.
2. **`mobile-clean-redesign.css` rompe el theme-lock.** 944 líneas con `!important` que invierten dark a light + cambian `Inter` a `Poppins` solo en `<= 768px`. Eliminar por contrato.
3. **`site.webmanifest theme_color/background_color` mismatch.** `#4CAF50` y `#0a0e13` no corresponden a tokens activos.
4. **`#fff` y `#000` puros prohibidos en docs.** Migrar a OKLCH tintado.

### P1 - Bloqueantes para `/impeccable typeset`
5. **Inter como única familia.** Sumar display (carácter editorial) + mono (cifras y metadata).
6. **Heading colors verde/naranja en `.article-content h2/h3`.** Migrar a color de texto principal; jerarquía por escala y peso, no color rainbow.
7. **`.blog-pullquote` patrón Medium-AI.** Refactor a tipografía editorial sobria.
8. **Line-height `1.9` en cuerpo editorial.** Bajar a 1.6.

### P1 - Bloqueantes para `/impeccable distill` blog
9. **`.article-content` envuelto en `.neuro-card`.** Quitar wrap, fluir sobre background de página claro.
10. **`.article-header` con radial-gradient verde.** Eliminar; padding sobrio + foto hero.
11. **`max-width:100%` en article body.** Limitar a 70ch.

### P2 - Mejoras de superficie
12. **Emojis funcionales fuera de footer.** Sustituir por icon set SVG (Phosphor/Tabler, stroke 1.5px, 24x24). Excepción mantenida: telefono, sobre, globo en footer.
13. **Shadows neuromórficos al 50%.** O migrar a tonal layering.
14. **Estados de formulario incompletos.** `/harden` debe cerrar focus, error, disabled, loading.
15. **GSAP CDN sin `defer`.** Decidir si seguimos con GSAP o migramos a CSS scroll-driven animations.

### Roadmap de aplicación recomendado
1. `/impeccable colorize` -> emitir paleta OKLCH definitiva, alinear webmanifest, eliminar legacy.
2. `/impeccable typeset` -> sumar display + mono, fijar escala editorial.
3. `/impeccable distill blog hub + artículo` -> vira a light editorial, quita wrap card, refactor pullquote.
4. `/impeccable harden` -> estados de formulario, edge cases.
5. `/impeccable polish` -> micro-spacing, focus rings, alineaciones ópticas.
6. `/impeccable audit` -> re-ejecutar audit completo y comparar contra esta línea base.
