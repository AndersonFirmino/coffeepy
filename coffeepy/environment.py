from __future__ import annotations

from .errors import CoffeeRuntimeError


class Environment:
    def __init__(self, parent: "Environment | None" = None):
        self.parent = parent
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assign(self, name: str, value: object) -> None:
        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        self.values[name] = value

    def get(self, name: str) -> object:
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise CoffeeRuntimeError(f"Undefined identifier '{name}'.")
