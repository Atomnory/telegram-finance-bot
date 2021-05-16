import db
from decimal import Decimal
from services.service import get_today


def get_today_sum_statistic() -> str:
    """ Get statistic of sum today expenses. """
    today = get_today()
    cur = db.get_cursor()

    # Try to SELECT at least one expense
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE expense.time_creating::DATE=%s::DATE;", (today, ))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense today"
    sum_today_all_expenses = result[0]

    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE type_of_category.type_name=%s "
                "AND expense.time_creating::DATE=%s::DATE;", ('Groceries', today))
    result = cur.fetchone()

    # Return sum of all today groceries expenses or 0.00 if that expenses doesn't exist
    sum_today_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()

    return (f"Today expenses: \n\n"
            f"All: {sum_today_all_expenses} \u20BD \n"
            f"Groceries: {sum_today_groceries_expenses} \u20BD \n\n"
            f"Today statistic by category: /day_category \n"
            f"Week statistic: /week")


def get_today_statistic_by_category() -> str:
    """ Get statistic of today expenses grouped by category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), category.category_name, expense.payment_type, expense.category_id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "WHERE expense.time_creating::DATE=%s::DATE "
                "GROUP BY expense.category_id, category.category_name, expense.payment_type "
                "ORDER BY expense.category_id;", (today, ))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense today"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' category "
                    f"with payment by {row[2]}. ")

    answer_message = "Today expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple today statistic: /day \n"
                       "Today statistic by type: /day_type \n"
                       "Week statistic by category: /week_category")
    return answer_message


def get_today_statistic_by_type() -> str:
    """ Get statistic of today expenses grouped by type of category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), type_of_category.type_name, expense.payment_type, type_of_category.id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE expense.time_creating::DATE=%s::DATE "
                "GROUP BY type_of_category.id, type_of_category.type_name, expense.payment_type "
                "ORDER BY type_of_category.id;", (today, ))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense today"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' type "
                    f"with payment by {row[2]}. ")

    answer_message = "Today expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple today statistic: /day \n"
                       "Today statistic by category: /day_category \n"
                       "Week statistic by type: /week_type")
    return answer_message


def get_week_sum_statistic() -> str:
    """ Get statistic of this ISO week expenses. """
    today = get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                "AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s);", (today, today))
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
                "GROUP BY budget.weekly_limit;", (today, today))
    result = cur.fetchone()

    # Return sum of all week groceries expenses or 0.00 if that expenses doesn't exist
    sum_week_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()
    groceries_expenses_week_limit = result[1]    # Budget limit to Groceries type

    return (f"This week expenses: \n\n"
            f"All: {sum_week_all_expenses} \u20BD \n"
            f"Groceries: {sum_week_groceries_expenses} \u20BD of {groceries_expenses_week_limit} \u20BD \n\n"
            f"Week statistic by category: /week_category \n"
            f"Detail week statistic: /week_detail \n"
            f"Month statistic: /month")


def get_week_statistic_by_category() -> str:
    """ Get statistic of this ISO week expenses grouped by category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), category.category_name, expense.payment_type, expense.category_id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                "AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s) "
                "GROUP BY expense.category_id, category.category_name, expense.payment_type "
                "ORDER BY expense.category_id;", (today, today))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense in this week"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' category "
                    f"with payment by {row[2]}. ")

    answer_message = "This week expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple week statistic: /week \n"
                       "Week statistic by type: /week_type \n"
                       "Month statistic by category: /month_category")
    return answer_message


def get_week_statistic_by_type() -> str:
    """ Get statistic of this ISO week expenses grouped by type of category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), type_of_category.type_name, expense.payment_type, type_of_category.id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                "AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s) "
                "GROUP BY type_of_category.id, type_of_category.type_name, expense.payment_type "
                "ORDER BY type_of_category.id;", (today, today))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense in this week"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' type "
                    f"with payment by {row[2]}. ")

    answer_message = "This week expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple week statistic: /week \n"
                       "Week statistic by category: /week_category \n"
                       "Month statistic by type: /month_type")
    return answer_message


def get_detail_week_statistic() -> str:
    """ Get detail statistic of this ISO week expenses. Displays only expenses which should have additional_info. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), "
                "category.category_name, expense.payment_type, expense.additional_info, expense.category_id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "WHERE extract(ISOYEAR FROM expense.time_creating)=extract(ISOYEAR FROM %s) "
                "AND extract(WEEK FROM expense.time_creating)=extract(WEEK FROM %s) "
                "AND category.is_additional_info_needed=true "
                "GROUP BY expense.category_id, category.category_name, expense.payment_type, expense.additional_info "
                "ORDER BY expense.category_id;", (today, today))
    result = cur.fetchall()
    if not result[0]:
        return "There's none such expense in this week"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' category "
                    f"with payment by {row[2]}, "
                    f"describing: {row[3]}. ")

    answer_message = "Detail this week expenses: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple week statistic: /week \n"
                       "Detail month statistic: /month_detail")
    return answer_message


def get_month_sum_statistic() -> str:
    """ Get statistic of this month expenses. """
    today = get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s);", (today, today))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this month"
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

    return (f"This month expenses: \n\n"
            f"All: {sum_month_all_expenses} \u20BD \n"
            f"Groceries: {sum_month_groceries_expenses} \u20BD of {groceries_expenses_month_limit} \u20BD \n\n"
            f"Month statistic by category: /month_category \n"
            f"Detail month statistic: /month_detail \n"
            f"Year statistic: /year")


def get_month_statistic_by_category() -> str:
    """ Get statistic of this month expenses grouped by category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), category.category_name, expense.payment_type, expense.category_id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s) "
                "GROUP BY expense.category_id, category.category_name, expense.payment_type "
                "ORDER BY expense.category_id;", (today, today))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense in this month"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' category "
                    f"with payment by {row[2]}. ")

    answer_message = "This month expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple month statistic: /month \n"
                       "Month statistic by type: /month_type \n"
                       "Year statistic by category: /year_category")
    return answer_message


