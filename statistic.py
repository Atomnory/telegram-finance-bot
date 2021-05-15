# TODO: add funcs with category statistic with payment for each period
# TODO: add funcs with type statistic with payment for each period
# TODO: add funcs with detail statistic with additional info for 4 and 5 types for week and month


import db
import datetime
from pytz import timezone
from decimal import Decimal


def _get_quantize_zero_decimal() -> Decimal:
    """
        Return Decimal with two trailing zeros because all 'amount's from db have two precision numbers
        and keep that style will be better.
    """
    return Decimal(0.00).quantize(Decimal('1.11'))


def get_today_sum_statistic() -> str:
    """ Get statistic of today."""
    today = _get_today()
    cur = db.get_cursor()

    # Try to SELECT at least one expense
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE expense.time_creating::DATE=%s::DATE", (today, ))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense today"
    sum_today_all_expenses = result[0]

    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE type_of_category.type_name='Grocery' "       # TODO: change to 'Groceries'
                "AND expense.time_creating::DATE=%s::DATE", (today, ))
    result = cur.fetchone()

    # Return sum of all today groceries expenses or 0.00 if that expenses doesn't exist
    sum_today_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()

    return (f"Today expenses: \n"
            f"All: {sum_today_all_expenses} \u20BD \n"
            f"Groceries: {sum_today_groceries_expenses} \u20BD \n"
            f"Week statistic: /week")


def get_week_sum_statistic() -> str:
    """ Get statistic of this iso week."""
    today = _get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                "AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s)", (today, today))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this week"
    sum_week_all_expenses = result[0]

    cur.execute("SELECT SUM(expense.amount), budget.weekly_limit "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "JOIN budget ON type_of_category.id = budget.type_of_category_id "
                "WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                "AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s) "
                "GROUP BY budget.weekly_limit", (today, today))
    result = cur.fetchone()

    # Return sum of all week groceries expenses or 0.00 if that expenses doesn't exist
    sum_week_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()
    groceries_expenses_week_limit = result[1]    # Budget limit to Groceries type

    return (f"This week expenses: \n"
            f"All: {sum_week_all_expenses} \u20BD \n"
            f"Groceries: {sum_week_groceries_expenses} \u20BD of {groceries_expenses_week_limit} \u20BD \n"
            f"Month statistic: /month")


def get_month_sum_statistic() -> str:
    today = _get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s);", (today, today))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this week"
    sum_month_all_expenses = result[0]

    cur.execute("SELECT SUM(expense.amount), budget.monthly_limit "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "JOIN budget ON type_of_category.id = budget.type_of_category_id "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s) "
                "GROUP BY budget.monthly_limit;", (today, today))
    result = cur.fetchone()

    # Return sum of all month groceries expenses or 0.00 if that expenses doesn't exist
    sum_month_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()
    groceries_expenses_month_limit = result[1]   # Budget limit to Groceries type

    return (f"This month expenses: \n"
            f"All: {sum_month_all_expenses} \u20BD \n"
            f"Groceries: {sum_month_groceries_expenses} \u20BD of {groceries_expenses_month_limit} \u20BD \n"
            f"Year statistic: /year")


def get_year_sum_statistic() -> str:
    today = _get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s);", (today, ))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this week"
    sum_year_all_expenses = result[0]

    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE type_of_category.type_name='Grocery' "       # TODO: change to 'Groceries'
                "AND extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s)", (today, ))
    result = cur.fetchone()

    # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
    sum_year_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()

    return (f"This year expenses: \n"
            f"All: {sum_year_all_expenses} \u20BD \n"
            f"Groceries: {sum_year_groceries_expenses} \u20BD \n"
            f"Day statistic: /day")


def _get_today() -> datetime.datetime:
    msc = timezone('Europe/Moscow')
    today = datetime.datetime.now(msc)
    return today


