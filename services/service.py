import datetime
from pytz import timezone
from models import TypeofCategory, Category
from typing import List


def get_today_now() -> datetime.datetime:
    """ Get today date and now time with Moscow timezone. """
    msc = timezone('Europe/Moscow')
    today = datetime.datetime.now(msc)
    return today


def get_format_types() -> str:
    result = get_list_all_types()
    answer_message = "List of all Types: \n\n# " + "\n\n# ".join(result)
    answer_message += "\n\nList of Categories: /categories"
    return answer_message


def get_list_all_types() -> List[str]:
    result = []
    for row in TypeofCategory.select():
        result.append(row.name)
    return result


# TODO: rename
def get_all_categories() -> str:
    result = []
    for row in Category.select():
        payment_type = ''
        if row.is_card_accepted and row.is_cash_accepted:
            payment_type = 'both'
        elif row.is_card_accepted and not row.is_cash_accepted:
            payment_type = 'card'
        elif not row.is_card_accepted and row.is_cash_accepted:
            payment_type = 'cash'

        result.append(f" '{row.name}', payment: {payment_type}, aliases: {row.aliases}. ")

    answer_message = "List of all Categories: \n\n# " + "\n\n# ".join(result)
    answer_message += "\n\nList of Types: /types"
    return answer_message


def get_type_by_name(type_name: str) -> TypeofCategory:
    type_obj = TypeofCategory.get(TypeofCategory.name == type_name)
    return type_obj


def get_categories_name_by_type(type_obj: TypeofCategory) -> List[str]:
    result = []
    for category in Category.select().where(Category.type_id == type_obj.id):
        result.append(category.name)
    return result


# TODO: add alias support
def get_category_by_name(category_name: str) -> Category:
    return Category.get(Category.name == category_name)


def get_category_by_name_or_other(category_name: str) -> Category:
    try:
        result = get_category_by_name(category_name)
    except Category.DoesNotExist as e:
        result = get_category_by_name('Other')
    finally:
        return result


def is_both_payment_type_accepted(category: Category) -> bool:
    return category.accepted_payments_type == 'Both'
