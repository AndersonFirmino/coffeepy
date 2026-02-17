from __future__ import annotations


class CoffeeError(Exception):
    """Base error for CoffeePy."""


class CoffeeLexerError(CoffeeError):
    """Raised for lexical errors."""


class CoffeeParseError(CoffeeError):
    """Raised for parse errors."""


class CoffeeRuntimeError(CoffeeError):
    """Raised for runtime evaluation errors."""
