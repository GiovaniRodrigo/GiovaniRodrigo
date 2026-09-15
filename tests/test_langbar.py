"""Tests for the language-bar render seam."""

import xml.etree.ElementTree as ET

import pytest

import langbar

GOOD = {
    "axes": [
        {"label": "Python", "value": 90},
        {"label": "TypeScript", "value": 85},
        {"label": "Go", "value": 40},
    ],
}


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_render_is_well_formed_svg(theme):
    root = ET.fromstring(langbar.render(GOOD, theme))
    assert root.tag.endswith("svg")


def test_labels_and_percentages_present():
    svg = langbar.render(GOOD, "dark")
    for ax in GOOD["axes"]:
        assert ax["label"] in svg
    assert "%" in svg


def test_themes_differ():
    assert langbar.render(GOOD, "dark") != langbar.render(GOOD, "light")


@pytest.mark.parametrize(
    "bad",
    [
        {},
        {"axes": []},
        {"axes": [{"label": "Python", "value": 0}]},  # sums to zero
        {"axes": [{"label": "Python", "value": -1}]},  # negative
        {"axes": [{"label": "Python"}]},  # missing value
    ],
)
def test_malformed_input_raises(bad):
    with pytest.raises(ValueError):
        langbar.render(bad, "dark")
