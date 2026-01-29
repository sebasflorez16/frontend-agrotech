/**
 * Engine del Blog de AgroTech
 * Carga posts desde data/posts.json y renderiza el contenido
 */

const BLOG_DATA_URL = 'data/posts.json';

document.addEventListener('DOMContentLoaded', () => {
    // Detectar si estamos en la lista o en un post individual
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get('id');

    if (postId) {
        // Estamos viendo un post específico
        loadSinglePost(postId);
    } else {
        // Estamos en la página principal del blog
        loadBlogGrid();
    }
});

/**
 * Carga la lista de posts y renderiza las tarjetas
 */
async function loadBlogGrid() {
    const gridContainer = document.getElementById('blog-grid');
    if (!gridContainer) return; // No estamos en la página del blog

    try {
        const response = await fetch(BLOG_DATA_URL);
        const posts = await response.json();

        gridContainer.innerHTML = ''; // Limpiar loader

        posts.forEach(post => {
            const card = createPostCard(post);
            gridContainer.appendChild(card);
        });

    } catch (error) {
        console.error('Error cargando el blog:', error);
        gridContainer.innerHTML = '<p class="text-center">Hubo un error cargando los artículos. Por favor intente más tarde.</p>';
    }
}

/**
 * Crea el HTML para una tarjeta de artículo
 */
function createPostCard(post) {
    const card = document.createElement('div');
    card.className = 'blog-card';

    // Fallback image si no existe
    const imageUrl = post.image || 'images/agrotech satelite 1.png';

    card.innerHTML = `
        <div class="blog-card-image">
            <img src="${imageUrl}" alt="${post.title}">
        </div>
        <div class="blog-card-content">
            <span class="blog-date">${formatDate(post.date)}</span>
            <h3 class="blog-title">${post.title}</h3>
            <p class="blog-summary">${post.summary}</p>
            <a href="post.html?id=${post.id}" class="blog-link">Leer más →</a>
        </div>
    `;

    return card;
}

/**
 * Carga un post individual basado en su ID
 */
async function loadSinglePost(id) {
    const titleEl = document.getElementById('post-title');
    const contentEl = document.getElementById('post-content');
    const metaEl = document.getElementById('post-meta');
    const bgEl = document.getElementById('post-bg');

    if (!titleEl) return;

    try {
        const response = await fetch(BLOG_DATA_URL);
        const posts = await response.json();

        const post = posts.find(p => p.id === id);

        if (!post) {
            titleEl.textContent = 'Artículo no encontrado';
            contentEl.innerHTML = '<a href="blog.html" class="neuro-button neuro-button-primary">Volver al Blog</a>';
            return;
        }

        // Renderizar contenido
        document.title = `${post.title} | Blog AgroTech`; // Cambiar título de la pestaña
        titleEl.textContent = post.title;
        contentEl.innerHTML = post.content;
        metaEl.innerHTML = `Publicado el ${formatDate(post.date)} por <span style="color: var(--brand-green);">${post.author}</span>`;

        // Background image opcional (si quieres que el hero tenga la imagen del post)
        /* if (post.image && bgEl) {
           bgEl.style.backgroundImage = `url('${post.image}')`;
        } */

    } catch (error) {
        console.error('Error cargando el post:', error);
    }
}

/**
 * Helper para formatear fechas
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-CO', options);
}
