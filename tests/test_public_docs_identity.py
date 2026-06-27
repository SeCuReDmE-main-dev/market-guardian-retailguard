# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublicDocsIdentityTests(unittest.TestCase):
    def test_readme_contains_construction_spaces(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Construction Philosophy", readme)
        self.assertIn("Jean-Sébastien Construction Space", readme)
        self.assertIn("Codex Construction Space", readme)
        self.assertIn("Integration Space", readme)

    def test_public_names_are_documented(self) -> None:
        combined = "\n".join(
            [
                (ROOT / "README.md").read_text(encoding="utf-8"),
                (ROOT / "NOTICE").read_text(encoding="utf-8"),
                (ROOT / "docs" / "vision" / "README.md").read_text(encoding="utf-8"),
            ]
        )
        self.assertIn("V.I.S Guardian", combined)
        self.assertIn("V.O.T Guardian", combined)
        self.assertIn("Neutro", combined)

    def test_construction_and_vision_docs_exist(self) -> None:
        required = [
            ROOT / "docs" / "construction" / "README.md",
            ROOT / "docs" / "construction" / "DUAL_CONSTRUCTION_SPACES.md",
            ROOT / "docs" / "construction" / "INTEGRATION_PROTOCOL.md",
            ROOT / "docs" / "vision" / "README.md",
            ROOT / "docs" / "vision" / "VIS_GUARDIAN_PRIMITIVES.md",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
