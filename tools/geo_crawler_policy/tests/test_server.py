from tools.geo_crawler_policy.server import run


def test_policy_detects_missing_and_blocked_crawlers() -> None:
    result = run({"robotsTxt": "User-agent: GPTBot\nDisallow: /\n"})

    assert {finding["code"] for finding in result["report"]["findings"]} >= {
        "blocked_crawler",
        "unspecified_crawler",
    }


def test_policy_accepts_explicit_allow_rules() -> None:
    robots_txt = "\n".join(
        f"User-agent: {crawler}\nDisallow:"
        for crawler in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended")
    )

    assert run({"robotsTxt": robots_txt})["report"]["score"] == 100
