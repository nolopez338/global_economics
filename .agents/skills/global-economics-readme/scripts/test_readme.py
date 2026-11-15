"""Isolated behavioral regression tests; never writes repository example files."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from argparse import Namespace

SPEC = importlib.util.spec_from_file_location("readme", Path(__file__).with_name("readme.py"))
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)
REPO = Path(__file__).resolve().parents[4]


class Workflow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        template = self.root / m.TEMPLATE
        template.parent.mkdir(parents=True)
        template.write_bytes((REPO / m.TEMPLATE).read_bytes())
        self.target = self.root / "lessons"
        self.target.mkdir()
        (self.target / "lesson.tex").write_text("\\section{Café | decisión}\nRevenue minus cost.\n", encoding="utf-8")
        self.root, self.target, self.ident, self.cache = m.setup(self.root, "lessons")

    def tearDown(self):
        self.temp.cleanup()

    def scan(self, **kwargs):
        args = Namespace(force=False, dependency=[], drop_dependency=[], readme=None)
        for key, value in kwargs.items():
            setattr(args, key, value)
        result = m.scan(self.root, self.target, self.ident, self.cache, args)
        self.plan = m.load(Path(result["plan"]))
        return result

    def certify(self):
        p = self.plan
        p["analysis"]["purpose"] = "Provides classroom practice in profit modelling."
        for n, data in p["analysis"]["files"].items():
            data.update(type="LaTeX", description="Explains revenue, cost, and profit.", commands=[],
                        sections=[{"level": 1, "title": "Café | decisión", "description": "Introduces profit modelling."}])
        for n, data in p["analysis"]["folders"].items():
            data.update(description="Provides complementary classroom materials.", readme=next(iter(p["dirs"][n]), None))
        p.update(verified=p["review"], conformance=p["template"], reconciled=True)
        m.atomic(self.cache / "plan.json", json.dumps(p, ensure_ascii=False).encode())
        return m.commit(self.root, self.target, self.ident, self.cache, self.cache / "plan.json")

    def baseline(self):
        self.scan()
        return self.certify()

    def test_initial_and_unchanged(self):
        self.assertEqual(self.baseline()["status"], "created")
        output = self.target / "README.md"
        before = output.read_bytes(), output.stat().st_mtime_ns
        self.assertIn("Café &#124; decisión", output.read_text(encoding="utf-8"))
        self.assertEqual(self.scan()["review"], [])
        self.assertEqual(self.certify()["status"], "already current")
        self.assertEqual(before, (output.read_bytes(), output.stat().st_mtime_ns))

    def test_custom_name(self):
        (self.target / "README-lessons.md").write_text("Existing descriptions", encoding="utf-8")
        self.assertEqual(self.baseline()["status"], "updated")
        self.assertFalse((self.target / "README.md").exists())
        (self.target / "README-lessons.md").unlink()
        self.scan()
        self.assertEqual(self.plan["readme"], "README-lessons.md")
        self.assertEqual(self.certify()["status"], "created")

    def test_content_and_timestamp(self):
        self.baseline()
        source = self.target / "lesson.tex"
        old = source.stat()
        os.utime(source, ns=(old.st_atime_ns, old.st_mtime_ns + 1000000))
        self.assertEqual(self.scan()["review"], [])
        self.certify()
        source.write_text("Changed profit modelling", encoding="utf-8")
        self.assertIn("file:lesson.tex", self.scan()["content_changed"])

    def test_add_remove_rename(self):
        self.baseline()
        path = self.target / "new.tex"
        path.write_text("New model", encoding="utf-8")
        self.assertIn("file:new.tex", self.scan()["added"])
        self.certify()
        path.rename(self.target / "renamed.tex")
        report = self.scan()
        self.assertIn("file:new.tex", report["removed"])
        self.assertIn("file:renamed.tex", report["added"])
        self.certify()
        (self.target / "renamed.tex").unlink()
        self.assertIn("file:renamed.tex", self.scan()["removed"])

    def test_child_membership(self):
        self.baseline()
        child = self.target / "child"
        child.mkdir()
        self.assertIn("folder:child", self.scan()["added"])
        self.certify()
        readme = child / "README-child.md"
        readme.write_text("# Child\nExercises", encoding="utf-8")
        self.assertIn("folder:child", self.scan()["content_changed"])
        self.certify()
        readme.write_text("# Child\nExamples", encoding="utf-8")
        self.assertIn("child:child/README-child.md", self.scan()["content_changed"])
        self.certify()
        readme.rename(child / "README-renamed.md")
        report = self.scan()
        self.assertIn("child:child/README-child.md", report["removed"])
        # Selecting the newly renamed child summary is part of semantic review.
        self.plan["analysis"]["folders"]["child"]["readme"] = "README-renamed.md"
        self.certify()
        (child / "README-renamed.md").unlink()
        self.plan = None
        self.assertIn("folder:child", self.scan()["content_changed"])
        self.certify()
        child.rename(self.target / "renamed")
        report = self.scan()
        self.assertIn("folder:child", report["removed"])
        self.assertIn("folder:renamed", report["added"])

    def test_template_manual_missing_and_cache(self):
        self.baseline()
        template = self.root / m.TEMPLATE
        template.write_bytes(template.read_bytes() + b"\nUse exact subject names.\n")
        report = self.scan()
        self.assertTrue(report["template_review"])
        self.assertEqual(report["review"], [])
        self.certify()
        output = self.target / "README.md"
        output.write_text(output.read_text(encoding="utf-8") + "Manual note", encoding="utf-8")
        self.assertTrue(self.scan()["manual_output"])
        self.assertEqual(self.certify()["status"], "updated")
        output.unlink()
        self.assertTrue(self.scan()["manual_output"])
        self.assertEqual(self.certify()["status"], "created")
        state = self.cache / "state.json"
        state.unlink()
        self.assertTrue(self.scan()["baseline"])
        self.certify()
        state.write_text("corrupt", encoding="utf-8")
        self.assertTrue(self.scan()["baseline"])
        self.certify()
        corrupt = m.load(state)
        corrupt["analysis"]["files"]["lesson.tex"] = None
        state.write_text(json.dumps(corrupt), encoding="utf-8")
        self.assertTrue(self.scan()["baseline"])

    def test_exclusions_and_force(self):
        for name in ["old.pdf", "tracked.aux", "compile.bat", "slide.nav", "file.synctex.gz"]:
            (self.target / name).write_text("artifact", encoding="utf-8")
        self.baseline()
        self.assertEqual(list(self.plan["analysis"]["files"]), ["lesson.tex"])
        source = self.target / "lesson.tex"
        old = source.stat()
        data = source.read_bytes()
        source.write_bytes(data.replace(b"cost", b"gain"))
        os.utime(source, ns=(old.st_atime_ns, old.st_mtime_ns))
        self.assertEqual(self.scan()["review"], [])
        self.assertIn("file:lesson.tex", self.scan(force=True)["content_changed"])

    def test_dependency_and_concurrent_edit(self):
        dep = self.root / "sections.tex"
        dep.write_text("Custom section definition", encoding="utf-8")
        self.scan(dependency=["sections.tex=file:lesson.tex"])
        self.certify()
        dep.write_text("Changed custom section definition", encoding="utf-8")
        self.assertIn("file:lesson.tex", self.scan()["review"])
        self.certify()
        self.scan()
        (self.target / "lesson.tex").write_text("Concurrent source edit", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Inputs changed"):
            self.certify()

    def test_dependency_removal_invalidates_owner(self):
        (self.root / "sections.tex").write_text("Custom heading", encoding="utf-8")
        self.scan(dependency=["sections.tex=file:lesson.tex"])
        self.certify()
        self.assertIn("file:lesson.tex", self.scan(drop_dependency=["sections.tex"])["review"])

    def test_ambiguous_and_structural_template(self):
        for name in ["README-a.md", "README-b.md"]:
            (self.target / name).write_text("# Notes", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            self.scan()
        self.scan(readme="README-b.md")
        self.certify()
        template = self.root / m.TEMPLATE
        template.write_text(template.read_text(encoding="utf-8").replace("## Purpose", "## Role"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "structure changed"):
            self.scan(readme="README-b.md")

    def test_validation_and_incomplete(self):
        self.scan()
        with self.assertRaisesRegex(ValueError, "conformance"):
            m.commit(self.root, self.target, self.ident, self.cache, self.cache / "plan.json")
        self.plan["analysis"]["purpose"] = "Links [missing](absent.tex)."
        with self.assertRaisesRegex(ValueError, "Invalid/excluded link"):
            m.validate("# Directory Summary\n" + "\n".join("## " + h for h in m.HEADINGS) +
                       "\n[missing](absent.tex)", self.target, "README.md", m.rules(self.root)[1], self.plan["inputs"])


if __name__ == "__main__":
    unittest.main()
