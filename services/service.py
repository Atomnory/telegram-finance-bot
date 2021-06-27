import datetime
from pytz import timezone
from models import TypeofCategory, Category, FixedPrice
from typing import List


def get_today() -> datetime.datetime:
    """ Get today date and now time with Moscow timezone. """
    msc = timezone('Europe/Moscow')
    today = datetime.datetime.now(msc)
    return today


# TODO: rename, refact result and append
def get_all_types() -> str:
    """ Get formatted string with name of all types. """
    result = []
    for row in TypeofCategory.select():
        result.append(f" '{row.name}'. ")

    answer_message = "List of all Types: \n\n# " + "\n\n# ".join(result)
    answer_message += "\n\nList of Categories: /categories"
    return answer_message


# TODO: rename, refact result and append
def get_list_all_types() -> List[str]:
    """ Get list with name of all types. """
    result = []
    for row in TypeofCategory.select():
        result.append(row.name)
    return result


# TODO: rename
def get_all_categories() -> str:
    """ Get formatted string with all categories. """
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


def get_type_id_by_type_name(type_name: str) -> int:
    """ Convert Type name in Type id. """
    type_obj = TypeofCategory.get(TypeofCategory.name == type_name)
    return type_obj.id


def get_type_name_by_id(type_id: int) -> str:
    """ Convert Type id in Type name. """
    type_obj = TypeofCategory.get_by_id(type_id)
    return type_obj.name


# TODO: add alias support
def get_category_id_by_category_name(category_name: str) -> int:
    """ Convert Category name in Category id. """
    category_obj = Category.get(Category.name == category_name)
    return category_obj.id


def get_category_name_by_id(category_id: int) -> str:
    """ Convert Category id in Category name. """
    category_obj = Category.get_by_id(category_id)
    return category_obj.name


# TODO: refact result and append
def get_categories_name_by_type_id(type_id: int) -> List[str]:
    """ Get list with all categories by type id. """
    result = []
    for category in Category.select().where(Category.type_id == type_id):
        result.append(category.name)
    return result


# TODO: add alias support and other if error
def get_category_by_name(category_name: str) -> Category:
    """ Return instance of Category by name. """
    return Category.get(Category.name == category_name)


def get_category_by_name_or_other(category_name: str) -> Category:
    """ Return instance of Category by name or instance of 'other' Category. """
    try:
        result = get_category_by_name(category_name)
    except Category.DoesNotExist as e:
        result = get_category_by_name('Other')
    finally:
        return result


def is_cash_accepted(category_name: str) -> bool:
    """ Check does category accept cash. """
    category_obj = Category.get(Category.name == category_name)
    return category_obj.is_cash_accepted


def is_card_accepted(category_name: str) -> bool:
    """ Check does category accept card. """
    category_obj = Category.get(Category.name == category_name)
    return category_obj.is_card_accepted


def is_additional_info_needed(category_name: str) -> bool:
    """ Check does category need additional info. """
    category_obj = Category.get(Category.name == category_name)
    return category_obj.is_additional_info_needed


# TODO: refact result and append
def get_fixed_price_categories_name() -> List[str]:
    """ Get list with name of every category which has fixed price. """
    result = []
    for row in Category.select().join(FixedPrice, on=(Category.id == FixedPrice.category_id)):
        result.append(row.name)
    return result


# TODO: refact get() to get_by_id()
def get_category_price_by_id(category_id: int) -> int:
    """ Get integer fixed price of category. """
    fixed_price_obj = FixedPrice.get(FixedPrice.category_id == category_id)
    return fixed_price_obj.price
