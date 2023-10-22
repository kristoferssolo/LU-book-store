from attrs import define, field, validators


# TODO: create checksum method
@define(frozen=True)
class ISBN(str):
    number: str = field(converter=str, validator=validators.matches_re(r"^\d{10}$|^\d{13}$"))

    def __str__(self):
        if len(self.number) == 10:
            return f"{self.number[:9]}-{self.number[9:]}"
        return f"{self.number[:3]}-{self.number[3:4]}-{self.number[4:6]}-{self.number[6:12]}-{self.number[12:]}"
