

let allCards = [];
let filtered = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadCards();
    initFilters();
});

async function loadCards() {
    const grid = document.getElementById('cardsGrid');
    Utils.showLoading(grid, 'Loading cards...');

    try {
        const data = await API.cards.getAll();
        allCards = data.cards;
        filtered = [...allCards];
        renderCards();
    } catch (error) {
        Utils.showError(grid, 'Failed to load cards');
    }
}

function renderCards() {
    const grid = document.getElementById('cardsGrid');

    if (filtered.length === 0) {
        grid.innerHTML = '<p style="text-align:center;padding:2rem;color:var(--text-muted);">No cards found</p>';
        return;
    }

    grid.innerHTML = filtered.map(card => `
        <div class="card-tile" onclick='showCardDetail(${JSON.stringify(card).replace(/'/g, "&apos;")})'>
            <div class="card-tile-elixir">${card.elixir_cost}</div>
            <div class="card-tile-icon">
                <img src="${Utils.getCardImageUrl(card.name)}" 
                     alt="${card.name}" 
                     onerror="Utils.handleImageError(this)"
                     style="width: 90px; height: 110px; object-fit: contain;">
            </div>
            <div class="card-tile-name">${card.name}</div>
            <span class="card-tile-rarity" 
                  style="background: ${Utils.getRarityColor(card.rarity)}33; color: ${Utils.getRarityColor(card.rarity)};">
                ${card.rarity}
            </span>
            <div class="card-tile-stats">
                <div class="card-tile-stat">
                    Win<strong>${card.win_rate?.toFixed(1) || '--'}%</strong>
                </div>
                <div class="card-tile-stat">
                    Use<strong>${card.usage_rate?.toFixed(1) || '--'}%</strong>
                </div>
            </div>
        </div>
    `).join('');
}

function initFilters() {
    const search = document.getElementById('searchInput');
    const rarity = document.getElementById('rarityFilter');
    const type = document.getElementById('typeFilter');
    const sort = document.getElementById('sortFilter');

    const applyFilters = () => {
        let result = [...allCards];

        if (search.value) {
            result = result.filter(c => c.name.toLowerCase().includes(search.value.toLowerCase()));
        }
        if (rarity.value) {
            result = result.filter(c => c.rarity === rarity.value);
        }
        if (type.value) {
            result = result.filter(c => c.type === type.value);
        }

        result.sort((a, b) => {
            const sortKey = sort.value;
            if (sortKey === 'name') return a.name.localeCompare(b.name);
            return (b[sortKey] || 0) - (a[sortKey] || 0);
        });

        filtered = result;
        renderCards();
    };

    search.addEventListener('input', Utils.debounce(applyFilters, 300));
    rarity.addEventListener('change', applyFilters);
    type.addEventListener('change', applyFilters);
    sort.addEventListener('change', applyFilters);
}

function showCardDetail(card) {
    const modal = document.getElementById('cardModal');
    const content = document.getElementById('modalContent');
    const rarityColor = Utils.getRarityColor(card.rarity);

    content.innerHTML = `
        <button class="modal-close" onclick="closeModal()">X</button>
        <div class="modal-header">
            <img src="${Utils.getCardImageUrl(card.name)}" 
                 alt="${card.name}" 
                 onerror="Utils.handleImageError(this)"
                 style="width: 140px; height: 170px; object-fit: contain; margin: 0 auto 1rem; display: block; filter: drop-shadow(0 10px 30px rgba(255, 215, 0, 0.4));">
            <div class="modal-elixir">${card.elixir_cost}</div>
            <h2>${card.name}</h2>
            <span class="badge" style="background:${rarityColor}33;color:${rarityColor};margin-top:0.5rem;">
                ${card.rarity}
            </span>
            <p style="color:var(--text-secondary);margin-top:0.5rem;">
                ${Utils.getTypeIcon(card.type)} ${card.type} | ${Utils.getArchetypeIcon(card.archetype)} ${card.archetype}
            </p>
        </div>
        <div class="modal-stats">
            <div class="modal-stat">
                <div class="modal-stat-label">Win Rate</div>
                <div class="modal-stat-value">${card.win_rate?.toFixed(2) || '--'}%</div>
            </div>
            <div class="modal-stat">
                <div class="modal-stat-label">Usage Rate</div>
                <div class="modal-stat-value">${card.usage_rate?.toFixed(2) || '--'}%</div>
            </div>
            <div class="modal-stat">
                <div class="modal-stat-label">Damage</div>
                <div class="modal-stat-value">${card.damage || '--'}</div>
            </div>
            <div class="modal-stat">
                <div class="modal-stat-label">Hit Points</div>
                <div class="modal-stat-value">${card.hitpoints || '--'}</div>
            </div>
        </div>
    `;
    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('cardModal').classList.remove('active');
}