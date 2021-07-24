from playhouse.postgres_ext import fn
from decimal import Decimal
from models import TypeofCategory, Category, Expense
from utils.exceptions import QueryIsEmpty
from .statisticformatter import StatisticFormatter


# TODO: change main calling class from Statistic to StatisticFormatter
class Statistic:
    def __init__(self):
        self._period = None
        self._formatter = StatisticFormatter('')
        # set base formatter with empty period name because implementing in derived class override it

    def _set_period(self):
        pass

    def get_sum(self):
        try:
            expense_sum = self._get_sum_stat()
            groceries_sum = self._get_sum_groceries()
        except QueryIsEmpty as e:
            print(str(e))
            self._formatter.format_answer_sum_error()
            return self._formatter.answer
        else:
            self._formatter.format_answer_sum(expense_sum, groceries_sum)
            return self._formatter.answer

    def _get_sum_stat(self):
        query = self.__select_sum_query()
        if query[0].sum:
            return query[0].sum
        else:
            raise QueryIsEmpty(f"Sum row doesn't exist. "
                               f"period_name: {self._formatter.period_name}, period_date: {self._period}.")

    def __select_sum_query(self) -> Expense:
        expense_sum_query = (Expense
                             .select(fn.SUM(Expense.amount).alias('sum'))
                             .where(Expense.time_creating.truncate(self._formatter.period_name) == self._period))
        return expense_sum_query

    def _get_sum_groceries(self):
        # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
        query = self.__select_groceries_sum_query()
        if query[0].sum:
            return query[0].sum
        else:
            return self._get_zero_decimal()

    @staticmethod
    def _get_zero_decimal() -> Decimal:
        """ Using for display '0' with trailing zeros '0.00'. """
        return Decimal('0.00')

    def __select_groceries_sum_query(self) -> Expense:
        groceries_sum_query = (Expense
                               .select(fn.SUM(Expense.amount).alias('sum'))
                               .join(Category)
                               .join(TypeofCategory)
                               .where((TypeofCategory.name == 'Groceries')
                                      & (Expense.time_creating.truncate(self._formatter.period_name) == self._period)))
        return groceries_sum_query

    def get_by_category(self):
        try:
            expense_query = self.__get_statistic_by_category()
        except QueryIsEmpty as e:
            print(str(e))
            self._formatter.format_answer_by_category_error()
            return self._formatter.answer
        else:
            self._formatter.format_answer_by_category(expense_query)
            return self._formatter.answer

    def __get_statistic_by_category(self):
        query = self.__select_categories_query()
        if query:
            return query
        else:
            raise QueryIsEmpty(f"Categories row doesn't exist. "
                               f"period_name: {self._formatter.period_name}, period_date: {self._period}. ")

    def __select_categories_query(self):
        stat_category_query = (Expense
                               .select(fn.SUM(Expense.amount).alias('sum'), Category.name, Expense.payment_type)
                               .join(Category)
                               .where(Expense.time_creating.truncate(self._formatter.period_name) == self._period)
                               .group_by(Expense.category_id, Category.name, Expense.payment_type)
                               .order_by(Expense.category_id))
        return stat_category_query

    def get_by_type(self):
        try:
            expense_query = self.__get_statistic_by_type()
        except QueryIsEmpty as e:
            print(str(e))
            self._formatter.format_answer_by_type_error()
            return self._formatter.answer
        else:
            self._formatter.format_answer_by_type(expense_query)
            return self._formatter.answer

    def __get_statistic_by_type(self):
        query = self.__select_types_query()
        if query:
            return query
        else:
            raise QueryIsEmpty(f"Types row doesn't exist. "
                               f"period_name: {self._formatter.period_name}, period_date: {self._period}. ")

    def __select_types_query(self):
        stat_type_query = (Expense
                           .select(fn.SUM(Expense.amount).alias('sum'), TypeofCategory.name, Expense.payment_type)
                           .join(Category)
                           .join(TypeofCategory)
                           .where(Expense.time_creating.truncate(self._formatter.period_name) == self._period)
                           .group_by(TypeofCategory.id, TypeofCategory.name, Expense.payment_type)
                           .order_by(TypeofCategory.id))
        return stat_type_query

    def get_with_detail(self):
        try:
            query = self.__get_expense_detail_query()
        except QueryIsEmpty as e:
            print(str(e))
            self._formatter.format_answer_detail_error()
            return self._formatter.answer
        else:
            self._formatter.format_answer_detail(query)
            return self._formatter.answer

    def __get_expense_detail_query(self):
        result = self.__select_detail_query()
        if result:
            return result
        else:
            raise QueryIsEmpty(f"Expense row doesn't exist. "
                               f"period_name: {self._formatter.period_name}, period_date: {self._period}. ")

    def __select_detail_query(self):
        expense_detail_query = (Expense
                                .select(fn.SUM(Expense.amount).alias('sum'),
                                        Category.name, Expense.payment_type, Expense.additional_info)
                                .join(Category)
                                .where((Expense.time_creating.truncate(self._formatter.period_name) == self._period)
                                       & (Category.is_additional_info_needed == True))
                                .group_by(Expense.category_id, Category.name, Expense.payment_type,
                                          Expense.additional_info)
                                .order_by(Expense.category_id))
        return expense_detail_query

    # is should this func will be implemented in derived class as overriding func of try_get_sum_statistic?
    def _try_get_sum_with_limit_statistic(self) -> str:
        try:
            expense_sum = self._get_sum_stat()
            groceries_sum_and_limit = self.__get_sum_groceries_and_limit()
        except QueryIsEmpty as e:
            print(str(e))
            self._formatter.format_answer_sum_error()
            return self._formatter.answer
        else:
            self._formatter.format_answer_sum_with_limit(expense_sum, groceries_sum_and_limit)
            return self._formatter.answer

    def __get_sum_groceries_and_limit(self):
        # Return sum of all year groceries expenses or 0.00 if that expenses doesn't exist
        query = self._select_groceries_sum_with_limit_query()
        if query:
            return query[0][0], query[0][1]
        else:
            return self._get_zero_decimal(), self._get_period_limit('Groceries')

    def _select_groceries_sum_with_limit_query(self):
        pass

    def _get_period_limit(self, type_name: str) -> Decimal:
        pass
