# Decorator Cheat Sheet (ex06)

> Quick-review reference for the decorators covered in OOP Advanced.

## The core idea

A decorator is a function that wraps another function to add behavior.

```python
@deco
def foo(): ...
# is literally shorthand for:
foo = deco(foo)
```

Unlike Java annotations (passive metadata), Python decorators actually RUN
and transform the thing below them. Closest cousin: TS decorators.

---

## The five we learned

| Decorator | Goes on | First param | What it does |
|---|---|---|---|
| `@property` | a method | `self` | makes a method act like a read-only attribute (GETTER) |
| `@x.setter` | a method | `self, value` | adds write behavior to property `x` (SETTER) |
| `@dataclass` | a class | -- | auto-generates `__init__`, `__repr__`, `__eq__` from fields |
| `@staticmethod` | a method | *(none)* | plain function parked in a class; no instance/class passed |
| `@classmethod` | a method | `cls` | receives the CLASS instead of an instance |

---

## @property + @x.setter  (smart attributes)

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius       # goes THROUGH the setter (validates!)

    @property                        # GETTER: runs on  read  t.celsius
    def celsius(self):
        return self._celsius         # real value lives in _celsius

    @celsius.setter                  # SETTER: runs on  write t.celsius = x
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property                        # read-only computed (no setter)
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32
```

Key facts:
- Getter + setter MUST share the same name.
- `@property` first, then `@name.setter` (setter attaches to the property).
- Store the real value in a separate `_name` field, else infinite recursion.
- `_name` is born only when the setter first assigns to it.
- No setter defined => attribute is read-only.
- Internals: property object has `fget`/`fset`/`fdel` slots (None until filled).

Java analogy: getters/setters, but with clean field syntax (no `getX()`).

---

## @dataclass  (kill the boilerplate)

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int          # declare fields with type annotations
    y: int          # that's the whole "field declaration"

    def manhattan(self):     # your own methods still allowed
        return abs(self.x) + abs(self.y)
```

Auto-generates: `__init__`, `__repr__` (`Point(x=3, y=-4)`), `__eq__` (field-by-field).
NOTE: the type annotation is load-bearing here -- the ONE place hints matter
at runtime. Stepping stone to Pydantic BaseModel (adds validation).

Java analogy: `record` / Lombok `@Data`.

---

## @staticmethod vs @classmethod  (methods without an instance)

```python
class MathUtils:
    @staticmethod
    def add(a, b):               # no self, no cls
        return a + b

    @classmethod
    def description(cls):         # cls = the class itself
        return f"This is {cls.__name__}"

MathUtils.add(2, 3)          # -> 5           (call on the class, no object)
MathUtils.description()      # -> "This is MathUtils"
```

- `@staticmethod`: turns OFF auto-passing. Just a function in a class. = Java `static`.
- `@classmethod`: auto-passes the CLASS as `cls`. Killer use = alternative
  constructors (like `dict.fromkeys`, `datetime.fromtimestamp`).

---

## self / cls reminder

Neither is a keyword -- both are naming CONVENTIONS. Python auto-passes:
- regular method  -> the instance -> caught by `self`
- `@classmethod`  -> the class    -> caught by `cls`
- `@staticmethod` -> nothing      -> no first param needed

Forgetting `self` gives: `TypeError: ... takes N positional arguments but N+1 were given`.
