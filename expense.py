from typing import List, Dict, NamedTuple, Optional
from category import Categories
from type_of_category import TypesOfCategory
from exceptions import NotCorrectMessage
import re
import db
import datetime
from statistic import _get_today      # maybe should move this func to another module(service/date)
from decimal import *


class Message(NamedTuple):
    amount: Decimal
    category_text: str
    payment_type_text: Optional[str]
    additional_info_text: Optional[str]


# expense( id INTEGER,
#     amount INTEGER,
#     time_creating DATETIME,
#     category_id INTEGER,
#     payment_type VARCHAR(4),
#     additional_info VARCHAR(255),
#     raw_text TEXT)
class Expense(NamedTuple):
    id: Optional[int]
    amount: Decimal
    category_id: int
    payment_type: str
    additional_info: Optional[str]


def get_category_name(category_id: int) -> str:
    category = Categories().get_category_by_id(category_id)
    return category.name


# TODO: add class Message(NamedTuple)       -- Message handling
# TODO: add class Expense(NamedTuple)       -- Expense handling
# TODO: add def add_expense()               -- Expense handling
# TODO: add def last_ten()                  -- Expense handling
# TODO: add def delete_expense()            -- Expense handling
# TODO: add def _parse_message()            -- Message handling
# TODO: add def _get_now_formatted()        -- Date handling
# TODO: add def _get_now()                  -- Date handling
# TODO: add def _get_weekly_budget_limit()  -- Db data fetching
# TODO: add def _get_monthly_budget_limit() -- Db data fetching
# TODO: add def get_fixed_price()           -- Db data fetching


def add_expense(raw_message: str) -> Expense:
    payment_type_result = ''
    additional_info = None

    parsed_message = _parse_message(raw_message)
    category = Categories().get_category_by_name(parsed_message.category_text)

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
                                'time_creating': _get_today(),
                                'category_id': category.id,
                                'payment_type': payment_type_result,
                                'additional_info': additional_info,
                                'raw_text': raw_message})
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_id=category.id,
                   payment_type=payment_type_result,
                   additional_info=additional_info)


def last_expenses(limit: int = 10) -> str:
    """Return last expense with limit(default 10)"""
    cur = db.get_cursor()

    cur.execute(f"SELECT e.id, e.amount, c.id, e.payment_type, e.additional_info "
                f"FROM expense e LEFT JOIN category c ON c.id=e.category_id "
                f"ORDER BY e.time_creating DESC LIMIT {limit}")
    result = cur.fetchall()
    if not result[0]:
        return "There's none any expense"

    last_rows = []
    for row in result:
        last_rows.append(f"{row[1]} \u20BD "
                         f"for '{get_category_name(row[2])}' category. "
                         f"Click /delete{row[0]} to delete it.")

    answer_message = "Last expenses: \n\n* " + "\n\n* ".join(last_rows)
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
        raise NotCorrectMessage('Message format: <amount> <category_name> <payment_type> <additional_info>')

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


