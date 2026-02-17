from __future__ import annotations

from .errors import CoffeeLexerError
from .tokens import (
    AND,
    ARROW,
    AS,
    COLON,
    COMMA,
    DOT,
    ELSE,
    EOF,
    EQ,
    EQEQ,
    FALSE,
    FROM,
    GT,
    GTE,
    IDENT,
    IF,
    IMPORT,
    INDENT,
    LBRACE,
    LBRACKET,
    LPAREN,
    LT,
    LTE,
    MINUS,
    MINUSMINUS,
    MINUS_EQ,
    NEQ,
    NEWLINE,
    NOT,
    NULL,
    NUMBER,
    OR,
    OUTDENT,
    PERCENT,
    PLUS,
    PLUSPLUS,
    PLUS_EQ,
    RBRACE,
    RBRACKET,
    RETURN,
    RPAREN,
    SEMICOLON,
    SLASH,
    STAR,
    STARSTAR,
    STRING,
    THEN,
    TRUE,
    Token,
    UNDEFINED,
    UNLESS,
)


KEYWORDS = {
    "import": IMPORT,
    "from": FROM,
    "as": AS,
    "return": RETURN,
    "if": IF,
    "unless": UNLESS,
    "then": THEN,
    "else": ELSE,
    "and": AND,
    "or": OR,
    "not": NOT,
    "true": TRUE,
    "false": FALSE,
    "yes": TRUE,
    "no": FALSE,
    "on": TRUE,
    "off": FALSE,
    "null": NULL,
    "undefined": UNDEFINED,
}


