from typing import NamedTuple, Optional
from utils.exceptions import NotCorrectMessage
import re
from services.service import get_today_now, get_category_by_name
from datetime import datetime
from decimal import *
from models import Category, Expense


class Message(NamedTuple):
    amount: Decimal
    category_text: str
    payment_type_text: Optional[str]
    additional_info_text: Optional[str]


def add_expense(raw_message: str) -> str:
    payment_type_result = ''
    additional_info = None

    parsed_message = _parse_message(raw_message)
    category_obj = get_category_by_name(parsed_message.category_text)

    # TODO: move if below to another module
    if parsed_message.amount <= 0:
        raise NotCorrectMessage('Amount should be more than 0')

    # TODO: move if below to another module
    if category_obj.is_cash_accepted and not category_obj.is_card_accepted:     # CASH only
        if not parsed_message.payment_type_text:
            payment_type_result = 'cash'
        elif parsed_message.payment_type_text == 'cash':
            payment_type_result = 'cash'
        else:
            raise NotCorrectMessage('This category only Cash is accepted')
    elif not category_obj.is_cash_accepted and category_obj.is_card_accepted:   # CARD only
        if not parsed_message.payment_type_text:
            payment_type_result = 'card'
        elif parsed_message.payment_type_text == 'card':
            payment_type_result = 'card'
        else:
            raise NotCorrectMessage('This category only Card is accepted')
    elif category_obj.is_cash_accepted and category_obj.is_card_accepted:       # BOTH
        if not parsed_message.payment_type_text:
            raise NotCorrectMessage('You should choose type of payment')
        elif parsed_message.payment_type_text == 'cash':
            payment_type_result = 'cash'
        elif parsed_message.payment_type_text == 'card':
            payment_type_result = 'card'
        else:
            raise NotCorrectMessage("Payment type only may be 'cash' or 'card'")

    # TODO: move if below to another module
    if category_obj.is_additional_info_needed:
        if parsed_message.additional_info_text:
            additional_info = parsed_message.additional_info_text
        else:
            raise NotCorrectMessage('This category is needed additional info')

    insert_expense(amount=parsed_message.amount,
                   date=get_today_now(),
                   category_id=category_obj.id,
                   payment=payment_type_result,
                   add_info=additional_info,
                   raw_text=raw_message)

    answer_message = (f"Expense was added by {parsed_message.amount} \u20BD "
                      f"to '{category_obj.name}' category "
                      f"with payment by {payment_type_result}. \n\n"
                      f"To see all expenses: /expenses")
    return answer_message


def last_expenses(limit: int = 10) -> str:
    """ Return last expense with limit (default 10). """
    expenses_query = (Expense
                      .select(Expense.id, Expense.amount, Category.name, Expense.payment_type)
                      .join(Category, on=(Expense.category_id == Category.id))
                      .order_by(Expense.id.desc())
                      .limit(limit))
    last_rows = []
    for row in expenses_query:
        last_rows.append(f"{row.amount} \u20BD "
                         f"to '{row.category_id.name}' category "
                         f"with payment by {row.payment_type}. \n"
                         f"   Click /delete{row.id} to delete.")

    answer_message = "Last expenses: \n\n# " + "\n\n# ".join(last_rows)
    return answer_message


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
    swap_float_sign = re.sub(',', '..', regexp_result.group('amount'), count=1)  # Replace first occurrence of ',' to '.'
    decim = Decimal(swap_float_sign.replace(' ', ''))        # Delete possibly redundant spaces and convert to Decimal
    amount = decim.quantize(Decimal('1.01'), rounding=ROUND_HALF_UP)      # Round .005 on the end to .01

    category_text = regexp_result.group('category').strip()

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


def insert_expense(*, amount: Decimal, date: datetime, category_id: int, payment: str, add_info: str, raw_text: str)\
        -> None:
    """ Insert expense to database. """
    Expense.create(amount=amount,
                   time_creating=date,
                   category_id=category_id,
                   payment_type=payment,
                   additional_info=add_info,
                   raw_text=raw_text)


def delete_expense(expense_id: int) -> None:
    """ Delete expense from database by expense id. """
    expense_to_delete = Expense.get_by_id(expense_id)
    expense_to_delete.delete_instance()
