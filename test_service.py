import pytest
import peewee
import datetime
from pytz import timezone
from services import service


def test_get_today_now():
    assert service.get_today_now() == datetime.datetime.now(timezone('Europe/Moscow'))


def test_get_formatted_types():
    assert service.get_formatted_types() == 'List of all Types: \n\n' \
                                            '# Groceries\n\n' \
                                            '# Transport\n\n' \
                                            '# Bill\n\n' \
                                            '# Product\n\n' \
                                            '# Other\n\n' \
                                            'List of Categories: /categories'


def test_get_formatted_categories():
    assert service.get_formatted_categories() == "List of all Categories: \n\n#  " \
                                                 "'Food', payment: Both, type: Groceries.\n\n#  " \
                                                 "'Drinking water', payment: Cash, type: Groceries.\n\n#  " \
                                                 "'Bus', payment: Cash, type: Transport.\n\n#  " \
                                                 "'Trolleybus', payment: Cash, type: Transport.\n\n#  " \
                                                 "'Minibus', payment: Cash, type: Transport.\n\n#  " \
                                                 "'Water', payment: Card, type: Bill.\n\n#  " \
                                                 "'Electricity', payment: Card, type: Bill.\n\n#  " \
                                                 "'Garbage', payment: Card, type: Bill.\n\n#  " \
                                                 "'Heating', payment: Card, type: Bill.\n\n#  " \
                                                 "'Gas', payment: Card, type: Bill.\n\n#  " \
                                                 "'Major overhaul', payment: Card, type: Bill.\n\n#  " \
                                                 "'Management company', payment: Card, type: Bill.\n\n#  " \
                                                 "'Simcard', payment: Card, type: Bill.\n\n#  " \
                                                 "'Internet', payment: Card, type: Bill.\n\n#  " \
                                                 "'Mobile banking', payment: Card, type: Bill.\n\n#  " \
                                                 "'Clothes', payment: Both, type: Product.\n\n#  " \
                                                 "'Footwear', payment: Both, type: Product.\n\n#  " \
                                                 "'Electronic devices', payment: Both, type: Product.\n\n#  " \
                                                 "'Games', payment: Both, type: Product.\n\n#  " \
                                                 "'Books', payment: Both, type: Product.\n\n#  " \
                                                 "'Learning', payment: Both, type: Product.\n\n#  " \
                                                 "'Entertainment', payment: Both, type: Other.\n\n#  " \
                                                 "'Money transfer', payment: Card, type: Other.\n\n#  " \
                                                 "'Taxi', payment: Both, type: Other.\n\n#  " \
                                                 "'Other', payment: Both, type: Other.\n\n" \
                                                 "List of Types: /types"


def test_get_list_all_types():
    assert service.get_list_all_types() == ['Groceries', 'Transport', 'Bill', 'Product', 'Other']


def test_get_type_by_name():
    types = service.get_list_all_types()
    for type_ in types:
        assert service.get_type_by_name(type_).name == type_


def test_get_type_by_name_error():
    with pytest.raises(peewee.DoesNotExist):
        service.get_type_by_name('Error')
        service.get_type_by_name('')
        service.get_type_by_name(1)


def test_get_categories_name_by_type():
    assert service.get_categories_name_by_type(service.get_type_by_name('Groceries')) == ['Food', 'Drinking water']
    assert service.get_categories_name_by_type(service.get_type_by_name('Transport')) == \
           ['Bus', 'Trolleybus', 'Minibus']
    assert service.get_categories_name_by_type(service.get_type_by_name('Bill')) == \
           ['Water', 'Electricity', 'Garbage', 'Heating', 'Gas', 'Major overhaul',
            'Management company', 'Simcard', 'Internet', 'Mobile banking']
    assert service.get_categories_name_by_type(service.get_type_by_name('Product')) == \
           ['Clothes', 'Footwear', 'Electronic devices', 'Games', 'Books', 'Learning']
    assert service.get_categories_name_by_type(service.get_type_by_name('Other')) == \
           ['Entertainment', 'Money transfer', 'Taxi', 'Other']


def test_get_categories_name_by_type_error():
    with pytest.raises(AttributeError):
        service.get_categories_name_by_type(service.get_category_by_name('Bus'))
        service.is_both_payment_type_accepted('')


def test_get_category_by_name():
    categories = ['Food', 'Drinking water', 'Bus', 'Trolleybus', 'Minibus',
                  'Water', 'Electricity', 'Garbage', 'Heating', 'Gas',
                  'Major overhaul', 'Management company', 'Simcard', 'Internet', 'Mobile banking',
                  'Clothes', 'Footwear', 'Electronic devices', 'Games', 'Books',
                  'Learning', 'Entertainment', 'Money transfer', 'Taxi', 'Other']
    for category in categories:
        assert service.get_category_by_name(category).name == category


def test_get_category_by_name_error():
    with pytest.raises(peewee.DoesNotExist):
        service.get_category_by_name('Error')
        service.get_category_by_name('')


def test_is_both_payment_type_accepted():
    assert service.is_both_payment_type_accepted(service.get_category_by_name('Food')) == True
    assert service.is_both_payment_type_accepted(service.get_category_by_name('Bus')) == False
    assert service.is_both_payment_type_accepted(service.get_category_by_name('Water')) == False


def test_is_both_payment_type_accepted_error():
    with pytest.raises(AttributeError):
        service.is_both_payment_type_accepted(service.get_type_by_name('Groceries'))
        service.is_both_payment_type_accepted('')

