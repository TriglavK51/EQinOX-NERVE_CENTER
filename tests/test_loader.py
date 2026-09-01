"""Integration checks for workspace skill discovery."""

from loader import load_skills


def test_loader_discovers_example_skill() -> None:
    skills = load_skills()

    assert [skill.name for skill in skills] == ["example"]
    assert skills[0].run({"source": "test"}) == {
        "status": "ok",
        "input": {"source": "test"},
    }
