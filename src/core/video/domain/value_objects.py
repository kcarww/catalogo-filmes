import enum
from dataclasses import dataclass
from enum import Enum, auto, unique
from uuid import UUID


@unique
class Rating(Enum):
    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"


@unique
class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()


@dataclass(frozen=True)
class ImageMedia:
    id: UUID
    check_sum: str
    name: str
    location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus