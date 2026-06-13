/* ==========================================================================
   🏆 NAVBAR - Mobile Toggle + Active Link
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const toggle = document.querySelector('.navbar-toggle');
    const menu = document.querySelector('.navbar-menu');

    if (toggle) {
        toggle.addEventListener('click', () => {
            menu.classList.toggle('active');
        });
    }

    // Active link highlighting
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.navbar-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });

    // Navbar scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const currentScroll = window.scrollY;
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(10, 14, 39, 0.95)';
        } else {
            navbar.style.background = 'rgba(10, 14, 39, 0.85)';
        }
    });
});