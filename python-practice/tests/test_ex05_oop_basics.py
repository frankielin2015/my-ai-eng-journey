import pytest

from exercises.ex05_oop_basics import BankAccount, Circle, Counter


def test_counter():
    c = Counter()
    assert c.value == 0
    assert c.increment() == 1
    assert c.increment(5) == 6
    c.reset()
    assert c.value == 0


def test_counter_start():
    c = Counter(10)
    assert c.value == 10


def test_bank_deposit_withdraw():
    acc = BankAccount("Sam", 100)
    acc.deposit(50)
    assert acc.balance == 150
    acc.withdraw(30)
    assert acc.balance == 120


def test_bank_str():
    assert str(BankAccount("Sam", 100)) == "Sam: $100"


def test_bank_bad_deposit():
    acc = BankAccount("Sam")
    with pytest.raises(ValueError):
        acc.deposit(0)


def test_bank_insufficient():
    acc = BankAccount("Sam", 10)
    with pytest.raises(ValueError):
        acc.withdraw(50)


def test_circle():
    c = Circle(2)
    assert round(c.area(), 4) == 12.5664
    assert round(c.circumference(), 4) == 12.5664


def test_circle_class_attr():
    assert Circle.pi == 3.14159
