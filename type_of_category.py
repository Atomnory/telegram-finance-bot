from typing import List, NamedTuple
import db
from services.exceptions import TypeOfCategoryDoesNotExist


# type_of_category(id INTEGER, type_name VARCHAR)
class TypeOfCategory(NamedTuple):
    id: int
    type_name: str


class TypesOfCategory:
    def __init__(self):
        self._types = self._load_types()

    def _load_types(self) -> List[TypeOfCategory]:
        """
            Fetch all rows from 'type_of_category' table.
            Convert them from List[Dict] to List[TypeOfCategory(NamedTuple)].
        """
        types = db.fetchall_from_db('type_of_category', 'id type_name'.split())
        types_result = []
        for index, type_of_category in enumerate(types):   # TODO: change 'for enumerate' to simple 'for'
            types_result.append(TypeOfCategory(id=type_of_category['id'],
                                               type_name=type_of_category['type_name']))
        return types_result

    def get_all_types_of_category(self) -> List[TypeOfCategory]:
        return self._types

    def get_type_of_category_by_name(self, type_name: str) -> TypeOfCategory:
        """
            If TypeOfCategory with 'type_name' was found return that TypeOfCategory.
            Else raise an Exception.
        """
        result = None
        for type_category in self._types:
            if type_category.type_name == type_name:
                result = type_category
        if not result:
            raise TypeOfCategoryDoesNotExist('Table has not any type with that name')
        return result

    def get_type_of_category_by_name_or_other(self, type_name: str) -> TypeOfCategory:
        """
            If TypeOfCategory with 'type_name' was found return that TypeOfCategory.
            Else return 'Other' TypeOfCategory.
        """
        try:
            result = self.get_type_of_category_by_name(type_name)
        except TypeOfCategoryDoesNotExist:
            for type_category in self._types:
                if type_category.type_name == 'Other':
                    result = type_category
        finally:
            return result
