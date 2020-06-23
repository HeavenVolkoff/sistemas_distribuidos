# Standard
from collections import Counter
import re
import string
import typing as T

# External
import click

# Project
from .. import rpc

punctuation_map = dict.fromkeys(ord(c) for c in string.punctuation)


def count_words(content: str) -> T.Sequence[T.Tuple[str, int]]:
    return Counter(str(content).translate(punctuation_map).split()).most_common()


@click.command()
@click.option(
    "--host",
    "-h",
    type=str,
    default="localhost",
    help="Interface address which will be used to expose the hello server",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=5678,
    help="Port which will be used to accept connection to the hello server",
)
def server(host: str = "localhost", port: int = 5678) -> T.NoReturn:
    """Remote calculator server."""
    rpc.server(host, port, {"count_words": count_words})
    exit(0)


if __name__ == "__main__":
    server()
