"""Geometry review for the independent NumbersAsArrows scene."""
from importlib import import_module
from pathlib import Path
import sys
import numpy as np
from manim import config, VMobject, VGroup

sys.path.insert(0, str(Path.cwd()))
m = import_module('assets.manim.algebra.stage1_arithmetic_foundations.01_1numbers-arrows')
config.media_dir = str(Path('assets/manim/.render_review/numbers_as_arrows').resolve())
axis = m.NumberLine(x_range=[-11,11,1], length=12.1)
number = m.CenteredNumber()
slots = VGroup(VMobject(), VMobject())
number_family = [id(obj) for obj in number.get_family()]
arrow_family = [id(obj) for obj in slots.get_family()]
bottoms = {c:g.get_bottom()[1] for c,g in number.glyphs.items()}
for tenths in list(range(-100,101)) + list(range(100,-101,-1)):
    number.show_value(tenths)
    assert [id(obj) for obj in number.get_family()] == number_family
    assert abs(number.get_x()) < 1e-9
    for char,glyph in zip(m.number_string(tenths), number):
        assert abs(glyph.get_bottom()[1] - bottoms[char]) < 1e-9
    for unused in number[len(m.number_string(tenths)):]:
        assert len(unused.points) == 0
    m.update_arrow_geometry(slots, axis, tenths)
    assert [id(obj) for obj in slots.get_family()] == arrow_family
    if tenths == 0:
        assert all(len(slot.points) == 0 for slot in slots)
    else:
        geometry = m.signed_arrow(axis, tenths)[0]
        np.testing.assert_allclose(geometry.get_start(), axis.n2p(0)+m.ARROW_OFFSET, atol=1e-9)
        np.testing.assert_allclose(geometry.get_end(), axis.n2p(tenths/10)+m.ARROW_OFFSET, atol=1e-9)
        np.testing.assert_allclose(slots[0].points, geometry.points, atol=1e-9)
        np.testing.assert_allclose(slots[1].points, geometry.tip.points, atol=1e-9)
    assert number.width < 6
assert m.number_string(m.displayed_tenths(-0.001)) == '0'
assert [m.number_string(x) for x in (10,-100,100,0,-1,1)] == ['1','−10','10','0','−0.1','0.1']
print('PASS: 402 signed updates, stable object families, fixed baselines, horizontal centering, exact endpoints, fully empty zero, formatting.')
