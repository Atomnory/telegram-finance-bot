

class NotCorrectMessage(Exception):
    """Incorrect message send to bot, unavailable to unparsing"""
    pass


class TypeOfCategoryDoesNotExist(Exception):
    """
        Try to get access to object of TypeOfCategory which doesn't exist.

        TypeOfCategory objects creating is based on createdb.sql script.
        So, if in createdb.sql none some row in type_of_category table that row cannot be found.
    """
    pass


class CategoryDoesNotExist(Exception):
    """
        Try to get access to object of Category that doesn't exist.
    """
    pass


class FixedPriceDoesNotExist(Exception):
    """
        Try to get access to object of FixedPrice that doesn't exist.
    """
    pass


class QueryIsEmpty(Exception):
    """
        Selecting query return None.
    """
    pass
