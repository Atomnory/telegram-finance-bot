from models import TypeofCategory, Budget, Category, Expense
from playhouse.postgres_ext import fn
from decimal import Decimal
from services.service import get_today
from datetime import datetime


def get_today_sum_statistic() -> str:
    """ Get statistic of sum today expenses. """
    today = get_today().date()
    expense_sum_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'))
                         .where(Expense.time_creating.truncate('day') == today))

    if not expense_sum_query[0].sum:
        return (f"There's none any expense today \n\n"
                f"Week statistic: /week")

    sum_groceries_query = (Expense
                           .select(fn.SUM(Expense.amount).alias('sum'))
                           .join(Category)
                           .join(TypeofCategory)
                           .where((TypeofCategory.name == 'Groceries')
                                  & (Expense.time_creating.truncate('day') == today)))

    # Return sum of all today groceries expenses or 0.00 if that expenses doesn't exist
    sum_groceries_expenses = sum_groceries_query[0].sum if sum_groceries_query[0].sum else _get_quantize_zero_decimal()

    return (f"Today expenses: \n\n"
            f"All: {expense_sum_query[0].sum} \u20BD \n"
            f"Groceries: {sum_groceries_expenses} \u20BD \n\n"
            f"Today statistic by category: /day_category \n"
            f"Week statistic: /week")


def get_today_statistic_by_category() -> str:
    """ Get statistic of today expenses grouped by category and payment type. """
    today = get_today().date()
    stat_category_query = (Expense
                           .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                           .join(Category)
                           .where(Expense.time_creating.truncate('day') == today)
                           .group_by(Expense.category_id, Category.name, Expense.payment_type)
                           .order_by(Expense.category_id))

    if not stat_category_query:
        return "There's none any expense today"

    rows = []
    for row in stat_category_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}. ")

    answer_message = "Today expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple today statistic: /day \n"
                       "Today statistic by type: /day_type \n"
                       "Week statistic by category: /week_category")
    return answer_message


def get_today_statistic_by_type() -> str:
    """ Get statistic of today expenses grouped by type of category and payment type. """
    today = get_today().date()
    stat_type_query = (Expense
                       .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                       .join(Category)
                       .join(TypeofCategory)
                       .where(Expense.time_creating.truncate('day') == today)
                       .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                       .order_by(TypeofCategory.id))

    if not stat_type_query:
        return "There's none any expense today"

    rows = []
    for row in stat_type_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.type_id.name}' type "
                    f"with payment by {row.payment_type}. ")

    answer_message = "Today expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple today statistic: /day \n"
                       "Today statistic by category: /day_category \n"
                       "Week statistic by type: /week_type")
    return answer_message


def get_week_sum_statistic() -> str:
    """ Get statistic of this ISO week expenses. """
    today = get_today()
    today_iso_week = datetime.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=1)

    expense_sum_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'))
                         .where(Expense.time_creating.truncate('week') == today_iso_week))

    if not expense_sum_query[0].sum:
        return (f"There's none any expense in this week \n\n"
                f"Month statistic: /month")

    sum_grocery_query = (Expense
                        .select(fn.SUM(Expense.amount).alias('sum'), Budget.weekly_limit)
                        .join(Category)
                        .join(TypeofCategory)
                        .join(Budget)
                        .where(Expense.time_creating.truncate('week') == today_iso_week)
                        .group_by(Budget.weekly_limit).dicts())

    # Return sum of all week groceries expenses or 0.00 if that expenses doesn't exist
    sum_grocery_expenses = sum_grocery_query[0]['sum'] if sum_grocery_query else _get_quantize_zero_decimal()
    grocery_limit = sum_grocery_query[0]['weekly_limit'] if sum_grocery_query else _get_weekly_limit('Groceries')

    return (f"This week expenses: \n\n"
            f"All: {expense_sum_query[0].sum} \u20BD \n"
            f"Groceries: {sum_grocery_expenses} \u20BD of {grocery_limit} \u20BD \n\n"
            f"Week statistic by category: /week_category \n"
            f"Detail week statistic: /week_detail \n"
            f"Month statistic: /month")


def get_week_statistic_by_category() -> str:
    """ Get statistic of this ISO week expenses grouped by category and payment type. """
    today = get_today()
    today_iso_week = datetime.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=1)

    expense_category_query = (Expense
                              .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                              .join(Category)
                              .where(Expense.time_creating.truncate('week') == today_iso_week)
                              .group_by(Expense.category_id, Category.name, Expense.payment_type)
                              .order_by(Expense.category_id))

    if not expense_category_query:
        return "There's none any expense in this week"

    rows = []
    for row in expense_category_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}. ")

    answer_message = "This week expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple week statistic: /week \n"
                       "Week statistic by type: /week_type \n"
                       "Month statistic by category: /month_category")
    return answer_message


