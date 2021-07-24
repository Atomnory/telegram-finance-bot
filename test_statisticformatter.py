import pytest
from services.statistics.statisticformatter import StatisticFormatter


class TestStatisticFormatter:
    def test_next_period_name_day(self):
        answer = (f"There's none any expense in this day \n\n"
                f"Week statistic: /week")
        sf = StatisticFormatter('day')
        sf.format_answer_sum_error()
        assert sf.answer == answer

    def test_next_period_name_week(self):
        answer = (f"There's none any expense in this week \n\n"
                f"Month statistic: /month")
        sf = StatisticFormatter('week')
        sf.format_answer_sum_error()
        assert sf.answer == answer

    def test_next_period_name_month(self):
        answer = (f"There's none any expense in this month \n\n"
                f"Year statistic: /year")
        sf = StatisticFormatter('month')
        sf.format_answer_sum_error()
        assert sf.answer == answer

    def test_next_period_name_year(self):
        answer = (f"There's none any expense in this year \n\n"
                f"Day statistic: /day")
        sf = StatisticFormatter('year')
        sf.format_answer_sum_error()
        assert sf.answer == answer

    def test_next_period_name_invalid_error(self):
        with pytest.raises(AttributeError):
            sf = StatisticFormatter('invalid')
            sf.format_answer_sum_error()

    def test_next_detail_period_name_day_error(self):
        with pytest.raises(AttributeError):
            sf = StatisticFormatter('day')
            sf.format_answer_detail_error()

    def test_next_detail_period_name_week(self):
        answer = (f"There's none such expense in this week \n\n"
                f"Month detail statistic: "
                f"/month_detail")
        sf = StatisticFormatter('week')
        sf.format_answer_detail_error()
        assert sf.answer == answer

    def test_next_detail_period_name_month(self):
        answer = (f"There's none such expense in this month \n\n"
                  f"Week detail statistic: "
                  f"/week_detail")
        sf = StatisticFormatter('month')
        sf.format_answer_detail_error()
        assert sf.answer == answer

    def test_next_detail_period_name_year_error(self):
        with pytest.raises(AttributeError):
            sf = StatisticFormatter('year')
            sf.format_answer_detail_error()

    def test_next_detail_period_name_invalid_error(self):
        with pytest.raises(AttributeError):
            sf = StatisticFormatter('invalid')
            sf.format_answer_detail_error()
