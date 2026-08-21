from exercises.ex02_builtins import (
    all_positive,
    has_any_negative,
    index_each,
    min_max,
    only_even,
    pair_up,
    rounded,
    sort_by_length,
    sort_desc,
    squares,
    total_and_count,
)


def test_total_and_count():
    assert total_and_count([1, 2, 3, 4]) == (10, 4)


def test_min_max():
    assert min_max([3, 1, 9, 2]) == (1, 9)


def test_sort_desc():
    assert sort_desc([1, 3, 2]) == [3, 2, 1]


def test_sort_by_length():
    assert sort_by_length(["bbb", "a", "cc"]) == ["a", "cc", "bbb"]


def test_index_each():
    assert index_each(["x", "y"]) == [(0, "x"), (1, "y")]


def test_pair_up():
    assert pair_up(["a", "b"], [1, 2]) == [("a", 1), ("b", 2)]


def test_squares():
    assert squares([1, 2, 3]) == [1, 4, 9]


def test_only_even():
    assert only_even([1, 2, 3, 4, 5, 6]) == [2, 4, 6]


def test_has_any_negative():
    assert has_any_negative([1, 2, -1]) is True
    assert has_any_negative([1, 2, 3]) is False


def test_all_positive():
    assert all_positive([1, 2, 3]) is True
    assert all_positive([1, 0, 3]) is False


def test_rounded():
    assert rounded([1.234, 2.567]) == [1.23, 2.57]
    assert rounded([1.234], 1) == [1.2]
