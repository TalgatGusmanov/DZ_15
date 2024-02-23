from telebot import types

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu(get_pr_name_id ):
    buttons = InlineKeyboardMarkup(row_width=2)

    order = InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    cart = InlineKeyboardButton(text='Корзина', callback_data='cart')

    all_products = [InlineKeyboardButton(text=f'{i[0]}', callback_data=i[1]) for i in get_pr_name_id]

    buttons.row(order)
    buttons.add(all_products)
    buttons.row(cart)

    return buttons


def choose_product_count(plus_or_minus='', current_amount=1):
    buttons = InlineKeyboardMarkup(row_width=3)

    plus = InlineKeyboardButton(text='+', callback_data='plus')
    minus = InlineKeyboardButton(text='-', callback_data='minus')
    count = InlineKeyboardButton(text=str(current_amount), callback_data=str(current_amount))
    add_to_cart = InlineKeyboardButton(text='Добавить в корзину', callback_data='to_cart')
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    if plus_or_minus == 'plus':
        new_amount = int(current_amount) + 1
        count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    elif plus_or_minus == 'minus':
        if int(current_amount) > 1:
            new_amount = int(current_amount) - 1
            count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    buttons.add(minus, count, plus)
    buttons.row(add_to_cart)
    buttons.row(back)

    return buttons

def get_cart_buttons():
    buttons = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton('Очистить корзину', callback_data='clear_cart')
    order = InlineKeyboardButton('Оформить заказ', callback_data='order')
    back = InlineKeyboardButton('Назад', callback_data='back')

    buttons.add(clear_cart, order, back)

    return buttons

def choice_buttons():
    # Создаем пространство для кнопок
    # row_width and resize_keyboard = check in home
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # добавляем кнопки
    service_button = types.KeyboardButton('Заказать услугу')

    buttons.add(service_button)

    return buttons


def number_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    num_button = types.KeyboardButton('Поделиться номером', request_contact=True)

    buttons.add(num_button)

    return buttons


def geo_button():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    g_button = types.KeyboardButton('Поделиться геолокацией', request_location=True)

    buttons.add(g_button)

    return buttons