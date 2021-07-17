from datetime import date
from .statistic import Statistic
from services.service import get_today_now
from .statisticformatter import StatisticFormatter


class YearStatistic(Statistic):
    def __init__(self):
        super().__init__()
        self._set_period()
        self._formatter = StatisticFormatter('year')

    def _set_period(self):
        today = get_today_now()
        self._period = date(year=today.year, month=1, day=1)
