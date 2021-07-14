from datetime import date
from .statistic import Statistic
from services.service import get_today_now


class YearStatistic(Statistic):
    def __init__(self):
        super().__init__()
        self._period_name = 'year'
        self._next_period_name = 'day'
        self._set_period()

    def _set_period(self):
        today = get_today_now()
        self._period = date(year=today.year, month=1, day=1)

    def get_sum(self) -> str:
        return self._try_get_sum_statistic()

    def get_by_category(self) -> str:
        return self._try_get_statistic_by_category()

    def get_by_type(self) -> str:
        return self._try_get_statistic_by_type()
