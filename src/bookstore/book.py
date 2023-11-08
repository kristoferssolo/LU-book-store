from attrs import define, field, setters, validators

from .isbn import ISBN


def _check_price_value(instance, attribute, value):
    if value < 0:
        raise ValueError("Price must be larger or equal to 0!")


def _check_stock_value(instance, attribute, value):
    if value < 0:
        raise ValueError("Stock must be larger or equal to 0!")


def _to_isbn(number: str):
    return ISBN(number)


@define
class Book:
    isbn: ISBN = field(converter=_to_isbn, validator=validators.instance_of(ISBN), on_setattr=setters.frozen, repr=lambda value: f"'{value}'")
    title: str = field()
    author: str = field()
    price: float = field(converter=float, validator=[validators.instance_of(float), _check_price_value])
    stock: int = field(converter=int, validator=[validators.instance_of(int), _check_stock_value])

    @classmethod
    def fields(cls) -> tuple[str, str, str, str, str]:
        return "ISBN", "Title", "Author", "Price", "Stock"

    def values(self) -> tuple[ISBN, str, str, float, int]:
        return self.isbn, self.title, self.author, self.price, self.stock

    def get(self, field: str, default: str = "") -> ISBN | str | float | int:
        match field:
            case "ISBN":
                return self.isbn
            case "Title":
                return self.title
            case "Author":
                return self.author
            case "Price":
                return self.price
            case "Stock":
                return self.stock
            case _:
                return default

    def __iter__(self):
        yield from self.values()
