


const CARD_SLUG_MAP = {
    
    "Knight": "knight",
    "Archers": "archers",
    "Bomber": "bomber",
    "Goblins": "goblins",
    "Spear Goblins": "spear-goblins",
    "Skeletons": "skeletons",
    "Minions": "minions",
    "Minion Horde": "minion-horde",
    "Barbarians": "barbarians",
    "Royal Giant": "royal-giant",
    "Cannon": "cannon",
    "Tesla": "tesla",
    "Mortar": "mortar",
    "Fire Spirit": "fire-spirits",
    "Ice Spirit": "ice-spirit",
    "Royal Recruits": "royal-recruits",
    "Rascals": "rascals",
    "Elite Barbarians": "elite-barbarians",
    "Goblin Gang": "goblin-gang",
    "Skeleton Barrel": "skeleton-barrel",
    "Arrows": "arrows",
    "Zap": "zap",
    "Royal Delivery": "royal-delivery",
    "Firecracker": "firecracker",
    
    
    "Mini PEKKA": "mini-pekka",
    "Musketeer": "musketeer",
    "Giant": "giant",
    "Valkyrie": "valkyrie",
    "Fireball": "fireball",
    "Hog Rider": "hog-rider",
    "Wizard": "wizard",
    "Three Musketeers": "three-musketeers",
    "Battle Ram": "battle-ram",
    "Zappies": "zappies",
    "Mega Minion": "mega-minion",
    "Goblin Hut": "goblin-hut",
    "Furnace": "furnace",
    "Bomb Tower": "bomb-tower",
    "Flying Machine": "flying-machine",
    "Ice Golem": "ice-golem",
    "Tombstone": "tombstone",
    "Rocket": "rocket",
    "Royal Hogs": "royal-hogs",
    "Elixir Collector": "elixir-collector",
    "Inferno Tower": "inferno-tower",
    "Earthquake": "earthquake",
    "Goblin Cage": "goblin-cage",
    "Battle Healer": "battle-healer",
    "Elixir Golem": "elixir-golem",
    "Heal Spirit": "heal-spirit",
    
    
    "Witch": "witch",
    "Skeleton Army": "skeleton-army",
    "Baby Dragon": "baby-dragon",
    "Prince": "prince",
    "Giant Skeleton": "giant-skeleton",
    "Balloon": "balloon",
    "PEKKA": "pekka",
    "Goblin Barrel": "goblin-barrel",
    "Freeze": "freeze",
    "Dark Prince": "dark-prince",
    "Lightning": "lightning",
    "X-Bow": "x-bow",
    "Poison": "poison",
    "Hunter": "hunter",
    "Bowler": "bowler",
    "Executioner": "executioner",
    "Cannon Cart": "cannon-cart",
    "Wall Breakers": "wall-breakers",
    "Tornado": "tornado",
    "Clone": "clone",
    "Mirror": "mirror",
    
    
    "Electro Wizard": "electro-wizard",
    "Royal Ghost": "royal-ghost",
    "Princess": "princess",
    "Ice Wizard": "ice-wizard",
    "Miner": "miner",
    "Sparky": "sparky",
    "Lava Hound": "lava-hound",
    "Inferno Dragon": "inferno-dragon",
    "Graveyard": "graveyard",
    "The Log": "the-log",
    "Lumberjack": "lumberjack",
    "Night Witch": "night-witch",
    "Bandit": "bandit",
    "Mega Knight": "mega-knight",
    "Magic Archer": "magic-archer",
    "Ram Rider": "ram-rider",
    "Fisherman": "fisherman",
    "Mother Witch": "mother-witch",
    
    
    "Royal Champion": "royal-champion",
    "Archer Queen": "archer-queen",
    "Skeleton King": "skeleton-king",
    "Mighty Miner": "mighty-miner",
    "Phoenix": "phoenix",
    "Goblinstein": "goblinstein",
    "Little Prince": "little-prince",
    "Monk": "monk"
};


const CDN_SOURCES = [
    (slug) => `https://cdn.royaleapi.com/static/img/cards-150/${slug}.png`,
    (slug) => `https://api.clashroyale.com/v1/cards/${slug}/image`,
    (slug) => `https://royaleapi.com/cards/${slug}.png`
];


const Utils = {
    
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

    
    getTypeIcon(type) {
        const icons = {
            'Troop': 'T',
            'Spell': 'S',
            'Building': 'B'
        };
        return icons[type] || 'C';
    },

    
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

    
    formatNumber(num) {
        if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
        if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K';
        return num.toString();
    },

    
    getCardSlug(cardName) {
        if (CARD_SLUG_MAP[cardName]) return CARD_SLUG_MAP[cardName];
        return cardName
            .toLowerCase()
            .replace(/\./g, '')
            .replace(/\s+/g, '-')
            .replace(/[^a-z0-9-]/g, '');
    },

    
    getCardImageUrl(cardName) {
        if (!cardName) return '';
        const slug = this.getCardSlug(cardName);
        return CDN_SOURCES[0](slug);
    },

    
    handleImageError(img) {
        const cardName = img.alt || 'Unknown';
        const slug = this.getCardSlug(cardName);
        const attempts = parseInt(img.dataset.attempts || '0');

        
        if (attempts < CDN_SOURCES.length - 1) {
            const nextAttempt = attempts + 1;
            img.dataset.attempts = nextAttempt.toString();
            img.src = CDN_SOURCES[nextAttempt](slug);
            return;
        }

        
        img.onerror = null;
        img.style.display = 'none';

        const parent = img.parentElement;
        if (!parent || parent.querySelector('.svg-fallback')) return;

        const svgCard = this.generateFallbackCard(cardName, img.width || 80);
        parent.appendChild(svgCard);
    },

    
    generateFallbackCard(cardName, size = 80) {
        const initials = cardName
            .split(' ')
            .map(w => w[0])
            .slice(0, 2)
            .join('')
            .toUpperCase();

        
        const hash = cardName.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
        const hue1 = hash % 360;
        const hue2 = (hash * 7) % 360;
        const color1 = `hsl(${hue1}, 70%, 50%)`;
        const color2 = `hsl(${hue2}, 70%, 40%)`;

        const div = document.createElement('div');
        div.className = 'svg-fallback';
        div.style.cssText = `
            width: ${size}px;
            height: ${size * 1.2}px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, ${color1} 0%, ${color2} 100%);
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3), inset 0 1px 2px rgba(255,255,255,0.3);
            color: white;
            font-family: 'Bangers', cursive;
            font-size: ${size * 0.4}px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            margin: 0 auto;
            position: relative;
            border: 2px solid rgba(255,255,255,0.2);
        `;
        div.innerHTML = `
            <div style="font-size: ${size * 0.5}px; line-height: 1;">${initials}</div>
            <div style="font-size: ${size * 0.12}px; margin-top: 4px; opacity: 0.8; text-align: center; padding: 0 4px;">
                ${cardName.length > 10 ? cardName.substring(0, 10) + '..' : cardName}
            </div>
        `;
        return div;
    },

    
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
            color: var(--text-primary);
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    
    showLoading(element, message = 'Loading...') {
        element.innerHTML = `
            <div style="text-align: center; padding: 3rem;">
                <div class="spinner"></div>
                <p class="loading-text">${message}</p>
            </div>
        `;
    },

    
    showError(element, message) {
        element.innerHTML = `
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 3rem;">⚠️</div>
                <h3 style="margin: 1rem 0; color: var(--color-danger);">Error</h3>
                <p>${message}</p>
            </div>
        `;
    },

    
    debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    }
};