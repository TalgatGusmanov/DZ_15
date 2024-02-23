import sqlite3

from datetime import datetime

db = sqlite3.connect('delivery.db')

fake_evos = db.cursor()

fake_evos.execute('CREATE TABLE IF NOT EXISTS users'
                  '(tg_id INTEGER, name TEXT, phone INTEGER, address TEXT, reg_date DATETIME)')


fake_evos.execute('CREATE TABLE IF NOT EXISTS '
                  'products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT,'
                  'pr_price REAL, pr_quantity INTEGER, pr_des TEXT, pr_photo TEXT,'
                  'reg_date DATETIME);')

fake_evos.execute('CREATE TABLE IF NOT EXISTS user_cart'
                  '(user_id INTEGER, user_product TEXT, quantity INTEGER, total_for_product REAL)')


def register_user(tg_id, name, phone, address):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    fake_evos.execute('INSERT INTO user'
                      '(tg_id, name, phone, address, reg_date) VALUES'
                      '(?, ?, ?, ?, ?, ?);', (tg_id, name, phone, address, datetime.now()))

    db.commit()


def check_user(user_id):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    checker = fake_evos.execute('SELECT tg_id FROM users WHERE tg_id=?', (user_id,))

    if checker.fetchone():
        return True
    else:
        return False


def add_product(pr_name, pr_price, pr_quantity, pr_des, pr_photo):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    fake_evos.execute('INSERT INTO products '
                      '(pr_name, pr_price, pr_quantity, pr_des, pr_photo, reg_date) VALUES'
                      '(?, ?, ?, ?, ?, ?);', (pr_name, pr_price, pr_quantity, pr_des, pr_photo, datetime.now()))

    db.commit()

def get_pr_name_id():
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    products = fake_evos.execute('SELECT pr_name, pr_id, pr_quantity FROM products').fetchall()

    sorted_products = [(i[0], i[1]) for i in products if i[2] > 0]

    return sorted_products

def get_product_id(pr_id):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    product_id = fake_evos.execute('SELECT pr_name, pr_des, pr_photo, pr_price'
                                   'FROM products WHERE pr_id=?', (pr_id,)).fetchone()

    return product_id

def add_product_to_cart(user_id, user_product, quantity):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    product_price = get_product_id(user_product)[2]

    fake_evos.execute('INSERT INTO user_cart'
               '(user_id, user_product, quantity, total_for_product) VALUES'
               '(?, ?, ?, ?);', (user_id, user_product, quantity, quantity * product_price))

def remove_product_from_cart(pr_id):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    fake_evos.execute('DELETE FROM user_cart WHERE user_product=?;', (pr_id,))

def get_user_cart(user_id):
    db = sqlite3.connect('delivery.db')

    fake_evos = db.cursor()

    user_cart = fake_evos.execute('SELECT products.pr_name, user_cart.quantity, user_cart.total_for_price'
                           'INNER JOIN products ON products.pr_id = user_cart.user_products, '
                           'FROM user cart WHERE user_id=?;', (user_id,)).fetchall()

    return user_cart