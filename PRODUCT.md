# PRODUCT.md — AgroTech Colombia

> Documento fuente de verdad para diseño y producto. Generado por `/impeccable teach` (modo auto-inferencia).
> Cualquier decisión visual o de copy debe respetar este documento. Si algo entra en conflicto con `PRODUCT.md`, gana `PRODUCT.md`.

---

## 1. Register

**Principal: `brand`** — el diseño *es* el producto en las superficies públicas. La landing, el blog hub y los artículos venden confianza antes que features. La estética debe sentirse editorial, honesta y técnica, no SaaS-startup.

**Secundario: `product`** — el dashboard interno (`dashboard.html`, `parcels/`, `employees/`, `analysis.js`) sirve a la operación. Allí manda la legibilidad de datos, los estados (loading, empty, error), y la densidad de información. **Fuera del scope inmediato de este teach.**

---

## 2. Product Purpose

AgroTech Colombia entrega **historial satelital del lote** a agricultores colombianos: NDVI, NDMI, SAVI y datos climáticos de los últimos 1–3 años de su tierra, en un informe claro con mapas a color y recomendaciones prácticas. El producto contesta una pregunta concreta antes de sembrar, comprar o arrendar: *¿qué ha pasado en este terreno?*. En el futuro próximo, vigilancia día a día (monitoreo activo) y dashboard de gestión de parcelas, labores y empleados.

---

## 3. Users

- **Agricultor mediano-grande colombiano**, 40–65 años. Dueño o socio de finca con 50–500+ hectáreas. Cultivos típicos: arroz, café, palma, maíz, caña, frutales. Tomó la decisión de comprar/arrendar/sembrar con experiencia y olfato; ahora empieza a oír "satélite" y "NDVI" pero no se quiere sentir tonto preguntando.
- **Gerente agrícola / administrador de finca**, 30–55 años. Reporta resultados a un dueño o a una junta. Necesita datos defendibles para justificar inversión.
- **Agrónomo de campo / asesor técnico**, 28–50 años. Quiere material visual para mostrar al cliente y recomendar con argumento.

**Contexto de uso:** lectura desde Android de gama media, 4G inestable en zona rural, pantalla bajo sol fuerte. WhatsApp es el canal de contacto natural. Lee en **español de Colombia formal ("usted")**. Se conecta tarde en la noche o muy temprano. Si el sitio es lento o pide registro antes de mostrar valor, se va.

---

## 4. Brand voice / tone

**Voice words:** honesto, mecánico, llano, preciso, agro-tech.

**Lo que decimos:**
- Cifras concretas (`+60% sobre el promedio`, `200 ha → $1.100.000`).
- Verbos de campo: *sembrar, arrendar, comprar, cosechar, regar, abonar*.
- "Usted" siempre. "Su finca", "su lote", "su cosecha".
- Reconocer la experiencia del agricultor antes de proponer tecnología.
- Decir lo que **no** hacemos (no somos predicción mágica, no reemplazamos al agrónomo).

**Lo que NO decimos:**
- Jerga startup ("revolucionamos", "disrupción", "leverage").
- Anglicismos innecesarios ("insights", "real-time", "tracking").
- Emojis decorativos en contenido serio. Se admiten 📞 ✉️ 🌐 en footer/contacto donde son icono funcional.
- Em-dashes (`—`) en UI copy. Usar punto y seguido o guion corto.
- Lorem ipsum, nunca.
- Promesas absolutas ("100% seguro", "garantizamos rentabilidad").

---

## 5. Strategic principles

1. **Trust-first.** El primer scroll debe transmitir solidez técnica y honestidad, no entusiasmo. Logos, números reales, ejemplo real de informe antes que CTA grande.
2. **Datos antes que opinión.** Cada afirmación va con cifra, fecha, fuente (IDEAM, Sentinel, FNA, DANE).
3. **Contexto Colombia primero.** Llanos, Tolima, Huila, Eje Cafetero antes que ejemplos de Iowa o Punjab.
4. **Honestidad sobre limitaciones.** Decimos qué resolución tiene Sentinel-2 (10 m), cuándo no hay imagen (nubes), qué no hace el producto.
5. **WhatsApp es producto.** El botón de WhatsApp no es un "extra de soporte"; es el flujo principal de conversión y atención.
6. **Velocidad sobre efectismo.** LCP < 2.5 s en 4G rural. Cualquier animación que cueste eso, se corta.

---

## 6. Aesthetic family

**Editorial trust-first agro-tech.**

Una mezcla de **revista técnica agro** (tipografía de cuerpo cómoda, jerarquía clara, fotografía honesta de campo colombiano) con **dashboard sobrio de datos** (mapas NDVI con escala cromática técnica, números monoespaciados donde toca, mucho whitespace). Cero glassmorphism. Cero gradiente text. Cero hero centrado sobre mesh oscuro. Si dudamos entre "más diseñado" y "más legible", gana legible.

**Paleta direccional** (a confirmar en `/impeccable colorize` posterior, usar OKLCH):
- Verde marca (campo, sano) — ancla principal.
- Naranja/ocre marca (alerta, cosecha) — acento limitado a estados y badges.
- Neutros tintados hacia el verde (no `#000` ni `#fff` puros).
- Azul técnico solo para NDMI/datos de humedad.

---

## 7. Anti-references (NO)

