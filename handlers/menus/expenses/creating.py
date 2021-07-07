from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from decimal import *
from .state import CreateExpense
from services.service import get_list_all_types, get_type_id_by_type_name, get_categories_name_by_type_id
from services.service import get_type_name_by_id, get_fixed_price_categories_name, get_category_id_by_category_name
from services.service import get_category_price_by_id, get_today_now
from services.service import is_card_accepted, is_cash_accepted, is_additional_info_needed
from services.expense import insert_expense
from utils.exceptions import CategoryDoesNotExist
# TODO: add Back handler and possibility to repeat step


@dp.message_handler(Text(equals=['Add']))
async def start_add_expense(message: Message):
    answer_message = 'Choose type of expense: '

    reply_keyboard = ReplyKeyboardMarkup()
    for name in get_list_all_types():
        reply_keyboard.add(name)
    reply_keyboard.row('Cancel')
    await message.answer(answer_message, reply_markup=reply_keyboard)
    await CreateExpense.waiting_for_type.set()


@dp.message_handler(Text(equals=['Cancel']), state='*')
async def cancel_add_expense(message: Message, state: FSMContext):
    pass


@dp.message_handler(state=CreateExpense.waiting_for_start)
async def start_attempt_from_confirmation(message: Message):
    answer_message = 'Choose type of expense: '

    reply_keyboard = ReplyKeyboardMarkup()
    for name in get_list_all_types():
        reply_keyboard.add(name)
    reply_keyboard.row('Cancel')
    await message.answer(answer_message, reply_markup=reply_keyboard)
    await CreateExpense.waiting_for_type.set()


@dp.message_handler(state=CreateExpense.waiting_for_type)
async def choose_type(message: Message, state: FSMContext):
    user_type = message.text
    if user_type in get_list_all_types():
        type_id = get_type_id_by_type_name(user_type)
        types_categories_list = get_categories_name_by_type_id(type_id)

        async with state.proxy() as data:
            data['type'] = user_type
            data['type_id'] = type_id

        answer_message = 'Choose category of expense: '
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for name in types_categories_list:
            reply_keyboard.add(name)
        reply_keyboard.add('Cancel')

        await message.answer(answer_message, reply_markup=reply_keyboard)
        await CreateExpense.waiting_for_category.set()
    else:
        answer_invalid_message = 'That category does not exist. Try again '
        await message.answer(answer_invalid_message)
        return


@dp.message_handler(state=CreateExpense.waiting_for_category)
async def choose_category_by_type(message: Message, state: FSMContext):
    user_category = message.text.strip()        # TODO: test without strip
    data = await state.get_data()
    type_id = data.get('type_id')
    types_categories = get_categories_name_by_type_id(type_id)
    if user_category in types_categories:
        async with state.proxy() as data:
            data['category'] = user_category

        if is_card_accepted(user_category) and not is_cash_accepted(user_category):
            # Only Card
            async with state.proxy() as data:
                data['payment'] = 'card'

            answer_message = f"Category '{user_category}' accept only Card payment."
            await message.answer(answer_message)
            # TODO: Inner async func to skip step if category accept only one type of payment.

        elif not is_card_accepted(user_category) and is_cash_accepted(user_category):
            # Only Cash
            async with state.proxy() as data:
                data['payment'] = 'cash'

            answer_message = f"Category '{user_category}' accept only Cash payment."
            await message.answer(answer_message)
            # TODO: Inner async func to skip step if category accept only one type of payment.

        elif is_card_accepted(user_category) and is_cash_accepted(user_category):
            # Both

            answer_message = 'Choose type of payment: '
            reply_keyboard = ReplyKeyboardMarkup()
            reply_keyboard.row('Card', 'Cash')
            reply_keyboard.add('Cancel')
            await message.answer(answer_message, reply_markup=reply_keyboard)
            await CreateExpense.waiting_for_payment_type.set()
        else:
            raise CategoryDoesNotExist()
    else:
        answer_invalid_message = 'That category does not exist. Try again '
        await message.answer(answer_invalid_message)
        return


@dp.message_handler(state=CreateExpense.waiting_for_payment_type)
async def choose_payment_type(message: Message, state: FSMContext):
    user_payment = message.text
    if user_payment in ['Card', 'Cash']:
        if user_payment == 'Card':
            async with state.proxy() as data:
                data['payment'] = 'card'

        elif user_payment == 'Cash':
            async with state.proxy() as data:
                data['payment'] = 'cash'
        else:
            raise CategoryDoesNotExist('That payment does not exist.')

        data = await state.get_data()
        category_name = data.get('category')
        if is_additional_info_needed(category_name):
            answer_message = 'Write additional info about expense: '
            await message.answer(answer_message)
            await CreateExpense.waiting_for_additional_info.set()
        else:
            async with state.proxy() as data:   # Maybe needy to be deleted, check existing additional_info
                data['additional_info'] = ''

            # TODO: Inner async func to skip step if category accept only one type of payment.

    else:
        answer_invalid_message = 'Such type of payment is not accepted. Try again '
        await message.answer(answer_invalid_message)
        return


