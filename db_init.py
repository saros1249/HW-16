# Файл с программой заполнения таблиц БД
import data
from utils import *

db.drop_all()

db.create_all()

for user in data.USERS:
    add_user(user)

for order in data.ORDERS:
    add_order(order)

for offer in data.OFFERS:
    add_offer(offer)
