from typing import NamedTuple, Optional
from category import Categories
from services.exceptions import NotCorrectMessage
import re
import db
from services.service import get_today      # maybe should move this func to another module(service/date)
from services.service import get_category_name_by_id
from decimal import *


class Message(NamedTuple):
    amount: Decimal
    category_text: str
    payment_type_text: Optional[str]
    additional_info_text: Optional[str]


# TODO: add class Message(NamedTuple)       -- Message handling
# TODO: add class Expense(NamedTuple)       -- Expense handling
# TODO: add def add_expense()               -- Expense handling
# TODO: add def last_ten()                  -- Expense handling
# TODO: add def delete_expense()            -- Expense handling
# TODO: add def _parse_message()            -- Message handling
# TODO: add def _get_now()                  -- Date handling
# TODO: add def _get_weekly_budget_limit()  -- Db data fetching
# TODO: add def _get_monthly_budget_limit() -- Db data fetching
# TODO: add def get_fixed_price()           -- Db data fetching


def add_expense(raw_message: str) -> str:
    payment_type_result = ''
    additional_info = None

    parsed_message = _parse_message(raw_message)
    category = Categories().get_category_by_name(parsed_message.category_text)

    # TODO: move if below to another module
    if parsed_message.amount <= 0:
        raise NotCorrectMessage('Amount should be more than 0')

    # TODO: move if below to another module
    if category.is_cash_accepted and not category.is_card_accepted:     # CASH only
        if not parsed_message.payment_type_text:
            payment_type_result = 'cash'
        elif parsed_message.payment_type_text == 'cash':
            payment_type_result = 'cash'
        else:
            raise NotCorrectMessage('This category only Cash is accepted')
    elif not category.is_cash_accepted and category.is_card_accepted:   # CARD only
        if not parsed_message.payment_type_text:
            payment_type_result = 'card'
        elif parsed_message.payment_type_text == 'card':
            payment_type_result = 'card'
        else:
            raise NotCorrectMessage('This category only Card is accepted')
    elif category.is_cash_accepted and category.is_card_accepted:       # BOTH
        if not parsed_message.payment_type_text:
            raise NotCorrectMessage('You should choose type of payment')
        elif parsed_message.payment_type_text == 'cash':
            payment_type_result = 'cash'
        elif parsed_message.payment_type_text == 'card':
            payment_type_result = 'card'
        else:
            raise NotCorrectMessage("Payment type only may be 'cash' or 'card'")

    # TODO: move if below to another module
    if category.is_additional_info_needed:
        if parsed_message.additional_info_text:
            additional_info = parsed_message.additional_info_text
        else:
            raise NotCorrectMessage('This category is needed additional info')

    db.insert_to_db('expense', {'amount': parsed_message.amount,
                                'time_creating': get_today(),
                                'category_id': category.id,
                                'payment_type': payment_type_result,
                                'additional_info': additional_info,
                                'raw_text': raw_message})

    return (f"Expense was added by {parsed_message.amount} \u20BD "
            f"to '{get_category_name_by_id(category.id)}' category "
            f"with payment by {payment_type_result}. \n\n"
            f"To see all expenses: /expenses")


def last_expenses(limit: int = 10) -> str:
    """ Return last expense with limit (default 10). """
    cur = db.get_cursor()

    cur.execute("SELECT expense.id, expense.amount, category.category_name, expense.payment_type "
                "FROM expense "
                "JOIN category ON category.id=expense.category_id "
                "ORDER BY expense.time_creating DESC LIMIT %s;", (limit, ))
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense"

    last_rows = []
    for row in result:
        last_rows.append(f"{row[1]} \u20BD "
                         f"to '{row[2]}' category "
                         f"with payment by {row[3]}. \n"
                         f"   Click /delete{row[0]} to delete.")

    answer_message = "Last expenses: \n\n# " + "\n\n# ".join(last_rows)
    return answer_message


def delete_expense(row_id: int) -> None:
    db.delete_from_db('expense', row_id)


def _parse_message(raw_message: str) -> Message:
    regexp_result = re.match(
        r"(?P<amount>\d+[,.]?\d*) *"        # Float number with ',' or '.' (or int) for amount
        r"(?P<category>(?!cash|card)[A-ZА-ЯЁa-zа-яё]+ *(?!cash|card)[A-ZА-ЯЁa-zа-яё]*) *"   # Max two words for category
        r"(?P<payment>cash|card)? *"        # Only 'cash' or 'card' for payment
        r"(?P<info>.+)?",                   # Any signs, any length for info
        raw_message)

    if not regexp_result or not regexp_result.group(0) or not regexp_result.group('amount') \
            or not regexp_result.group('category'):
        raise NotCorrectMessage('Expense format: <amount> <category_name> <payment_type> <additional_info>')

    # Usually dot sign '.' will be using to convert 'str' to 'float'
    # But comma sign ',' may be used in float number too and it will not raise any exception
    swap_float_sign = re.sub(',', '.', regexp_result.group('amount'), count=1)  # Replace first occurrence of ',' to '.'
    decim = Decimal(swap_float_sign.replace(' ', ''))        # Delete possibly redundant spaces and convert to Decimal
    amount = decim.quantize(Decimal('1.01'), rounding=ROUND_HALF_UP)      # Round .005 on the end to .01

    category_text = regexp_result.group('category').strip().lower()

    payment_type = None
    additional_info = None
    if regexp_result.group('payment'):
        payment_type = regexp_result.group('payment').strip()
    if regexp_result.group('info'):
        additional_info = regexp_result.group('info')

    result = Message(amount=amount,
                     category_text=category_text,
                     payment_type_text=payment_type,
                     additional_info_text=additional_info)

    return result


