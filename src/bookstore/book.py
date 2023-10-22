from attrs import define, field, setters, validators

from .isbn import ISBN


def _check_price_value(instance, attribute, value):
    if value < 0:
        raise ValueError("Price must be larger or equal to 0!")


def _check_stock_value(instance, attribute, value):
    if value < 0:
        raise ValueError("Stock must be larger or equal to 0!")


@define
class Book:
    title: str = field()
    author: str = field()  # TODO: add default author as "Unknown"
    isbn: ISBN = field(on_setattr=setters.frozen, repr=lambda value: f"'{value}'")
    price: float = field(converter=float, validator=[validators.instance_of(float), _check_price_value])
    stock: int = field(converter=int, validator=[validators.instance_of(int), _check_stock_value])
