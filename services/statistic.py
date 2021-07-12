from playhouse.postgres_ext import fn
from decimal import Decimal
from datetime import date
from typing import List
from models import TypeofCategory, Category, Expense
from services.service import get_today_now
from utils.exceptions import QueryIsEmpty, InvalidPeriod


# TODO: create base class Statistic and derived classes DayStatistic, WeekStatistic, MonthStatistic, YearStatistic
def get_today_sum_statistic() -> str:
    """ Get statistic of sum today expenses. """
    today = _get_today_truncated_to_date()
    return try_get_sum_statistic('day', today)


def get_today_statistic_by_category() -> str:
    """ Get statistic of today expenses grouped by category and payment type. """
    today = _get_today_truncated_to_date()
    return try_get_statistic_by_category('day', today)


def get_today_statistic_by_type() -> str:
    """ Get statistic of today expenses grouped by type of category and payment type. """
    today = _get_today_truncated_to_date()
    return try_get_statistic_by_type('day', today)


def get_week_sum_statistic() -> str:
    """ Get statistic of this ISO week expenses. """
    today_iso_week = _get_today_truncated_to_week()
    return try_get_sum_with_limit_statistic('week', today_iso_week)


def get_week_statistic_by_category() -> str:
    """ Get statistic of this ISO week expenses grouped by category and payment type. """
    today_iso_week = _get_today_truncated_to_week()
    return try_get_statistic_by_category('week', today_iso_week)


def get_week_statistic_by_type() -> str:
    """ Get statistic of this ISO week expenses grouped by type of category and payment type. """
    today_iso_week = _get_today_truncated_to_week()
    return try_get_statistic_by_type('week', today_iso_week)


def get_detail_week_statistic() -> str:
    """ Get detail statistic of this ISO week expenses. Displays only expenses which should have additional_info. """
    today_iso_week = _get_today_truncated_to_week()
    return try_get_detail_statistic('week', today_iso_week)


def get_month_sum_statistic() -> str:
    """ Get statistic of this month expenses. """
    today_month = _get_today_truncated_to_month()
    return try_get_sum_with_limit_statistic('month', today_month)


def get_month_statistic_by_category() -> str:
    """ Get statistic of this month expenses grouped by category and payment type. """
    today_month = _get_today_truncated_to_month()
    return try_get_statistic_by_category('month', today_month)


def get_month_statistic_by_type() -> str:
    """ Get statistic of this month expenses grouped by type of category and payment type. """
    today_month = _get_today_truncated_to_month()
    return try_get_statistic_by_type('month', today_month)


def get_detail_month_statistic() -> str:
    """ Get detail statistic of this month expenses. Displays only expenses which should have additional_info. """
    today_month = _get_today_truncated_to_month()
    return try_get_detail_statistic('month', today_month)


def get_year_sum_statistic() -> str:
    """ Get statistic of this year expenses. """
    today_year = _get_today_truncated_to_year()
    return try_get_sum_statistic('year', today_year)


def get_year_statistic_by_category() -> str:
    """ Get statistic of this year expenses grouped by category and payment type. """
    today_year = _get_today_truncated_to_year()
    return try_get_statistic_by_category('year', today_year)


def get_year_statistic_by_type() -> str:
    """ Get statistic of this year expenses grouped by type of category and payment type. """
    today_year = _get_today_truncated_to_year()
    return try_get_statistic_by_type('year', today_year)


def _get_quantize_zero_decimal() -> Decimal:
    """ Using for display '0' with trailing zeros '0.00'. """
    return Decimal(0.00).quantize(Decimal('1.11'))


def try_get_sum_statistic(period_name: str, period: date) -> str:
    try:
        expense_sum = get_sum(period_name, period)
        groceries_sum = get_sum_groceries(period_name, period)
    except QueryIsEmpty as e:
        answer_message = get_formatted_answer_sum_error(e, period_name)
    else:
        answer_message = get_formatted_answer_sum(expense_sum, groceries_sum, period_name)
    finally:
        return answer_message


