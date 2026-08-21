import pytest

from exercises.ex07_generators_errors import (
    WithdrawalError,
    countdown,
    fibonacci,
    parse_int,
    running_total,
    safe_divide,
    take,
    track_calls,
    withdraw,
)


def test_countdown():
    assert list(countdown(3)) == [3, 2, 1]


def test_take():
    assert take([1, 2, 3, 4], 2) == [1, 2]
    assert take(countdown(100), 3) == [100, 99, 98]


def test_fibonacci():
    assert take(fibonacci(), 7) == [0, 1, 1, 2, 3, 5, 8]


def test_running_total():
    assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10]


def test_safe_divide():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(1, 0) is None


def test_parse_int():
    assert parse_int("42") == 42
    assert parse_int("nope") == 0
    assert parse_int("nope", -1) == -1


def test_withdraw_ok():
    assert withdraw(100, 30) == 70


def test_withdraw_raises():
    with pytest.raises(WithdrawalError):
        withdraw(10, 50)


def test_track_calls():
    log = []
    with track_calls(log):
        log.append("inside")
    assert log == ["enter", "inside", "exit"]


def test_track_calls_on_exception():
    log = []
    with pytest.raises(RuntimeError):
        with track_calls(log):
            raise RuntimeError("boom")
    assert log == ["enter", "exit"]
