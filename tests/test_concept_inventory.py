# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "concept_inventory"


class ConceptInventoryTests(unittest.TestCase):
    def test_required_inventory_files_exist(self):
        required = {
            "CASE_STUDY_INVENTORY.md",
            "REUSABLE_COMPONENT_MAP.md",
            "DO_NOT_REUSE_RISKS.md",
            "NEUTRO_IMPLEMENTATION_SOURCE_MAP.md",
            "FIRST_BUILD_BACKLOG.md",
        }
        missing = [name for name in sorted(required) if not (DOCS / name).is_file()]
        self.assertEqual([], missing)

    def test_required_lanes_are_covered(self):
        inventory = (DOCS / "CASE_STUDY_INVENTORY.md").read_text(encoding="utf-8")
        for lane in [
            "modele",
            "neutrosophique",
            "Quasicrystal",
            "swarm",
            "Memoire",
            "mechanique quantique",
            "biologie",
            "STUDY_CASE_FOUNDATION_PROCESS.md",
        ]:
            self.assertIn(lane, inventory)

    def test_public_name_is_neutro(self):
        source_map = (DOCS / "NEUTRO_IMPLEMENTATION_SOURCE_MAP.md").read_text(encoding="utf-8")
        self.assertIn("Neutro", source_map)
        self.assertIn("src/neutro/", source_map)

    def test_reserved_private_name_not_leaked(self):
        reserved = "Neu" + "UuR-o"
        checked_suffixes = {".md", ".py", ".txt", ".toml", ".yml", ".yaml", ".json"}
        leaks = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in checked_suffixes:
                continue
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            if reserved in path.read_text(encoding="utf-8", errors="ignore"):
                leaks.append(str(path.relative_to(ROOT)))
        self.assertEqual([], leaks)


if __name__ == "__main__":
    unittest.main()
