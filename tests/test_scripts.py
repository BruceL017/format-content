import subprocess
import sys
import tempfile
import unittest
from html import escape
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


def run_validator_html(html):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_gzh_html.py"), "--stdin"],
        cwd=SKILL_ROOT,
        input=html,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class ScriptIntegrationTests(unittest.TestCase):
    def assert_structure_rejected(self, html):
        result = run_validator_html(html)
        diagnostics = result.stdout + result.stderr

        self.assertEqual(result.returncode, 1, diagnostics)
        self.assertIn("ERROR", diagnostics)

    def test_valid_section_passes_without_warnings(self):
        result = run_script(
            "validate_gzh_html.py", FIXTURES / "valid-section.html"
        )
        diagnostics = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, diagnostics)
        self.assertNotIn("WARNING", diagnostics)

    def test_validator_accepts_unclosed_html_void_elements(self):
        result = run_validator_html(
            '<section><p><span leaf="">正文。</span><br></p>'
            '<hr><img src="https://example.com/image.png" alt="示意图">'
            '</section>'
        )
        diagnostics = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, diagnostics)
        self.assertNotIn("WARNING", diagnostics)

    def test_validator_rejects_fragment_without_root_section(self):
        self.assert_structure_rejected(
            '<p><span leaf="">正文。</span></p>'
        )

    def test_validator_rejects_two_top_level_sections(self):
        self.assert_structure_rejected(
            '<section><span leaf="">第一段。</span></section>'
            '<section><span leaf="">第二段。</span></section>'
        )

    def test_validator_rejects_full_html_document(self):
        self.assert_structure_rejected(
            '<!DOCTYPE html><html><body>'
            '<section><span leaf="">正文。</span></section>'
            '</body></html>'
        )

    def test_validator_rejects_text_outside_root_section(self):
        self.assert_structure_rejected(
            'outside<section><span leaf="">正文。</span></section>'
        )

    def test_validator_rejects_unbalanced_markup(self):
        self.assert_structure_rejected(
            '<section><p><span leaf="">正文。</span></section>'
        )

    def test_warning_only_validation_exits_zero_but_reports_warning(self):
        result = run_validator_html(
            '<section><p><span leaf="">已包裹。</span>未包裹。</p></section>'
        )
        diagnostics = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, diagnostics)
        self.assertIn("WARNING ×1", diagnostics)

    def test_invalid_section_fails_validation(self):
        result = run_script(
            "validate_gzh_html.py", FIXTURES / "invalid-section.html"
        )
        diagnostics = result.stdout + result.stderr

        self.assertEqual(result.returncode, 1, diagnostics)
        self.assertIn("<div> 会被改写", diagnostics)

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

    def test_preview_escapes_title_before_marker_like_filename_text(self):
        clean = (FIXTURES / "valid-section.html").read_text(
            encoding="utf-8"
        ).strip()
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "literal-<!--GZH_CONTENT-->.html"
            preview_path = Path(temp_dir) / "preview.html"
            source_path.write_text(clean, encoding="utf-8")
            result = run_script(
                "wrap_preview.py",
                source_path,
                preview_path,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            preview = preview_path.read_text(encoding="utf-8")

        copy_target = f'<div id="gzh-content">\n{clean}\n  </div>'
        expected_title = (
            f"<title>{escape(source_path.stem)} · 公众号排版预览</title>"
        )
        self.assertEqual(preview.count(clean), 1)
        self.assertIn(copy_target, preview)
        self.assertIn(expected_title, preview)

    def test_component_lint_reports_zero_errors(self):
        result = run_script("component_lint.py", SKILL_ROOT)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ERROR×0", result.stdout)


if __name__ == "__main__":
    unittest.main()
