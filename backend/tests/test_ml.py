"""
Test ML integration: ModelLoader + MLPredictor
Run: python -m backend.tests.test_ml
"""

import json
from backend.ml.model_loader import ModelLoader
from backend.ml.predictor import MLPredictor
from backend.utils.logger import get_logger

logger = get_logger("test_ml")


def test_model_loader():
    """Test ModelLoader loads all models."""
    print("\n" + "=" * 60)
    print("🤖 TEST 1: MODEL LOADER")
    print("=" * 60)

    loader = ModelLoader()
    info = loader.get_model_info()

    print(f"\n📊 Loaded Models: {info['total_models']}")
    for model in info['loaded_models']:
        print(f"   ✅ {model}")

    print(f"\n📂 Models Path:        {info['models_path']}")
    print(f"🃏 Valid Cards Count:  {info['valid_cards_count']}")
    print(f"🏆 Archetypes:         {', '.join(info['available_archetypes'])}")


def test_predictor():
    """Test all ML predictions on sample deck."""
    print("\n" + "=" * 60)
    print("🔮 TEST 2: ML PREDICTOR")
    print("=" * 60)

    predictor = MLPredictor()

    # Sample deck: Classic Hog Cycle
    sample_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
                   "Fireball", "The Log", "Cannon", "Ice Golem"]

    print(f"\n🎴 SAMPLE DECK:")
    for i, card in enumerate(sample_deck, 1):
        print(f"   {i}. {card}")

    # ── Win Rate ────────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print(f"🎯 WIN RATE PREDICTION")
    print(f"{'─' * 60}")
    wr = predictor.predict_win_rate(sample_deck)
    print(f"   Win Rate:   {wr['predicted_win_rate']}%")
    print(f"   Confidence: {wr['confidence']}")

    # ── Strength ───────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print(f"💪 DECK STRENGTH")
    print(f"{'─' * 60}")
    st = predictor.predict_strength(sample_deck)
    print(f"   Strength:   {st['strength_score']}/100")
    print(f"   Grade:      {st['grade']}")

    # ── Archetype ──────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print(f"🏷️  ARCHETYPE CLASSIFICATION")
    print(f"{'─' * 60}")
    arch = predictor.predict_archetype(sample_deck)
    print(f"   Archetype:  {arch['predicted_archetype']}")
    print(f"   Confidence: {arch['confidence']}%")
    print(f"   All probabilities:")
    for a, p in arch['all_probabilities'].items():
        print(f"      • {a:15} {p}%")

    # ── Similar Decks ──────────────────────────────────────
    print(f"\n{'─' * 60}")
    print(f"🔍 TOP 3 SIMILAR DECKS")
    print(f"{'─' * 60}")
    similar = predictor.find_similar_decks(sample_deck, top_n=3)
    for i, d in enumerate(similar, 1):
        print(f"   #{i} Similarity: {d['similarity_score']}% | "
              f"Win Rate: {d['win_rate']}% | {d['archetype']}")

    # ── Suggestions ────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print(f"💡 IMPROVEMENT SUGGESTIONS")
    print(f"{'─' * 60}")
    sug = predictor.suggest_card_replacements(sample_deck, top_n=3)
    if sug['weakest_card']:
        print(f"   ❌ Weakest: {sug['weakest_card']['name']} "
              f"({sug['weakest_card']['win_rate']:.2f}%)")
        print(f"   ✨ Suggested replacements:")
        for r in sug['replacements']:
            print(f"      • {r['name']:20} (+{r['improvement']}% better)")


def test_predict_all():
    """Test ultimate predict_all() method."""
    print("\n" + "=" * 60)
    print("🎯 TEST 3: ALL-IN-ONE PREDICTION")
    print("=" * 60)

    predictor = MLPredictor()
    sample_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
                   "Fireball", "The Log", "Cannon", "Ice Golem"]

    result = predictor.predict_all(sample_deck)

    print(f"\n🎴 Complete Analysis Generated!")
    print(f"   • Win Rate:       {result['win_rate_prediction']['predicted_win_rate']}%")
    print(f"   • Strength:       {result['strength_prediction']['strength_score']}/100 "
          f"({result['strength_prediction']['grade']})")
    print(f"   • Archetype:      {result['archetype_prediction']['predicted_archetype']}")
    print(f"   • Similar Decks:  {len(result['similar_decks'])}")
    print(f"   • Suggestions:    {len(result['improvement_suggestions']['replacements'])}")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🧪 TESTING STEP 4: ML INTEGRATION")
    print("=" * 70)

    test_model_loader()
    test_predictor()
    test_predict_all()

    print("\n" + "=" * 70)
    print("🎉 ALL ML TESTS PASSED!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()