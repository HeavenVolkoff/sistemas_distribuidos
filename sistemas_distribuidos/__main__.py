# isort:skip_file

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

    # External
    from sistemas_distribuidos import hello
    from sistemas_distribuidos import calculator

    programs = {
        "hello_server": hello.server,
        "hello_client": hello.client,
        "remote_calculator_server": calculator.server,
        "remote_calculator_client": calculator.client,
    }

    program_name = path.basename(sys.argv[0])
    if program_name not in programs:
        raise ValueError(f"Program {program_name} not implemented")

    programs[program_name]()
    sys.exit(0)


if __name__ == "__main__":
    main()
