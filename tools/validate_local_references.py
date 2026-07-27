#!/usr/bin/env python3
"""Validate statically declared local references in repository HTML and CSS.

Run from the repository root.  EXCLUSIONS is intentionally kept in source so
every exception is reviewable; entries must represent verified parser false
positives, never known missing files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SCANNED_SUFFIXES = {".html", ".css"}
IGNORED_SCHEMES = {"data", "http", "https", "javascript", "mailto", "tel"}

# (source repository-relative path, original reference). Keep this empty unless
# a statically written value is proven to be a parser false positive.
EXCLUSIONS: frozenset[tuple[str, str]] = frozenset()

CSS_URL_RE = re.compile(r"url\(\s*(?P<quote>['\"]?)(?P<ref>.*?)(?P=quote)\s*\)", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(
    r"@import\s+(?!url\()[\"'](?P<ref>[^\"']+)[\"']", re.IGNORECASE
)
TEMPLATE_MARKERS = ("${", "{{", "}}", "<%", "%>")


@dataclass(frozen=True, order=True)
class Failure:
    source: str
    reference: str
    target: str
    reason: str


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for name, value in attrs:
            if name.lower() in {"href", "src"} and value:
                self.references.append(value)

    handle_startendtag = handle_starttag


def extract_references(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".html":
        parser = ReferenceParser()
        parser.feed(text)
        return parser.references

    references = [match.group("ref").strip() for match in CSS_URL_RE.finditer(text)]
    references.extend(match.group("ref").strip() for match in CSS_IMPORT_RE.finditer(text))
    return references


def normalize_reference(reference: str) -> str | None:
    value = reference.strip()
    if not value or value.startswith("#") or any(marker in value for marker in TEMPLATE_MARKERS):
        return None
    if value.startswith("//"):
        return None

    split = urlsplit(value)
    if split.scheme.lower() in IGNORED_SCHEMES or split.netloc:
        return None
    if split.scheme:
        return None

    path = unquote(split.path)
    return path or None


def resolve_reference(root: Path, source: Path, reference: str) -> tuple[Path | None, str | None]:
    normalized = normalize_reference(reference)
    if normalized is None:
        return None, None

    candidate = root / normalized.lstrip("/") if normalized.startswith("/") else source.parent / normalized
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        return resolved, "target escapes repository root"
    if not resolved.exists():
        return resolved, "target does not exist"
    return resolved, None


def repository_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SCANNED_SUFFIXES and ".git" not in path.parts
    )


def validate(root: Path) -> list[Failure]:
    failures: list[Failure] = []
    for source in repository_files(root):
        source_relative = source.relative_to(root).as_posix()
        for reference in extract_references(source):
            if (source_relative, reference) in EXCLUSIONS:
                continue
            target, reason = resolve_reference(root, source, reference)
            if reason is None:
                continue
            try:
                target_text = target.relative_to(root).as_posix() if target else "<not resolved>"
            except ValueError:
                target_text = str(target)
            failures.append(Failure(source_relative, reference, target_text, reason))
    return sorted(failures)


def run_self_tests() -> None:
    assert normalize_reference("#section") is None
    assert normalize_reference("https://example.test/a.css") is None
    assert normalize_reference("data:image/png;base64,abc") is None
    assert normalize_reference("images/a%20b.png?v=1#x") == "images/a b.png"
    assert normalize_reference("{{ dynamic_asset }}") is None

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory).resolve()
        (root / "pages").mkdir()
        source = root / "pages" / "index.html"
        source.write_text('<link href="../assets/site.css?v=1#top">', encoding="utf-8")
        (root / "assets").mkdir()
        (root / "assets" / "site.css").write_text("", encoding="utf-8")
        target, reason = resolve_reference(root, source, "../assets/site.css?v=1#top")
        assert reason is None and target == (root / "assets" / "site.css")
        _, reason = resolve_reference(root, source, "../../../outside.css")
        assert reason == "target escapes repository root"
        _, reason = resolve_reference(root, source, "missing.css")
        assert reason == "target does not exist"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run normalization and resolution self-tests first")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        print("Local-reference validator self-tests passed.")

    failures = validate(REPOSITORY_ROOT)
    if failures:
        print(f"Local-reference validation failed ({len(failures)} issue(s)):")
        for failure in failures:
            print(f"- source: {failure.source}")
            print(f"  reference: {failure.reference}")
            print(f"  target: {failure.target}")
            print(f"  reason: {failure.reason}")
        return 1

    print(f"Local-reference validation passed ({len(repository_files(REPOSITORY_ROOT))} files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
