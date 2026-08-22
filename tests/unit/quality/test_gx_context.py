import great_expectations as gx


def test_gx_context_and_suites_exist() -> None:
    context = gx.get_context()  # type: ignore[attr-defined]
    suite_names = context.list_expectation_suite_names()

    expected_suites = [
        "market_quotes_suite",
        "price_history_suite",
        "news_articles_suite",
    ]

    for suite_name in expected_suites:
        assert suite_name in suite_names, f"Suite {suite_name} non-existent in GX context"
