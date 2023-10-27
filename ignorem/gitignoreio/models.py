from dataclasses import asdict, dataclass, fields
from typing import Iterable, Self

from ignorem.gitignoreio.types_ import TTemplate


@dataclass(frozen=True)
class TemplateModel:
    key: str
    name: str
    fileName: str  # noqa: N815
    contents: str

    @classmethod
    def fields(cls) -> Iterable[str]:
        return tuple(field.name for field in fields(cls))

    @classmethod
    def from_data(cls, data: TTemplate) -> Self:
        return cls(**data)

    def to_data(self) -> TTemplate:
        return asdict(self)  # type: ignore
