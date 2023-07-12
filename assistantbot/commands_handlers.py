from pathlib import Path
from typing import List


def get_implemented_command_handlers() -> List[str]:
    """
    This function gets all the implemented handlers.

    Returns
    -------
    List[Callable[[None], Union[CommandHandler, List[CommandHandler]]]
        The list of implemented handlers.
    """
    path_commands = Path("assistantbot/commands")
    exclude_files = ["__pycache__", "base.py", "__init__.py"]

    implemented_handlers = [
        command.name
        for command in path_commands.iterdir()
        if command.name not in exclude_files
    ]

    return implemented_handlers


if __name__ == "__main__":
    print(get_implemented_command_handlers())
