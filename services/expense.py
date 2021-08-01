from typing import Optional
from models import Category, Expense
from services.service import get_today_now
from .expenses.message_parser import MessageParser
from .expenses.expense_validator import ExpenseValidator


class ExpenseCreator:
    def __init__(self):
        self._parser = MessageParser()
        self._validator = None
        self._parsed_message = None
        self._expense = None

    def parse_message_and_create_expense_if_valid(self, message: str) -> str:
        """ Return string with expense creating confirmation. """
        self._parse(message)
        self._validate()
        self._create()
        return self._get_answer_message()

    def _parse(self, message: str):
        self._parsed_message = self._parser.parse_from(message)

    def _validate(self):
        self._validator = ExpenseValidator(self._parsed_message)
        if self._validator.is_valid():
            self._expense = self._validator.expense

    def _create(self):
        Expense.create(amount=self._expense.amount,
                       time_creating=get_today_now(),
                       category_id=self._expense.category_id,
                       payment_type=self._expense.payment_type,
                       additional_info=self._expense.additional_info,
                       raw_text=self._expense.raw_text)

    def _get_answer_message(self) -> str:
        answer_message = (f"Expense was added by {self._expense.amount} \u20BD "
                          f"to '{self._expense.category_name}' category "
                          f"with payment by {self._expense.payment_type}. \n\n"
                          f"To see all expenses: /expenses")
        return answer_message


class ExpenseDisplayer:
    def __init__(self):
        self._limit = 10    # Using as limit to showing 10 last expenses
        self._query = None
        self._rows = []
        self._answer_message = None

    def get_last(self, limit: Optional[int] = None) -> str:
        """ Receive 'limit' for expense selecting. By default limit = 10. """
        if limit:
            self._limit = limit
        self._select_last()
        self._format_rows()
        self._format_answer()
        return self._answer_message

    def _select_last(self):
        self._query = (Expense
                       .select(Expense.id, Expense.amount, Category.name, Expense.payment_type)
                       .join(Category, on=(Expense.category_id == Category.id))
                       .order_by(Expense.id.desc())
                       .limit(self._limit))

    def _format_rows(self):
        for row in self._query:
            self._rows.append(f"{row.amount} \u20BD "
                             f"to '{row.category_id.name}' category "
                             f"with payment by {row.payment_type}. \n"
                             f"   Click /delete{row.id} to delete.")

    def _format_answer(self):
        self._answer_message = "Last expenses: \n\n# " + "\n\n# ".join(self._rows)


class ExpenseDeleter:
    def __init__(self):
        self._expense = None

    def delete_expense(self, expense_id: int) -> str:
        self._expense = Expense.get_by_id(expense_id)
        self._expense.delete_instance()
        return self._get_answer_message()

    def _get_answer_message(self):
        answer_message = f"{self._expense.amount} \u20BD for '{self._expense.category_id.name}' category was deleted. "
        return answer_message
