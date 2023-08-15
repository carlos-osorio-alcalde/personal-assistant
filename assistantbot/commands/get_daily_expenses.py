from assistantbot.commands.get_expenses_base import GetExpensesCommand
from assistantbot.utils.expenses import get_expenses_a_day_like_today


class GetDailyExpensesCommand(GetExpensesCommand):
    """
    This class is the command that gets the daily expenses.
    """

    def __init__(self):
        super().__init__()
        self._command = "get_daily_expenses"
        self._timeframe = "daily"
        (
            self._mean_num_purchases,
            self._median_amount_purchases,
        ) = get_expenses_a_day_like_today()
