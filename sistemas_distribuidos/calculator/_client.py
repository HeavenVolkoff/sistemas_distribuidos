# Standard
from cmd import Cmd
import typing as T

# External
import click

# Project
from .. import rpc

try:
    import readline
except ImportError:
    pass


class CalculatorCmd(Cmd):
    intro = "Welcome to remote calculator. Type help or ? to list commands.\n"
    prompt = "> "

    def __init__(self, connection: T.Generator[rpc.Response, rpc.Request, None]):
        super().__init__()

        self._connection = connection

    def _do(self, name: str, line: str) -> bool:
        try:
            response = self._connection.send({"name": name, "args": tuple(map(int, line.split()))})
        except StopIteration:
            print("Connection to remote server was closed")
            return True

        if response["error"]:
            raise RuntimeError(response["error"])
        print(response["data"])

        return False

    def do_add(self, line: str) -> bool:
        """Add all given numbers"""
        return self._do("add", line)

    def do_sub(self, line: str) -> bool:
        """Subtract all given numbers"""
        return self._do("sub", line)

    def do_mul(self, line: str) -> bool:
        """Multiply all given numbers"""
        return self._do("mul", line)

    def do_div(self, line: str) -> bool:
        """Divide all given numbers"""
        return self._do("div", line)

    def do_exit(self, _: str) -> bool:
        """Exit Calculator"""
        self._connection.close()
        return True


@click.command()
@click.option(
    "--host",
    "-h",
    type=str,
    default="localhost",
    help="Address for the host serving the hello server.",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=5678,
    help="Port where the hello server is available in the remote host.",
)
def client(host: str = "localhost", port: int = 5678) -> T.NoReturn:
    """Remote calculator client."""
    connection = rpc.client(host, port)
    connection.send(None)  # type: ignore [arg-type]
    CalculatorCmd(connection).cmdloop()
    exit(0)


if __name__ == "__main__":
    client()
