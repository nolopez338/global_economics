"""Incremental README review planning and validated atomic publication (stdlib)."""
import argparse
import copy
import fnmatch
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import quote, unquote

SCHEMA = 1
VERSION = "1.0"
TEMPLATE = "book/preamble/template_README.md"
HEADINGS = ["Purpose", "Files", "Folders", "Directory Structure", "Public Commands", "Document Sections"]
EXTRA = ["*.nav", "*.snm", "*.vrb", "*.bcf", "*.run.xml", "*.xdv", "*.dvi", "*.blg", "*.bbl", "*.ilg", "*.ind", "*.idx"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        return False
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=".readme-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return True


def inside(root, value):
    path = (root / value).resolve()
    path.relative_to(root)
    return path


def candidates(folder):
    return sorted((p for p in folder.iterdir() if p.is_file() and
                   (p.name.lower() == "readme.md" or
                    fnmatch.fnmatch(p.name.lower(), "readme-*.md"))), key=lambda p: p.name.casefold())


def choose(folder, requested=None):
    choices = candidates(folder)
    if requested:
        is_readme = requested.lower() == "readme.md" or fnmatch.fnmatch(requested.lower(), "readme-*.md")
        if not is_readme or Path(requested).name != requested or (choices and requested not in [p.name for p in choices]):
            raise ValueError("--readme must select an immediate README candidate")
        return requested
    if len(choices) == 1:
        return choices[0].name
    if len(choices) > 1:
        summaries = [p for p in choices if p.read_text(encoding="utf-8-sig").startswith("# Directory Summary")]
        if len(summaries) == 1:
            return summaries[0].name
        raise ValueError("Ambiguous README candidates; inspect them and use --readme NAME")
    return "README.md"


def fingerprint(path, old=None, force=False):
    stat = path.stat()
    meta = {"mtime_ns": stat.st_mtime_ns, "size": stat.st_size}
    if not force and old and all(meta[k] == old.get(k) for k in meta):
        return {**meta, "hash": old["hash"]}
    data = path.read_bytes()
    after = path.stat()
    if (stat.st_mtime_ns, stat.st_size) != (after.st_mtime_ns, after.st_size):
        raise ValueError("Concurrent edit while hashing: " + str(path))
    return {**meta, "hash": digest(data)}


def setup(root, target):
    root = root.resolve()
    target = inside(root, target)
    if not target.is_dir():
        raise ValueError("Target is not a repository directory")
    if target == root or target == root / ".cache" or root / ".cache" in target.parents:
        raise ValueError("Target must permit a repository-local cache outside the documented folder")
    ident = target.relative_to(root).as_posix()
    cache = root / ".cache/global-economics-readme" / digest(ident.encode())
    return root, target, ident, cache


def rules(root):
    data = (root / TEMPLATE).read_bytes()
    template = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    patterns = re.findall(r"^\*[^\s`]+$", template, re.M)
    if not patterns:
        raise ValueError("Cannot extract live template exclusions; adapt helper")
    output = template.split("## Output Template", 1)[-1]
    if re.findall(r"^## (.+)$", output, re.M) != HEADINGS:
        raise ValueError("Live template structure changed; adapt helper before generation")
    return digest(data), patterns + EXTRA


def excluded(name, patterns):
    return any(fnmatch.fnmatch(name.lower(), p.lower()) for p in patterns)


def snapshot(root, target, name, patterns, dependencies, old=None, force=False):
    old = old or {}
    inputs, dirs = {}, {}
    for path in sorted(target.iterdir()):
        if path.is_symlink():
            raise ValueError("Resolve symlink scope explicitly before documenting: " + str(path))
        if path.is_file() and path.name != name and not excluded(path.name, patterns):
            key = "file:" + path.name
            inputs[key] = fingerprint(path, old.get(key), force)
        elif path.is_dir():
            children = candidates(path)
            records = {}
            for child in children:
                key = "child:" + path.name + "/" + child.name
                records[child.name] = fingerprint(child, old.get(key), force)
                inputs[key] = records[child.name]
            dirs[path.name] = list(records)
            inputs["folder:" + path.name] = {"hash": digest(json.dumps(
                {n: r["hash"] for n, r in records.items()}, sort_keys=True).encode())}
    for dep in dependencies:
        path = inside(root, dep)
        if path == target / name or excluded(path.name, patterns):
            raise ValueError("Output/artifact cannot be a source dependency: " + dep)
        inputs["dep:" + dep] = fingerprint(path, old.get("dep:" + dep), force) if path.is_file() else {"hash": None}
    return inputs, dirs


def valid_state(state, ident, helper):
    try:
        analysis = state["analysis"]
        if set(analysis["files"]) != {k[5:] for k in state["inputs"] if k.startswith("file:")}:
            return False
        if set(analysis["folders"]) != {k[7:] for k in state["inputs"] if k.startswith("folder:")}:
            return False
        for key, record in state["inputs"].items():
            if not re.fullmatch(r"[0-9a-f]{64}", record["hash"]):
                return False
            if not key.startswith("folder:") and not (
                isinstance(record["mtime_ns"], int) and isinstance(record["size"], int) and record["size"] >= 0
            ):
                return False
        for data in analysis["files"].values():
            require_text(data["type"])
            require_text(data["description"])
            if not isinstance(data["commands"], list) or not all(isinstance(c, str) for c in data["commands"]):
                return False
            if not isinstance(data["sections"], list):
                return False
            for section in data["sections"]:
                require_text(section["title"])
                require_text(section["description"])
                if not isinstance(section["level"], int) or not 1 <= section["level"] <= 6:
                    return False
        for data in analysis["folders"].values():
            require_text(data["description"])
            if data["readme"] is not None and not isinstance(data["readme"], str):
                return False
        if not all(isinstance(k, str) and isinstance(v, list) and all(isinstance(o, str) for o in v)
                   for k, v in analysis["dependencies"].items()):
            return False
        return (state["schema"] == SCHEMA and state["helper"] == helper and state["target"] == ident
                and isinstance(state["inputs"], dict) and isinstance(state["analysis"]["files"], dict)
                and isinstance(state["analysis"]["folders"], dict)
                and isinstance(state["analysis"]["dependencies"], dict)
                and isinstance(state["analysis"]["purpose"], str)
                and isinstance(state["output_hash"], str)
                and isinstance(state["readme"], str) and isinstance(state["template"], str)
                and all(isinstance(v, dict) and "hash" in v and
                        (k.startswith("folder:") or ("mtime_ns" in v and "size" in v))
                        for k, v in state["inputs"].items()))
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def scan(root, target, ident, cache, args):
    helper = digest(Path(__file__).read_bytes()) + ":" + VERSION
    thash, patterns = rules(root)
    try:
        state = load(cache / "state.json")
    except (OSError, ValueError):
        state = {}
    baseline = not valid_state(state, ident, helper)
    if baseline:
        state = {}
    analysis = copy.deepcopy(state.get("analysis", {"purpose": "", "files": {}, "folders": {}, "dependencies": {}}))
    deps = analysis["dependencies"].copy()
    for value in args.dependency:
        path, owner = value.rsplit("=", 1)
        path = inside(root, path).relative_to(root).as_posix()
        deps.setdefault(path, [])
        if owner not in deps[path]:
            deps[path].append(owner)
    for path in args.drop_dependency:
        deps.pop(inside(root, path).relative_to(root).as_posix(), None)
    analysis["dependencies"] = deps
    remembered = state.get("readme") if not candidates(target) else None
    name = choose(target, args.readme or remembered)
    old = state.get("inputs", {})
    inputs, dirs = snapshot(root, target, name, patterns, deps, old, args.force)
    added = sorted(inputs.keys() - old.keys())
    removed = sorted(old.keys() - inputs.keys())
    changed = sorted(k for k in inputs.keys() & old.keys() if inputs[k]["hash"] != old[k]["hash"])
    unchanged = sorted(inputs.keys() & old.keys() - set(changed))
    review = set(inputs if baseline or args.force else added + changed)
    for dep, owners in {**state.get("analysis", {}).get("dependencies", {}), **deps}.items():
        if "dep:" + dep in set(added + changed + removed):
            review.update(o for o in owners if o in inputs)
    review = sorted(review)
    for key in inputs:
        if key.startswith("file:"):
            analysis["files"].setdefault(key[5:], {"type": "", "description": "", "commands": [], "sections": []})
        if key.startswith("folder:"):
            analysis["folders"].setdefault(key[7:], {"description": "", "readme": None})
    analysis["files"] = {n: v for n, v in analysis["files"].items() if "file:" + n in inputs}
    analysis["folders"] = {n: v for n, v in analysis["folders"].items() if n in dirs}
    output_hash = digest((target / name).read_bytes()) if (target / name).exists() else None
    manual = output_hash != state.get("output_hash") or output_hash is None or name != state.get("readme")
    plan = {"schema": SCHEMA, "helper": helper, "target": ident, "readme": name,
            "template": thash, "inputs": inputs, "dirs": dirs, "analysis": analysis,
            "report": {"added": added, "content_changed": changed, "removed": removed, "unchanged": unchanged},
            "baseline": baseline, "review": review, "verified": [],
            "summary_review": bool(review or removed or manual or thash != state.get("template")),
            "manual_output": manual, "output_before": output_hash,
            "conformance": thash if not baseline and thash == state.get("template") and not manual else "",
            "reconciled": not manual}
    atomic(cache / "plan.json", (json.dumps(plan, ensure_ascii=False, indent=2) + "\n").encode())
    return {"plan": str(cache / "plan.json"), **plan["report"], "baseline": baseline,
            "review": review, "summary_review": plan["summary_review"], "manual_output": manual,
            "template_review": plan["conformance"] != thash}


def cell(text):
    # Preserve inline relative links; encode table delimiters without losing Unicode.
    return str(text).replace("&", "&amp;").replace("|", "&#124;").replace("<", "&lt;").replace(
        ">", "&gt;").replace("\r\n", "<br>").replace("\n", "<br>")


def link(name, destination=None):
    label = html.escape(name).replace("|", "&#124;").replace("`", "&#96;")
    return f"[`{label}`]({quote(destination or name, safe='/.-_')})"


def require_text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Missing verified text")
    if re.search(r"\[(?:One-sentence|specific task|specific functionality)|\bTODO\b|\bTBD\b|\bPLACEHOLDER\b", value, re.I):
        raise ValueError("Template/scaffold placeholder remains")
    return value


def render(target, name, analysis, dirs):
    require_text(analysis["purpose"])
    files = dict(analysis["files"])
    files[name] = {"type": "Markdown", "description": "Summarizes this directory.", "commands": [],
                   "sections": [{"level": 1, "title": h, "description": d} for h, d in zip(HEADINGS, [
                       "Explains the directory's role.", "Summarizes immediate files.", "Describes immediate subfolders.",
                       "Shows the folder hierarchy.", "Lists reusable commands.", "Summarizes document sections."])]}
    for data in files.values():
        require_text(data["type"])
        require_text(data["description"])
        if not isinstance(data["commands"], list) or not isinstance(data["sections"], list):
            raise ValueError("Commands/sections must be lists")
    order = sorted(files, key=lambda n: (files[n]["type"].casefold(), n.casefold(), n))
    folders = sorted(dirs, key=lambda n: (n.casefold(), n))
    parts = ["# Directory Summary", "## Purpose", cell(analysis["purpose"]), "## Files",
             "| File | Type | Purpose |\n|---|---|---|\n" + "\n".join(
                 f"| {link(n)} | {cell(files[n]['type'])} | {cell(files[n]['description'])} |" for n in order), "## Folders"]
    rows = []
    for n in folders:
        data = analysis["folders"][n]
        require_text(data["description"])
        readme = data["readme"]
        if readme is not None and readme not in dirs[n]:
            raise ValueError("Unverified child README: " + n)
        if dirs[n] and readme is None:
            raise ValueError("Select the child summary README: " + n)
        rows.append(f"| {link(n + '/')} | {cell(data['description'])} | " +
                    (link(readme, n + "/" + readme) if readme else "None.") + " |")
    parts.append("| Folder | Purpose | README |\n|---|---|---|\n" + "\n".join(rows) if rows else "None.")
    nodes = [n + "/" for n in folders] + order
    tree = target.name + "/\n" + "\n".join(("└── " if i == len(nodes)-1 else "├── ") + n for i, n in enumerate(nodes))
    parts += ["## Directory Structure", "```text\n" + tree + "\n```", "## Public Commands"]
    rows = []
    for n in order:
        commands = files[n]["commands"]
        for command in commands:
            require_text(command)
        rows.append(f"| {link(n)} | " + (", ".join("`" + cell(c).replace("`", "&#96;") + "`" for c in commands) or "None.") + " |")
    parts += ["| File | Commands |\n|---|---|\n" + "\n".join(rows), "## Document Sections"]
    rows = []
    for n in order:
        sections = []
        for section in files[n]["sections"]:
            if not isinstance(section["level"], int) or not 1 <= section["level"] <= 6:
                raise ValueError("Invalid section hierarchy")
            title = cell(require_text(section["title"]))
            description = cell(require_text(section["description"]))
            sections.append("&nbsp;" * (4 * (section["level"]-1)) + f"**{title}:** {description}")
        rows.append(f"| {link(n)} | " + ("<br>".join(sections) or "None.") + " |")
    parts.append("| File | Sections and Descriptions |\n|---|---|\n" + "\n".join(rows))
    return "\n\n".join(parts) + "\n"


def validate(text, target, name, patterns, inputs):
    if not text.startswith("# Directory Summary\n") or re.findall(r"^## (.+)$", text, re.M) != HEADINGS:
        raise ValueError("Invalid section structure")
    require_text(text)
    for dest in re.findall(r"\]\(([^)]+)\)", text):
        dest = html.unescape(unquote(dest)).split("#", 1)[0]
        if not dest:
            continue
        if "\\" in dest or re.match(r"[a-zA-Z]+:", dest) or dest.startswith("/"):
            raise ValueError("Link is not relative: " + dest)
        path = target / dest
        if excluded(path.name, patterns) or (path != target / name and not path.exists()):
            raise ValueError("Invalid/excluded link: " + dest)
    # Reject excluded artifact mentions as well as inventory rows/links.
    tokens = re.findall(r"[\w.()/-]+\.[\w.]+", text)
    if any(excluded(t.rsplit("/", 1)[-1].rstrip("."), patterns) for t in tokens):
        raise ValueError("Excluded artifact reference in README")
    expected = {k[5:] for k in inputs if k.startswith("file:")} | {name}
    for heading in ("Files", "Public Commands", "Document Sections"):
        block = text.split("## " + heading + "\n", 1)[1].split("\n## ", 1)[0]
        found = [unquote(x) for x in re.findall(r"^\| \[`.*?`\]\((.*?)\)", block, re.M)]
        if set(found) != expected or len(found) != len(expected):
            raise ValueError("Inconsistent file inventory")


def commit(root, target, ident, cache, plan_path):
    plan = load(Path(plan_path))
    thash, patterns = rules(root)
    if plan["schema"] != SCHEMA or plan["target"] != ident or plan["helper"] != digest(Path(__file__).read_bytes()) + ":" + VERSION:
        raise ValueError("Incompatible plan; rescan")
    if plan["template"] != thash or plan["conformance"] != thash or not plan["reconciled"]:
        raise ValueError("Template conformance/output reconciliation required")
    if not set(plan["review"]).issubset(plan["verified"]):
        raise ValueError("Incomplete analysis; review all required inputs")
    analysis = plan["analysis"]
    name = choose(target, plan["readme"])
    current, dirs = snapshot(root, target, name, patterns, analysis["dependencies"], force=True)
    if current != plan["inputs"] or dirs != plan["dirs"]:
        raise ValueError("Inputs changed or dependency not fingerprinted; rescan")
    if set(analysis["files"]) != {k[5:] for k in current if k.startswith("file:")} or set(analysis["folders"]) != set(dirs):
        raise ValueError("Analysis membership differs from snapshot")
    for dep, owners in analysis["dependencies"].items():
        if current["dep:" + dep]["hash"] is None or not owners or any(o not in current for o in owners):
            raise ValueError("Missing dependency or invalid affected owner")
    text = render(target, name, analysis, dirs)
    validate(text, target, name, patterns, current)
    path = target / name
    before = digest(path.read_bytes()) if path.exists() else None
    if before != plan["output_before"]:
        raise ValueError("README edited during review; rescan and reconcile")
    # Final full check after rendering/validation; no cache is committed on failure.
    check, check_dirs = snapshot(root, target, name, patterns, analysis["dependencies"], force=True)
    if check != current or check_dirs != dirs or rules(root)[0] != thash:
        raise ValueError("Concurrent input edits; rescan")
    changed = atomic(path, text.encode("utf-8"))
    final_inputs, final_dirs = snapshot(root, target, name, patterns, analysis["dependencies"], force=True)
    if final_inputs != current or final_dirs != dirs or rules(root)[0] != thash or path.read_bytes() != text.encode("utf-8"):
        raise ValueError("Concurrent edits during publication; output needs reconciliation; cache not committed")
    state = {k: plan[k] for k in ("schema", "helper", "target", "template", "readme", "analysis")}
    state.update(inputs=current, output_hash=digest(path.read_bytes()))
    atomic(cache / "state.json", (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode())
    return {"path": str(path), "status": "created" if before is None else "updated" if changed else "already current",
            "reviewed": len(plan["review"]), "reused": len(current) - len(plan["review"])}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--readme")
    parser.add_argument("--dependency", action="append", default=[])
    parser.add_argument("--drop-dependency", action="append", default=[])
    parser.add_argument("--commit", type=Path)
    args = parser.parse_args()
    root = args.root
    if root is None:
        root = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / TEMPLATE).is_file()), None)
        if root is None:
            parser.error("Repository root not found; supply --root")
    try:
        root, target, ident, cache = setup(root, args.target)
        result = commit(root, target, ident, cache, args.commit) if args.commit else scan(root, target, ident, cache, args)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, "README workflow stopped: " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
