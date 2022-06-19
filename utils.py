# Функции для внесения данных в таблицы БД
import datetime
from models import *

def add_user(user):
    """
    Добавляет строку в таблицу User
    :param user: Список
    :return: Строка в таблице
    """
    db.session.add(User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    ))
    db.session.commit()
    db.session.close()


def add_order(order):
    """
    Добавляет строку в таблицу Order
    :param order: Список
    :return: Строка в таблице
    """
    month_start, day_start, year_start = [int(_) for _ in order['start_date'].split('/')]
    month_end, day_end, year_end = [int(_) for _ in order['end_date'].split('/')]
    db.session.add(Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=datetime.date(year=year_start, month=month_start, day=day_start),
        end_date=datetime.date(year=year_end, month=month_end, day=day_end),
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    ))
    db.session.commit()
    db.session.close()


def add_offer(offer):
    """
    Добавляет строку в таблицу Offer
    :param offer: Список
    :return: Строка в таблице
    """
    db.session.add(Offer(
    id=offer['id'],
    order_id=offer['order_id'],
    executor_id=offer['executor_id']
    ))
    db.session.commit()
    db.session.close()