def get_sum(period_name: str, period: date):
    query = select_sum_query(period_name, period)
    if query[0].sum:
        return query[0].sum
    else:
        raise QueryIsEmpty(f"Sum row doesn't exist. period_name: {period_name}, period_date: {period}. ")


def select_sum_query(period_name: str, period: date) -> Expense:
    expense_sum_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'))
                         .where(Expense.time_creating.truncate(period_name) == period))
    return expense_sum_query


def get_sum_groceries(period_name: str, period: date):
    # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
    query = select_groceries_sum_query(period_name, period)
    if query[0].sum:
        return query[0].sum
    else:
        return _get_quantize_zero_decimal()


def select_groceries_sum_query(period_name: str, period: date) -> Expense:
    groceries_sum_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'))
                         .join(Category)
                         .join(TypeofCategory)
                         .where((TypeofCategory.name == 'Groceries')
                                & (Expense.time_creating.truncate(period_name) == period)))
    return groceries_sum_query


def get_formatted_answer_sum_error(error: Exception, period_name: str) -> str:
    print(str(error))
    next_period_name = get_next_period_name(period_name)
    answer_message = (f"There's none any expense in this {period_name} \n\n"
                      f"{next_period_name.title()} statistic: /{next_period_name}")
    return answer_message


def get_formatted_answer_sum(expense_sum, groceries_sum, period_name: str) -> str:
    next_period_name = get_next_period_name(period_name)

    answer_message = (f"This {period_name} expenses: \n\n"
                      f"All: {expense_sum} \u20BD \n"
                      f"Groceries: {groceries_sum} \u20BD \n\n"
                      f"{period_name.title()} statistic by category: /{period_name}_category \n"
                      f"{next_period_name.title()} statistic: /{next_period_name}")
    return answer_message


def try_get_sum_with_limit_statistic(period_name: str, period: date) -> str:
    try:
        expense_sum = get_sum(period_name, period)
        groceries_sum_and_limit = get_sum_groceries_and_limit(period_name, period)
    except QueryIsEmpty as e:
        answer_message = get_formatted_answer_sum_error(e, period_name)
    else:
        answer_message = get_formatted_answer_sum_with_limit(expense_sum, groceries_sum_and_limit, period_name)
    finally:
        return answer_message


def get_sum_groceries_and_limit(period_name: str, period: date):
    # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
    query = choose_groceries_sum_with_limit_query(period_name, period)
    if query:
        return query[0][0], query[0][1]
    else:
        return _get_quantize_zero_decimal(), _get_period_limit('Groceries', period_name)


def choose_groceries_sum_with_limit_query(period_name: str, period: date) -> Expense:
    if period_name == 'week':
        groceries_sum_query = select_groceries_sum_with_weekly_limit_query(period_name, period)
    elif period_name == 'month':
        groceries_sum_query = select_groceries_sum_with_monthly_limit_query(period_name, period)
    else:
        raise InvalidPeriod(f'sum_with_limit invalid period. period_name: {period_name}, period: {period}')
    return groceries_sum_query


def select_groceries_sum_with_weekly_limit_query(period_name: str, period: date) -> Expense:
    groceries_weekly_limit_query = (Expense
                                    .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.weekly_limit)
                                    .join(Category)
                                    .join(TypeofCategory)
                                    .where((Expense.time_creating.truncate(period_name) == period)
                                           & (TypeofCategory.weekly_limit.is_null(False)))
                                    .group_by(TypeofCategory.weekly_limit).tuples())
    return groceries_weekly_limit_query


def select_groceries_sum_with_monthly_limit_query(period_name: str, period: date) -> Expense:
    groceries_monthly_limit_query = (Expense
                                    .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.monthly_limit)
                                    .join(Category)
                                    .join(TypeofCategory)
                                    .where((Expense.time_creating.truncate(period_name) == period)
                                        & (TypeofCategory.monthly_limit.is_null(False)))
                                    .group_by(TypeofCategory.monthly_limit).tuples())
    return groceries_monthly_limit_query