def get_week_statistic_by_type() -> str:
    """ Get statistic of this ISO week expenses grouped by type of category and payment type. """
    today = get_today()
    today_iso_week = datetime.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=1)

    expense_type_query = (Expense
                        .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                        .join(Category)
                        .join(TypeofCategory)
                        .where(Expense.time_creating.truncate('week') == today_iso_week)
                        .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                        .order_by(TypeofCategory.id))

    if not expense_type_query:
        return "There's none any expense in this week"

    rows = []
    for row in expense_type_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.type_id.name}' type "
                    f"with payment by {row.payment_type}. ")

    answer_message = "This week expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple week statistic: /week \n"
                       "Week statistic by category: /week_category \n"
                       "Month statistic by type: /month_type")
    return answer_message


def get_detail_week_statistic() -> str:
    """ Get detail statistic of this ISO week expenses. Displays only expenses which should have additional_info. """
    today = get_today()
    today_iso_week = datetime.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=1)

    expense_detail_query = (Expense
                            .select(fn.SUM(Expense.amount).alias('sum'),
                                    Category.name, Expense.payment_type, Expense.additional_info)
                            .join(Category)
                            .where((Expense.time_creating.truncate('week') == today_iso_week)
                                   & (Category.is_additional_info_needed == True))
                            .group_by(Expense.category_id, Category.name, Expense.payment_type, Expense.additional_info)
                            .order_by(Expense.category_id))

    if not expense_detail_query:
        return "There's none such expense in this week"

    rows = []
    for row in expense_detail_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}, "
                    f"describing: {row.additional_info}. ")

    answer_message = "Detail this week expenses: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple week statistic: /week \n"
                       "Detail month statistic: /month_detail")
    return answer_message


def get_month_sum_statistic() -> str:
    """ Get statistic of this month expenses. """
    today = get_today()
    today_month = datetime(year=today.year, month=today.month, day=1)

    expense_sum_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'))
                         .where(Expense.time_creating.truncate('month') == today_month))

    if not expense_sum_query[0].sum:
        return (f"There's none any expense in this month \n\n"
                f"Year statistic: /year")

    sum_grocery_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'), Budget.monthly_limit)
                         .join(Category)
                         .join(TypeofCategory)
                         .join(Budget)
                         .where(Expense.time_creating.truncate('month') == today_month)
                         .group_by(Budget.monthly_limit).dicts())

    # Return sum of all month groceries expenses or 0.00 if that expenses doesn't exist
    sum_grocery_expenses = sum_grocery_query[0]['sum'] if sum_grocery_query else _get_quantize_zero_decimal()
    grocery_limit = sum_grocery_query[0]['monthly_limit'] if sum_grocery_query else _get_monthly_limit('Groceries')

    return (f"This month expenses: \n\n"
            f"All: {expense_sum_query[0].sum} \u20BD \n"
            f"Groceries: {sum_grocery_expenses} \u20BD of {grocery_limit} \u20BD \n\n"
            f"Month statistic by category: /month_category \n"
            f"Detail month statistic: /month_detail \n"
            f"Year statistic: /year")


def get_month_statistic_by_category() -> str:
    """ Get statistic of this month expenses grouped by category and payment type. """
    today = get_today()
    today_month = datetime(year=today.year, month=today.month, day=1)

    expense_category_query = (Expense
                              .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                              .join(Category)
                              .where(Expense.time_creating.truncate('month') == today_month)
                              .group_by(Expense.category_id, Category.name, Expense.payment_type)
                              .order_by(Expense.category_id))

    if not expense_category_query:
        return "There's none any expense in this month"

    rows = []
    for row in expense_category_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}. ")

    answer_message = "This month expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple month statistic: /month \n"
                       "Month statistic by type: /month_type \n"
                       "Year statistic by category: /year_category")
    return answer_message


def get_month_statistic_by_type() -> str:
    """ Get statistic of this month expenses grouped by type of category and payment type. """
    today = get_today()
    today_month = datetime(year=today.year, month=today.month, day=1)

    expense_type_query = (Expense
                          .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                          .join(Category)
                          .join(TypeofCategory)
                          .where(Expense.time_creating.truncate('month') == today_month)
                          .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                          .order_by(TypeofCategory.id))

    if not expense_type_query:
        return "There's none any expense in this month"

    rows = []
    for row in expense_type_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.type_id.name}' type "
                    f"with payment by {row.payment_type}. ")

    answer_message = "This month expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple month statistic: /month \n"
                       "Month statistic by category: /month_category \n"
                       "Year statistic by type: /year_type")
    return answer_message


