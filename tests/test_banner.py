"""Tests for the banner render seam."""

import xml.etree.ElementTree as ET

import pytest

import banner

GOOD = {
    "prompt": "$ ./profile.sh --live",
    "lines": [
        {"key": "name", "value": "Giovani Rodrigo"},
        {"key": "role", "value": "DevOps & Full-Stack Engineer"},
    ],
}


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_render_is_well_formed_svg(theme):
    root = ET.fromstring(banner.render(GOOD, theme))
    assert root.tag.endswith("svg")


def test_prompt_and_content_present():
    svg = banner.render(GOOD, "dark")
    assert "profile.sh --live" in svg
    assert "Giovani Rodrigo" in svg
    assert "role" in svg


def test_special_characters_are_escaped():
    svg = banner.render(GOOD, "dark")
    # The ampersand in "DevOps & Full-Stack" must be XML-escaped, not raw.
    assert "&amp;" in svg
    ET.fromstring(svg)  # would raise if raw & leaked through


def test_themes_differ():
    assert banner.render(GOOD, "dark") != banner.render(GOOD, "light")


@pytest.mark.parametrize(
    "bad",
    [
        {},
        {"prompt": "$ x", "lines": []},
        {"prompt": "", "lines": [{"key": "a", "value": "b"}]},
        {"prompt": "$ x", "lines": [{"key": "a"}]},  # missing value
        {"prompt": "$ x", "lines": [{"key": 1, "value": "b"}]},  # non-string key
    ],
)
def test_malformed_input_raises(bad):
    with pytest.raises(ValueError):
        banner.render(bad, "dark")
