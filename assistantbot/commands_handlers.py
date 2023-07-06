from telegram.ext import CommandHandler

from typing import List, Callable, Union
from pathlib import Path
import importlib


def get_implemented_command_handlers() -> List[
    Callable[[None], Union[CommandHandler, List[CommandHandler]]]
]:
    """
    This function gets all the implemented handlers.

    Returns
    -------
    List[Callable[[None], Union[CommandHandler, List[CommandHandler]]]
        The list of implemented handlers.
    """
    path_commands = Path("assistantbot/commands")
    implemented_handlers = []

    for path in path_commands.iterdir():
        if path.is_dir():
            for file in path.iterdir():
                if file.is_file():
                    if file.name == "handlers.py":
                        module = importlib.import_module(
                            f"assistantbot.commands.{path.name}.handlers"
                        )
                        # Load the function {path.name} from the module
                        implemented_handlers.append(
                            getattr(module, f"{path.name}_handler")
                        )

    return implemented_handlers
