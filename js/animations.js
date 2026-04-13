/**
 * AGROTECH DIGITAL — PREMIUM VISUAL EFFECTS
 * 
 * Sin Lenis (scroll nativo). Todo es aditivo.
 * gsap.from() con clearProps para no romper nada.
 */

(function () {
  'use strict';

  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    console.warn('[Agrotech] GSAP not loaded.');
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  document.body.classList.add('anim-engine-active');

  // ── Scroll Progress Bar ──
  function initScrollProgress() {
    var bar = document.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.prepend(bar);

    gsap.to(bar, {
      width: '100%',
      ease: 'none',
      scrollTrigger: {
        trigger: document.documentElement,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.3,
      },
    });
  }

  // ── Cursor Glow (desktop) ──
  function initCursorGlow() {
    if (window.matchMedia('(pointer: coarse)').matches || window.innerWidth < 769) return;

    var glow = document.createElement('div');
    glow.className = 'anim-cursor-glow';
    glow.setAttribute('aria-hidden', 'true');
    document.body.appendChild(glow);

    var mx = 0, my = 0, gx = 0, gy = 0;
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
    }, { passive: true });

    (function loop() {
      gx += (mx - gx) * 0.12;
      gy += (my - gy) * 0.12;
      glow.style.left = gx + 'px';
      glow.style.top = gy + 'px';
      requestAnimationFrame(loop);
    })();
  }

  // ── Hero Cinematic Entrance ──
  function initHero() {
    var badge = document.querySelector('.hero-badge');
    var h1 = document.querySelector('.hero h1');
    var desc = document.querySelector('.hero-description');
    var buttons = document.querySelector('.hero-buttons');
    var stats = document.querySelector('.hero-stats');

    // Badge bounce
    if (badge) {
      gsap.from(badge, { scale: 0.8, y: 15, duration: 0.6, delay: 0.2, ease: 'back.out(1.7)', clearProps: 'all' });
    }

    // H1 char-by-char
    if (h1) {
      var txt = h1.textContent;
      h1.innerHTML = txt.split(' ').map(function (w) {
        return '<span style="display:inline-block;white-space:nowrap">' +
          w.split('').map(function (c) {
            return '<span class="anim-char" style="display:inline-block">' + c + '</span>';
          }).join('') + '</span>';
      }).join(' ');

      gsap.from('.hero h1 .anim-char', {
        y: 25, opacity: 0, rotateX: -50,
        duration: 0.45, stagger: 0.018, delay: 0.35,
        ease: 'power3.out', clearProps: 'all',
      });
    }

    if (desc) gsap.from(desc, { y: 18, opacity: 0, duration: 0.6, delay: 0.8, ease: 'power2.out', clearProps: 'all' });
    if (buttons) gsap.from(buttons, { y: 18, opacity: 0, duration: 0.5, delay: 1.0, ease: 'power2.out', clearProps: 'all' });
    if (stats) gsap.from(stats, { y: 18, opacity: 0, duration: 0.6, delay: 1.2, ease: 'power2.out', clearProps: 'all' });

    // Hero BG parallax
    var heroBg = document.querySelector('.hero-bg');
    if (heroBg) {
      gsap.to(heroBg, {
        y: 100, scale: 1.04, ease: 'none',
        scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true },
      });
    }
  }

  // ── Floating Particles (hero, desktop) ──
  function initParticles() {
    if (window.innerWidth < 769) return;
    var hero = document.querySelector('.hero');
    if (!hero) return;

    var c = document.createElement('div');
    c.className = 'anim-particles-container';
    c.setAttribute('aria-hidden', 'true');
    var colors = ['anim-particle--green', 'anim-particle--gold', 'anim-particle--white'];

    for (var i = 0; i < 18; i++) {
      var p = document.createElement('div');
      p.className = 'anim-particle ' + colors[i % 3];
      p.style.left = Math.random() * 100 + '%';
      p.style.top = (50 + Math.random() * 45) + '%';
      var s = (2 + Math.random() * 4) + 'px';
      p.style.width = s; p.style.height = s;
      p.style.animationDuration = (7 + Math.random() * 10) + 's';
      p.style.animationDelay = Math.random() * 6 + 's';
      c.appendChild(p);
    }
    hero.appendChild(c);
  }

  // ── Counter Animation (uses data attributes) ──
  function initCounters() {
    document.querySelectorAll('[data-count]').forEach(function (el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      var suffix = el.getAttribute('data-suffix') || '';
      if (isNaN(target)) return;

      // Format with Colombian thousands separator (dot)
      function fmt(n) {
        if (n >= 1000) return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return n.toString();
      }

      var finalText = fmt(target) + suffix;
      var obj = { val: 0 };

      // Don't reset text to 0 — keep original visible until animation starts
      ScrollTrigger.create({
        trigger: el,
        start: 'top 92%',
        once: true,
        onEnter: function () {
          gsap.to(obj, {
            val: target,
            duration: 2.2,
            ease: 'power2.out',
            onUpdate: function () {
              el.textContent = fmt(Math.round(obj.val)) + suffix;
            },
            onComplete: function () {
              el.textContent = finalText;
            },
          });
        },
      });
    });
  }

  // ── Section Scroll Reveals ──
  function initReveals() {
    // Section headers
    document.querySelectorAll('.section-header').forEach(function (h) {
      var els = [];
      var b = h.querySelector('.section-badge');
      var t = h.querySelector('.section-title');
      var d = h.querySelector('.section-description');
      if (b) els.push(b);
      if (t) els.push(t);
      if (d) els.push(d);
      if (!els.length) return;

      gsap.from(els, {
        y: 25, opacity: 0, duration: 0.6, stagger: 0.12,
        ease: 'power2.out', clearProps: 'all',
        scrollTrigger: { trigger: h, start: 'top 85%', toggleActions: 'play none none none' },
      });
    });

    // Feature cards
    animateGroup('.features-grid', '.feature-card', { y: 40, opacity: 0, scale: 0.96 });

    // Pricing
    animateGroup('#precios', '.neuro-card', { y: 50, opacity: 0, scale: 0.93 });

    // Satellite gallery
    animateGroup('.satellite-gallery', '.neuro-card', { scale: 0.88, opacity: 0, y: 25 }, 'back.out(1.3)');

    // Product cards
    animateGroup('.products-showcase', '.product-card', { y: 40, opacity: 0 });

    // Stats
    animateGroup('.stats-grid', '.stat-card', { y: 35, opacity: 0, scale: 0.92 }, 'back.out(1.3)');

    // Blog cards
    var blogLink = document.querySelector('a[href*="blog/"]');
    if (blogLink) {
      var sec = blogLink.closest('section, .section');
      if (sec) {
        var cards = sec.querySelectorAll('a[style*="text-decoration"]');
        if (cards.length) {
          gsap.from(cards, {
            y: 25, opacity: 0, scale: 0.97, duration: 0.5, stagger: 0.1,
            ease: 'power3.out', clearProps: 'all',
            scrollTrigger: { trigger: sec, start: 'top 82%', toggleActions: 'play none none none' },
          });
        }
      }
    }

    // FAQ slide-in
    var faqs = document.querySelectorAll('details.neuro-card');
    if (faqs.length) {
      gsap.from(faqs, {
        x: -35, opacity: 0, duration: 0.45, stagger: 0.06,
        ease: 'power2.out', clearProps: 'all',
        scrollTrigger: { trigger: faqs[0].parentElement, start: 'top 82%', toggleActions: 'play none none none' },
      });
    }

    // CTA split
    var cta = document.querySelector('.cta-content');
    if (cta) {
      var img = cta.querySelector('.cta-image-wrapper');
      var txt = cta.querySelector('.cta-text-content');
      if (img) gsap.from(img, { x: -50, opacity: 0, scale: 0.92, duration: 0.7, ease: 'power3.out', clearProps: 'all', scrollTrigger: { trigger: cta, start: 'top 80%', toggleActions: 'play none none none' } });
      if (txt) gsap.from(txt, { x: 40, opacity: 0, duration: 0.7, delay: 0.1, ease: 'power3.out', clearProps: 'all', scrollTrigger: { trigger: cta, start: 'top 80%', toggleActions: 'play none none none' } });
    }

    // Footer
    var fs = document.querySelectorAll('.footer-section');
    if (fs.length) {
      var ft = fs[0].closest('footer, .footer');
      if (ft) {
        gsap.from(fs, {
          y: 20, opacity: 0, duration: 0.45, stagger: 0.07,
          ease: 'power2.out', clearProps: 'all',
          scrollTrigger: { trigger: ft, start: 'top 92%', toggleActions: 'play none none none' },
        });
      }
    }
  }

  // Helper
  function animateGroup(containerSel, childSel, fromVars, easing) {
    var container = document.querySelector(containerSel);
    if (!container) return;
    var items = container.querySelectorAll(childSel);
    if (!items.length) return;
    var vars = Object.assign({}, fromVars, {
      duration: 0.6, stagger: 0.1,
      ease: easing || 'power3.out',
      clearProps: 'all',
      scrollTrigger: { trigger: container, start: 'top 80%', toggleActions: 'play none none none' },
    });
    gsap.from(items, vars);
  }

  // ── Illustration Parallax ──
  function initParallax() {
    var sat = document.querySelector('.parallax-satellite');
    if (sat) {
      var sec = sat.closest('section');
      if (sec) gsap.to(sat, { y: -70, rotation: 3, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 1 } });
    }

    document.querySelectorAll('.products[style*="position: absolute"] img, #productos [style*="position: absolute"] img').forEach(function (img) {
      var alt = (img.getAttribute('alt') || '').toLowerCase();
      if (alt.indexOf('ilustraci') === -1 && alt.indexOf('terreno') === -1) return;
      var wrapper = img.closest('[style*="position: absolute"]');
      var sec = wrapper ? wrapper.closest('section') : null;
      if (sec && wrapper) gsap.to(wrapper, { y: -40, rotation: 2, ease: 'none', scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 1 } });
    });
  }

  // ── 3D Magnetic Tilt (desktop) ──
  function initTilt() {
    if (window.matchMedia('(pointer: coarse)').matches) return;

    function tilt(cards, power) {
      cards.forEach(function (card) {
        card.classList.add('magnetic-hover');
        card.addEventListener('mousemove', function (e) {
          var r = card.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width - 0.5;
          var y = (e.clientY - r.top) / r.height - 0.5;
          gsap.to(card, { rotateY: x * power, rotateX: -y * power, transformPerspective: 800, duration: 0.3, ease: 'power2.out' });
        });
        card.addEventListener('mouseleave', function () {
          gsap.to(card, { rotateY: 0, rotateX: 0, duration: 0.5, ease: 'elastic.out(1, 0.5)' });
        });
      });
    }

    tilt(document.querySelectorAll('.feature-card'), 4);
    var p = document.getElementById('precios');
    if (p) tilt(p.querySelectorAll('.neuro-card'), 5);
  }

  // ── Card Spotlight (mouse glow) ──
  function initSpotlight() {
    if (window.matchMedia('(pointer: coarse)').matches) return;
    document.querySelectorAll('.feature-card').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mouse-x', (e.clientX - r.left) + 'px');
        card.style.setProperty('--mouse-y', (e.clientY - r.top) + 'px');
      });
    });
  }

  // ── Init ──
  function init() {
    initScrollProgress();
    initHero();
    initParticles();
    initCounters();
    initReveals();
    initParallax();
    initTilt();
    initSpotlight();
    initCursorGlow();

    window.addEventListener('load', function () { ScrollTrigger.refresh(); });
    console.log('%c✨ AgroTech Effects OK', 'color:#4CAF50;font-size:13px;font-weight:bold');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
