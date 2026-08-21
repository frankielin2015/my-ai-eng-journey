from exercises.ex03_data_structures import (
    common_elements,
    dedupe_keep_order,
    flatten,
    group_by_parity,
    invert,
    merge_dicts,
    only_in_first,
    top_n,
    word_count,
)


def test_dedupe_keep_order():
    assert dedupe_keep_order([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_merge_dicts():
    assert merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 3, "c": 4}


def test_word_count():
    assert word_count("a b a c a b") == {"a": 3, "b": 2, "c": 1}


def test_group_by_parity():
    assert group_by_parity([1, 2, 3, 4]) == {"odd": [1, 3], "even": [2, 4]}


def test_common_elements():
    assert common_elements([1, 2, 3], [2, 3, 4]) == {2, 3}


def test_only_in_first():
    assert only_in_first([1, 2, 3], [2, 3, 4]) == {1}


def test_top_n():
    result = top_n({"a": 5, "b": 1, "c": 3}, 2)
    assert result == ["a", "c"]


def test_invert():
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_flatten():
    assert flatten([[1, 2], [3], [4, 5]]) == [1, 2, 3, 4, 5]
