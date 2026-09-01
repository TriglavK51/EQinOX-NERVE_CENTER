"""Minimal example of a skill discovered by loader.py."""

from typing import Any

from skills.skill_base import SkillBase


class ExampleSkill(SkillBase):
    """Return the input unchanged to demonstrate the local skill contract."""

    @property
    def name(self) -> str:
        return "example"

    def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "input": input_data}
