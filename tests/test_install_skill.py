import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools/install_skill.py"
spec = importlib.util.spec_from_file_location("install_skill", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallSkillTests(unittest.TestCase):
    def test_all_clients_receive_the_complete_same_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            for client, folder in installer.CLIENT_DIRS.items():
                with self.subTest(client=client):
                    target = installer.install(client, home=directory)
                    self.assertEqual(target, Path(directory) / folder / "skills/saas-builder")
                    originals = {p.relative_to(installer.SOURCE): p.read_bytes()
                                 for p in installer.SOURCE.rglob("*")
                                 if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
                    copies = {p.relative_to(target): p.read_bytes()
                              for p in target.rglob("*") if p.is_file()}
                    self.assertEqual(originals, copies)

    def test_existing_skill_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            target = installer.install("claude-code", home=directory)
            sentinel = target / "SKILL.md"
            sentinel.write_text("User changes")
            with self.assertRaises(FileExistsError):
                installer.install("claude-code", home=directory)
            self.assertEqual(sentinel.read_text(), "User changes")

    def test_broken_symlink_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / ".cursor/skills/saas-builder"
            target.parent.mkdir(parents=True)
            target.symlink_to(Path(directory) / "missing", target_is_directory=True)
            with self.assertRaises(FileExistsError):
                installer.install("cursor", home=directory)
            self.assertTrue(target.is_symlink())

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            target = installer.install("cursor", home=directory, dry_run=True)
            self.assertFalse(target.parent.exists())

    def test_project_scope_and_invalid_options(self):
        with tempfile.TemporaryDirectory() as directory:
            target = installer.install("cursor", scope="project", project_dir=directory)
            self.assertTrue(target.is_dir())
            with self.assertRaises(ValueError):
                installer.install("cursor", scope="project")
            with self.assertRaises(ValueError):
                installer.install("cursor", project_dir=directory)
            with self.assertRaises(ValueError):
                installer.install("cursor", scope="project", project_dir=Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
