from typing import Union

from typing_extensions import Literal

ByteOrder = Union[Literal["big"], Literal["little"]]

LITTLE: Literal["little"] = "little"
BIG: Literal["big"] = "big"
