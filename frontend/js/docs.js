/* ==========================================================================
   📚 DOCS - Inject icons, FAQ toggle, copy buttons
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    injectIcons();
    initActiveLinks();
});

function injectIcons() {
    if (typeof Icons === 'undefined') return;
    
    const iconMap = {
        docsIcon: 'book',
        apiIcon: 'code',
        tutIcon: 'sparkles',
        ctbIcon: 'sword',
        bugIcon: 'shield',
        privacyIcon: 'shield',
        termsIcon: 'book',
        infoIcon1: 'info', infoIconApi: 'info', infoIconCtb: 'info', infoIconBug: 'info',
        successIcon: 'check', sucIcon: 'check',
        warnIcon: 'warning', warnIcon2: 'warning',
        codeIcon: 'code', bookIcon: 'book', designIcon: 'sparkles',
        iconBeginner: 'play', iconMeta: 'chart', iconApiUse: 'code',
        ar1: 'arrow_right', ar2: 'arrow_right', ar3: 'arrow_right',
        arr1: 'arrow_right', arr2: 'arrow_right', arr3: 'arrow_right',
        calIcon: 'info', calIcon2: 'info',
        versionMeta: 'sparkles',
        updatedMeta: 'refresh'
    };
    
    // Add check icon to Icons if missing
    if (!Icons.check) {
        Icons.check = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;
    }
    if (!Icons.warning) {
        Icons.warning = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
    }
    
    Object.entries(iconMap).forEach(([id, name]) => {
        const el = document.getElementById(id);
        if (el && Icons[name]) {
            if (id === 'versionMeta') {
                el.innerHTML = Icons[name] + '<span style="margin-left:6px;">v1.0.0</span>';
            } else if (id === 'updatedMeta') {
                el.innerHTML = Icons[name] + '<span style="margin-left:6px;">Updated June 2026</span>';
            } else {
                el.innerHTML = Icons[name];
            }
        }
    });
}

function initActiveLinks() {
    const links = document.querySelectorAll('.docs-sidebar-link');
    const sections = document.querySelectorAll('.docs-article > section, .legal-section');
    
    if (!links.length || !sections.length) return;

    // Click handlers
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Scroll spy
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                links.forEach(link => {
                    link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
                });
            }
        });
    }, { rootMargin: '-20% 0px -70% 0px' });

    sections.forEach(s => observer.observe(s));
}

function toggleFaq(button) {
    const item = button.closest('.faq-item');
    item.classList.toggle('open');
}

function copyCode(button) {
    const codeBlock = button.closest('.code-block');
    const pre = codeBlock.querySelector('pre');
    if (!pre) return;
    
    const text = pre.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const original = button.textContent;
        button.textContent = 'Copied!';
        button.style.color = '#10B981';
        setTimeout(() => {
            button.textContent = original;
            button.style.color = '';
        }, 2000);
    });
}