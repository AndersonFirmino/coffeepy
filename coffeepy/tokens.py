"""
CoffeePy - Token Definitions
============================

This module defines all token types and the Token dataclass used by the lexer.

Token Types:
    - Literals: NUMBER, STRING
    - Identifiers: IDENT
    - Keywords: IF, THEN, ELSE, FOR, WHILE, CLASS, etc.
    - Operators: PLUS, MINUS, STAR, SLASH, etc.
    - Punctuation: LPAREN, RPAREN, LBRACE, RBRACE, etc.
    - Special: EOF, NEWLINE, INDENT, OUTDENT
"""

from __future__ import annotations

from dataclasses import dataclass


# ============ Special Tokens ============
EOF = "EOF"           # End of file
NEWLINE = "NEWLINE"   # Line break
SEMICOLON = "SEMICOLON"  # Semicolon ;
INDENT = "INDENT"     # Indentation increase
OUTDENT = "OUTDENT"   # Indentation decrease

# ============ Literals ============
IDENT = "IDENT"       # Identifier (variable/function names)
NUMBER = "NUMBER"     # Numbers: 42, 3.14, 0xFF
STRING = "STRING"     # Strings: "hello", 'world', """block"""

# ============ Punctuation ============
LPAREN = "LPAREN"     # (
RPAREN = "RPAREN"     # )
COMMA = "COMMA"       # ,
DOT = "DOT"           # .
COLON = "COLON"       # :
LBRACKET = "LBRACKET" # [
RBRACKET = "RBRACKET" # ]
LBRACE = "LBRACE"     # {
RBRACE = "RBRACE"     # }

# ============ Comparison Operators ============
EQ = "EQ"             # =
EQEQ = "EQEQ"         # == (is)
NEQ = "NEQ"           # != (isnt)
LT = "LT"             # <
LTE = "LTE"           # <=
GT = "GT"             # >
GTE = "GTE"           # >=
IS = "IS"             # is alias
ISNT = "ISNT"         # isnt alias

# ============ Arithmetic Operators ============
PLUS = "PLUS"         # +
PLUSPLUS = "PLUSPLUS" # ++
PLUS_EQ = "PLUS_EQ"   # +=
MINUS = "MINUS"       # -
MINUSMINUS = "MINUSMINUS"  # --
MINUS_EQ = "MINUS_EQ" # -=
STAR = "STAR"         # *
STARSTAR = "STARSTAR" # ** (power)
STAR_EQ = "STAR_EQ"   # *=
SLASH = "SLASH"       # /
SLASH_EQ = "SLASH_EQ" # /=
PERCENT = "PERCENT"   # %
PERCENT_EQ = "PERCENT_EQ"  # %=

# ============ Logical Operators ============
AND = "AND"           # and
OR = "OR"             # or
NOT = "NOT"           # not
ANDAND = "ANDAND"     # &&
OROR = "OROR"         # ||
ANDAND_EQ = "ANDAND_EQ"  # &&=
OROR_EQ = "OROR_EQ"   # ||=

# ============ CoffeeScript Operators ============
ARROW = "ARROW"       # -> (function)
FAT_ARROW = "FAT_ARROW"  # => (bound function)
DOTDOT = "DOTDOT"     # .. (inclusive range)
DOTDOTDOT = "DOTDOTDOT"  # ... (exclusive range or splat)
ELLIPSIS = "ELLIPSIS"  # ...
AT = "AT"             # @ (this)
PROTO = "PROTO"       # :: (prototype access)
QUESTION = "QUESTION"  # ?
QUESTIONDOT = "QUESTIONDOT"  # ?.
QUESTIONEQ = "QUESTIONEQ"  # ?=
DO = "DO"             # do (IIFE)
BY = "BY"             # by (range step)
YIELD = "YIELD"       # yield (generators)
GET = "GET"           # get (property getter)
SET = "SET"           # set (property setter)

# ============ Keywords ============
IMPORT = "IMPORT"     # import
FROM = "FROM"         # from
AS = "AS"             # as
RETURN = "RETURN"     # return
IF = "IF"             # if
UNLESS = "UNLESS"     # unless
WHILE = "WHILE"       # while
UNTIL = "UNTIL"       # until
THEN = "THEN"         # then
ELSE = "ELSE"         # else
TRUE = "TRUE"         # true, yes, on
FALSE = "FALSE"       # false, no, off
NULL = "NULL"         # null
UNDEFINED = "UNDEFINED"  # undefined
BREAK = "BREAK"       # break
CONTINUE = "CONTINUE"  # continue
FOR = "FOR"           # for
IN = "IN"             # in
OF = "OF"             # of
CLASS = "CLASS"       # class
EXTENDS = "EXTENDS"   # extends
SUPER = "SUPER"       # super
THIS = "THIS"         # this
NEW = "NEW"           # new
TRY = "TRY"           # try
CATCH = "CATCH"       # catch
FINALLY = "FINALLY"   # finally
THROW = "THROW"       # throw
SWITCH = "SWITCH"     # switch
WHEN = "WHEN"         # when


@dataclass(frozen=True)
class Token:
    """Represents a lexical token.
    
    Attributes:
        kind: The token type (e.g., 'NUMBER', 'IDENT', 'IF')
        lexeme: The raw text of the token
        literal: The parsed value (for NUMBER and STRING tokens)
        line: Line number (1-indexed)
        column: Column number (1-indexed)
    """
    kind: str
    lexeme: str
    literal: object
    line: int
    column: int
