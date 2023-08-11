from assistantbot.commands.get_expenses_base import GetExpensesCommand


class GetDailyExpensesCommand(GetExpensesCommand):
    """
    This class is the command that gets the daily expenses.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_daily_expenses"
        self._timeframe = "daily"
