import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "format-content"
SCRIPTS = SKILL_ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
        cwd=SKILL_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class ScriptIntegrationTests(unittest.TestCase):
    def test_valid_section_passes_without_warnings(self):
        result = run_script(
            "validate_gzh_html.py", FIXTURES / "valid-section.html"
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("WARNING", result.stdout)

    def test_invalid_section_fails_validation(self):
        result = run_script(
            "validate_gzh_html.py", FIXTURES / "invalid-section.html"
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("<div> 会被改写", result.stdout)

    def test_preview_embeds_clean_section_once_in_copy_target(self):
        clean = (FIXTURES / "valid-section.html").read_text(
            encoding="utf-8"
        ).strip()
        with tempfile.TemporaryDirectory() as temp_dir:
            preview_path = Path(temp_dir) / "preview.html"
            result = run_script(
                "wrap_preview.py",
                FIXTURES / "valid-section.html",
                preview_path,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            preview = preview_path.read_text(encoding="utf-8")

        copy_target = f'<div id="gzh-content">\n{clean}\n  </div>'
        self.assertIn(copy_target, preview)
        self.assertEqual(preview.count(clean), 1)

    def test_component_lint_reports_zero_errors(self):
        result = run_script("component_lint.py", SKILL_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ERROR×0", result.stdout)


if __name__ == "__main__":
    unittest.main()
