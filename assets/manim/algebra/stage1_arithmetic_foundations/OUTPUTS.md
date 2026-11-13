# Stage 1 source order and stable outputs

The approved source sequence is `01_numbers-arrows.py`, `02_adding_subtracting.py`,
`03_signed_multiplication.py`; `00_preliminaries.py` is the combined lesson.
Git commit `d5f6f259` (2026-11-02) records the older sequence beginning with
`01_adding_subtracting.py`, `02_signed_multiplication_absolute_value.py`,
`03_real_number_properties.py`. The current working-tree split and renamed first
three lessons are preserved. Absolute value follows signed multiplication;
the remaining older lessons retain their relative order. No lessons were merged
or removed. The combined lesson retains its existing section membership and order.

## Rename and destination record

Destinations were captured from the working-tree `common.py` calculation before
renaming, rather than from stale source docstrings. Every MP4 below is under
`../manim_media/videos/algebra/stage1_arithmetic_foundations/`, relative to the
repository root. Rows with equal source names were preserved.

| Before | After | Stable MP4 filename | Scene class |
| --- | --- | --- | --- |
| `00_preliminaries.py` | `00_preliminaries.py` | `00_preliminaries.mp4` | `ArithmeticPreliminaries` |
| `01_numbers-arrows.py` | `01_numbers-arrows.py` | `01_numbers-arrows.mp4` | `NumbersAsArrows` |
| `02_adding_subtracting.py` | `02_adding_subtracting.py` | `02_adding_subtracting.mp4` | `AddingSubtracting` |
| `03_signed_multiplication.py` | `03_signed_multiplication.py` | `03_signed_multiplication.mp4` | `SignedMultiplication` |
| `02_2absolute_value.py` | `04_absolute_value.py` | `02_2absolute_value.mp4` | `SignedMultiplicationAbsoluteValue` |
| `03_real_number_properties.py` | `05_real_number_properties.py` | `03_real_number_properties.mp4` | `RealNumberProperties` |
| `04_fractions_decimals.py` | `06_fractions_decimals.py` | `04_fractions_decimals.mp4` | `FractionsDecimals` |
| `05_ratios_percentages.py` | `07_ratios_percentages.py` | `05_ratios_percentages.mp4` | `RatiosPercentages` |
| `06_powers_roots.py` | `08_powers_roots.py` | `06_powers_roots.mp4` | `PowersRoots` |
| `07_order_of_operations.py` | `09_order_of_operations.py` | `07_order_of_operations.mp4` | `OrderOfOperations` |

For each row, the exact partial-movie directory is that same output directory plus
`partial_movie_files/<stable MP4 filename without .mp4>/{quality}/<Scene class>/`.
Quality resolves to `480p15` for `-ql` and `1080p60` for `-qh --fps 60`.
Other media caches remain under `../manim_media/`. Existing rendered media was
not moved, renamed, or deleted.

Each class now declares its immutable `output_identity`, relative to the video
root. `assets/manim/output_paths.py` validates and resolves it for both runtime
configuration and the path skill. The partial cache stem also comes from that
identity. `source_file` remains source metadata and never chooses the output.
Future source renames must retain the identity, scene class, flags, content,
timing, typography, and render settings; update the command's source argument
and loader references only. Helpers without an identity have no video destination.
The older `algebra/output_config.py` serves other stages and is unchanged.

## Windows CMD commands

Run these from the repository root. The existing command prefixes, flags, and
scene classes are preserved; only renamed source arguments changed. Both
existing quality variants are included where they were documented.

```cmd
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries
python -m manim -qh --fps 60 assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/01_numbers-arrows.py NumbersAsArrows
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/02_adding_subtracting.py AddingSubtracting
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/03_signed_multiplication.py SignedMultiplication
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/04_absolute_value.py SignedMultiplicationAbsoluteValue
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/05_real_number_properties.py RealNumberProperties
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/06_fractions_decimals.py FractionsDecimals
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/07_ratios_percentages.py RatiosPercentages
python -m manim -qh --fps 60 assets/manim/algebra/stage1_arithmetic_foundations/07_ratios_percentages.py RatiosPercentages
manim -ql assets/manim/algebra/stage1_arithmetic_foundations/08_powers_roots.py PowersRoots
python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/09_order_of_operations.py OrderOfOperations
```

Read-only path resolution (normal successful output is one forward-slash path):

```cmd
python -B assets/manim/output_paths.py assets/manim/algebra/stage1_arithmetic_foundations/05_real_number_properties.py
```

Missing sources, missing/nonliteral/invalid identities, and conflicting scene
identities return an error and no destination. The path skill requests the
missing information instead of guessing from the filename.

## Verification

- Captured all ten final and partial-movie paths before editing.
- Confirmed unique contiguous numbering 00–09 and preserved approved 01–03 names.
- Compared pre/post scene ASTs, excluding docstrings, the new identity declarations,
  and loader module-path literals: executable scene content is identical.
- Loaded all ten classes with Manim's module and scene-discovery helpers, including
  the combined loader. Instantiated each with dry-run output at low quality and
  high quality/60 fps; runtime final/cache paths match the captured baseline.
- Copied each scene to a temporary differently named source, loaded it, and
  confirmed both static resolution and runtime final/cache paths remain identical.
  Temporary source probes were removed; bytecode writing was disabled.
- Checked missing-file, missing-identity, and outside-root errors produce no path.
- Compared documented command tokens: only source-path arguments changed; every
  resulting source exists and every class is discoverable. Confirmed the path
  resolver runs through Windows CMD and both Manim command prefixes use CE 0.17.3.
- Rendered the actual order-of-operations opening transition (12 frames, 0.8 s)
  with isolated temporary media and stopped before math creation in the test
  harness. A final MP4 and partial movie were produced. An initial attempt to
  continue into math failed because local LaTeX produced no log file. Full videos
  were not rendered; this environment issue does not affect the load/path checks.
