from assistantbot.commands.get_expenses_base import GetExpensesCommand


class GetMonthlyExpensesCommand(GetExpensesCommand):
    """
    This class is the command that gets the monthly expenses.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_monthly_expenses"
        self._timeframe = "monthly"
