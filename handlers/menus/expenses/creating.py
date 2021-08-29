from typing import List
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from decimal import Decimal, ROUND_HALF_UP
from loader import dp
from .state import CreateExpense
from services.service import get_list_all_types, get_type_by_name, get_categories_name_by_type
from services.service import get_category_by_name, is_both_payment_type_accepted
from services.expense import ExpenseCreator
from handlers.default import send_welcome
# TODO: add Back handler and possibility to repeat step
# TODO: add tests


PAYMENT_TYPES = ['Card', 'Cash']


@dp.message_handler(Text(equals=['Add']))
async def start_add_expense(message: Message):
    answer_message = 'Choose type of expense: '
    await message.answer(answer_message, reply_markup=get_reply_keyboard_with_cancel_by(get_list_all_types()))
    await CreateExpense.waiting_for_type.set()


@dp.message_handler(Text(equals=['Cancel']), state='*')
async def cancel_add_expense(message: Message, state: FSMContext):
    answer_invalid_message = 'Expense adding was cancel. '
    await state.finish()
    await message.answer(answer_invalid_message)
    return await send_welcome(message)


@dp.message_handler(state=CreateExpense.waiting_for_type)
async def choose_type(message: Message, state: FSMContext):
    type_by_user = message.text
    if type_by_user in get_list_all_types():
        type_obj = get_type_by_name(type_by_user)

        async with state.proxy() as data:
            data['type'] = type_obj

        answer_message = 'Choose category of expense: '
        await message.answer(answer_message,
                             reply_markup=get_reply_keyboard_with_cancel_by(get_categories_name_by_type(type_obj)))
        await CreateExpense.waiting_for_category.set()
    else:
        answer_invalid_message = 'That category does not exist. Try again '
        return await message.answer(answer_invalid_message)


@dp.message_handler(state=CreateExpense.waiting_for_category)
async def choose_category_by_type(message: Message, state: FSMContext):
    category_name_by_user = message.text
    data = await state.get_data()
    type_obj = data.get('type')

    if category_name_by_user in get_categories_name_by_type(type_obj):
        category = get_category_by_name(category_name_by_user)
        async with state.proxy() as data:
            data['category'] = category

        if is_both_payment_type_accepted(category):
            answer_message = 'Choose type of payment: '
            await message.answer(answer_message, reply_markup=get_reply_keyboard_with_cancel_by(PAYMENT_TYPES))
            await CreateExpense.waiting_for_payment_type.set()
        else:
            async with state.proxy() as data:
                data['payment'] = category.accepted_payments_type
            await add_additional_info_if_needed(message, state)
    else:
        answer_invalid_message = 'That category does not exist. Try again '
        return await message.answer(answer_invalid_message)


async def add_additional_info_if_needed(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get('category')

    if category.is_additional_info_needed:
        answer_message = 'Write additional info about expense: '
        await message.answer(answer_message)
        await CreateExpense.waiting_for_additional_info.set()
    else:
        async with state.proxy() as data:
            data['additional_info'] = None
        await add_fixed_price_if_exist(message, state)


@dp.message_handler(state=CreateExpense.waiting_for_payment_type)
async def choose_payment_type(message: Message, state: FSMContext):
    payment_by_user = message.text
    if payment_by_user in PAYMENT_TYPES:
        async with state.proxy() as data:
            data['payment'] = payment_by_user
        await add_additional_info_if_needed(message, state)
    else:
        answer_invalid_message = 'Such type of payment is not accepted. Try again '
        return await message.answer(answer_invalid_message)


async def add_fixed_price_if_exist(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get('category')

    if category.fixed_price:
        decimal_fixed_price = Decimal(category.fixed_price).quantize(Decimal('1.11'), rounding=ROUND_HALF_UP)
        async with state.proxy() as data:
            data['amount'] = decimal_fixed_price
        await ask_confirmation(message, state)
    else:
        answer_message = 'Enter amount of expense: '
        await message.answer(answer_message)
        await CreateExpense.waiting_for_amount.set()


@dp.message_handler(state=CreateExpense.waiting_for_additional_info)
async def adding_additional_info(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['additional_info'] = message.text     # TODO: test if message.text is empty
    await add_fixed_price_if_exist(message, state)


async def ask_confirmation(message: Message, state: FSMContext):
    data = await state.get_data()
    answer_message = f"Do you want to add this expense?: \n" \
                     f"{data.get('amount')} \u20BD for '{data.get('category').name}' with {data.get('payment')}"
    reply_keyboard = ReplyKeyboardMarkup()
    reply_keyboard.row('Confirm', 'Cancel')
    await CreateExpense.waiting_for_confirm.set()
    await message.answer(answer_message, reply_markup=reply_keyboard)


@dp.message_handler(regexp='^\d+[,.]?\d*', state=CreateExpense.waiting_for_amount)
async def add_amount(message: Message, state: FSMContext):
    amount_by_user = message.text
    amount = Decimal(amount_by_user.replace(',', '.')).quantize(Decimal('1.11'), rounding=ROUND_HALF_UP)
    if amount > 0:
        async with state.proxy() as data:
            data['amount'] = amount
        await ask_confirmation(message, state)
    else:
        answer_invalid_message = 'Amount should be greater than 0.00. Try again '
        return await message.answer(answer_invalid_message)


@dp.message_handler(Text(equals=['Confirm']), state=CreateExpense.waiting_for_confirm)
async def finish_add_expense(message: Message, state: FSMContext):
    answer_message = ''
    data = await state.get_data()
    try:
        ExpenseCreator().create_expense_by_dict_if_valid(data)
    except Exception as e:
        print(e)
        answer_message = str(e) + '\nExpense adding was failure. Try again? '
    else:
        answer_message = 'Expense was added. Do you want add one more expense?'
    finally:
        await state.finish()
        reply_keyboard = ReplyKeyboardMarkup()
        reply_keyboard.row('Add', '/start')
        return await message.answer(answer_message, reply_markup=reply_keyboard)


def get_reply_keyboard_with_cancel_by(name_list: List[str]) -> ReplyKeyboardMarkup:
    reply_keyboard = ReplyKeyboardMarkup()
    for name in name_list:
        reply_keyboard.add(name)
    reply_keyboard.add('Cancel')
    return reply_keyboard