def get_formatted_answer_sum_with_limit(expense_sum, groceries_sum_and_limit, period_name: str) -> str:
    next_period_name = get_next_period_name(period_name)
    grocery_sum, grocery_limit = groceries_sum_and_limit

    answer_message = (f"This {period_name} expenses: \n\n"
                      f"All: {expense_sum} \u20BD \n"
                      f"Groceries: {grocery_sum} \u20BD of {grocery_limit} \u20BD \n\n"
                      f"{period_name.title()} statistic by category: /{period_name}_category \n"
                      f"Detail {period_name} statistic: /{period_name}_detail \n"
                      f"{next_period_name.title()} statistic: /{next_period_name}")
    return answer_message


def try_get_statistic_by_category(period_name: str, period: date) -> str:
    try:
        expense_query = get_statistic_by_category(period_name, period)
    except QueryIsEmpty as e:
        answer_message = get_formatted_answer_by_category_error(e, period_name)
    else:
        answer_message = get_formatted_answer_by_category(expense_query, period_name)
    finally:
        return answer_message


def get_statistic_by_category(period_name: str, period: date):
    query = select_categories_query(period_name, period)
    if query:
        return query
    else:
        raise QueryIsEmpty(f"Categories row doesn't exist. period_name: {period_name}, period_date: {period}. ")


def select_categories_query(period_name: str, period: date):
    stat_category_query = (Expense
                           .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                           .join(Category)
                           .where(Expense.time_creating.truncate(period_name) == period)
                           .group_by(Expense.category_id, Category.name, Expense.payment_type)
                           .order_by(Expense.category_id))
    return stat_category_query


def get_formatted_answer_by_category_error(error: Exception, period_name: str) -> str:
    print(str(error))
    next_period_name = get_next_period_name(period_name)
    answer_message = (f"There's none any expense in this {period_name} \n\n"
                      f"{next_period_name.title()} statistic by category: /{next_period_name}_category")
    return answer_message


def get_formatted_answer_by_category(query, period_name: str) -> str:
    rows = get_formatted_categories_rows(query)
    next_period_name = get_next_period_name(period_name)

    answer_message = f"This {period_name} expenses by category: \n\n# "
    answer_message += "\n\n# ".join(rows)
    answer_message += (f"\n\n{period_name.title()} sum statistic: /{period_name} \n"
                       f"{period_name.title()} statistic by type: /{period_name}_type \n"
                       f"{next_period_name.title()} statistic by category: /{next_period_name}_category")
    return answer_message


def get_formatted_categories_rows(query) -> List[str]:
    rows = []
    for row in query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}. ")
    return rows


def try_get_statistic_by_type(period_name: str, period: date) -> str:
    try:
        expense_query = get_statistic_by_type(period_name, period)
    except QueryIsEmpty as e:
        answer_message = get_formatted_answer_by_type_error(e, period_name)
    else:
        answer_message = get_formatted_answer_by_type(expense_query, period_name)
    finally:
        return answer_message


def get_statistic_by_type(period_name: str, period: date):
    query = select_types_query(period_name, period)
    if query:
        return query
    else:
        raise QueryIsEmpty(f"Types row doesn't exist. period_name: {period_name}, period_date: {period}. ")


def select_types_query(period_name: str, period: date):
    stat_type_query = (Expense
                       .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                       .join(Category)
                       .join(TypeofCategory)
                       .where(Expense.time_creating.truncate(period_name) == period)
                       .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                       .order_by(TypeofCategory.id))
    return stat_type_query


def get_formatted_answer_by_type_error(error: Exception, period_name: str) -> str:
    print(str(error))
    next_period_name = get_next_period_name(period_name)
    answer_message = (f"There's none any expense in this {period_name} \n\n"
                      f"{next_period_name.title()} statistic by type: /{next_period_name}_type")
    return answer_message


def get_formatted_answer_by_type(query, period_name: str) -> str:
    rows = get_formatted_types_rows(query)
    next_period_name = get_next_period_name(period_name)

    answer_message = f"This {period_name} expenses by type: \n\n# "
    answer_message += "\n\n# ".join(rows)
    answer_message += (f"\n\n{period_name.title()} sum statistic: /{period_name} \n"
                       f"{period_name.title()} statistic by category: /{period_name}_category \n"
                       f"{next_period_name.title()} statistic by type: /{next_period_name}_type")
    return answer_message


