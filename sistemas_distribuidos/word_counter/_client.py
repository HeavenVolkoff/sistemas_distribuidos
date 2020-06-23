# Standard
from sys import stderr
from pathlib import Path
import typing as T

# External
from rich.table import Table
from rich.console import Console
from rich.progress import Progress
import click

# Project
from .. import rpc


@click.command()
@click.argument("file", type=str)
@click.option(
    "--host",
    "-h",
    type=str,
    default="localhost",
    help="Address for the host serving the calculator server.",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=5678,
    help="Port where the calculator server is available in the remote host.",
)
def client(file: str, host: str = "localhost", port: int = 5678) -> T.NoReturn:
    """Count word frequency of a text file.

    FILE is the path for a file to be uploaded to the server, so it's words can be counted.

    """
    path = Path(file)
    console = Console()
    console_err = Console(file=stderr)
    with Progress(console=console, transient=True) as progress:
        progress.add_task(f"Processing file {path.absolute()}", start=False)
        connection = rpc.client(host, port)
        connection.send(None)  # type: ignore [arg-type]
        try:
            response: rpc.Response = connection.send(
                rpc.Request(
                    name="count_words", args=[path.read_text(errors="replace", encoding="utf8")]
                )
            )
        except StopIteration:
            raise ConnectionAbortedError("Server closed the connection unexpectedly") from None

        if error := response["error"]:
            console_err.print(f"Request failed due to: {error}")
            exit(-1)

        table = Table(show_lines=True, show_header=True, header_style="bold magenta")
        table.add_column("Word")
        table.add_column("Count")

        data: T.Sequence[T.Tuple[str, int]] = response["data"]
        for name, value in data:
            table.add_row(name, str(value))

        console.print(table)
    exit(0)


if __name__ == "__main__":
    client()
