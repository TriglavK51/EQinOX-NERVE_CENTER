"""Deterministic, local-only chain recipes R01-R10."""

from __future__ import annotations

from collections.abc import Iterable

RECIPES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "R01": (
        ("landing page", "strona", "website", "homepage"),
        ("artifacts_builder", "seo_technical", "security_best_practices"),
    ),
    "R02": (
        ("content seo", "artyku", "blog", "pozycjonowanie"),
        ("seo_audit", "seo_schema", "seo_technical"),
    ),
    "R03": (
        ("deploy", "wdroz", "production", "hosting"),
        ("security_best_practices", "docker_hub"),
    ),
    "R04": (
        ("nowy projekt", "new project", "setup", "inicjalizacja"),
        ("security_threat_model", "artifacts_builder"),
    ),
    "R05": (
        ("stworz skill", "nowy skill", "create skill"),
        ("artifacts_builder", "ponytail_review"),
    ),
    "R06": (
        ("audyt", "bezpieczenstwo", "pentest", "security"),
        ("security_threat_model", "security_best_practices"),
    ),
    "R07": (
        ("review", "przeglad kodu", "sprawdz kod", "refactor"),
        ("ponytail_review", "security_best_practices"),
    ),
    "R08": (("research", "prezentac", "slajdy"), ("artifacts_builder",)),
    "R09": (("raport", "dokument", "report", "brief"), ("artifacts_builder", "pdf")),
    "R10": (("sprawdz skille", "skill audit", "health check"), ("caveman", "ponytail_review")),
}


def build_chain(intent: str, available: Iterable[str], max_depth: int) -> list[str]:
    """Return the first matching executable recipe, bounded by max_depth."""
    normalized = intent.lower()
    available_names = set(available)
    for triggers, recipe in RECIPES.values():
        if any(trigger in normalized for trigger in triggers):
            return [name for name in recipe if name in available_names][:max_depth]
    return []
