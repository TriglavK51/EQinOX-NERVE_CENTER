"""Base contract for workspace-discoverable skills."""

from abc import ABC, abstractmethod
from typing import Any


class SkillBase(ABC):
    """Minimal contract implemented by dynamically discovered skills."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the stable, human-readable skill name."""

    @abstractmethod
    def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute the skill using structured input and output."""
