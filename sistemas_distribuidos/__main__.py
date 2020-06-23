# isort:skip_file
import importlib

from rich.traceback import install

# Setup rich traceback hook
install()

from logging import basicConfig
from rich.logging import RichHandler

# Setup rich logger handler
basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

import typing as T


def main() -> T.NoReturn:
    # Standard
    from os import path
    import sys

    programs: T.Dict[str, T.Callable[[], T.NoReturn]] = {
        "hello_server": (
            lambda: getattr(importlib.import_module("sistemas_distribuidos.hello"), "server")()
        ),
        "hello_client": (
            lambda: getattr(importlib.import_module("sistemas_distribuidos.hello"), "client")()
        ),
        "word_counter_server": (
            lambda: getattr(
                importlib.import_module("sistemas_distribuidos.word_counter"), "server"
            )()
        ),
        "word_counter_client": (
            lambda: getattr(
                importlib.import_module("sistemas_distribuidos.word_counter"), "client"
            )()
        ),
        "remote_calculator_server": (
            lambda: getattr(
                importlib.import_module("sistemas_distribuidos.calculator"), "server"
            )()
        ),
        "remote_calculator_client": (
            lambda: getattr(
                importlib.import_module("sistemas_distribuidos.calculator"), "client"
            )()
        ),
    }

    program_name = path.basename(sys.argv[0])
    if program_name not in programs:
        raise ValueError(f"Program {program_name} not implemented")

    programs[program_name]()
    sys.exit(0)


if __name__ == "__main__":
    main()
