from db import pg_db
from models import TypeofCategory, Category, Expense


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
        pg_db.create_tables([TypeofCategory, Category, Expense])


def _insert_data_in_db():
    data_typeofcategory = [(1, 'Groceries', 1000, 5000),
                           (2, 'Transport', None, None),
                           (3, 'Bill', None, None),
                           (4, 'Product', None, None),
                           (5, 'Other', None, None)]

    TypeofCategory.insert_many(data_typeofcategory, fields=[TypeofCategory.id,
                                                            TypeofCategory.name,
                                                            TypeofCategory.weekly_limit,
                                                            TypeofCategory.monthly_limit]).execute()

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
                     (25, 'Other', 'Both', True, None, 'другое, прекол, приколдес, хз, остальное', 5)]

    Category.insert_many(data_category, fields=[Category.id, Category.name, Category.accepted_payments_type,
                                                Category.is_additional_info_needed, Category.fixed_price,
                                                Category.aliases, Category.type_id]).execute()
