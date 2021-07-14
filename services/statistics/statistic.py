from playhouse.postgres_ext import fn
from decimal import Decimal
from typing import List
from models import TypeofCategory, Category, Expense
from utils.exceptions import QueryIsEmpty


class Statistic:
    def __init__(self):
        self._period_name = None
        self._next_period_name = None
        self._next_detail_period_name = None    # will be using only for 'detail statistics'
        self._period = None

    def get_sum(self):
        pass

    def get_by_category(self):
        pass

    def get_by_type(self):
        pass

    def get_with_detail(self):
        pass

    def _set_period(self):
        pass

    def _try_get_sum_statistic(self) -> str:
        try:
            expense_sum = self.__get_sum_stat()
            groceries_sum = self.__get_sum_groceries()
        except QueryIsEmpty as e:
            print(str(e))
            return self.__get_formatted_answer_sum_error()
        else:
            return self.__get_formatted_answer_sum(expense_sum, groceries_sum)

    def __get_sum_stat(self):
        query = self.__select_sum_query()
        if query[0].sum:
            return query[0].sum
        else:
            raise QueryIsEmpty(f"Sum row doesn't exist. period_name: {self._period_name}, period_date: {self._period}.")

    def __select_sum_query(self) -> Expense:
        expense_sum_query = (Expense
                             .select(fn.SUM(Expense.amount).alias('sum'))
                             .where(Expense.time_creating.truncate(self._period_name) == self._period))
        return expense_sum_query

    def __get_sum_groceries(self):
        # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
        query = self.__select_groceries_sum_query()
        if query[0].sum:
            return query[0].sum
        else:
            return self.__get_quantize_zero_decimal()

    def __select_groceries_sum_query(self) -> Expense:
        groceries_sum_query = (Expense
                               .select(fn.SUM(Expense.amount).alias('sum'))
                               .join(Category)
                               .join(TypeofCategory)
                               .where((TypeofCategory.name == 'Groceries')
                                      & (Expense.time_creating.truncate(self._period_name) == self._period)))
        return groceries_sum_query

    def __get_formatted_answer_sum_error(self) -> str:
        answer_message = (f"There's none any expense in this {self._period_name} \n\n"
                          f"{self._next_period_name.title()} statistic: /{self._next_period_name}")
        return answer_message

    def __get_formatted_answer_sum(self, expense_sum, groceries_sum) -> str:
        answer_message = (f"This {self._period_name} expenses: \n\n"
                          f"All: {expense_sum} \u20BD \n"
                          f"Groceries: {groceries_sum} \u20BD \n\n"
                          f"{self._period_name.title()} statistic by category: /{self._period_name}_category \n"
                          f"{self._next_period_name.title()} statistic: /{self._next_period_name}")
        return answer_message

    def _try_get_sum_with_limit_statistic(self) -> str:
        try:
            expense_sum = self.__get_sum_stat()
            groceries_sum_and_limit = self.__get_sum_groceries_and_limit()
        except QueryIsEmpty as e:
            print(str(e))
            return self.__get_formatted_answer_sum_error()
        else:
            return self.__get_formatted_answer_sum_with_limit(expense_sum, groceries_sum_and_limit)

    def __get_sum_groceries_and_limit(self):
        # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
        query = self._select_groceries_sum_with_limit_query()
        if query:
            return query[0][0], query[0][1]
        else:
            return self.__get_quantize_zero_decimal(), self._get_period_limit('Groceries')

    def _select_groceries_sum_with_limit_query(self):
        pass

    def _get_period_limit(self, type_name: str) -> Decimal:
        pass

    def __get_formatted_answer_sum_with_limit(self, expense_sum, groceries_sum_and_limit) -> str:
        grocery_sum, grocery_limit = groceries_sum_and_limit

        answer_message = (f"This {self._period_name} expenses: \n\n"
                          f"All: {expense_sum} \u20BD \n"
                          f"Groceries: {grocery_sum} \u20BD of {grocery_limit} \u20BD \n\n"
                          f"{self._period_name.title()} statistic by category: /{self._period_name}_category \n"
                          f"Detail {self._period_name} statistic: /{self._period_name}_detail \n"
                          f"{self._next_period_name.title()} statistic: /{self._next_period_name}")
        return answer_message

    def _try_get_statistic_by_category(self) -> str:
        try:
            expense_query = self.__get_statistic_by_category()
        except QueryIsEmpty as e:
            print(str(e))
            return self.__get_formatted_answer_by_category_error()
        else:
            return self.__get_formatted_answer_by_category(expense_query)

    def __get_statistic_by_category(self):
        query = self.__select_categories_query()
        if query:
            return query
        else:
            raise QueryIsEmpty(f"Categories row doesn't exist. "
                               f"period_name: {self._period_name}, period_date: {self._period}. ")

    def __select_categories_query(self):
        stat_category_query = (Expense
                               .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                               .join(Category)
                               .where(Expense.time_creating.truncate(self._period_name) == self._period)
                               .group_by(Expense.category_id, Category.name, Expense.payment_type)
                               .order_by(Expense.category_id))
        return stat_category_query

    def __get_formatted_answer_by_category_error(self) -> str:
        answer_message = (f"There's none any expense in this {self._period_name} \n\n"
                          f"{self._next_period_name.title()} statistic by category: /{self._next_period_name}_category")
        return answer_message

    def __get_formatted_answer_by_category(self, query) -> str:
        rows = self.__get_formatted_categories_rows(query)

        answer_message = f"This {self._period_name} expenses by category: \n\n# "
        answer_message += "\n\n# ".join(rows)
        answer_message += (f"\n\n{self._period_name.title()} sum statistic: /{self._period_name} \n"
                           f"{self._period_name.title()} statistic by type: /{self._period_name}_type \n"
                        f"{self._next_period_name.title()} statistic by category: /{self._next_period_name}_category")
        return answer_message

    def _try_get_statistic_by_type(self) -> str:
        try:
            expense_query = self.__get_statistic_by_type()
        except QueryIsEmpty as e:
            print(str(e))
            return self.__get_formatted_answer_by_type_error()
        else:
            return self.__get_formatted_answer_by_type(expense_query)

    def __get_statistic_by_type(self):
        query = self.__select_types_query()
        if query:
            return query
        else:
            raise QueryIsEmpty(f"Types row doesn't exist. "
                               f"period_name: {self._period_name}, period_date: {self._period}. ")

    def __select_types_query(self):
        stat_type_query = (Expense
                           .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                           .join(Category)
                           .join(TypeofCategory)
                           .where(Expense.time_creating.truncate(self._period_name) == self._period)
                           .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                           .order_by(TypeofCategory.id))
        return stat_type_query

    def __get_formatted_answer_by_type_error(self) -> str:
        answer_message = (f"There's none any expense in this {self._period_name} \n\n"
                          f"{self._next_period_name.title()} statistic by type: /{self._next_period_name}_type")
        return answer_message

    def __get_formatted_answer_by_type(self, query) -> str:
        rows = self.__get_formatted_types_rows(query)

        answer_message = f"This {self._period_name} expenses by type: \n\n# "
        answer_message += "\n\n# ".join(rows)
        answer_message += (f"\n\n{self._period_name.title()} sum statistic: /{self._period_name} \n"
                           f"{self._period_name.title()} statistic by category: /{self._period_name}_category \n"
                           f"{self._next_period_name.title()} statistic by type: /{self._next_period_name}_type")
        return answer_message

    def _try_get_detail_statistic(self) -> str:
        try:
            query = self.__get_expense_detail_query()
        except QueryIsEmpty as e:
            print(str(e))
            return self.__get_formatted_answer_detail_error()
        else:
            return self.__get_formatted_answer_detail(query)

    def __get_expense_detail_query(self):
        result = self.__select_detail_query()
        if result:
            return result
        else:
            raise QueryIsEmpty(f"Expense row doesn't exist. "
                               f"period_name: {self._period_name}, period_date: {self._period}. ")

    def __select_detail_query(self):
        expense_detail_query = (Expense
                                .select(fn.SUM(Expense.amount).alias('sum'),
                                        Category.name, Expense.payment_type, Expense.additional_info)
                                .join(Category)
                                .where((Expense.time_creating.truncate(self._period_name) == self._period)
                                       & (Category.is_additional_info_needed == True))
                                .group_by(Expense.category_id, Category.name, Expense.payment_type,
                                          Expense.additional_info)
                                .order_by(Expense.category_id))
        return expense_detail_query

    def __get_formatted_answer_detail_error(self) -> str:
        answer_message = (f"There's none such expense in this {self._period_name} \n\n"
                          f"{self._next_detail_period_name.title()} detail statistic: "
                          f"/{self._next_detail_period_name}_detail")
        return answer_message

    def __get_formatted_answer_detail(self, query) -> str:
        rows = self.__get_formatted_detail_rows(query)

        answer_message = f"Detail this {self._period_name} expenses: \n\n# "
        answer_message += "\n\n# ".join(rows)
        answer_message += (f"\n\n{self._period_name.title()} sum statistic: /{self._period_name} \n"
                           f"Detail {self._next_detail_period_name} statistic: /{self._next_detail_period_name}_detail")
        return answer_message

    @staticmethod
    def __get_quantize_zero_decimal() -> Decimal:
        """ Using for display '0' with trailing zeros '0.00'. """
        return Decimal(0.00).quantize(Decimal('1.11'))

    @staticmethod
    def __get_formatted_categories_rows(query) -> List[str]:
        rows = []
        for row in query:
            rows.append(f"{row.sum} \u20BD "
                        f"to '{row.category_id.name}' category "
                        f"with payment by {row.payment_type}. ")
        return rows

    @staticmethod
    def __get_formatted_types_rows(query) -> List[str]:
        rows = []
        for row in query:
            rows.append(f"{row.sum} \u20BD "
                        f"to '{row.category_id.type_id.name}' type "
                        f"with payment by {row.payment_type}. ")
        return rows

    @staticmethod
    def __get_formatted_detail_rows(query) -> List[str]:
        rows = []
        for row in query:
            rows.append(f"{row.sum} \u20BD "
                        f"to '{row.category_id.name}' category "
                        f"with payment by {row.payment_type}, "
                        f"describing: {row.additional_info}. ")
        return rows
