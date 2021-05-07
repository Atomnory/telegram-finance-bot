# TODO: add def get_today_statistic()       -- Statistic handling
# TODO: add def get_week_statistic()        -- Statistic handling
# TODO: add def get_month_statistic()       -- Statistic handling


import db
import datetime
from pytz import timezone


def get_today_statistic():
    today = _get_today()
    cur = db.get_cursor()

    # Try to SELECT at least one expense
    cur.execute(f"SELECT SUM(amount) FROM expense WHERE DATE(time_creating)=DATE({today})")  # TODO: test convert today
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense today"

    today_expenses = result[0]
    return (f"Today expenses: \n"
            f"all: {today_expenses} rub.\n"
            f"Month statistic: /month")


def _get_today() -> datetime.datetime:
    msc = timezone('Europe/Moscow')
    today = datetime.datetime.now(msc)
    return today


def _get_today_formatted() -> str:
    """
        Return datetime without milliseconds and timezone.
        Maybe sqlite3 cannot convert not formatted datetime throw DATE() func.
    """
    return _get_today().strftime("%Y-%m-%d %H:%M:%S")


def _get_budget_limit():
    pass

# td.date() return year, month, day
# td.isocalendar() return year, week of year, weekday
# td.isocalendar()[1] return week of year
# td.year return year
# td.month return month
# td.day return day

