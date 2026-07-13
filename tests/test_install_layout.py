import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "format-content"


class InstallLayoutTests(unittest.TestCase):
    def test_installable_skill_is_nested_and_complete(self):
        self.assertFalse(
            (ROOT / "SKILL.md").exists(),
            "repository root must not contain SKILL.md",
        )

        required_files = (
            "SKILL.md",
            "references/theme-red-white.md",
            "references/common-components.md",
            "scripts/component_lint.py",
            "scripts/validate_gzh_html.py",
            "scripts/wrap_preview.py",
            "assets/preview-template.html",
            "agents/openai.yaml",
            "LICENSE",
            "NOTICE",
        )
        for relative_path in required_files:
            with self.subTest(path=relative_path):
                self.assertTrue(
                    (SKILL_ROOT / relative_path).is_file(),
                    f"missing installable Skill file: {relative_path}",
                )


if __name__ == "__main__":
    unittest.main()