@dp.message_handler(state=CreateExpense.waiting_for_additional_info)
async def adding_additional_info(message: Message, state: FSMContext):
    user_additional_info = message.text     # TODO: test if message.text is empty

    async with state.proxy() as data:
        data['additional_info'] = user_additional_info

    data = await state.get_data()
    category_name = data.get('category')

    if category_name in get_fixed_price_categories_name():
        category_id = get_category_id_by_category_name(category_name)
        fixed_price = get_category_price_by_id(category_id)
        decimal_fixed_price = Decimal(fixed_price).quantize(Decimal('1.11'), rounding=ROUND_HALF_UP)
        async with state.proxy() as data:
            data['amount'] = decimal_fixed_price

        answer_message = f"Category has fixed price: {decimal_fixed_price} \u20BD. "
        await message.answer(answer_message)
        # TODO: inner func to skip step

    else:
        answer_message = 'Enter amount of expense: '
        reply_keyboard = ReplyKeyboardMarkup()
        reply_keyboard.add('Cancel')

        await message.answer(answer_message, reply_markup=reply_keyboard)
        await CreateExpense.waiting_for_amount.set()


@dp.message_handler(regexp='^\d+[,.]?\d*', state=CreateExpense.waiting_for_amount)
async def add_amount(message: Message, state: FSMContext):
    user_amount = message.text
    amount = Decimal(user_amount.replace(',', '.')).quantize(Decimal('1.11'), rounding=ROUND_HALF_UP)
    if amount <= 0:
        answer_invalid_message = 'Amount should be greater than 0.00. Try again '
        await message.answer(answer_invalid_message)
        return
    else:
        async with state.proxy() as data:
            data['amount'] = amount

        if await _validate_data(message=message, state=state):
            await CreateExpense.waiting_for_confirm.set()

        data = await state.get_data()
        answer_message = f"Do you want to add this expense?: \n" \
                         f"{data.get('amount')} \u20BD for '{data.get('category')}' with {data.get('payment')}"
        reply_keyboard = ReplyKeyboardMarkup()
        reply_keyboard.row('Confirm', 'Cancel')
        await message.answer(answer_message, reply_markup=reply_keyboard)


@dp.message_handler(state=CreateExpense.waiting_for_amount)
async def add_amount_invalid(message: Message, state: FSMContext):
    answer_message = 'Amount may consist only positive digits. Try again '
    return await message.answer(answer_message)


@dp.message_handler(Text(equals=['Confirm']), state=CreateExpense.waiting_for_confirm)
async def finish_add_expense(message: Message, state: FSMContext):
    data = await state.get_data()
    type_name = data.get('type')
    category_name = data.get('category')
    payment = data.get('payment')
    additional_info = data.get('additional_info')
    amount = data.get('amount')
    raw_message = ' '.join([str(amount), type_name, category_name,  payment, additional_info])

    insert_expense(amount=amount,
                   date=get_today_now(),
                   category_id=get_category_id_by_category_name(category_name),
                   payment=payment,
                   add_info=additional_info,
                   raw_text=raw_message)

    await state.finish()
    answer_message = 'Expense was added. ' \
                     'Do you want add one more expense?'
    reply_keyboard = ReplyKeyboardMarkup()
    reply_keyboard.row('Add', '/start')
    return await message.answer(answer_message, reply_markup=reply_keyboard)


async def _validate_data(message: Message, state: FSMContext) -> bool:
    data = await state.get_data()
    type_id = data.get('type_id')
    type_name = data.get('type')
    category_name = data.get('category')
    payment = data.get('payment')
    additional_info = data.get('additional_info')
    amount = data.get('amount')
    # TODO: add states in checks

    result = True
    if type_name == get_type_name_by_id(type_id):
        pass
    else:
        answer_invalid_message = 'Type does not exist. VALIDATING ERROR'
        result = False
        await message.answer(answer_invalid_message)

    if category_name in get_categories_name_by_type_id(type_id):
        pass
    else:
        answer_invalid_message = 'Category does not exist. VALIDATING ERROR'
        result = False
        await message.answer(answer_invalid_message)

    if payment == 'card' and is_card_accepted(category_name):
        pass
    elif payment == 'cash' and is_cash_accepted(category_name):
        pass
    else:
        answer_invalid_message = 'This payment type is unavailable for category. VALIDATING ERROR'
        result = False
        await message.answer(answer_invalid_message)

    if is_additional_info_needed(category_name) and not additional_info:
        answer_invalid_message = 'You should write additional info about expense. VALIDATING ERROR'
        result = False
        await message.answer(answer_invalid_message)

    if amount <= 0:
        answer_invalid_message = 'Amount should be greater than 0.00. VALIDATING ERROR'
        result = False
        await message.answer(answer_invalid_message)

    return result
