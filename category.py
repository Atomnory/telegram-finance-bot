from typing import Dict, List, NamedTuple
import db
from exceptions import CategoryDoesNotExist


# category(id INTEGER,
#         category_name VARCHAR,
#         is_cash_accepted BOOLEAN,
#         is_card_accepted BOOLEAN,
#         is_additional_info_needed BOOLEAN,
#         aliases TEXT,
#         type_id INTEGER)
class Category(NamedTuple):
    id: int
    name: str
    is_cash_accepted: bool
    is_card_accepted: bool
    is_additional_info_needed: bool
    aliases: List[str]
    type_id: int


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """
            Fetch all rows from 'category' table.
            Convert them from List[Dict] to List[Category(NamedTuple)].
        """
        categories = db.fetchall_from_db('category',
            'id category_name is_cash_accepted is_card_accepted is_additional_info_needed aliases type_id'.split())
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """
            Convert taken List[Dict] to List[Category(NamedTuple)].

            Make 'aliases' class attribute easy to handle.

            Append to 'aliases' 'category_name' because only 'aliases' will be using to find by name.
        """
        categories_result = []
        for index, category in enumerate(categories):       # TODO: try without enumerate
            aliases_list = category['aliases'].split(',')       # TODO: test .split('')
            aliases_list = list(filter(None, map(str.strip, aliases_list)))
            aliases_list.append(category['category_name'])
            categories_result.append(Category(id=category['id'],
                                              name=category['category_name'],
                                              is_cash_accepted=category['is_cash_accepted'],
                                              is_card_accepted=category['is_card_accepted'],
                                              is_additional_info_needed=category['is_additional_info_needed'],
                                              aliases=aliases_list,
                                              type_id=category['type_id']))
        return categories_result

    def get_all_categories(self) -> List[Category]:
        return self._categories

    def get_all_categories_by_type_id(self, type_of_category_id: int) -> List[Category]:
        """
            Return List of Category's which have exact type_of_category_id if at least one such Category is exist.
            Else raise an Exception.
        """
        result = []
        for category in self._categories:
            if category.type_id == type_of_category_id:
                result.append(category)
        if not result:
            raise CategoryDoesNotExist('Table has not any category with that type_id')
        return result

    def get_category_by_name(self, category_name: str) -> Category:
        """
            If Category with 'category_name' was found return that Category.
            Else return 'Other' Category.
        """
        result = None
        category_other = None
        for category in self._categories:
            if category.name == 'Other':
                category_other = category
            for alias in category.aliases:
                if category_name in alias:
                    result = category
        if not result:
            result = category_other
        return result

    def get_category_by_id(self, category_id: int) -> Category:
        """
            If Category with 'category_id' was found return that Category.
            Else raise an Exception.
        """
        result = None
        for category in self._categories:
            if category.id == category_id:
                result = category
        if not result:
            raise CategoryDoesNotExist('Table has not any category with that id')
        return result
