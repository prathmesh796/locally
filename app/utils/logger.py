import logging
from rich.console import Console
from rich.logging import RichHandler

console = Console()

def get_logger(name: str):
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger(name)

logger = get_logger("locally796")
