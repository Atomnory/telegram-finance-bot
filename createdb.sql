CREATE TABLE type_of_category(
    id INTEGER PRIMARY KEY,
    type_name VARCHAR(31)
);

CREATE TABLE budget(
    type_of_category_id INTEGER,
    weekly_limit INTEGER,
    monthly_limit INTEGER,
    FOREIGN KEY(type_of_category_id) REFERENCES type_of_category(id)
);

CREATE TABLE category(
    id INTEGER PRIMARY KEY,
    category_name VARCHAR(63),
    is_cash_accepted BOOLEAN,
    is_card_accepted BOOLEAN,
    is_additional_info_needed BOOLEAN,
    aliases TEXT,
    type_id INTEGER,
    FOREIGN KEY(type_id) REFERENCES type_of_category(id)
);

CREATE TABLE fixed_price(
    category_id INTEGER,
    price INTEGER,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

CREATE TABLE expense(
    id INTEGER PRIMARY KEY,
    amount DECIMAL(17,2),
    time_creating DATETIME,
    category_id INTEGER,
    payment_type VARCHAR(4),
    additional_info VARCHAR(255),
    raw_text TEXT,
    FOREIGN KEY(category_id) REFERENCES category(id)
);

INSERT INTO type_of_category(id, type_name)
VALUES (1, 'Grocery'),
    (2, 'Transport'),
    (3, 'Bill'),
    (4, 'Product'),
    (5, 'Other');

INSERT INTO budget(type_of_category_id, weekly_limit, monthly_limit)
VALUES (1, 1000, 5000);

INSERT INTO category(id, category_name, is_cash_accepted, is_card_accepted, is_additional_info_needed, aliases, type_id)
VALUES (1, 'Food', true, true, false, 'еда, продукты, магаз', 1),
    (2, 'Drinking water', true, false, false, 'питьевая вода', 1),
    (3, 'Bus', true, false, false, 'автобус', 2),
    (4, 'Trolleybus', true, false, false, 'троллейбус', 2),
    (5, 'Minibus', true, false, false, 'маршрутка', 2),
    (6, 'Water', false, true, false, 'холодная вода', 3),
    (7, 'Electricity', false, true, false, 'электричество, свет', 3),
    (8, 'Garbage', false, true, false, 'тко, мусор', 3),
    (9, 'Heating', false, true, false, 'тепло', 3),
    (10, 'Gas', false, true, false, 'газ', 3),
    (11, 'Major overhaul', false, true, false, 'кап ремонт', 3),
    (12, 'Management company', false, true, false, 'ук', 3),
    (13, 'Simcard', false, true, false, 'телефон, симка, связь, мегафон', 3),
    (14, 'Internet', false, true, false, 'интернет, инет', 3),
    (15, 'Mobile banking', false, true, false, 'сбер, банкинг', 3),
    (16, 'Clothes', true, true, true, 'одежда, трусы', 4),
    (17, 'Footwear', true, true, true, 'обувь, кросы, boots', 4),
    (18, 'Electronic devices', true, true, true, 'приборы, техника, device, electronic', 4),
    (19, 'Games', true, true, true, 'игры, игра, game', 4),
    (20, 'Books', true, true, true, 'книги, книга, book', 4),
    (21, 'Learning', true, true, true, 'обучение, курсы, course, courses', 4),
    (22, 'Entertainment', true, true, true, 'развлечение, развлечения, кутёж, кутеж, туса, балдёж, балдеж, кафе, мак, cafe, kfc, ресторан, рестик', 5),
    (23, 'Money transfer', false, true, true, 'перевод, transfer', 5),
    (24, 'Taxi', true, true, false, 'такси, личный извозчик', 5),
    (25, 'Other', true, true, true, 'другое, прекол, приколдес, хз, остальное', 5);

INSERT INTO fixed_price(category_id, price)
VALUES (2, 40),
    (3, 27),
    (4, 20),
    (5, 32);