def get_month_statistic_by_type() -> str:
    """ Get statistic of this month expenses grouped by type of category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), type_of_category.type_name, expense.payment_type, type_of_category.id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s) "
                "GROUP BY type_of_category.id, type_of_category.type_name, expense.payment_type "
                "ORDER BY type_of_category.id;", (today, today))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense in this month"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' type "
                    f"with payment by {row[2]}. ")

    answer_message = "This month expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple month statistic: /month \n"
                       "Month statistic by category: /month_category \n"
                       "Year statistic by type: /year_type")
    return answer_message


def get_detail_month_statistic() -> str:
    """ Get detail statistic of this month expenses. Displays only expenses which should have additional_info. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), "
                "category.category_name, expense.payment_type, expense.additional_info, expense.category_id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "AND extract(MONTH FROM expense.time_creating)=extract(MONTH FROM %s) "
                "AND category.is_additional_info_needed=true "
                "GROUP BY expense.category_id, category.category_name, expense.payment_type, expense.additional_info "
                "ORDER BY expense.category_id;", (today, today))
    result = cur.fetchall()
    if not result[0]:
        return "There's none such expense in this month"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' category "
                    f"with payment by {row[2]}, "
                    f"describing: {row[3]}. ")

    answer_message = "Detail this month expenses: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple month statistic: /month \n"
                       "Detail week statistic: /week_detail")
    return answer_message


def get_year_sum_statistic() -> str:
    """ Get statistic of this year expenses. """
    today = get_today()
    cur = db.get_cursor()

    # Try to fetch at least one row
    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s);", (today, ))
    result = cur.fetchone()
    if not result[0]:
        return "There's none any expense in this year"
    sum_year_all_expenses = result[0]

    cur.execute("SELECT SUM(expense.amount) "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE type_of_category.type_name=%s "
                "AND extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s);", ('Groceries', today))
    result = cur.fetchone()

    # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
    sum_year_groceries_expenses = result[0] if result[0] else _get_quantize_zero_decimal()

    return (f"This year expenses: \n\n"
            f"All: {sum_year_all_expenses} \u20BD \n"
            f"Groceries: {sum_year_groceries_expenses} \u20BD \n\n"
            f"Year statistic by category: /year_category \n"
            f"Day statistic: /day")


def get_year_statistic_by_category() -> str:
    """ Get statistic of this year expenses grouped by category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), category.category_name, expense.payment_type, expense.category_id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "GROUP BY expense.category_id, category.category_name, expense.payment_type "
                "ORDER BY expense.category_id;", (today, ))
    result = cur. fetchall()
    if not result[0]:
        return "There's none any expense in this year"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' category "
                    f"with payment by {row[2]}. ")

    answer_message = "This year expenses by category: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple year statistic: /year \n"
                       "Year statistic by type: /year_type \n"
                       "Day statistic by category: /day_category")
    return answer_message


def get_year_statistic_by_type() -> str:
    """ Get statistic of this year expenses grouped by type of category and payment type. """
    today = get_today()
    cur = db.get_cursor()

    cur.execute("SELECT SUM(expense.amount), type_of_category.type_name, expense.payment_type, type_of_category.id "
                "FROM expense "
                "JOIN category ON expense.category_id = category.id "
                "JOIN type_of_category ON category.type_id = type_of_category.id "
                "WHERE extract(YEAR FROM expense.time_creating)=extract(YEAR FROM %s) "
                "GROUP BY type_of_category.id, type_of_category.type_name, expense.payment_type "
                "ORDER BY type_of_category.id;", (today, ))
    result = cur. fetchall()
    if not result[0]:
        return "There's none any expense in this year"

    rows = []
    for row in result:
        rows.append(f"{row[0]} \u20BD "
                    f"to '{row[1]}' type "
                    f"with payment by {row[2]}. ")

    answer_message = "This year expenses by type: \n\n# " + "\n\n# ".join(rows)
    answer_message += ("\n\nSimple year statistic: /year \n"
                       "Year statistic by category: /year_category \n"
                       "Day statistic by type: /day_type")
    return answer_message


def _get_quantize_zero_decimal() -> Decimal:
    """
        Return Decimal with two trailing zeros because all 'amount's from db have two precision numbers
        and keep that style will be better.
    """
    return Decimal(0.00).quantize(Decimal('1.11'))
