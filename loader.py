"""Load workspace skills declared by the local Nerve-Center manifest."""

from __future__ import annotations

import importlib.util
import json
import logging
from pathlib import Path

from skills.skill_base import SkillBase

LOGGER = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = PROJECT_ROOT / "manifest.json"


def load_skills(manifest_path: Path = MANIFEST_PATH) -> list[SkillBase]:
    """Load concrete ``SkillBase`` implementations found in the manifest directory."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise RuntimeError(f"Cannot read manifest '{manifest_path}': {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON in manifest '{manifest_path}': {error}") from error

    skills_dir = manifest_path.parent / manifest.get("skills_dir", "skills")
    if not skills_dir.is_dir():
        raise RuntimeError(f"Configured skills directory does not exist: '{skills_dir}'")

    skills: list[SkillBase] = []
    for module_path in sorted(skills_dir.glob("*.py")):
        if module_path.name in {"__init__.py", "skill_base.py"}:
            continue
        module_name = f"workspace_skills.{module_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            LOGGER.error("Cannot create an import specification for '%s'.", module_path)
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except (
            Exception
        ) as error:  # noqa: BLE001 - discovery must report third-party skill failures.
            LOGGER.error("Cannot import skill module '%s': %s", module_path.name, error)
            continue
        for candidate in vars(module).values():
            if (
                isinstance(candidate, type)
                and issubclass(candidate, SkillBase)
                and candidate is not SkillBase
            ):
                try:
                    skills.append(candidate())
                except Exception as error:  # noqa: BLE001 - a bad skill must not stop discovery.
                    LOGGER.error("Cannot instantiate skill '%s': %s", candidate.__name__, error)
    return skills


def main() -> None:
    """Print the names of all skills discovered from the workspace manifest."""
    logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
    skills = load_skills()
    print(f"Loaded {len(skills)} skill(s):")
    for skill in skills:
        print(f"- {skill.name}")


if __name__ == "__main__":
    main()
