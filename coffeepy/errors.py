from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ast_nodes import SourceLocation


class CoffeeError(Exception):
    """Base error for CoffeePy."""


class CoffeeLexerError(CoffeeError):
    """Raised for lexical errors."""


class CoffeeParseError(CoffeeError):
    """Raised for parse errors."""


class CoffeeRuntimeError(CoffeeError):
    """Raised for runtime evaluation errors."""
    
    def __init__(self, message: str, location: "SourceLocation | None" = None, source: str | None = None):
        super().__init__(message)
        self.message = message
        self.location = location
        self.source = source
    
    def __str__(self) -> str:
        if self.location is None:
            return self.message
        
        result = f"{self.message}\n  at {self.location}"
        
        if self.source:
            lines = self.source.split('\n')
            line_idx = self.location.line - 1
            if 0 <= line_idx < len(lines):
                line_text = lines[line_idx]
                result += f"\n    {line_text}"
                pointer = ' ' * (self.location.column - 1) + '^' * max(1, len(line_text) - self.location.column + 1)
                result += f"\n    {pointer}"
        
        return result
