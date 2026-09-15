"""Tests for the stats-card render seam (the pure part only; fetch() is not exercised)."""

import xml.etree.ElementTree as ET

import pytest

import stats_card

STATS = {
    "name": "Giovani Rodrigo",
    "followers": 3,
    "public_repos": 22,
    "stars": 0,
    "forks_made_of_my_repos": 1,
}


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_render_is_well_formed_svg(theme):
    root = ET.fromstring(stats_card.render(STATS, theme))
    assert root.tag.endswith("svg")


def test_numbers_and_labels_present():
    svg = stats_card.render(STATS, "dark")
    assert ">22<" in svg  # repos
    assert ">3<" in svg  # followers
    assert "repos" in svg and "followers" in svg


def test_themes_differ():
    assert stats_card.render(STATS, "dark") != stats_card.render(STATS, "light")


@pytest.mark.parametrize(
    "bad",
    [
        {},
        {"name": "x"},  # missing numeric fields
        {"name": "x", "followers": "3", "public_repos": 1, "stars": 0},  # non-int
    ],
)
def test_malformed_input_raises(bad):
    with pytest.raises(ValueError):
        stats_card.render(bad, "dark")
