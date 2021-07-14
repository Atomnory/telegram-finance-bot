from datetime import date
from playhouse.postgres_ext import fn
from models import TypeofCategory, Category, Expense
from .statistic import Statistic
from services.service import get_today_now


class WeekStatistic(Statistic):
    def __init__(self):
        super().__init__()
        self._period_name = 'week'
        self._next_period_name = 'month'
        self._next_detail_period_name = 'month'
        self._set_period()

    def _set_period(self):
        today = get_today_now()
        self._period = date.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=1)

    def get_sum(self) -> str:
        return self._try_get_sum_with_limit_statistic()

    def get_by_category(self) -> str:
        return self._try_get_statistic_by_category()

    def get_by_type(self) -> str:
        return self._try_get_statistic_by_type()

    def get_with_detail(self):
        return self._try_get_detail_statistic()

    def _select_groceries_sum_with_limit_query(self) -> Expense:
        groceries_weekly_limit_query = (Expense
                                        .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.weekly_limit)
                                        .join(Category)
                                        .join(TypeofCategory)
                                        .where((Expense.time_creating.truncate(self._period_name) == self._period)
                                               & (TypeofCategory.weekly_limit.is_null(False)))
                                        .group_by(TypeofCategory.weekly_limit).tuples())
        return groceries_weekly_limit_query

    def _get_period_limit(self, type_name: str):
        type_category = TypeofCategory.get(TypeofCategory.name == type_name)
        return type_category.weekly_limit
