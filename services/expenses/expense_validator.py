from decimal import Decimal
from typing import NamedTuple, Optional
from utils.exceptions import NotCorrectMessage
from services.service import get_category_by_name
from .message_parser import Message


class MockExpense(NamedTuple):
    amount: Decimal
    category_id: int
    category_name: str
    payment_type: str
    additional_info: Optional[str]
    raw_text: str


class ExpenseValidator:
    def __init__(self, message: Message):
        self._message = message
        self._expense = None
        self._category = None

        self._define_category()
        self._set_expense_from_message()

    def _define_category(self):
        try:
            self._category = get_category_by_name(self._message.category_name)
        except Exception:
            raise NotCorrectMessage(f"Invalid category name: '{self._message.category_name}'")

    def _set_expense_from_message(self):
        raw_text = str(self._message.amount) + ' ' + \
                   str(self._category.id) + ' ' + \
                   str(self._category.name) + ' ' + \
                   str(self._message.payment_type) + ' ' + \
                   str(self._message.additional_info)
        self._expense = MockExpense(amount=self._message.amount,
                                    category_id=self._category.id,
                                    category_name=self._category.name,
                                    payment_type=self._message.payment_type,
                                    additional_info=self._message.additional_info,
                                    raw_text=raw_text)

    def is_valid(self) -> bool:
        if self._is_amount_greater_zero()\
                and self._is_payment_type_accepted()\
                and self._is_additional_info_valid():
            return True

    def _is_amount_greater_zero(self) -> bool:
        if self._expense.amount > 0:
            return True
        else:
            raise NotCorrectMessage(f'Amount less or equal zero: {self._expense.amount}')

    def _is_payment_type_accepted(self) -> bool:
        if self._category.accepted_payments_type == 'Both' and self._expense.payment_type in ['Card', 'Cash']:
            return True
        elif self._expense.payment_type == self._category.accepted_payments_type:
            return True
        else:
            raise NotCorrectMessage(f"Invalid payment type for '{self._category.name}' : {self._expense.payment_type}")

    def _is_additional_info_valid(self) -> bool:
        if self._category.is_additional_info_needed and not self._expense.additional_info:
            raise NotCorrectMessage(f"Additional info is empty but needy for '{self._category.name}' category")
        else:
            return True

    @property
    def expense(self) -> MockExpense:
        return self._expense
