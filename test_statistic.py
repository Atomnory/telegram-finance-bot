import pytest
from services.statistics.statistic import Statistic
from services.statistics.daystatistic import DayStatistic
from services.statistics.weekstatistic import WeekStatistic
from services.statistics.monthstatistic import MonthStatistic
from services.statistics.yearstatistic import YearStatistic
from db_test import create_test_db, init_test_db, delete_test_db


@pytest.fixture()
def db_env():
    create_test_db()
    init_test_db()

    yield

    delete_test_db()


def test_get_quantize_zero_decimal():
    stat = Statistic()
    assert '0.00' == str(stat._get_zero_decimal())


@pytest.mark.skip(reason="I can create new db but i can't test it because models bind with original db.")
def test_get_sum(db_env):
    day = DayStatistic()
    assert str(day._get_sum_stat()) == '325.00'
    assert str(day._get_sum_groceries()) == '300.00'

