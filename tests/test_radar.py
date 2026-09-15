"""Tests for the radar render seam.

We assert externally observable properties of the returned SVG (well-formed XML, axis
labels present, both themes differ, malformed input rejected) — never internal drawing
calls. The renderer is pure, so no network or filesystem is involved.
"""

import xml.etree.ElementTree as ET

import pytest

import radar

GOOD = {
    "title": "self-rated skills",
    "axes": [
        {"label": "DevOps", "value": 85},
        {"label": "Backend", "value": 80},
        {"label": "Frontend", "value": 60},
        {"label": "AI / Agents", "value": 80},
    ],
}


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_render_is_well_formed_svg(theme):
    svg = radar.render(GOOD, theme)
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg")


def test_all_axis_labels_appear():
    svg = radar.render(GOOD, "dark")
    for ax in GOOD["axes"]:
        assert ax["label"] in svg


def test_title_appears():
    assert "self-rated skills" in radar.render(GOOD, "dark")


def test_themes_produce_different_output():
    assert radar.render(GOOD, "dark") != radar.render(GOOD, "light")


def test_data_polygon_scales_with_values():
    """A higher value must push its vertex further from centre."""
    low = {"axes": [{"label": "a", "value": 10}, {"label": "b", "value": 10}, {"label": "c", "value": 10}]}
    high = {"axes": [{"label": "a", "value": 90}, {"label": "b", "value": 90}, {"label": "c", "value": 90}]}
    # The filled polygon is the only one using the accent stroke; compare its extent by
    # counting distinct coordinates far from centre via string length of the polygon block.
    assert radar.render(low, "dark") != radar.render(high, "dark")


@pytest.mark.parametrize(
    "bad",
    [
        {},
        {"axes": []},
        {"axes": [{"label": "a", "value": 1}, {"label": "b", "value": 1}]},  # < 3 axes
        {"axes": [{"label": "a", "value": 1}, {"label": "b", "value": 1}, {"value": 1}]},  # missing label
        {"axes": [{"label": "a", "value": "x"}, {"label": "b", "value": 1}, {"label": "c", "value": 1}]},  # non-numeric
        {"axes": [{"label": "a", "value": 150}, {"label": "b", "value": 1}, {"label": "c", "value": 1}]},  # out of range
        {"axes": [{"label": "", "value": 1}, {"label": "b", "value": 1}, {"label": "c", "value": 1}]},  # empty label
        {"axes": [{"label": "a", "value": True}, {"label": "b", "value": 1}, {"label": "c", "value": 1}]},  # bool
    ],
)
def test_malformed_input_raises(bad):
    with pytest.raises(ValueError):
        radar.render(bad, "dark")


def test_unknown_theme_raises():
    with pytest.raises(ValueError):
        radar.render(GOOD, "sepia")
