from datetime import date
from playhouse.postgres_ext import fn
from models import TypeofCategory, Category, Expense
from .statistic import Statistic
from services.service import get_today_now
from .statisticformatter import StatisticFormatter


class MonthStatistic(Statistic):
    def __init__(self):
        super().__init__()
        self._set_period()
        self._formatter = StatisticFormatter('month')

    def _set_period(self):
        today = get_today_now()
        self._period = date(year=today.year, month=today.month, day=1)

    def get_sum(self) -> str:
        return self._try_get_sum_with_limit_statistic()

    def _select_groceries_sum_with_limit_query(self) -> Expense:
        groceries_monthly_limit_query = (Expense
                                         .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.monthly_limit)
                                         .join(Category)
                                         .join(TypeofCategory)
                                         .where((Expense.time_creating
                                                 .truncate(self._formatter.period_name) == self._period)
                                                & (TypeofCategory.monthly_limit.is_null(False)))
                                         .group_by(TypeofCategory.monthly_limit).tuples())
        return groceries_monthly_limit_query

    def _get_period_limit(self, type_name: str):
        type_category = TypeofCategory.get(TypeofCategory.name == type_name)
        return type_category.monthly_limit
