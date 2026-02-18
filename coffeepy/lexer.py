from __future__ import annotations

from .errors import CoffeeLexerError
from .tokens import (
    AND,
    ANDAND,
    ANDAND_EQ,
    ARROW,
    AS,
    AT,
    BREAK,
    BY,
    CATCH,
    CLASS,
    COLON,
    COMMA,
    CONTINUE,
    DO,
    DOT,
    DOTDOT,
    DOTDOTDOT,
    ELLIPSIS,
    ELSE,
    EOF,
    EQ,
    EQEQ,
    EXTENDS,
    FAT_ARROW,
    FALSE,
    FINALLY,
    FOR,
    FROM,
    GET,
    GT,
    GTE,
    IDENT,
    IF,
    IMPORT,
    IN,
    INDENT,
    IS,
    ISNT,
    LBRACE,
    LBRACKET,
    LPAREN,
    LT,
    LTE,
    MINUS,
    MINUSMINUS,
    MINUS_EQ,
    NEQ,
    NEW,
    NEWLINE,
    NOT,
    NULL,
    NUMBER,
    OF,
    OR,
    OROR,
    OROR_EQ,
    OUTDENT,
    PERCENT,
    PERCENT_EQ,
    PLUS,
    PLUSPLUS,
    PLUS_EQ,
    PROTO,
    QUESTION,
    QUESTIONDOT,
    QUESTIONEQ,
    RBRACE,
    RBRACKET,
    RETURN,
    RPAREN,
    SEMICOLON,
    SET,
    SLASH,
    SLASH_EQ,
    STAR,
    STARSTAR,
    STAR_EQ,
    STRING,
    SUPER,
    SWITCH,
    THEN,
    THIS,
    THROW,
    TRUE,
    TRY,
    Token,
    UNDEFINED,
    UNTIL,
    UNLESS,
    WHEN,
    WHILE,
    YIELD,
)