- ❌ **Linear / Notion / Vercel / Fluence dark-purple SaaS.** No somos una herramienta de productividad para founders.
- ❌ **Glassmorphism everywhere.** Es un efecto, no un sistema.
- ❌ **Gradient text en H1** (esto se acaba de eliminar en quick-win 1).
- ❌ **Hero centrado sobre dark mesh con blur radial.** Cliché 2024–2026.
- ❌ **Neomorphism** (cards con doble sombra suave estilo iOS 2020).
- ❌ **Emoji-heavy WhatsApp aesthetic** en contenido editorial.
- ❌ **Material Design defaults** (botones llenos morados, ripple, FAB).
- ❌ **Awwwards experimental** (scroll-jacking, animaciones de 4 s por sección, transiciones de página largas).
- ❌ **Agro-cliché verde fosforescente + tractor genérico stock.**

---

## 8. References (SÍ)

- **Stripe Press** — composición editorial, tipografía con peso, respeto al texto largo.
- **Bloomberg Green** — datos en serio, fotografía documental, jerarquía periodística.
- **NYT Cooking** — claridad tipográfica, foto honesta, instrucciones legibles a una mano.
- **Patagonia.com** — B2C honesto con tema ambiental, voz humana sin perder rigor.
- **Klim Type Foundry** — display de carácter sin sobreproducir.
- **GOV.UK** — trust-first absoluto, accesibilidad como decisión estética.
- **The Pudding / Reuters Graphics** — narrativa con datos espaciales (mapas), útil para artículos NDVI.

---

## 9. Content domains (blog y landing)

- NDVI, NDMI, SAVI y teledetección aplicada a cultivos.
- IoT agro (sensores de humedad, estaciones meteo, telemetría de riego).
- Precios y mercado agro CO: arroz, café, palma, maíz, caña, cacao.
- Política pública agro CO (incentivos, créditos FINAGRO, ICA, FNA, DANE).
- Clima Colombia: ENSO, fenómeno El Niño / La Niña, IDEAM, predicciones de cosecha.
- Casos de éxito reales con cifras y geografía concreta.
- Errores costosos / lo que cuesta no medir.

---

## 10. Competitors / context

| Player | Qué hace | Por qué AgroTech CO es distinto |
|---|---|---|
| **Solinftec** | Plataforma agro de gran escala (Brasil, USA). | Demasiado pesada y cara para mediana finca CO. Nosotros entregamos un informe puntual, sin obligar contrato anual. |
| **Taranis** | Visión por computadora + drones, foco USA/LATAM corporativo. | Requiere flota propia y operación grande. Nosotros entregamos vía satélite sin que el cliente compre hardware. |
| **Cropwise (Syngenta)** | Suite atada a portafolio Syngenta. | Nosotros somos agnósticos de insumo. No vendemos químico. |
| **Agrosmart** | Brasilera, IoT + clima, foco caña/soja. | Producto en portugués/inglés, lejos del agricultor colombiano. Nosotros estamos en es-CO, WhatsApp directo, precios en COP. |
| **Consultores locales sueltos** | Agrónomo con experiencia, sin datos satelitales. | Nosotros complementamos al agrónomo (no lo reemplazamos) con histórico de 1–3 años. |

**Posicionamiento de una línea:** *El historial satelital del lote, en español de Colombia, sin que usted tenga que comprar drones ni firmar un contrato anual.*

---

## 11. Constraints

- **WCAG AA mínimo.** Contraste 4.5:1 cuerpo, 3:1 títulos grandes. Focus visible. Tap targets ≥ 44 px.
- **Mobile-first.** Diseñar para Android gama media, 360–390 px, LTE inestable. Imágenes `.webp` ≤ 300 KB, max 1200 px.
- **Español-CO formal "usted".** Sin excepciones en superficie pública.
- **CSP estricta vía Netlify `_headers`.** Cualquier script de tercero requiere actualizar `script-src` / `connect-src` / `img-src` en el mismo commit.
- **Tracking declarado.** Meta Pixel `936082032542696` declarado. No añadir GA / Hotjar / Clarity sin decisión explícita.
- **Sin build step.** HTML/CSS/JS plano. Nada de Tailwind ni bundlers en este repo.
- **LCP objetivo < 2.5 s** en 4G simulado.
- **Reducir motion.** Respetar `prefers-reduced-motion`. Animaciones que no sirvan a comprensión, fuera.
- **Compatibilidad navegador:** Chrome/Edge/Safari últimos 2 mayores, Samsung Internet, Android WebView. No IE.

---

## 12. Surfaces

| Superficie | Register | Estado actual | Prioridad estética |
|---|---|---|---|
| `index.html` (landing) | brand | Hero + features + pricing + gallery + FAQ. Recién pasada por quick-wins 1–5. | Alta — primera impresión comercial. |
| `blog.html` (hub) | brand-editorial | Listado de artículos. | Media — entrada SEO. |
| `blog/*.html` (artículos) | brand-editorial | 7 posts activos, plantilla en `blog/tecnologia-satelital-aliado-agricultor.html`. | Alta — donde se construye la confianza. |
| `post.html` | brand-editorial | Plantilla de post dinámico. | Media. |
| `legal/privacidad.html`, `legal/terminos.html` | brand (sobrio) | Texto legal. | Baja — solo legibilidad. |
| `dashboard.html`, `parcels/`, `employees/`, `analysis.js` | **product** | Operación interna, gestión de parcelas, labores, empleados. | **Fuera del scope de este teach.** Se aborda en pasada `product`-register posterior. |
| `templates/contact_expert.html`, contacto WhatsApp | brand | CTA principal de conversión. | Alta. |

---

## Next: run `/impeccable document` to extract DESIGN.md from current CSS
