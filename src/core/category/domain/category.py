from dataclasses import dataclass

from core._shared.domain.entity import Entity


@dataclass(eq=False)
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            # raise ValueError("name must have less than 256 characters")
            self.notification.add_error("name must have less than 256 characters")

        if not self.name:
            # raise ValueError("name is required")
            self.notification.add_error("name is required")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __repr__(self):
        return f"{self.name} - {self.description} - {self.is_active}"

    def update_category(self, name: str, description: str):
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
