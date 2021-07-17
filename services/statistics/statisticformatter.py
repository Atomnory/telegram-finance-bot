from typing import List


class StatisticFormatter:
    def __init__(self, period_name: str):
        self.__period_name = period_name
        self.__next_period_name = None
        self.__next_detail_period_name = None
        self.__answer = None
        self.__define_next_period_name_by(period_name)
        self.__define_next_detail_period_name_by(period_name)

    @property
    def period_name(self):
        return self.__period_name

    @property
    def answer(self):
        return self.__answer

    def __define_next_period_name_by(self, period_name: str):
        if period_name == 'day':
            self.__next_period_name = 'week'
        elif period_name == 'week':
            self.__next_period_name = 'month'
        elif period_name == 'month':
            self.__next_period_name = 'year'
        elif period_name == 'year':
            self.__next_period_name = 'day'
        # get_detail_period accept only day, week, month and year periods.

    def __define_next_detail_period_name_by(self, period_name: str):
        if period_name == 'week':
            self.__next_detail_period_name = 'month'
        elif period_name == 'month':
            self.__next_detail_period_name = 'week'
        # get_next_detail_period accept only week and month periods.

    def form_answer_sum_error(self):
        self.__answer = (f"There's none any expense in this {self.__period_name} \n\n"
                         f"{self.__next_period_name.title()} statistic: /{self.__next_period_name}")

    def form_answer_sum(self, expense_sum, groceries_sum):
        self.__answer = (f"This {self.__period_name} expenses: \n\n"
                         f"All: {expense_sum} \u20BD \n"
                         f"Groceries: {groceries_sum} \u20BD \n\n"
                         f"{self.__period_name.title()} statistic by category: /{self.__period_name}_category \n"
                         f"{self.__next_period_name.title()} statistic: /{self.__next_period_name}")

    def form_answer_sum_with_limit(self, expense_sum, groceries_sum_and_limit):
        grocery_sum, grocery_limit = groceries_sum_and_limit
        self.__answer = (f"This {self.__period_name} expenses: \n\n"
                         f"All: {expense_sum} \u20BD \n"
                         f"Groceries: {grocery_sum} \u20BD of {grocery_limit} \u20BD \n\n"
                         f"{self.__period_name.title()} statistic by category: /{self.__period_name}_category \n"
                         f"Detail {self.__period_name} statistic: /{self.__period_name}_detail \n"
                         f"{self.__next_period_name.title()} statistic: /{self.__next_period_name}")

    def form_answer_by_category_error(self):
        self.__answer = (f"There's none any expense in this {self.__period_name} \n\n"
                         f"{self.__next_period_name.title()} statistic by category: "
                         f"/{self.__next_period_name}_category")

    def form_answer_by_category(self, query):
        rows = self.__get_formatted_categories_rows(query)
        self.__answer = f"This {self.__period_name} expenses by category: \n\n# " + "\n\n# ".join(rows)
        self.__answer += (f"\n\n{self.__period_name.title()} sum statistic: /{self.__period_name} \n"
                          f"{self.__period_name.title()} statistic by type: /{self.__period_name}_type \n"
                          f"{self.__next_period_name.title()} statistic by category: "
                          f"/{self.__next_period_name}_category")

    @staticmethod
    def __get_formatted_categories_rows(query) -> List[str]:
        rows = []
        for row in query:
            rows.append(f"{row.sum} \u20BD "
                        f"to '{row.category_id.name}' category "
                        f"with payment by {row.payment_type}. ")
        return rows

    def form_answer_by_type_error(self):
        self.__answer = (f"There's none any expense in this {self.__period_name} \n\n"
                         f"{self.__next_period_name.title()} statistic by type: /{self.__next_period_name}_type")

    def form_answer_by_type(self, query):
        rows = self.__get_formatted_types_rows(query)
        self.__answer = f"This {self.__period_name} expenses by type: \n\n# " + "\n\n# ".join(rows)
        self.__answer += (f"\n\n{self.__period_name.title()} sum statistic: /{self.__period_name} \n"
                          f"{self.__period_name.title()} statistic by category: /{self.__period_name}_category \n"
                          f"{self.__next_period_name.title()} statistic by type: /{self.__next_period_name}_type")

    @staticmethod
    def __get_formatted_types_rows(query) -> List[str]:
        rows = []
        for row in query:
            rows.append(f"{row.sum} \u20BD "
                        f"to '{row.category_id.type_id.name}' type "
                        f"with payment by {row.payment_type}. ")
        return rows

    def formatted_answer_detail_error(self):
        self.__answer = (f"There's none such expense in this {self.__period_name} \n\n"
                         f"{self.__next_detail_period_name.title()} detail statistic: "
                         f"/{self.__next_detail_period_name}_detail")

    def formatted_answer_detail(self, query):
        rows = self.__get_formatted_detail_rows(query)
        self.__answer = f"Detail this {self.__period_name} expenses: \n\n# " + "\n\n# ".join(rows)
        self.__answer += (f"\n\n{self.__period_name.title()} sum statistic: /{self.__period_name} \n"
                          f"Detail {self.__next_detail_period_name} statistic: /{self.__next_detail_period_name}_detail")

    @staticmethod
    def __get_formatted_detail_rows(query) -> List[str]:
        rows = []
        for row in query:
            rows.append(f"{row.sum} \u20BD "
                        f"to '{row.category_id.name}' category "
                        f"with payment by {row.payment_type}, "
                        f"describing: {row.additional_info}. ")
        return rows
