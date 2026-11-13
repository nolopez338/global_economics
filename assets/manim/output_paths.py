"""Stable declared video identities; resolving a source never imports Manim."""

import ast
from pathlib import Path, PurePosixPath

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPOSITORY_ROOT / "assets" / "manim"
MEDIA_ROOT = REPOSITORY_ROOT.parent / "manim_media"


def output_destination(output_identity):
    """Resolve a literal path relative to the video root, without creating it."""
    if not isinstance(output_identity, str) or not output_identity:
        raise ValueError("A scene must declare a nonempty output_identity")
    identity = PurePosixPath(output_identity)
    if (identity.is_absolute() or ".." in identity.parts
            or "\\" in output_identity or ":" in output_identity
            or identity.suffix != ".mp4" or output_identity != identity.as_posix()):
        raise ValueError("output_identity must be a normalized relative .mp4 path")
    return MEDIA_ROOT / "videos" / Path(*identity.parts)


def partial_movie_directory(output_identity):
    """Keep the existing per-identity, quality and scene cache isolation."""
    destination = output_destination(output_identity)
    return (destination.parent / "partial_movie_files" / destination.stem
            / "{quality}" / "{scene_name}")


def source_destination(source_path):
    """Read explicit scene declarations statically; never guess from a filename."""
    source = (REPOSITORY_ROOT / source_path).resolve()
    if not source.is_relative_to(SOURCE_ROOT) or source.suffix != ".py":
        raise ValueError("Provide a Python source path inside assets/manim/")
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    identities = []
    for scene in tree.body:
        if not isinstance(scene, ast.ClassDef):
            continue
        for statement in scene.body:
            if isinstance(statement, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "output_identity"
                for target in statement.targets
            ):
                try:
                    identities.append(ast.literal_eval(statement.value))
                except (ValueError, TypeError) as error:
                    raise ValueError("output_identity must be a literal string") from error
    if not identities:
        raise ValueError("Source has no declared output_identity; request its stable identity")
    destinations = {output_destination(identity) for identity in identities}
    if len(destinations) != 1:
        raise ValueError("Source declares multiple destinations; specify the intended scene")
    return "../manim_media/videos/" + destinations.pop().relative_to(
        MEDIA_ROOT / "videos"
    ).as_posix()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="repository-relative existing Python source")
    args = parser.parse_args()
    try:
        print(source_destination(args.source))
    except (OSError, SyntaxError, ValueError) as error:
        parser.exit(1, f"{error}\n")
