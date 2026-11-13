---
name: manim-output-path
description: Resolve only the declared stable repository-relative MP4 destination of an existing Manim Python source under assets/manim.
---

# Manim output path

Return only the declared MP4 destination relative to the repository root. Use forward slashes. The repository root is `../../..` relative to this skill directory.

Source root: `assets/manim/`.
Video root: `../manim_media/videos/` (outside the repository).

Each renderable scene must declare a literal class attribute `output_identity`, a normalized relative `.mp4` path below the video root, such as `algebra/stage1_arithmetic_foundations/03_real_number_properties.mp4`. This identity is permanent: never derive it from the source filename, source numbering, class name, or quality, and never change it during source renames.

Read the existing source and its explicit declaration without importing or executing the scene. The shared standard-library resolver implements the same identity validation used by the runtime:

```text
python -B assets/manim/output_paths.py assets/manim/algebra/stage1_arithmetic_foundations/05_real_number_properties.py
```

Run from the repository root, or invoke the resolver by absolute path; its source argument is always resolved against the repository root. This read-only resolver prints:

```text
../manim_media/videos/algebra/stage1_arithmetic_foundations/03_real_number_properties.mp4
```

The MP4 itself need not exist. The source must exist. If the path is absent, outside the source root, or the source file does not exist, ask only for a valid existing repository-relative Python source path. If the source has no literal output identity (including older scene implementations), report that it has no declared stable destination and ask for the intended stable identity; never invent a path or fall back to replacing `.py`. Invalid declarations must be corrected by the author. If multiple scenes declare distinct destinations, ask which scene is intended. Errors produce no destination on stdout.

Partial movies use the MP4's containing directory plus `partial_movie_files/<MP4 stem>/{quality}/{scene_name}/`, as implemented by `partial_movie_directory` in `assets/manim/output_paths.py`. These components depend on the declared output identity and existing render settings, never on the source filename. Do not create directories.

On successful resolution return only the repository-relative MP4 path, without Markdown, labels, or explanation. Only exceptional missing/ambiguous input warrants the focused question above.

Do not create or edit Python files, configure Manim, render videos, create directories, move files, or perform any other task. Reading the source and running the read-only standard-library path resolver are permitted.
