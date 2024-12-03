import enum
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto, unique
from uuid import UUID
import uuid


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


@dataclass(frozen=True, kw_only=True)
class AudioVideoMedia:
    id: UUID = field(default_factory=uuid.uuid4)
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus

@unique
class MediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"