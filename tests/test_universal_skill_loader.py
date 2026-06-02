import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "universal_skill_loader.py"


def load_module():
    spec = importlib.util.spec_from_file_location("universal_skill_loader", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class UniversalSkillLoaderTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.source = self.root / "skills"
        self.source.mkdir()

        alpha = self.source / "alpha"
        alpha.mkdir()
        (alpha / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Alpha skill\n---\n\n# Alpha\n",
            encoding="utf-8",
        )
        (alpha / "helper.sh").write_text("#!/usr/bin/env bash\necho alpha\n", encoding="utf-8")

        beta = self.source / "beta"
        beta.mkdir()
        (beta / "skill.md").write_text(
            "---\nname: beta\ndescription: Beta skill\n---\n\n# Beta\n",
            encoding="utf-8",
        )

        hidden = self.source / ".ignored"
        hidden.mkdir()
        (hidden / "SKILL.md").write_text("# Hidden\n", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_discover_skills_supports_upper_and_lowercase_docs(self):
        module = load_module()

        skills = module.discover_skills(self.source)
        names = [skill.name for skill in skills]

        self.assertEqual(names, ["alpha", "beta"])
        self.assertEqual(skills[0].doc_path.name, "SKILL.md")
        self.assertEqual(skills[1].doc_path.name, "skill.md")

    def test_build_generates_codex_and_claude_skill_mirrors(self):
        module = load_module()
        output_dir = self.root / "generated"

        module.build_adapters(self.source, output_dir)

        for tool in ("codex", "claude"):
            skill_dir = output_dir / tool / "skills" / "beta"
            self.assertTrue(skill_dir.is_dir(), tool)
            self.assertTrue((skill_dir / "SKILL.md").exists(), tool)
            self.assertIn("name: beta", (skill_dir / "SKILL.md").read_text(encoding="utf-8"))

        helper_link = output_dir / "codex" / "skills" / "alpha" / "helper.sh"
        self.assertTrue(helper_link.exists())
        self.assertEqual(helper_link.read_text(encoding="utf-8"), "#!/usr/bin/env bash\necho alpha\n")

    def test_build_generates_cursor_loader_rule_and_catalog(self):
        module = load_module()
        output_dir = self.root / "generated"

        module.build_adapters(self.source, output_dir)

        rule_path = output_dir / "cursor" / ".cursor" / "rules" / "00-universal-skill-loader.mdc"
        catalog_path = output_dir / "cursor" / "skill-catalog.md"

        self.assertTrue(rule_path.exists())
        self.assertTrue(catalog_path.exists())
        rule_text = rule_path.read_text(encoding="utf-8")
        catalog_text = catalog_path.read_text(encoding="utf-8")

        self.assertIn(str(self.source), rule_text)
        self.assertIn("alpha", rule_text)
        self.assertIn("beta", catalog_text)
        self.assertIn("alpha/SKILL.md", catalog_text)

    def test_build_inlines_always_load_skill_into_global_loader_docs(self):
        module = load_module()
        output_dir = self.root / "generated"
        always_load = self.root / "always-load.json"
        always_load.write_text('["alpha"]\n', encoding="utf-8")

        module.build_adapters(self.source, output_dir, always_load_path=always_load)

        claude_text = (output_dir / "claude" / "CLAUDE.md").read_text(encoding="utf-8")
        codex_text = (output_dir / "codex" / "AGENTS.md").read_text(encoding="utf-8")
        cursor_text = (output_dir / "cursor" / ".cursor" / "rules" / "00-universal-skill-loader.mdc").read_text(
            encoding="utf-8"
        )

        self.assertIn("Always-Load Skills", claude_text)
        self.assertIn("Alpha skill", claude_text)
        self.assertIn("Always-Load Skills", codex_text)
        self.assertIn("Alpha skill", cursor_text)

    def test_install_inlines_loader_text_into_claude_and_codex_entry_files(self):
        module = load_module()
        output_dir = self.root / "generated"
        always_load = self.root / "always-load.json"
        always_load.write_text('["alpha"]\n', encoding="utf-8")
        claude_home = self.root / ".claude"
        codex_home = self.root / ".codex"
        cursor_home = self.root / ".cursor"

        module.install(
            source_dir=self.source,
            output_dir=output_dir,
            claude_home=claude_home,
            codex_home=codex_home,
            cursor_home=cursor_home,
            always_load_path=always_load,
        )

        self.assertIn("Always-Load Skills", (claude_home / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertIn("Alpha skill", (claude_home / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertIn("Always-Load Skills", (codex_home / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("Alpha skill", (codex_home / "AGENTS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
