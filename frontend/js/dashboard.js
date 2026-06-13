/* ==========================================================================
   📊 DASHBOARD LOGIC - Charts + Premium Top Decks
   ========================================================================== */

const CHART_COLORS = [
    '#FFD700', '#FF6B35', '#4FC3F7', '#9B5DE5', '#06D6A0',
    '#E63946', '#FFB627', '#A8DADC', '#F15BB5', '#00BBF9'
];

Chart.defaults.color = '#B8BCD4';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.font.family = "'Inter', sans-serif";

document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([
        loadPopularChart(),
        loadWinRateChart(),
        loadArchetypeChart(),
        loadTrendsChart(),
        loadTopDecks()
    ]);
});

// ── POPULAR CARDS CHART ──────────────────────────────────────────
async function loadPopularChart() {
    try {
        const data = await API.meta.getPopular(10);
        const cards = data.cards;

        new Chart(document.getElementById('popularChart'), {
            type: 'bar',
            data: {
                labels: cards.map(c => c.name),
                datasets: [{
                    label: 'Usage Rate (%)',
                    data: cards.map(c => c.usage_rate),
                    backgroundColor: CHART_COLORS,
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    } catch (e) { console.error(e); }
}

// ── WIN RATE CHART ───────────────────────────────────────────────
async function loadWinRateChart() {
    try {
        const data = await API.cards.getTopByWinRate(10);
        const cards = data.cards;

        new Chart(document.getElementById('winRateChart'), {
            type: 'bar',
            data: {
                labels: cards.map(c => c.name),
                datasets: [{
                    label: 'Win Rate (%)',
                    data: cards.map(c => c.win_rate),
                    backgroundColor: 'rgba(6, 214, 160, 0.7)',
                    borderColor: '#06D6A0',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });
    } catch (e) { console.error(e); }
}

// ── ARCHETYPE CHART ──────────────────────────────────────────────
async function loadArchetypeChart() {
    try {
        const data = await API.meta.getArchetypes();
        const dist = data.distribution.counts;

        new Chart(document.getElementById('archetypeChart'), {
            type: 'doughnut',
            data: {
                labels: Object.keys(dist),
                datasets: [{
                    data: Object.values(dist),
                    backgroundColor: CHART_COLORS,
                    borderColor: '#0A0E2A',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    } catch (e) { console.error(e); }
}

// ── TRENDS CHART ─────────────────────────────────────────────────
async function loadTrendsChart() {
    try {
        const data = await API.meta.getTrends();
        const seasonal = data.trends.seasonal_data;

        new Chart(document.getElementById('trendsChart'), {
            type: 'line',
            data: {
                labels: seasonal.map(s => s.season),
                datasets: [
                    {
                        label: 'Avg Win Rate',
                        data: seasonal.map(s => s.avg_win_rate),
                        borderColor: '#FFD700',
                        backgroundColor: 'rgba(255, 215, 0, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Avg Usage',
                        data: seasonal.map(s => s.avg_usage),
                        borderColor: '#4FC3F7',
                        backgroundColor: 'rgba(79, 195, 247, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } catch (e) { console.error(e); }
}

// ══════════════════════════════════════════════════════════════════
// 🏆 TOP DECKS - PREMIUM DISPLAY WITH NAMES, TIERS, SOURCES
// ══════════════════════════════════════════════════════════════════
async function loadTopDecks() {
    const container = document.getElementById('topDecksList');
    try {
        const data = await API.meta.getTopDecks(10);
        const decks = data.decks;

        container.innerHTML = decks.map((deck, i) => {
            const cards = [
                deck.card_1, deck.card_2, deck.card_3, deck.card_4,
                deck.card_5, deck.card_6, deck.card_7, deck.card_8
            ];
            
            // Tier colors
            const tierColors = {
                'S': '#FFD700',
                'A': '#A78BFA',
                'B': '#60A5FA',
                'C': '#9CA3AF'
            };
            const tierColor = tierColors[deck.tier] || '#9CA3AF';
            
            // Use real deck name or fallback
            const deckName = deck.deck_name || `${deck.archetype} Deck #${i + 1}`;
            
            return `
                <div class="top-deck-item">
                    <div class="deck-rank">#${i + 1}</div>
                    
                    <div class="deck-info">
                        <div class="deck-info-header">
                            <strong class="deck-name">${deckName}</strong>
                            ${deck.tier ? `
                                <span class="deck-tier" style="background: ${tierColor}22; color: ${tierColor}; border-color: ${tierColor}55;">
                                    ${deck.tier}-Tier
                                </span>
                            ` : ''}
                        </div>
                        <div class="deck-info-meta">
                            <span><strong>${deck.archetype}</strong></span>
                            <span class="meta-dot">·</span>
                            <span>Avg Elixir: <strong>${deck.avg_elixir}</strong></span>
                            ${deck.source ? `
                                <span class="meta-dot">·</span>
                                <span class="deck-source">${deck.source}</span>
                            ` : ''}
                        </div>
                        <div class="deck-cards-display">
                            ${cards.map(c => `
                                <div class="deck-card-chip-img" title="${c}">
                                    <img src="${Utils.getCardImageUrl(c)}" 
                                         alt="${c}" 
                                         onerror="Utils.handleImageError(this)"
                                         style="width: 50px; height: 60px; object-fit: contain;">
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="deck-metric">
                        <div class="deck-metric-value">${deck.win_rate}%</div>
                        <div class="deck-metric-label">Win Rate</div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('Top decks error:', e);
        Utils.showError(container, 'Failed to load top decks');
    }
}