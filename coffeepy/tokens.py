from __future__ import annotations

from dataclasses import dataclass


EOF = "EOF"
NEWLINE = "NEWLINE"
SEMICOLON = "SEMICOLON"
INDENT = "INDENT"
OUTDENT = "OUTDENT"

IDENT = "IDENT"
NUMBER = "NUMBER"
STRING = "STRING"

LPAREN = "LPAREN"
RPAREN = "RPAREN"
COMMA = "COMMA"
DOT = "DOT"
COLON = "COLON"
LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"
LBRACE = "LBRACE"
RBRACE = "RBRACE"

EQ = "EQ"
EQEQ = "EQEQ"
NEQ = "NEQ"
LT = "LT"
LTE = "LTE"
GT = "GT"
GTE = "GTE"
PLUS = "PLUS"
MINUS = "MINUS"
STAR = "STAR"
STARSTAR = "STARSTAR"
SLASH = "SLASH"
PERCENT = "PERCENT"
ARROW = "ARROW"

IMPORT = "IMPORT"
FROM = "FROM"
AS = "AS"
RETURN = "RETURN"
IF = "IF"
UNLESS = "UNLESS"
THEN = "THEN"
ELSE = "ELSE"
AND = "AND"
OR = "OR"
NOT = "NOT"

TRUE = "TRUE"
FALSE = "FALSE"
NULL = "NULL"
UNDEFINED = "UNDEFINED"


@dataclass(frozen=True)
class Token:
    kind: str
    lexeme: str
    literal: object
    line: int
    column: int
