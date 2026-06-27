# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Jean-Sébastien Beaulieu

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCAN_EXTENSIONS = {
    ".md",
    ".py",
    ".txt",
    ".toml",
    ".yml",
    ".yaml",
    ".json",
    ".jsonl",
}


def project_text_files() -> list[Path]:
    ignored_parts = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        if path.suffix.lower() in SCAN_EXTENSIONS or path.name in {
            "LICENSE",
            "NOTICE",
        }:
            files.append(path)
    return files


class GovernanceFileTests(unittest.TestCase):
    def test_required_governance_files_exist(self) -> None:
        required = [
            "LICENSE",
            "NOTICE",
            "README.md",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "LICENSE_POLICY.md",
        ]
        missing = [name for name in required if not (ROOT / name).is_file()]
        self.assertEqual([], missing)

    def test_license_and_notice_identity(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        notice_text = (ROOT / "NOTICE").read_text(encoding="utf-8")
        self.assertIn("GNU AFFERO GENERAL PUBLIC LICENSE", license_text)
        self.assertIn("Version 3, 19 November 2007", license_text)
        self.assertIn("AGPL-3.0-or-later", notice_text)
        self.assertIn("https://orcid.org/0009-0007-2904-0443", notice_text)
        self.assertIn("Neutro", notice_text)

    def test_project_python_files_have_spdx_headers(self) -> None:
        missing: list[str] = []
        for path in [*ROOT.joinpath("src").rglob("*.py"), *ROOT.joinpath("tests").rglob("*.py")]:
            text = path.read_text(encoding="utf-8")
            if "SPDX-License-Identifier: AGPL-3.0-or-later" not in text:
                missing.append(str(path.relative_to(ROOT)))
            if "Copyright (C) 2026 Jean-Sébastien Beaulieu" not in text:
                missing.append(str(path.relative_to(ROOT)))
        self.assertEqual([], missing)

    def test_reserved_private_name_does_not_leak(self) -> None:
        reserved = "Neu" + "UuR-o"
        leaks = []
        for path in project_text_files():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if reserved in text:
                leaks.append(str(path.relative_to(ROOT)))
        self.assertEqual([], leaks)

    def test_confirmed_accusation_language_is_absent(self) -> None:
        phrases = [
            "theft " + "confirmed",
            "vol " + "confirme",
            "vol " + "confirm" + "\u00e9",
        ]
        leaks = []
        for path in project_text_files():
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for phrase in phrases:
                if phrase in text:
                    leaks.append(f"{path.relative_to(ROOT)}: {phrase}")
        self.assertEqual([], leaks)


if __name__ == "__main__":
    unittest.main()
