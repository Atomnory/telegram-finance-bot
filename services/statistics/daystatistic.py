from .statistic import Statistic
from services.service import get_today_now
from .statisticformatter import StatisticFormatter


class DayStatistic(Statistic):
    def __init__(self):
        super().__init__()
        self._set_period()
        self._formatter = StatisticFormatter('day')

    def _set_period(self):
        self._period = get_today_now().date()
