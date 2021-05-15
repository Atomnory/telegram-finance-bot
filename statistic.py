# TODO: add def get_today_statistic()       -- Statistic handling
# TODO: add def get_week_statistic()        -- Statistic handling
# TODO: add def get_month_statistic()       -- Statistic handling


import db
import datetime
from pytz import timezone


def get_today_sum_statistic() -> str:
    today = _get_today()
    cur = db.get_cursor()

    # Try to SELECT at least one expense
    cur.execute(f"SELECT SUM(expense.amount) "
                f"FROM expense "
                f"WHERE expense.time_creating::DATE=%s::DATE", (today, ))  # TODO: test convert today
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense today"

    sum_all_today_expenses = result[0]
    return (f"Today expenses: \n"
            f"all: {sum_all_today_expenses} \u20BD \n"
            f"Week statistic: /week")


def get_week_sum_statistic() -> str:
    """ Get statistic of this iso week."""
    today = _get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute(f"SELECT SUM(expense.amount) "
                f"FROM expense "
                f"WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                f"AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s)", (today, today))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this week"

    sum_all_week_expenses = result[0]
    return (f"This week expenses: \n"
            f"all: {sum_all_week_expenses} \u20BD \n"
            f"Month statistic: /month")


def get_month_sum_statistic() -> str:
    today = _get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute(f"SELECT SUM(expense.amount) "
                f"FROM expense "
                f"WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                f"AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s);", (today, today))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this week"

    sum_all_month_expenses = result[0]
    return (f"This month expenses: \n"
            f"all: {sum_all_month_expenses} \u20BD \n"
            f"Year statistic: /year")


def get_year_sum_statistic() -> str:
    today = _get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute(f"SELECT SUM(expense.amount) "
                f"FROM expense "
                f"WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s);", (today, ))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this week"

    sum_all_year_expenses = result[0]
    return (f"This year expenses: \n"
            f"all: {sum_all_year_expenses} \u20BD \n"
            f"Day statistic: /day")


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

