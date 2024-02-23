import telebot

import buttons

import database

from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('6598637803:AAGYlyomaOv6uhSTk2oMCDF3sxt_kq3_-mA')

users = {}
database.add_product('apple', 10000, 10, 'Apple the best',
                     'https://www.google.com/imgres?imgurl=http%3A%2F%2F5.imimg.com%2Fdata5%2FSELLER%2FDefault%2F2021%2F8%2FYN%2FSE%2FFV%2F72826034%2Fred-apple.jpg&tbnid=878qQx8JxewCGM&vet=12ahUKEwjIsIujha-BAxVeDxAIHfMUBIwQMygPegQIARBv..i&imgrefurl=https%3A%2F%2Fwww.indiamart.com%2Fproddetail%2Fred-apple-23783955091.html&docid=Z5F3h01TLy1zaM&w=1805&h=1803&q=apple&ved=2ahUKEwjIsIujha-BAxVeDxAIHfMUBIwQMygPegQIARBv')


@bot.message_handler(commands=['start'])
def start_mybot(message):
    user_id = message.from_user.id
    print(user_id)
    # Проверка пользователя
    checker = database.check_user(user_id)

    # Если есть пользователь в базе
    if checker:
        # Получим актуальный список продуктов
        products = database.get_pr_name_id()

        # Отправляем сообщения с меню
        bot.send_message(user_id, 'Привет', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт', reply_markup=buttons.main_menu(products))

    elif not checker:
        bot.send_message(user_id, 'Привет отправь своё имя')
        # Переход на этап получении имени
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id

    username = message.text

    bot.send_message(user_id, 'Отправьте свой номер телефона', reply_markup=buttons.number_buttons())
    bot.register_next_step_handler(message, get_number, username)


# def get_number(message, name):
#     user_id = message.from_user.id
#
#     if message.contact:
#         phone_number = message.contact.phone_number
#
#         database.register_user(user_id, name, phone_number, status='Not yet')
#         bot.send_message(user_id, 'Вы успешно зарегистрировались', reply_markup=telebot.types.ReplyKeyboardRemove())
#
#         products = database.get_pr_name_id()
#         bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))
#
#     elif not message.contact:
#         bot.send_message(user_id, 'Оправьте контакт через кнопку', reply_markup=buttons.number_buttons())
#         bot.register_next_step_handler(message, get_number, name)

def get_number(message, name):
    user_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number

    else:
        return bot.send_message(user_id, 'Отправьте контакт')

    database.register_user(user_id, name, phone_number, status='Not yet')

    bot.send_message(user_id, 'Вы успешно зарегистрировались', reply_markup=telebot.types.ReplyKeyboardRemove())

    # products = database.get_pr_name_id()
    # bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))


# @bot.callback_query_handler(lambda call: call.data in ['plus', 'minus', 'to_cart', 'back'])
# def get_user_product_count(call):
#     user_id = call.message.chat.id
#
#     if call.data == 'plus':
#         actual_count = users[user_id]['pr_quantity']
#
#         users[user_id]['pr_quantity'] += 1
#
#         bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.chat.id,
#                                       reply_markup=buttons.choose_product_count('plus', actual_count))
#
#     elif call.data == 'minus':
#         actual_count = users[user_id]['pr_quantity']
#
#         users[user_id]['pr_quantity'] -= 1
#
#         bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.chat.id,
#                                       reply_markup=buttons.choose_product_count('minus', actual_count))
#
#     elif call.data == 'back':
#         products = database.get_pr_name_id()
#         bot.edit_message_text('Выберите пункт меню', user_id, call.message_id, reply_markup=buttons.main_menu(products))
#
#     elif call.data == 'to_cart':
#         product_count = users[user_id]['pr_quantity']
#         user_product = users[user_id]['pr_name']
#
#         database.add_product_to_cart(user_id, user_product, product_count)
#
#         products = database.get_pr_name_id()
#
#         bot.edit_message_text('Продукт добавлен в корзину\nЧто нибудь ещё?',
#                               user_id,
#                               call.message.message_id,
#                               reply_markup=buttons.main_menu(products))
#
#
# @bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'clear_cart'])
# def main_menu_user(call):
#     user_id = call.message.chat.id
#     message_id = call.message.message_id
#
#     if call.data == 'order':
#         bot.delete_message(user_id, message_id)
#
#         bot.send_message(user_id, 'Отправьте локацию', reply_markup=buttons.geo_button())
#
#         bot.register_next_step_handler(call.message)  # get_location)
#
#     elif call.data == 'cart':
#         user_cart = database.get_user_cart()
#
#         full_text = 'Ваша корзина:\n\n'
#
#         total_amount = 0
#
#         for i in user_cart:
#             full_text += f'{i[0]} x {i[1]} = {i[3]}\n'
#             total_amount += i[2]
#
#         full_text = f'\nИтог: {total_amount}'
#
#         bot.edit_message_text(full_text, user_id, message_id, reply_markup=buttons.get_cart_buttons())


def get_location(message, user_name, user_number):
    user_id = message.from_user.id

    if message.location:
        user_location = message.location
        bot.send_message(user_id, 'Напишите услугу', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_service, user_name, user_number, user_location)
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку')
        # Отправляем пользовательно обратно
        bot.register_next_step_handler(message, get_location, user_name, user_number)
#
#
# def get_service(message, user_name, user_number, user_location):
#     user_service = message.text
#     bot.send_message(user_id, 'Какие сроки?')
#     # Перенапавляем на этап получения срока
#     bot.register_next_step_handler(message, get_deadline, user_number, user_name, user_service, user_location)
#
#
# def get_deadline(message, user_number, user_name, user_service, user_location):
#     user_deadline = message.text
#     bot.send_message(-904313728, f'Новая заяка!\n\nИмя: {user_name}\n'
#                                  f'Номер: {user_number}\n'
#                                  f'Локация: {user_location}\n'
#                                  f'Услуга: {user_service}\n'
#                                  f'Срок: {user_deadline}\n')
#     bot.send_message(user_id, 'Успешно!')
#     bot.register_next_step_handler(message, start_mybot_text)


bot.infinity_polling()