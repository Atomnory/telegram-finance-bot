import os
from datetime import date
from datetime import datetime
from playhouse.sqlite_ext import *
from decimal import Decimal

test_db_file = 'test.db'
test_db = SqliteExtDatabase(test_db_file, pragmas={
    'cache_size': -1024 * 64,
    'journal_mode': 'wal',
    'foreign_keys': 1
})


class BaseModel(Model):
    class Meta:
        database = test_db
        order_by = 'id'


class TypeofCategory(BaseModel):
    id = AutoField()
    name = CharField(max_length=63, unique=True, null=False)
    weekly_limit = IntegerField(null=True)
    monthly_limit = IntegerField(null=True)


class Category(BaseModel):
    id = AutoField()
    name = CharField(max_length=63, unique=True, null=False)
    accepted_payments_type = CharField(max_length=4, null=False)
    is_additional_info_needed = BooleanField(null=False)
    fixed_price = IntegerField(null=True)
    aliases = TextField(null=True)
    type_id = ForeignKeyField(TypeofCategory, on_delete='CASCADE')


class Expense(BaseModel):
    id = AutoField()
    amount = DecimalField(max_digits=12, decimal_places=2, null=False)
    time_creating = DateTimeField(null=False)
    category_id = ForeignKeyField(Category, on_delete='SET NULL')
    payment_type = CharField(max_length=4, null=False)
    additional_info = CharField(max_length=255, null=True)
    raw_text = TextField(null=True)


def init_test_db():
    """ Create tables and add row to them if database is empty. """
    with test_db:
        test_db.create_tables([TypeofCategory, Category, Expense])
        _insert_data()


def create_test_db():
    f = open(test_db_file, 'x')
    f.close()


def delete_test_db():
    if os.path.exists(test_db_file):
        os.remove(test_db_file)


def _insert_data():
    _insert_many_types()
    _insert_many_categories()
    _insert_many_expenses()


def _insert_many_types():
    data_typeofcategory = [(1, 'Groceries', 1000, 5000),
                           (2, 'Transport', None, None),
                           (3, 'Bill', None, None),
                           (4, 'Product', None, None),
                           (5, 'Other', None, None)]

    TypeofCategory.insert_many(data_typeofcategory, fields=[TypeofCategory.id,
                                                            TypeofCategory.name,
                                                            TypeofCategory.weekly_limit,
                                                            TypeofCategory.monthly_limit]).execute()


def _insert_many_categories():
    data_category = [(1, 'Food', 'Both', False, None, 'еда, продукты, магаз', 1),
                     (2, 'Drinking water', 'Cash', False, 40, 'питьевая вода', 1),
                     (3, 'Bus', 'Cash', False, 27, 'автобус', 2),
                     (4, 'Trolleybus', 'Cash', False, 20, 'троллейбус', 2),
                     (5, 'Minibus', 'Cash', False, 32, 'маршрутка', 2),
                     (6, 'Water', 'Card', False, None, 'холодная вода', 3),
                     (7, 'Electricity', 'Card', False, None, 'электричество, свет', 3),
                     (8, 'Garbage', 'Card', False, None, 'тко, мусор', 3),
                     (9, 'Heating', 'Card', False, None, 'тепло', 3),
                     (10, 'Gas', 'Card', False, None, 'газ', 3),
                     (11, 'Major overhaul', 'Card', False, None, 'кап ремонт', 3),
                     (12, 'Management company', 'Card', False, None, 'ук', 3),
                     (13, 'Simcard', 'Card', False, None, 'телефон, симка, связь, мегафон', 3),
                     (14, 'Internet', 'Card', False, None, 'интернет, инет', 3),
                     (15, 'Mobile banking', 'Card', False, None, 'сбер, банкинг', 3),
                     (16, 'Clothes', 'Both', True, None, 'одежда, трусы', 4),
                     (17, 'Footwear', 'Both', True, None, 'обувь, кросы, boots', 4),
                     (18, 'Electronic devices', 'Both', True, None, 'приборы, техника, device, electronic', 4),
                     (19, 'Games', 'Both', True, None, 'игры, игра, game', 4),
                     (20, 'Books', 'Both', True, None, 'книги, книга, book', 4),
                     (21, 'Learning', 'Both', True, None, 'обучение, курсы, course, courses', 4),
                     (22, 'Entertainment', 'Both', True, None, 'развлечение, кафе, мак, kfc, ресторан', 5),
                     (23, 'Money transfer', 'Card', True, None, 'перевод, transfer', 5),
                     (24, 'Taxi', 'Both', False, None, 'такси, личный извозчик', 5),
                     (25, 'Other', 'Both', True, None, 'другое, хз, остальное', 5)]

    Category.insert_many(data_category, fields=[Category.id,
                                                Category.name,
                                                Category.accepted_payments_type,
                                                Category.is_additional_info_needed,
                                                Category.fixed_price,
                                                Category.aliases,
                                                Category.type_id]).execute()


def get_today_now():
    today = datetime.today()
    return today


def _insert_many_expenses():
    # Every time period has 'displaying scope' in Statistic. Comments explain this scope.
    time = get_today_now().time()

    # In year, month, week and day will be displayed
    today = get_today_now().date()
    now = get_today_now()

    # Only in year, month and week will be displayed
    this_week_date = date.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=3)
    if this_week_date.day == today.day:
        this_week_date = date.fromisocalendar(year=today.isocalendar()[0], week=today.isocalendar()[1], day=5)
    this_week = datetime.combine(this_week_date, time)

    # Only in year and month will be displayed
    this_month_date = date(year=today.year, month=today.month, day=10)
    if this_month_date.day == today.day or this_month_date.isocalendar()[1] == today.isocalendar()[1]:
        this_month_date = date(year=today.year, month=today.month, day=20)  # in year and month will be displayed
    this_month = datetime.combine(this_month_date, time)

    # Only in year will be displayed
    this_year_date = date(year=today.year, month=2, day=10)
    if this_year_date.month == today.month:
        this_year_date = date(year=today.year, month=11, day=10)   # in year will be displayed
    this_year = datetime.combine(this_year_date, time)

    prev_year_date = date(year=today.year-1, month=3, day=10)   # never be displayed
    next_year_date = date(year=today.year-1, month=3, day=10)   # never be displayed
    prev_year = datetime.combine(prev_year_date, time)
    next_year = datetime.combine(next_year_date, time)

    money = 'Cash'
    card = 'Card'

    data_expense = [(1, Decimal('150.00'), now, 1, money, None, 'test'),
                    (2, Decimal('150.00'), now, 1, card, None, 'test'),
                    (3, Decimal('25.00'), now, 7, card, None, 'test')]

    Expense.insert_many(data_expense, fields=[Expense.id,
                                              Expense.amount,
                                              Expense.time_creating,
                                              Expense.category_id,
                                              Expense.payment_type,
                                              Expense.additional_info,
                                              Expense.raw_text]).execute()