def get_formatted_types_rows(query) -> List[str]:
    rows = []
    for row in query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.type_id.name}' type "
                    f"with payment by {row.payment_type}. ")
    return rows


def try_get_detail_statistic(period_name: str, period: date) -> str:
    try:
        query = get_expense_detail_query(period_name, period)
    except QueryIsEmpty as e:
        answer_message = get_formatted_answer_detail_error(e, period_name)
    else:
        answer_message = get_formatted_answer_detail(query, period_name)
    finally:
        return answer_message


def get_expense_detail_query(period_name: str, period: date):
    result = select_detail_query(period_name, period)
    if result:
        return result
    else:
        raise QueryIsEmpty(f"Expense row doesn't exist. period_name: {period_name}, period_date: {period}. ")


def select_detail_query(period_name: str, period: date):
    expense_detail_query = (Expense
                            .select(fn.SUM(Expense.amount).alias('sum'),
                                    Category.name, Expense.payment_type, Expense.additional_info)
                            .join(Category)
                            .where((Expense.time_creating.truncate(period_name) == period)
                                   & (Category.is_additional_info_needed == True))
                            .group_by(Expense.category_id, Category.name, Expense.payment_type, Expense.additional_info)
                            .order_by(Expense.category_id))
    return expense_detail_query


def get_formatted_answer_detail_error(error: Exception, period_name: str) -> str:
    print(str(error))
    answer_message = f"There's none such expense in this {period_name}"
    return answer_message


def get_formatted_answer_detail(query, period_name: str) -> str:
    rows = get_formatted_detail_rows(query)
    next_period_name = get_next_detail_period_name(period_name)

    answer_message = f"Detail this {period_name} expenses: \n\n# "
    answer_message += "\n\n# ".join(rows)
    answer_message += (f"\n\n{period_name.title()} sum statistic: /{period_name} \n"
                       f"Detail {next_period_name} statistic: /{next_period_name}_detail")
    return answer_message


def get_formatted_detail_rows(query) -> List[str]:
    rows = []
    for row in query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}, "
                    f"describing: {row.additional_info}. ")
    return rows


def get_next_detail_period_name(period_name: str) -> str:
    """ Func is using to navigating in chat by command. """
    if period_name == 'week':
        next_period_name = 'month'
    elif period_name == 'month':
        next_period_name = 'week'
    else:
        raise InvalidPeriod("get_next_detail_period accept only week and month periods. ")
    return next_period_name


def get_next_period_name(period_name: str) -> str:
    """ Func is using to navigating in chat by command. """
    if period_name == 'day':
        next_period_name = 'week'
    elif period_name == 'week':
        next_period_name = 'month'
    elif period_name == 'month':
        next_period_name = 'year'
    elif period_name == 'year':
        next_period_name = 'day'
    else:
        raise InvalidPeriod("get_detail_period accept only day, week, month and year periods. ")
    return next_period_name


def _get_weekly_limit(type_name: str) -> Decimal:
    type_category = TypeofCategory.get(TypeofCategory.name == type_name)
    return type_category.weekly_limit


def _get_monthly_limit(type_name: str) -> Decimal:
    type_category = TypeofCategory.get(TypeofCategory.name == type_name)
    return type_category.monthly_limit


def _get_period_limit(type_name: str, period_name: str) -> Decimal:
    if period_name == 'week':
        return _get_weekly_limit(type_name)
    elif period_name == 'month':
        return _get_monthly_limit(type_name)


def _get_today_truncated_to_date() -> date:
    today = get_today_now().date()
    return today


def _get_today_truncated_to_week() -> date:
    today = _get_today_truncated_to_date()
    today_iso_week = date.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=1)
    return today_iso_week


def _get_today_truncated_to_month() -> date:
    today = _get_today_truncated_to_date()
    today_month = date(year=today.year, month=today.month, day=1)
    return today_month


def _get_today_truncated_to_year() -> date:
    today = _get_today_truncated_to_date()
    today_year = date(year=today.year, month=1, day=1)
    return today_year
