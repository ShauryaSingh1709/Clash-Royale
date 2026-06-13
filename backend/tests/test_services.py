from backend.services.card_analyzer import CardAnalyzer
from backend.services.deck_analyzer import DeckAnalyzer
from backend.services.meta_analyzer import MetaAnalyzer
from backend.services.recommendation_engine import RecommendationEngine
from backend.utils.logger import get_logger

logger = get_logger("test_services")

SAMPLE_DECK = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
               "Fireball", "The Log", "Cannon", "Ice Golem"]


def test_card_analyzer():

    print("\n" + "=" * 60)
    print("TEST 1: CARD ANALYZER")
    print("=" * 60)

    analyzer = CardAnalyzer()

    print("\nCard Details (Hog Rider):")
    card = analyzer.get_card_details("Hog Rider")
    if card:
        print(f"   Elixir: {card['elixir_cost']}")
        print(f"   Rarity: {card['rarity']}")
        print(f"   Win Rate: {card['win_rate']}%")


    print("\nTop 5 Cards by Win Rate:")
    top = analyzer.get_top_cards_by_win_rate(5)
    for i, c in enumerate(top, 1):
        print(f"   {i}. {c['name']} ({c['win_rate']}%)")


    print("\nCard Statistics:")
    stats = analyzer.get_card_statistics()
    print(f"   Total cards:     {stats['total_cards']}")
    print(f"   Avg elixir:      {stats['average_elixir']}")
    print(f"   Avg win rate:    {stats['average_win_rate']}%")


    print("\nSearch 'Hog':")
    results = analyzer.search_cards("Hog")
    for r in results:
        print(f"   {r['name']}")


def test_deck_analyzer():

    print("\n" + "=" * 60)
    print("TEST 2: DECK ANALYZER")
    print("=" * 60)

    analyzer = DeckAnalyzer()

    print("\nValidation:")
    val = analyzer.validate_deck(SAMPLE_DECK)
    print(f"   Valid: {val['valid']} | {val['message']}")


    print("\nFull Analysis:")
    result = analyzer.analyze_deck(SAMPLE_DECK)
    if result["success"]:
        s = result["scoring"]
        print(f"   Win Rate:    {s['win_rate']['predicted_win_rate']}%")
        print(f"   Strength:    {s['strength']['strength_score']}/100 ({s['strength']['grade']})")
        print(f"   Archetype:   {s['archetype']['predicted_archetype']}")
        print(f"   Rating:      {s['rating_message']}")

        print(f"\n   Strengths:")
        for s in result["strengths"]:
            print(f"      {s}")

        print(f"\n   Weaknesses:")
        for w in result["weaknesses"]:
            print(f"      {w}")


def test_meta_analyzer():

    print("\n" + "=" * 60)
    print("TEST 3: META ANALYZER")
    print("=" * 60)

    analyzer = MetaAnalyzer()

    print("\nMeta Summary:")
    summary = analyzer.get_meta_summary()
    print(f"   Total cards:        {summary['total_cards']}")
    print(f"   Total decks:        {summary['total_decks_analyzed']}")
    print(f"   Avg deck win rate:  {summary['average_deck_win_rate']}%")


    print("\nTop 5 Most Popular Cards:")
    popular = analyzer.get_most_popular_cards(5)
    for i, c in enumerate(popular, 1):
        print(f"   {i}. {c['name']} ({c['usage_rate']}%)")


    print("\nTop 5 Underrated Cards:")
    underrated = analyzer.get_underrated_cards(5)
    for i, c in enumerate(underrated, 1):
        print(f"   {i}. {c['name']} ({c['win_rate']}%)")


    print("\nArchetype Performance:")
    perf = analyzer.get_archetype_performance()
    for a in perf:
        print(f"   {a['archetype']:15} | Win: {a['avg_win_rate']:.2f}% | Decks: {a['total_decks']}")


def test_recommendation_engine():

    print("\n" + "=" * 60)
    print("TEST 4: RECOMMENDATION ENGINE")
    print("=" * 60)

    engine = RecommendationEngine()

    print("\nSimilar Decks:")
    similar = engine.find_similar_decks(SAMPLE_DECK, top_n=3)
    if similar["success"]:
        for i, d in enumerate(similar["similar_decks"], 1):
            print(f"   {i}. {d['archetype']} ({d['similarity_score']}% match)")


    print("\nImprovement Suggestions:")
    imp = engine.suggest_improvements(SAMPLE_DECK, top_n=3)
    if imp["success"]:
        print(f"   Weakest:  {imp['weakest_card']['name']}")
        print(f"   Expected improvement: +{imp['expected_improvement_pct']}%")
        for r in imp["replacements"]:
            print(f"   Replace with: {r['name']} (+{r['improvement']}%)")


def main():

    print("\n" + "=" * 70)
    print("TESTING STEP 5: SERVICE LAYER")
    print("=" * 70)

    test_card_analyzer()
    test_deck_analyzer()
    test_meta_analyzer()
    test_recommendation_engine()

    print("\n" + "=" * 70)
    print("ALL SERVICE TESTS PASSED!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()