class Lexer:
    def __init__(self, source: str):
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1
        self.at_line_start = True
        self.indents = [0]

    def tokenize(self) -> list[Token]:
        while not self._is_at_end():
            if self.at_line_start and self._consume_line_prefix():
                continue

            if self._is_at_end():
                break

            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()

        while len(self.indents) > 1:
            self.indents.pop()
            self.tokens.append(Token(OUTDENT, "", None, self.line, 1))

        self.tokens.append(Token(EOF, "", None, self.line, self.column))
        return self.tokens

    def _consume_line_prefix(self) -> bool:
        indent = 0
        while not self._is_at_end() and self._peek() in {" ", "\t"}:
            ch = self._advance()
            indent += 4 if ch == "\t" else 1

        if self._is_at_end():
            return False

        if self._peek() == "\n":
            self._emit_newline()
            return True

        if self._peek() == "#":
            while not self._is_at_end() and self._peek() != "\n":
                self._advance()
            if not self._is_at_end() and self._peek() == "\n":
                self._emit_newline()
            return True

        current_indent = self.indents[-1]
        if indent > current_indent:
            self.indents.append(indent)
            self.tokens.append(Token(INDENT, "", None, self.line, 1))
        elif indent < current_indent:
            while indent < self.indents[-1]:
                self.indents.pop()
                self.tokens.append(Token(OUTDENT, "", None, self.line, 1))
            if indent != self.indents[-1]:
                raise self._error("Inconsistent indentation.")

        self.at_line_start = False
        return False

    def _emit_newline(self) -> None:
        line = self.line
        column = self.column
        self._advance()  # consume '\n'
        self.tokens.append(Token(NEWLINE, "\n", None, line, column))
        self.at_line_start = True

    def _scan_token(self) -> None:
        ch = self._advance()

        if ch in {" ", "\t"}:
            return

        if ch == "\n":
            self.tokens.append(Token(NEWLINE, "\n", None, self.start_line, self.start_column))
            self.at_line_start = True
            return

        if ch == "#":
            while not self._is_at_end() and self._peek() != "\n":
                self._advance()
            return

        if ch == "(":
            self._add_token(LPAREN)
            return
        if ch == ")":
            self._add_token(RPAREN)
            return
        if ch == "[":
            self._add_token(LBRACKET)
            return
        if ch == "]":
            self._add_token(RBRACKET)
            return
        if ch == "{":
            self._add_token(LBRACE)
            return
        if ch == "}":
            self._add_token(RBRACE)
            return
        if ch == ":":
            self._add_token(COLON)
            return
        if ch == ",":
            self._add_token(COMMA)
            return
        if ch == ".":
            self._add_token(DOT)
            return
        if ch == ";":
            self._add_token(SEMICOLON)
            return
        if ch == "=":
            if self._match("="):
                self._add_token(EQEQ)
            else:
                self._add_token(EQ)
            return
        if ch == "!":
            if self._match("="):
                self._add_token(NEQ)
                return
            raise self._error("Unexpected character '!'.")
        if ch == "<":
            if self._match("="):
                self._add_token(LTE)
            else:
                self._add_token(LT)
            return
        if ch == ">":
            if self._match("="):
                self._add_token(GTE)
            else:
                self._add_token(GT)
            return
        if ch == "+":
            if self._match("+"):
                self._add_token(PLUSPLUS)
            elif self._match("="):
                self._add_token(PLUS_EQ)
            else:
                self._add_token(PLUS)
            return
        if ch == "-":
            if self._match(">"):
                self._add_token(ARROW)
            elif self._match("-"):
                self._add_token(MINUSMINUS)
            elif self._match("="):
                self._add_token(MINUS_EQ)
            else:
                self._add_token(MINUS)
            return
        if ch == "*":
            if self._match("*"):
                self._add_token(STARSTAR)
            else:
                self._add_token(STAR)
            return
        if ch == "/":
            self._add_token(SLASH)
            return
        if ch == "%":
            self._add_token(PERCENT)
            return

        if ch in {'"', "'"}:
            self._string(ch)
            return

        if ch.isdigit():
            self._number()
            return

        if self._is_identifier_start(ch):
            self._identifier()
            return

        raise self._error(f"Unexpected character '{ch}'.")

    def _string(self, quote: str) -> None:
        chars: list[str] = []

        while not self._is_at_end():
            ch = self._advance()
            if ch == quote:
                self._add_token(STRING, "".join(chars))
                return

            if ch == "\\":
                chars.append(self._read_escape())
                continue

            if ch == "\n":
                raise self._error("Unterminated string literal.")

            chars.append(ch)

        raise self._error("Unterminated string literal.")

    def _read_escape(self) -> str:
        if self._is_at_end():
            raise self._error("Unterminated string literal.")

        ch = self._advance()
        escapes = {
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "b": "\b",
            "f": "\f",
            "v": "\v",
            "0": "\0",
            "\\": "\\",
            '"': '"',
            "'": "'",
        }

        if ch in escapes:
            return escapes[ch]

        if ch == "x":
            return self._read_fixed_hex_escape(2)
        if ch == "u":
            if self._peek() == "{":
                self._advance()
                return self._read_braced_unicode_escape()
            return self._read_fixed_hex_escape(4)

        return ch

    def _read_fixed_hex_escape(self, width: int) -> str:
        digits: list[str] = []
        for _ in range(width):
            if self._is_at_end():
                raise self._error("Invalid escape sequence.")
            ch = self._advance()
            if ch not in "0123456789abcdefABCDEF":
                raise self._error("Invalid escape sequence.")
            digits.append(ch)

        return chr(int("".join(digits), 16))

    def _read_braced_unicode_escape(self) -> str:
        digits: list[str] = []
        while not self._is_at_end() and self._peek() != "}":
            ch = self._advance()
            if ch not in "0123456789abcdefABCDEF":
                raise self._error("Invalid unicode escape sequence.")
            digits.append(ch)

        if self._is_at_end() or not self._match("}"):
            raise self._error("Invalid unicode escape sequence.")
        if not digits:
            raise self._error("Invalid unicode escape sequence.")

        codepoint = int("".join(digits), 16)
        if codepoint > 0x10FFFF:
            raise self._error("Invalid unicode escape sequence.")
        return chr(codepoint)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()

        text = self.source[self.start : self.current]
        literal: object
        if "." in text:
            literal = float(text)
        else:
            literal = int(text)

        self._add_token(NUMBER, literal)

    def _identifier(self) -> None:
        while self._is_identifier_part(self._peek()):
            self._advance()

        text = self.source[self.start : self.current]
        kind = KEYWORDS.get(text, IDENT)
        self._add_token(kind)

    def _add_token(self, kind: str, literal: object = None) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(kind, lexeme, literal, self.start_line, self.start_column))

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    @staticmethod
    def _is_identifier_start(ch: str) -> bool:
        return ch.isalpha() or ch in {"_", "$"}

    @staticmethod
    def _is_identifier_part(ch: str) -> bool:
        return ch.isalnum() or ch in {"_", "$"}

    def _error(self, message: str) -> CoffeeLexerError:
        return CoffeeLexerError(f"{message} (line {self.start_line}, column {self.start_column})")
