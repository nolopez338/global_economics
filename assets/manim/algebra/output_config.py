"""File-relative output convention for all algebra videos (Manim 0.17.3).

New scenes should inherit AlgebraScene and set positive stage_number and
video_number attributes. Videos go to
San Bartolo/manim_media/videos/algebra/stageX_Y/{quality}/SceneName.mp4.
Quality, frame rate, scene content and non-video output settings are unchanged.
"""

from pathlib import Path

from manim import Scene, config


MEDIA_ROOT = Path(__file__).resolve().parents[4] / "manim_media"


class AlgebraScene(Scene):
    """Select the destination before Manim initializes its scene file writer."""

    stage_number = None
    video_number = None

    def __init__(self, *args, **kwargs):
        for number in (self.stage_number, self.video_number):
            if type(number) is not int or number < 1:
                raise ValueError("Algebra scenes require positive stage/video numbers")
        config.media_dir = str(MEDIA_ROOT)
        config.video_dir = (
            "{media_dir}/videos/algebra/"
            f"stage{self.stage_number}_{self.video_number}/{{quality}}"
        )
        super().__init__(*args, **kwargs)
