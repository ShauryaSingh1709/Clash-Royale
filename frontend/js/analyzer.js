/* ==========================================================================
   🎯 DECK ANALYZER LOGIC
   ========================================================================== */

let allCards = [];
let currentDeck = [];
let currentFilter = 'all';
let currentSearch = '';

document.addEventListener('DOMContentLoaded', async () => {
    initDeckSlots();
    await loadCards();
    initEventListeners();
});

// ── INIT DECK SLOTS ───────────────────────────────────────────────
function initDeckSlots() {
    const slotsContainer = document.getElementById('deckSlots');
    slotsContainer.innerHTML = '';
    for (let i = 0; i < 8; i++) {
        const slot = document.createElement('div');
        slot.className = 'deck-slot';
        slot.dataset.index = i;
        slot.innerHTML = '<div class="deck-slot-empty">+</div>';
        slot.addEventListener('click', () => removeFromDeck(i));
        slotsContainer.appendChild(slot);
    }
}

// ── LOAD CARDS FROM API ───────────────────────────────────────────
async function loadCards() {
    try {
        const data = await API.cards.getAll();
        allCards = data.cards;
        renderCardPool();
    } catch (error) {
        Utils.showError(document.getElementById('cardsPool'), 'Failed to load cards');
    }
}

// ── RENDER CARD POOL ──────────────────────────────────────────────
function renderCardPool() {
    const pool = document.getElementById('cardsPool');
    let filtered = allCards;

    if (currentFilter !== 'all') {
        filtered = filtered.filter(c => c.rarity === currentFilter);
    }

    if (currentSearch) {
        filtered = filtered.filter(c =>
            c.name.toLowerCase().includes(currentSearch.toLowerCase())
        );
    }

    if (filtered.length === 0) {
        pool.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:2rem;grid-column:1/-1;">No cards found</p>';
        return;
    }

    pool.innerHTML = filtered.map(card => {
        const isInDeck = currentDeck.includes(card.name);
        const rarityColor = Utils.getRarityColor(card.rarity);
        return `
            <div class="pool-card ${isInDeck ? 'added' : ''}" 
                 data-name="${card.name}"
                 onclick="addToDeck('${card.name.replace(/'/g, "\\'")}')"
                 style="border-color: ${isInDeck ? rarityColor : ''};">
                <div class="pool-card-elixir">${card.elixir_cost}</div>
                <img src="${Utils.getCardImageUrl(card.name)}" 
                     alt="${card.name}" 
                     onerror="Utils.handleImageError(this)"
                     style="width: 70px; height: 85px; object-fit: contain; margin: 0 auto; display: block;">
                <div class="pool-card-name">${card.name}</div>
                <div class="pool-card-rarity" style="color: ${rarityColor};">
                    ${card.rarity}
                </div>
            </div>
        `;
    }).join('');
}

// ── ADD CARD TO DECK ──────────────────────────────────────────────
function addToDeck(cardName) {
    if (currentDeck.length >= 8) {
        Utils.showToast('Deck is full! Remove a card first.', 'error');
        return;
    }
    if (currentDeck.includes(cardName)) {
        Utils.showToast('Card already in deck', 'error');
        return;
    }

    currentDeck.push(cardName);
    updateDeckDisplay();
    renderCardPool();
}

// ── REMOVE CARD FROM DECK ─────────────────────────────────────────
function removeFromDeck(index) {
    if (currentDeck[index]) {
        currentDeck.splice(index, 1);
        updateDeckDisplay();
        renderCardPool();
    }
}

// ── UPDATE DECK DISPLAY ───────────────────────────────────────────
function updateDeckDisplay() {
    const slots = document.querySelectorAll('.deck-slot');
    slots.forEach((slot, i) => {
        const cardName = currentDeck[i];
        if (cardName) {
            const card = allCards.find(c => c.name === cardName);
            slot.classList.add('filled');
            slot.innerHTML = `
                <div class="deck-slot-elixir">${card.elixir_cost}</div>
                <div class="deck-slot-card">
                    <img src="${Utils.getCardImageUrl(card.name)}" 
                         alt="${card.name}" 
                         onerror="Utils.handleImageError(this)"
                         style="width: 100%; height: 70px; object-fit: contain;">
                    <div class="deck-slot-name">${card.name}</div>
                </div>
            `;
        } else {
            slot.classList.remove('filled');
            slot.innerHTML = '<div class="deck-slot-empty">+</div>';
        }
    });

    document.getElementById('deckCount').textContent = currentDeck.length;
    document.getElementById('analyzeBtn').disabled = currentDeck.length !== 8;
}

// ── EVENT LISTENERS ───────────────────────────────────────────────
function initEventListeners() {
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderCardPool();
        });
    });

    // Search
    document.getElementById('cardSearch').addEventListener('input', Utils.debounce((e) => {
        currentSearch = e.target.value;
        renderCardPool();
    }, 300));

    // Clear deck
    document.getElementById('clearDeck').addEventListener('click', () => {
        currentDeck = [];
        updateDeckDisplay();
        renderCardPool();
        document.getElementById('analysisResults').style.display = 'none';
    });

    // Random deck
    document.getElementById('randomDeck').addEventListener('click', () => {
        const shuffled = [...allCards].sort(() => Math.random() - 0.5);
        currentDeck = shuffled.slice(0, 8).map(c => c.name);
        updateDeckDisplay();
        renderCardPool();
    });

    // Analyze button
    document.getElementById('analyzeBtn').addEventListener('click', analyzeDeck);
}

