import importlib
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from assistantbot.commands.base import BaseCommand

# Load environment variables
load_dotenv()


def get_implemented_command_handlers() -> List[BaseCommand]:
    """
    This function gets all the implemented handlers.

    Returns
    -------
    List[BaseCommand]
        The list of implemented handlers.
    """
    # Excluded commands. The temperature command is excluded because it is
    # implemented in a different way using the command factory pattern.
    excluded_commands = [
        "__init__",
        "base",
        "temperature",
        "get_expenses_base",
    ]

    # The implemented command is the intersection of the commands in the
    # commands directory and the commands configured in the bot
    implemented_commands = [
        command_file.stem
        for command_file in Path("assistantbot/commands").glob("*.py")
        if command_file.stem not in excluded_commands
    ]

    # Add the and start commands
    implemented_commands.append("start")

    # Import all the implemented commands. This is done to avoid circular
    # imports.
    final_implemented_classes = []
    for command in sorted(implemented_commands, reverse=True):
        class_name_handler = (
            f"{command.replace('_', ' ').title().replace(' ', '')}Command"
        )
        final_implemented_classes.append(
            getattr(
                importlib.import_module(f"assistantbot.commands.{command}"),
                class_name_handler,
            )
        )
    return final_implemented_classes
