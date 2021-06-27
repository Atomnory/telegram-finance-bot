from db import pg_db
from models import TypeofCategory, Budget, Category, FixedPrice, Expense


def inspect_db():
    """ Create tables and add row to them if database is empty. """
    with pg_db:
        cur = pg_db.execute_sql("SELECT * FROM information_schema.tables WHERE table_name='expense';")
        if not cur.fetchall():
            _connect_models()
            _insert_data_in_db()


def _connect_models():
    """ Create tables in database by models. """
    with pg_db:
        pg_db.create_tables([TypeofCategory, Budget, Category, FixedPrice, Expense])


def _insert_data_in_db():
    data_typeofcategory = [(1, 'Groceries'),
                           (2, 'Transport'),
                           (3, 'Bill'),
                           (4, 'Product'),
                           (5, 'Other')]

    TypeofCategory.insert_many(data_typeofcategory, fields=[TypeofCategory.id, TypeofCategory.name]).execute()

    Budget.create(type_id=1, weekly_limit=1000, monthly_limit=5000)

    data_category = [(1, 'Food', True, True, False, 'еда, продукты, магаз', 1),
                     (2, 'Drinking water', True, False, False, 'питьевая вода', 1),
                     (3, 'Bus', True, False, False, 'автобус', 2),
                     (4, 'Trolleybus', True, False, False, 'троллейбус', 2),
                     (5, 'Minibus', True, False, False, 'маршрутка', 2),
                     (6, 'Water', False, True, False, 'холодная вода', 3),
                     (7, 'Electricity', False, True, False, 'электричество, свет', 3),
                     (8, 'Garbage', False, True, False, 'тко, мусор', 3),
                     (9, 'Heating', False, True, False, 'тепло', 3),
                     (10, 'Gas', False, True, False, 'газ', 3),
                     (11, 'Major overhaul', False, True, False, 'кап ремонт', 3),
                     (12, 'Management company', False, True, False, 'ук', 3),
                     (13, 'Simcard', False, True, False, 'телефон, симка, связь, мегафон', 3),
                     (14, 'Internet', False, True, False, 'интернет, инет', 3),
                     (15, 'Mobile banking', False, True, False, 'сбер, банкинг', 3),
                     (16, 'Clothes', True, True, True, 'одежда, трусы', 4),
                     (17, 'Footwear', True, True, True, 'обувь, кросы, boots', 4),
                     (18, 'Electronic devices', True, True, True, 'приборы, техника, device, electronic', 4),
                     (19, 'Games', True, True, True, 'игры, игра, game', 4),
                     (20, 'Books', True, True, True, 'книги, книга, book', 4),
                     (21, 'Learning', True, True, True, 'обучение, курсы, course, courses', 4),
                     (22, 'Entertainment', True, True, True, 'развлечение, развлечения, кутёж, кутеж, туса, балдёж, '
                                                             'балдеж, кафе, мак, cafe, kfc, ресторан, рестик', 5),
                     (23, 'Money transfer', False, True, True, 'перевод, transfer', 5),
                     (24, 'Taxi', True, True, False, 'такси, личный извозчик', 5),
                     (25, 'Other', True, True, True, 'другое, прекол, приколдес, хз, остальное', 5)]

    Category.insert_many(data_category, fields=[Category.id, Category.name, Category.is_cash_accepted,
                                                Category.is_card_accepted, Category.is_additional_info_needed,
                                                Category.aliases, Category.type_id]).execute()

    data_fixedprice = [(2, 40),
                       (3, 27),
                       (4, 20),
                       (5, 32)]

    FixedPrice.insert_many(data_fixedprice, fields=[FixedPrice.category_id, FixedPrice.price]).execute()
