"""
CoffeePy - Main Entry Point
============================

This module provides the CLI and REPL for CoffeePy, a CoffeeScript dialect
that runs directly on Python.

Usage:
    python -m coffeepy script.coffee      # Run a file
    python -m coffeepy -i                  # Start REPL
    python -m coffeepy -e "print 1 + 2"    # Evaluate code

Commands in REPL:
    .exit   - Exit the REPL
    .help   - Show help
    .clear  - Clear input buffer

Author: Anderson Firmino
License: MIT
Version: 1.1.0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import CoffeeError
from .interpreter import Interpreter


def repl() -> int:
    """Start an interactive REPL session.
    
    Returns:
        Exit code (0 for success)
    """
    print("CoffeePy REPL (Python-first CoffeeScript)")
    print("Type .exit to quit, .help for help")
    print()
    
    interpreter = Interpreter()
    buffer = []
    continuation = False
    
    while True:
        try:
            if continuation:
                prompt = "....... "
            else:
                prompt = "coffee> "
            
            line = input(prompt)
            
            if line == ".exit":
                return 0
            
            if line == ".help":
                print("Commands:")
                print("  .exit  - Exit the REPL")
                print("  .help  - Show this help")
                print("  .clear - Clear the input buffer")
                print()
                continue
            
            if line == ".clear":
                buffer.clear()
                continuation = False
                print("Buffer cleared")
                continue
            
            if line.strip() == "":
                if buffer:
                    source = "\n".join(buffer)
                    try:
                        result = interpreter.interpret(source)
                        if result is not None:
                            print(result)
                    except CoffeeError as exc:
                        print(f"Error: {exc}")
                    except Exception as exc:
                        print(f"Error: {exc}")
                    buffer.clear()
                    continuation = False
                continue
            
            buffer.append(line)
            
            if line.rstrip().endswith("->") or line.rstrip().endswith("-> ") or line.rstrip().endswith("then"):
                continuation = True
            elif line.endswith(":"):
                continuation = True
            elif line.startswith("  ") or line.startswith("\t"):
                continuation = True
            else:
                test_source = "\n".join(buffer)
                try:
                    from .lexer import Lexer
                    from .parser import Parser
                    Lexer(test_source).tokenize()
                    Parser(Lexer(test_source).tokenize()).parse()
                    source = test_source
                    result = interpreter.interpret(source)
                    if result is not None:
                        print(result)
                    buffer.clear()
                    continuation = False
                except Exception:
                    continuation = True
        
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            buffer.clear()
            continuation = False
            continue
    
    return 0


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        prog="coffeepy",
        description="CoffeePy - CoffeeScript that runs on Python"
    )
    parser.add_argument("-e", "--eval", dest="eval_code", help="Evaluate Coffee source from a string")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start REPL")
    parser.add_argument("file", nargs="?", help="Path to a .coffee file")
    args = parser.parse_args()

    if args.interactive or (args.eval_code is None and args.file is None):
        return repl()

    if args.eval_code is not None:
        source = args.eval_code.replace("\\n", "\n")
    else:
        assert args.file is not None
        path = Path(args.file)
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            return 1

        if path.suffix != ".coffee":
            print("Use a .coffee file", file=sys.stderr)
            return 1

        source = path.read_text(encoding="utf-8")

    interpreter = Interpreter()
    try:
        result = interpreter.interpret(source)
    except CoffeeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Internal error: {exc}", file=sys.stderr)
        return 1

    if args.eval_code is not None and result is not None:
        print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
