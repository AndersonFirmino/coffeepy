from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import CoffeeError
from .interpreter import Interpreter


def main() -> int:
    parser = argparse.ArgumentParser(prog="coffeepy")
    parser.add_argument("-e", "--eval", dest="eval_code", help="Evaluate Coffee source from a string")
    parser.add_argument("file", nargs="?", help="Path to a .coffee file")
    args = parser.parse_args()

    if args.eval_code is not None and args.file is not None:
        print("Use apenas --eval ou file, nao ambos.", file=sys.stderr)
        return 2

    if args.eval_code is None and args.file is None:
        print("CoffeePy bootstrap ativo. Use --eval ou um arquivo .coffee.")
        return 0

    if args.eval_code is not None:
        source = args.eval_code.replace("\\n", "\n")
    else:
        assert args.file is not None
        path = Path(args.file)
        if not path.exists():
            print(f"Arquivo nao encontrado: {path}", file=sys.stderr)
            return 1

        if path.suffix != ".coffee":
            print("Use um arquivo .coffee", file=sys.stderr)
            return 1

        source = path.read_text(encoding="utf-8")

    interpreter = Interpreter()
    try:
        result = interpreter.interpret(source)
    except CoffeeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"Falha interna: {exc}", file=sys.stderr)
        return 1

    if args.eval_code is not None and result is not None:
        print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
