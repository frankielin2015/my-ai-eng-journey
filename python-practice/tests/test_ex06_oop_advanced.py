import pytest

from exercises.ex06_oop_advanced import (
    Animal,
    Dog,
    MathUtils,
    Point,
    Temperature,
    Vector,
)


def test_animal():
    assert Animal("Generic").speak() == "Generic makes a sound"


def test_dog_inheritance():
    d = Dog("Rex")
    assert d.name == "Rex"
    assert d.speak() == "Rex says Woof"
    assert d.fetch() == "Rex fetches the ball"
    assert isinstance(d, Animal)


def test_vector_add():
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)


def test_vector_eq_repr():
    assert Vector(1, 2) == Vector(1, 2)
    assert repr(Vector(1, 2)) == "Vector(1, 2)"


def test_vector_abs():
    assert abs(Vector(3, 4)) == 5.0


def test_temperature():
    t = Temperature(100)
    assert t.celsius == 100
    assert t.fahrenheit == 212


def test_temperature_setter_validation():
    t = Temperature(0)
    with pytest.raises(ValueError):
        t.celsius = -300


def test_point_dataclass():
    p = Point(3, -4)
    assert p.x == 3 and p.y == -4
    assert Point(1, 2) == Point(1, 2)
    assert p.manhattan() == 7


def test_mathutils():
    assert MathUtils.add(2, 3) == 5
    assert MathUtils.description() == "This is MathUtils"