KEYWORDS = {
    "import": IMPORT,
    "from": FROM,
    "as": AS,
    "return": RETURN,
    "if": IF,
    "unless": UNLESS,
    "while": WHILE,
    "until": UNTIL,
    "then": THEN,
    "else": ELSE,
    "and": AND,
    "or": OR,
    "not": NOT,
    "is": IS,
    "isnt": ISNT,
    "true": TRUE,
    "false": FALSE,
    "yes": TRUE,
    "no": FALSE,
    "on": TRUE,
    "off": FALSE,
    "null": NULL,
    "undefined": UNDEFINED,
    "break": BREAK,
    "continue": CONTINUE,
    "for": FOR,
    "in": IN,
    "of": OF,
    "class": CLASS,
    "extends": EXTENDS,
    "super": SUPER,
    "this": THIS,
    "new": NEW,
    "try": TRY,
    "catch": CATCH,
    "finally": FINALLY,
    "throw": THROW,
    "switch": SWITCH,
    "when": WHEN,
    "do": DO,
    "by": BY,
    "yield": YIELD,
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
            if self._match(":"):
                self._add_token(PROTO)
            else:
                self._add_token(COLON)
            return
        if ch == ",":
            self._add_token(COMMA)
            return
        if ch == ".":
            if self._match("."):
                if self._match("."):
                    self._add_token(DOTDOTDOT)
                else:
                    self._add_token(DOTDOT)
            else:
                self._add_token(DOT)
            return
        if ch == ";":
            self._add_token(SEMICOLON)
            return
        if ch == "@":
            self._add_token(AT)
            return
        if ch == "?":
            if self._match("."):
                self._add_token(QUESTIONDOT)
            elif self._match("="):
                self._add_token(QUESTIONEQ)
            else:
                self._add_token(QUESTION)
            return
        if ch == "&":
            if self._match("&"):
                if self._match("="):
                    self._add_token(ANDAND_EQ)
                else:
                    self._add_token(ANDAND)
            else:
                raise self._error("Unexpected character '&'.")
            return
        if ch == "|":
            if self._match("|"):
                if self._match("="):
                    self._add_token(OROR_EQ)
                else:
                    self._add_token(OROR)
            else:
                raise self._error("Unexpected character '|'.")
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
        if ch == "=":
            if self._match(">"):
                self._add_token(FAT_ARROW)
            elif self._match("="):
                self._add_token(EQEQ)
            else:
                self._add_token(EQ)
            return
        if ch == "*":
            if self._match("*"):
                self._add_token(STARSTAR)
            elif self._match("="):
                self._add_token(STAR_EQ)
            else:
                self._add_token(STAR)
            return
        if ch == "%":
            if self._match("="):
                self._add_token(PERCENT_EQ)
            else:
                self._add_token(PERCENT)
            return

        if ch in {'"', "'"}:
            self._string(ch)
            return

        if ch == "/":
            if self._peek() == "/" and self._peek_next() == "/":
                self._advance()
                self._advance()
                self._heregex()
            elif self._match("="):
                self._add_token(SLASH_EQ)
            elif self._peek() not in (" ", "\t", "\n", "\0", "/", "=") and self._peek() != "":
                self._regex()
            else:
                self._add_token(SLASH)
            return

        if ch.isdigit():
            self._number()
            return

        if self._is_identifier_start(ch):
            self._identifier()
            return

        raise self._error(f"Unexpected character '{ch}'.")

    def _string(self, quote: str) -> None:
        is_block = (self._peek() == quote and self._peek_next() == quote)
        if is_block:
            self._advance()
            self._advance()
            self._block_string(quote)
            return
        
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

    def _block_string(self, quote: str) -> None:
        chars: list[str] = []
        lines: list[str] = []
        current_line: list[str] = []
        
        while not self._is_at_end():
            ch = self._advance()
            
            if ch == quote and self._peek() == quote and self._peek_next() == quote:
                self._advance()
                self._advance()
                
                result = "".join(chars)
                result = self._dedent_block_string(result)
                self._add_token(STRING, result)
                return

            if ch == "\\":
                escaped = self._read_escape()
                chars.append(escaped)
                current_line.append(escaped)
                continue

            chars.append(ch)
            current_line.append(ch)
            
            if ch == "\n":
                lines.append("".join(current_line))
                current_line = []

        raise self._error("Unterminated block string.")

    def _dedent_block_string(self, text: str) -> str:
        lines = text.split("\n")
        
        if len(lines) > 0 and lines[0].strip() == "":
            lines = lines[1:]
        if len(lines) > 0 and lines[-1].strip() == "":
            lines = lines[:-1]
        
        if not lines:
            return ""
        
        min_indent = float("inf")
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        if min_indent == float("inf"):
            min_indent = 0
        
        result_lines = []
        for line in lines:
            if line.strip():
                result_lines.append(line[min_indent:])
            else:
                result_lines.append("")
        
        return "\n".join(result_lines)

    def _heregex(self) -> None:
        chars: list[str] = []
        
        while not self._is_at_end():
            ch = self._advance()
            
            if ch == "/" and self._peek() == "/" and self._peek_next() == "/":
                self._advance()
                self._advance()
                pattern = "".join(chars)
                pattern = self._normalize_heregex(pattern)
                self._add_token(STRING, pattern)
                return

            if ch == "\\":
                if not self._is_at_end():
                    next_ch = self._advance()
                    chars.append("\\")
                    chars.append(next_ch)
                continue

            if ch == "#":
                while not self._is_at_end() and self._peek() != "\n":
                    self._advance()
                continue

            if ch in " \t\n\r":
                continue

            chars.append(ch)

        raise self._error("Unterminated heregex.")

    def _regex(self) -> None:
        chars: list[str] = []
        
        while not self._is_at_end():
            ch = self._advance()
            
            if ch == "/":
                flags = ""
                while not self._is_at_end() and self._peek() in "gimsuy":
                    flags += self._advance()
                pattern = "".join(chars)
                self._add_token(STRING, ("regex", pattern, flags))
                return

            if ch == "\\":
                if not self._is_at_end():
                    next_ch = self._advance()
                    chars.append("\\")
                    chars.append(next_ch)
                continue

            if ch == "\n":
                raise self._error("Unterminated regex literal.")

            chars.append(ch)

        raise self._error("Unterminated regex literal.")

    def _normalize_heregex(self, pattern: str) -> str:
        result = []
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c == "\\" and i + 1 < len(pattern):
                result.append(c)
                result.append(pattern[i + 1])
                i += 2
                continue
            result.append(c)
            i += 1
        return "".join(result)

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
