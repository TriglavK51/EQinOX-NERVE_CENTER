import pytest

from core.scoring import ToolScore, calculate_score


def test_score_rewards_low_cost() -> None:
    assert calculate_score(ToolScore(1, 0, 1, 1)) == 1.0


def test_score_rejects_out_of_range_factor() -> None:
    with pytest.raises(ValueError):
        calculate_score(ToolScore(1.1, 0, 1, 1))
