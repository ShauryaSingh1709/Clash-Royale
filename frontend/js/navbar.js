document.addEventListener('DOMContentLoaded', () => {
    renderNavbar();
    renderFooter();
    initNavbar();
});

function renderNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    navbar.innerHTML = `
        <div class="navbar-container">
            <a href="/" class="navbar-logo">
                <div class="navbar-logo-mark">
                    <img src="https://cdn.royaleapi.com/static/img/cards-150/archer-queen.png" 
                         alt="RoyaleForge" />
                </div>
                <div class="navbar-logo-text">
                    Royale<span>Forge</span>
                </div>
            </a>

            <ul class="navbar-menu" id="navMenu">
                <li><a href="/" class="navbar-link" data-page="">
                    ${Icons.home}<span>Home</span>
                </a></li>
                <li><a href="/analyzer" class="navbar-link" data-page="analyzer">
                    ${Icons.sword}<span>Analyzer</span>
                </a></li>
                <li><a href="/cards" class="navbar-link" data-page="cards">
                    ${Icons.cards}<span>Cards</span>
                </a></li>
                <li><a href="/dashboard" class="navbar-link" data-page="dashboard">
                    ${Icons.chart}<span>Dashboard</span>
                </a></li>
                <li><a href="/about" class="navbar-link" data-page="about">
                    ${Icons.info}<span>About</span>
                </a></li>
            </ul>

            <button class="navbar-toggle" id="navToggle" aria-label="Toggle menu">
                ${Icons.menu}
            </button>
        </div>
    `;
}

function renderFooter() {
    const footer = document.querySelector('.footer');
    if (!footer) return;

    footer.innerHTML = `
        <div class="footer-pattern"></div>
        
        <div class="footer-main">
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-brand-col">
                        <a href="/" class="footer-logo-link">
                            <div class="footer-logo">
                                <img src="https://cdn.royaleapi.com/static/img/cards-150/archer-queen.png" 
                                     alt="RoyaleForge" />
                            </div>
                            <div class="footer-brand-text">
                                Royale<span>Forge</span>
                            </div>
                        </a>
                        <p class="footer-tagline">
                            The most advanced Clash Royale analytics platform. 
                            Build smarter decks with AI-powered insights.
                        </p>
                        <div class="footer-socials">
                            <a href="https://github.com/ShauryaSingh1709/Clash-Royale" target="_blank" rel="noopener" class="footer-social-btn" title="GitHub">
                                ${Icons.github}
                            </a>
                            <a href="mailto:shaurya17092006@gmail.com" class="footer-social-btn" title="Email">
                                ${Icons.mail}
                            </a>
                        </div>
                    </div>

                    <div class="footer-col">
                        <h4 class="footer-col-title">Platform</h4>
                        <ul class="footer-links">
                            <li><a href="/analyzer">Deck Analyzer</a></li>
                            <li><a href="/cards">Card Explorer</a></li>
                            <li><a href="/dashboard">Meta Dashboard</a></li>
                            <li><a href="/about">About</a></li>
                        </ul>
                    </div>

                    <div class="footer-col">
                        <h4 class="footer-col-title">Resources</h4>
                        <ul class="footer-links">
                            <li><a href="/docs">Documentation</a></li>
                            <li><a href="/api">API Reference</a></li>
                            <li><a href="/tutorials">Tutorials</a></li>
                            <li><a href="/contributing">Contributing</a></li>
                        </ul>
                    </div>

                    <div class="footer-col">
                        <h4 class="footer-col-title">Community</h4>
                        <ul class="footer-links">
                            <li><a href="https://github.com/ShauryaSingh1709/Clash-Royale" target="_blank" rel="noopener">
                                GitHub ${Icons.arrow_up_right}
                            </a></li>
                            <li><a href="/contributing">How to Contribute</a></li>
                            <li><a href="/bugs">Bug Reports</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer-bottom-bar">
            <div class="container">
                <div class="footer-bottom-content">
                    <div class="footer-copyright">
                        © 2026 RoyaleForge. All rights reserved.
                    </div>
                    <div class="footer-legal">
                        <a href="/privacy">Privacy</a>
                        <span class="footer-dot">·</span>
                        <a href="/terms">Terms and Conditions</a>
                    </div>
                    <div class="footer-disclaimer">
                        Not affiliated with Supercell. Clash Royale is a trademark of Supercell.
                    </div>
                </div>
            </div>
        </div>
    `;
}

function initNavbar() {
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('navMenu');

    if (toggle && menu) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && !toggle.contains(e.target)) {
                menu.classList.remove('active');
            }
        });
    }


    const currentPath = window.location.pathname.replace('/', '');
    document.querySelectorAll('.navbar-link').forEach(link => {
        const page = link.dataset.page;
        if (page === currentPath) {
            link.classList.add('active');
        }
    });

    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 30) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}