def get_detail_month_statistic() -> str:
    """ Get detail statistic of this month expenses. Displays only expenses which should have additional_info. """
    today = get_today()
    today_month = datetime(year=today.year, month=today.month, day=1)

    expense_detail_query = (Expense
                            .select(fn.SUM(Expense.amount).alias('sum'),
                                    Category.name, Expense.payment_type, Expense.additional_info)
                            .join(Category)
                            .where((Expense.time_creating.truncate('month') == today_month)
                                   & (Category.is_additional_info_needed == True))
                            .group_by(Expense.category_id, Category.name, Expense.payment_type, Expense.additional_info)
                            .order_by(Expense.category_id))

    if not expense_detail_query:
        return "There's none such expense in this month"

    rows = []
    for row in expense_detail_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}, "
                    f"describing: {row.additional_info}. ")

    answer_message = "Detail this month expenses: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple month statistic: /month \n"
                       "Detail week statistic: /week_detail")
    return answer_message


def get_year_sum_statistic() -> str:
    """ Get statistic of this year expenses. """
    today = get_today()
    today_year = datetime(year=today.year, month=1, day=1)

    expense_sum_query = (Expense
                         .select(fn.SUM(Expense.amount).alias('sum'))
                         .where(Expense.time_creating.truncate('year') == today_year))

    if not expense_sum_query[0].sum:
        return (f"There's none any expense in this year \n\n"
                f"Day statistic: /day")

    sum_grocery_query = (Expense
                        .select(fn.SUM(Expense.amount).alias('sum'))
                        .join(Category)
                        .join(TypeofCategory)
                        .where((TypeofCategory.name == 'Groceries')
                               & (Expense.time_creating.truncate('year') == today_year)))

    # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
    sum_grocery_expenses = sum_grocery_query[0].sum if sum_grocery_query[0].sum else _get_quantize_zero_decimal()

    return (f"This year expenses: \n\n"
            f"All: {expense_sum_query[0].sum} \u20BD \n"
            f"Groceries: {sum_grocery_expenses} \u20BD \n\n"
            f"Year statistic by category: /year_category \n"
            f"Day statistic: /day")


def get_year_statistic_by_category() -> str:
    """ Get statistic of this year expenses grouped by category and payment type. """
    today = get_today()
    today_year = datetime(year=today.year, month=1, day=1)

    stat_category_query = (Expense
                           .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                           .join(Category)
                           .where(Expense.time_creating.truncate('year') == today_year)
                           .group_by(Expense.category_id, Category.name, Expense.payment_type)
                           .order_by(Expense.category_id))

    if not stat_category_query:
        return "There's none any expense in this year"

    rows = []
    for row in stat_category_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.name}' category "
                    f"with payment by {row.payment_type}. ")

    answer_message = "This year expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple year statistic: /year \n"
                       "Year statistic by type: /year_type \n"
                       "Day statistic by category: /day_category")
    return answer_message


def get_year_statistic_by_type() -> str:
    """ Get statistic of this year expenses grouped by type of category and payment type. """
    today = get_today()
    today_year = datetime(year=today.year, month=1, day=1)

    stat_type_query = (Expense
                       .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                       .join(Category)
                       .join(TypeofCategory)
                       .where(Expense.time_creating.truncate('year') == today_year)
                       .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                       .order_by(TypeofCategory.id))

    if not stat_type_query:
        return "There's none any expense in this year"

    rows = []
    for row in stat_type_query:
        rows.append(f"{row.sum} \u20BD "
                    f"to '{row.category_id.type_id.name}' type "
                    f"with payment by {row.payment_type}. ")

    answer_message = "This year expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple year statistic: /year \n"
                       "Year statistic by category: /year_category \n"
                       "Day statistic by type: /day_type")
    return answer_message


def _get_quantize_zero_decimal() -> Decimal:
    """ Using for display '0' with trailing zeros '0.00'. """
    return Decimal(0.00).quantize(Decimal('1.11'))


def _get_budget(type_name: str) -> Budget:
    """ Return budget instance by type_name. """
    return Budget.select().join(TypeofCategory).where(TypeofCategory.name == type_name)


def _get_weekly_limit(type_name: str) -> Decimal:
    """ Return weekly limit by type name"""
    budget = _get_budget(type_name)
    return budget[0].weekly_limit


def _get_monthly_limit(type_name: str) -> Decimal:
    """ Return monthly limit by type name"""
    budget = _get_budget(type_name)
    return budget[0].monthly_limit