// ── ANALYZE DECK ──────────────────────────────────────────────────
async function analyzeDeck() {
    const resultsDiv = document.getElementById('analysisResults');
    const contentDiv = document.getElementById('resultsContent');

    resultsDiv.style.display = 'block';
    Utils.showLoading(contentDiv, 'Analyzing deck with AI...');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        const data = await API.recommend.full(currentDeck);

        if (!data.success) {
            Utils.showError(contentDiv, data.error);
            return;
        }

        renderResults(data, contentDiv);
    } catch (error) {
        Utils.showError(contentDiv, error.message);
    }
}

// ── RENDER RESULTS ────────────────────────────────────────────────
function renderResults(data, container) {
    const ml = data.ml_predictions;
    const analysis = data.analysis;
    const improvements = data.improvements;
    const similar = data.similar_decks;

    const gradeColor = Utils.getGradeColor(ml.strength.grade);
    const archetypeIcon = Utils.getArchetypeIcon(ml.archetype.predicted_archetype);

    container.innerHTML = `
        <!-- Summary Cards -->
        <div class="results-summary animate-fadeIn">
            <div class="result-card">
                <div class="result-card-icon">📈</div>
                <div class="result-card-label">Win Rate</div>
                <div class="result-card-value">${ml.win_rate.predicted_win_rate}%</div>
                <div class="result-card-sub">${ml.win_rate.confidence} Confidence</div>
            </div>

            <div class="result-card">
                <div class="result-card-icon">💪</div>
                <div class="result-card-label">Strength Score</div>
                <div class="result-card-value">${ml.strength.strength_score}</div>
                <div class="result-card-sub">/ 100</div>
            </div>

            <div class="result-card">
                <div class="result-card-icon">🏆</div>
                <div class="result-card-label">Grade</div>
                <div class="grade-display" style="color: ${gradeColor};">
                    ${ml.strength.grade}
                </div>
            </div>

            <div class="result-card">
                <div class="result-card-icon">${archetypeIcon}</div>
                <div class="result-card-label">Archetype</div>
                <div class="result-card-value" style="font-size: 1.5rem;">
                    ${ml.archetype.predicted_archetype}
                </div>
                <div class="result-card-sub">${ml.archetype.confidence}% confident</div>
            </div>
        </div>

        <!-- Rating Message -->
        <div class="analysis-block animate-fadeIn">
            <h3>🎯 Overall Rating</h3>
            <p style="font-size: 1.2rem; color: var(--text-primary);">
                ${analysis.scoring.rating_message}
            </p>
        </div>

        <!-- Strengths -->
        <div class="analysis-block animate-fadeIn">
            <h3>💪 Strengths</h3>
            <ul class="list-items">
                ${analysis.strengths.map(s => `<li>${s}</li>`).join('')}
            </ul>
        </div>

        <!-- Weaknesses -->
        <div class="analysis-block animate-fadeIn">
            <h3>⚠️ Weaknesses</h3>
            <ul class="list-items weakness-list">
                ${analysis.weaknesses.map(w => `<li>${w}</li>`).join('')}
            </ul>
        </div>

        <!-- Improvements -->
        ${improvements.weakest_card ? `
        <div class="analysis-block animate-fadeIn">
            <h3>💡 Suggested Improvements</h3>
            <p style="margin-bottom: 1rem;">
                ❌ Weakest card: <strong style="color: var(--color-danger);">
                ${improvements.weakest_card.name}</strong>
                (${improvements.weakest_card.win_rate}%)
            </p>
            <p style="margin-bottom: 1rem;">Recommended replacements:</p>
            ${improvements.replacements.map(r => `
                <div class="replacement-card">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <img src="${Utils.getCardImageUrl(r.name)}" 
                             alt="${r.name}" 
                             onerror="Utils.handleImageError(this)"
                             style="width: 50px; height: 60px; object-fit: contain;">
                        <div>
                            <strong>${r.name}</strong>
                            <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.25rem;">
                                ⚡ ${r.elixir_cost} | ${r.rarity} | Win Rate: ${r.win_rate}%
                            </div>
                        </div>
                    </div>
                    <span class="improvement-badge">+${r.improvement}%</span>
                </div>
            `).join('')}
        </div>
        ` : ''}

        <!-- Similar Decks -->
        ${similar.length > 0 ? `
        <div class="analysis-block animate-fadeIn">
            <h3>🔍 Similar Decks</h3>
            ${similar.map((deck, i) => `
                <div class="similar-deck">
                    <div class="similar-deck-header">
                        <strong>Deck #${i + 1} - ${deck.archetype}</strong>
                        <span class="similarity-score">${deck.similarity_score}% match</span>
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.75rem;">
                        Win Rate: <strong style="color: var(--color-success);">${deck.win_rate}%</strong>
                        | Avg Elixir: ${deck.avg_elixir}
                    </div>
                    <div class="deck-cards-list">
                        ${deck.cards.map(c => `
                            <div class="mini-card-img" title="${c}">
                                <img src="${Utils.getCardImageUrl(c)}" 
                                     alt="${c}" 
                                     onerror="Utils.handleImageError(this)"
                                     style="width: 45px; height: 55px; object-fit: contain;">
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        </div>
        ` : ''}
    `;
}