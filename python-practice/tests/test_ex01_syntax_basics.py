from exercises.ex01_syntax_basics import (
    abs_or_zero,
    add,
    build_profile,
    classify,
    first_big,
    fizzbuzz,
    greet,
    sum_all,
    swap,
)


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_greet_default():
    assert greet("Sam") == "Hello, Sam!"


def test_greet_custom():
    assert greet("Sam", "Howdy") == "Howdy, Sam!"


def test_sum_all():
    assert sum_all() == 0
    assert sum_all(1, 2, 3) == 6


def test_build_profile():
    assert build_profile(name="Sam", role="staff") == {"name": "Sam", "role": "staff"}


def test_classify():
    assert classify(-4) == "negative"
    assert classify(0) == "zero"
    assert classify(9) == "positive"


def test_abs_or_zero():
    assert abs_or_zero(-5) == 5
    assert abs_or_zero(5) == 5
    assert abs_or_zero(0) == 0


def test_fizzbuzz():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[-1] == "FizzBuzz"


def test_swap():
    assert swap(1, 2) == (2, 1)
    assert swap("a", "b") == ("b", "a")


def test_first_big():
    assert first_big([1, 5, 3, 9], 4) == 5
    assert first_big([1, 2, 3], 10) is None
