

const API_BASE = '/api/v1';

const API = {
    
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                headers: { 'Content-Type': 'application/json' },
                ...options
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    
    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    
    post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body)
        });
    },

    
    
    
    cards: {
        getAll(filters = {}) {
            const params = new URLSearchParams(filters).toString();
            return API.get(`/cards${params ? '?' + params : ''}`);
        },
        getDetails(name) {
            return API.get(`/cards/${encodeURIComponent(name)}`);
        },
        search(query) {
            return API.get(`/cards/search?q=${encodeURIComponent(query)}`);
        },
        getTopByWinRate(n = 10) {
            return API.get(`/cards/top/win-rate?n=${n}`);
        },
        getTopByUsage(n = 10) {
            return API.get(`/cards/top/usage?n=${n}`);
        },
        getStats() {
            return API.get('/cards/stats');
        }
    },

    
    
    
    decks: {
        analyze(cards) {
            return API.post('/decks/analyze', { cards });
        },
        validate(cards) {
            return API.post('/decks/validate', { cards });
        },
        score(cards) {
            return API.post('/decks/score', { cards });
        }
    },

    
    
    
    meta: {
        getSummary() {
            return API.get('/meta/summary');
        },
        getPopular(n = 10) {
            return API.get(`/meta/popular?n=${n}`);
        },
        getUnderrated(n = 10) {
            return API.get(`/meta/underrated?n=${n}`);
        },
        getArchetypes() {
            return API.get('/meta/archetypes');
        },
        getTrends() {
            return API.get('/meta/trends');
        },
        getTopDecks(n = 10) {
            return API.get(`/meta/top-decks?n=${n}`);
        }
    },

    
    
    
    recommend: {
        similar(cards, top_n = 5) {
            return API.post('/recommend/similar', { cards, top_n });
        },
        improvements(cards, top_n = 3) {
            return API.post('/recommend/improvements', { cards, top_n });
        },
        full(cards) {
            return API.post('/recommend/full', { cards });
        }
    }
};