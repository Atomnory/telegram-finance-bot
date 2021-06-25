import datetime
from pytz import timezone
import db
from services.exceptions import CategoryDoesNotExist, TypeOfCategoryDoesNotExist, FixedPriceDoesNotExist
from category import Categories, Category
from type_of_category import TypesOfCategory
from typing import List
# TODO: create class ExpenseHandling() to do not calling db with every func.


def get_category_name_by_id(category_id: int) -> str:
    """
        If Category with 'category_id' was found return Category name.
        Else raise an Exception.
    """
    cur = db.get_cursor()
    cur.execute("SELECT category.category_name "
                "FROM category "
                "WHERE category.id=%s;", (category_id, ))
    result = cur.fetchone()
    if not result[0]:
        raise CategoryDoesNotExist('Table has not any category with that id')

    category_name = result[0]
    return category_name


def get_category_price_by_id(category_id: int) -> str:
    """ """
    cur = db.get_cursor()
    cur.execute("SELECT fixed_price.price "
                "FROM fixed_price "
                "WHERE fixed_price.category_id=%s;", (category_id, ))
    result = cur.fetchone()
    if not result[0]:
        raise FixedPriceDoesNotExist('Table has not any fixed price to this category')

    fixed_price = result[0]
    return fixed_price


def get_fixed_price_categories_name() -> List[str]:
    """ Get list with name of every category which have fixed price. """
    cur = db.get_cursor()
    cur.execute("SELECT category.category_name "
                "FROM category "
                "JOIN fixed_price ON category.id = fixed_price.category_id;")
    result = cur.fetchall()
    if not result[0]:
        raise FixedPriceDoesNotExist('Table has not any fixed price at all.')
    
    category_names = []
    for row in result:
        category_names.append(row[0])

    return category_names


def get_categories_name_by_type_id(type_id: int) -> List[str]:
    """ Get list with all categories by type id. """
    category_list = Categories().get_all_categories_by_type_id(type_id)
    result = []
    for category in category_list:
        result.append(category.name)
    return result


def get_type_name_by_id(type_id: int) -> str:
    """
        If Type with 'type_id' was found return Type name.
        Else raise an Exception.
    """
    cur = db.get_cursor()
    cur.execute("SELECT type_of_category.type_name "
                "FROM type_of_category "
                "WHERE type_of_category.id=%s;", (type_id, ))
    result = cur.fetchone()
    if not result[0]:
        raise TypeOfCategoryDoesNotExist('Table has not any type with that id')

    type_name = result[0]
    return type_name


def get_type_id_by_type_name(type_name: str) -> int:
    """
        If Type with 'type_name' was found return Type id.
        Else raise an Exception.
    """
    type_obj = TypesOfCategory().get_type_of_category_by_name(type_name)
    return type_obj.id


def get_today() -> datetime.datetime:
    """ Get today date and time with Moscow timezone. """
    msc = timezone('Europe/Moscow')
    today = datetime.datetime.now(msc)
    return today


def get_all_categories() -> str:
    """ Get string with all categories. """
    category_list = Categories().get_all_categories()
    result = []
    for row in category_list:

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


def get_list_all_types() -> List[str]:
    """ Get list with all types. """
    type_list = TypesOfCategory().get_all_types_of_category()
    result = []
    for row in type_list:
        result.append(row.type_name)
    return result


def get_all_types() -> str:
    """ Get string with all types. """
    type_list = TypesOfCategory().get_all_types_of_category()
    result = []
    for row in type_list:
        result.append(f" '{row.type_name}'. ")

    answer_message = "List of all Types: \n\n# " + "\n\n# ".join(result)
    answer_message += "\n\nList of Categories: /categories"
    return answer_message


def _get_category_by_name(category_name: str) -> Category:
    return Categories().get_category_by_name(category_name)


def is_cash_accepted(category_name: str) -> bool:
    """ Check does category accept cash. """
    return _get_category_by_name(category_name).is_cash_accepted


def is_card_accepted(category_name: str) -> bool:
    """ Check does category accept card. """
    return _get_category_by_name(category_name).is_card_accepted


def is_additional_info_needed(category_name: str) -> bool:
    """ Check does category need additional info. """
    return _get_category_by_name(category_name).is_additional_info_needed


def get_category_id_by_name(category_name: str) -> int:
    """ Get category id by category name. """
    return _get_category_by_name(category_name).id
