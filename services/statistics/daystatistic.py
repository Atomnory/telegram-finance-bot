from .statistic import Statistic
from services.service import get_today_now


class DayStatistic(Statistic):
    def __init__(self):
        super().__init__()
        self._period_name = 'day'
        self._next_period_name = 'week'
        self._set_period()

    def _set_period(self):
        self._period = get_today_now().date()

    def get_sum(self) -> str:
        return self._try_get_sum_statistic()

    def get_by_category(self) -> str:
        return self._try_get_statistic_by_category()

    def get_by_type(self) -> str:
        return self._try_get_statistic_by_type()
