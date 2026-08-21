from exercises.ex04_comprehensions import (
    even_squares,
    grid,
    initials,
    is_palindrome,
    lengths_by_word,
    normalize,
    reverse_words,
    squares_comp,
    to_snake_case,
    unique_first_letters,
)


def test_squares_comp():
    assert squares_comp(4) == [0, 1, 4, 9]


def test_even_squares():
    assert even_squares(6) == [0, 4, 16]


def test_lengths_by_word():
    assert lengths_by_word(["a", "bb", "ccc"]) == {"a": 1, "bb": 2, "ccc": 3}


def test_unique_first_letters():
    assert unique_first_letters(["apple", "ant", "bee"]) == {"a", "b"}


def test_grid():
    assert grid(2, 3) == [[0, 1, 2], [3, 4, 5]]


def test_to_snake_case():
    assert to_snake_case("Hello World Foo") == "hello_world_foo"


def test_normalize():
    assert normalize("  hello   world  ") == "hello world"


def test_reverse_words():
    assert reverse_words("the quick fox") == "fox quick the"


def test_is_palindrome():
    assert is_palindrome("Race car") is True
    assert is_palindrome("hello") is False


def test_initials():
    assert initials("ada lovelace") == "AL"
    assert initials("grace brewster murray hopper") == "GBMH"
