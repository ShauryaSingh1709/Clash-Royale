/* ==========================================================================
   🏆 CLASH ROYALE DECK ANALYZER - Utility Functions
   ========================================================================== */

const Utils = {
    // ── Rarity colors ──
    getRarityColor(rarity) {
        const colors = {
            'Common': '#A8DADC',
            'Rare': '#FFD700',
            'Epic': '#9B5DE5',
            'Legendary': '#FF6B35',
            'Champion': '#E63946'
        };
        return colors[rarity] || '#FFFFFF';
    },

    // ── Type icons ──
    getTypeIcon(type) {
        const icons = {
            'Troop': '⚔️',
            'Spell': '✨',
            'Building': '🏰'
        };
        return icons[type] || '🃏';
    },

    // ── Archetype icons ──
    getArchetypeIcon(archetype) {
        const icons = {
            'Beatdown': '💪',
            'Control': '🎯',
            'Cycle': '⚡',
            'Siege': '🏹',
            'Hog Cycle': '🐗'
        };
        return icons[archetype] || '🃏';
    },

    // ── Grade color ──
    getGradeColor(grade) {
        const colors = {
            'S': '#FFD700',
            'A': '#06D6A0',
            'B': '#4FC3F7',
            'C': '#FFB627',
            'D': '#FF6B35',
            'F': '#E63946'
        };
        return colors[grade] || '#FFFFFF';
    },

    // ── Format number ──
    formatNumber(num) {
        if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
        if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K';
        return num.toString();
    },

    // ── Show toast notification ──
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 90px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--bg-card);
            border-left: 4px solid var(--color-${type === 'error' ? 'danger' : 'success'});
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    // ── Loading state ──
    showLoading(element, message = 'Loading...') {
        element.innerHTML = `
            <div style="text-align: center; padding: 3rem;">
                <div class="spinner"></div>
                <p class="loading-text">${message}</p>
            </div>
        `;
    },

    // ── Error state ──
    showError(element, message) {
        element.innerHTML = `
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 3rem;">⚠️</div>
                <h3 style="margin: 1rem 0; color: var(--color-danger);">Error</h3>
                <p>${message}</p>
            </div>
        `;
    },

    // ── Debounce ──
    debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    }
};