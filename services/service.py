import datetime
from pytz import timezone
import db
from services.exceptions import CategoryDoesNotExist, TypeOfCategoryDoesNotExist
from category import Categories
from type_of_category import TypesOfCategory
# TODO: create menu and back commands


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


def get_all_types() -> str:
    """ Get string with all types. """
    type_list = TypesOfCategory().get_all_types_of_category()
    result = []
    for row in type_list:
        result.append(f" '{row.type_name}'. ")

    answer_message = "List of all Types: \n\n# " + "\n\n# ".join(result)
    answer_message += "\n\nList of Categories: /categories"
    return answer_message
