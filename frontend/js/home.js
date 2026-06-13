/* ==========================================================================
   🏠 HOME PAGE - Animate Stats
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const data = await API.meta.getSummary();
        const summary = data.summary;

        animateValue('statCards', 0, summary.total_cards, 1500);
        animateValue('statDecks', 0, summary.total_decks_analyzed, 1500);
        animateValue('statBattles', 0, 5000, 1500);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
});

function animateValue(id, start, end, duration) {
    const element = document.getElementById(id);
    if (!element) return;

    const startTime = performance.now();
    const update = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (end - start) * easeOut);
        element.textContent = current >= 1000 ? (current / 1000).toFixed(1) + 'K' : current;
        if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
}