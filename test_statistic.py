import pytest
import datetime
from services import statistic
from utils import exceptions


class TestDateTruncating:
    def test_return_today(self):
        today = datetime.date.today()
        assert today == statistic._get_today_truncated_to_date()


class TestGetNextPeriod:
    def test_invalid_period(self):
        with pytest.raises(exceptions.InvalidPeriod):
            any_str = ''
            statistic.get_next_period_name(any_str)
    
    def test_valid_period_day(self):
        period = 'day'
        next_period = 'week'
        assert statistic.get_next_period_name(period) == next_period

    def test_valid_period_week(self):
        period = 'week'
        next_period = 'month'
        assert statistic.get_next_period_name(period) == next_period

    def test_valid_period_month(self):
        period = 'month'
        next_period = 'year'
        assert statistic.get_next_period_name(period) == next_period

    def test_valid_period_year(self):
        period = 'year'
        next_period = 'day'
        assert statistic.get_next_period_name(period) == next_period


class TestGetNextDetailPeriod:
    def test_invalid_period(self):
        with pytest.raises(exceptions.InvalidPeriod):
            any_str = 'day'
            statistic.get_next_detail_period_name(any_str)

    def test_valid_period_week(self):
        period = 'week'
        next_period = 'month'
        assert statistic.get_next_detail_period_name(period) == next_period

    def test_valid_period_month(self):
        period = 'month'
        next_period = 'week'
        assert statistic.get_next_detail_period_name(period) == next_period

