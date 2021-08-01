import re
from decimal import Decimal, ROUND_HALF_UP
from typing import NamedTuple, Optional
from utils.exceptions import NotCorrectMessage


class Message(NamedTuple):
    amount: Decimal
    category_name: str
    payment_type: str
    additional_info: Optional[str]


class MessageParser:
    def __init__(self):
        self._reg_exp = None
        self._message = None

    def parse_from(self, raw_message: str) -> Message:
        self._match_reg_exp(raw_message)
        self._check_reg_exp_valid()
        self._format_message_to_structure()
        return self._message

    def _match_reg_exp(self, message: str):
        self._reg_exp = re.match(
            r"(?P<amount>\d+[,.]?\d*) *"  # Float number with ',' or '.' (or int) for amount
            r"(?P<category>(?!cash|card)[A-ZА-ЯЁa-zа-яё]+ *(?!cash|card)[A-ZА-ЯЁa-zа-яё]*) *"
            # Max two words for category, exclude 'cash' and 'card'
            r"(?P<payment>cash|card)? *"  # Only 'cash' or 'card' for payment
            r"(?P<info>.+)?",  # Any signs, any length for info
            message)

    def _check_reg_exp_valid(self):
        if not self._reg_exp\
                or not self._reg_exp.group(0)\
                or not self._reg_exp.group('amount') \
                or not self._reg_exp.group('category')\
                or not self._reg_exp.group('payment'):
            raise NotCorrectMessage('Expense format: <amount> <category_name> <payment_type> <additional_info>')

    def _format_message_to_structure(self):
        amount = self._format_amount()
        category = self._format_category()
        payment = self._format_payment()
        info = self._define_info()
        self._message = Message(amount, category, payment, info)

    def _format_amount(self) -> Decimal:
        swap_float_sign = re.sub(',', '.', self._reg_exp.group('amount'), count=1)
        pure_decimal = Decimal(swap_float_sign.replace(' ', ''))   # TODO: test without replace
        # Round .005 to .01 and .004 to .00
        rounded_decimal = pure_decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return rounded_decimal

    def _format_category(self) -> str:
        category_name = self._reg_exp.group('category').strip().capitalize()  # TODO: test without strip
        return category_name

    def _format_payment(self) -> str:
        payment_type = self._reg_exp.group('payment').strip().capitalize()    # TODO: test without strip
        return payment_type

    def _define_info(self) -> Optional[str]:
        additional_info = None
        if self._reg_exp.group('info'):
            additional_info = self._reg_exp.group('info')
        return additional_info
