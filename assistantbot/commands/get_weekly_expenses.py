from assistantbot.commands.get_expenses_base import GetExpensesCommand


class GetWeeklyExpensesCommand(GetExpensesCommand):
    """
    This class is the command that gets the weekly expenses.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_weekly_expenses"
        self._timeframe = "partial_weekly"
