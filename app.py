import datetime
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///date.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/')
def main_page():
    return 'Main PAGE'


@app.route('/users', methods=['GET', 'POST'])
def users():
    import utils
    from models import User
    if request.method == 'GET':
        all_user_list = []
        for user in User.query.all():
            all_user_list.append(user.to_dict())
        return jsonify(all_user_list)
    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            utils.add_user(user)
            return 'Новый пользователь создан.', 200
        except Exception as e:
            return e


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    from models import User
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user == None:
            return 'Отсутствует пользователь с введенным ID', 404
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user == None:
            return 'Отсутствует пользователь с введенным ID', 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f'Данные пользователя с ID {user_id} изменены и добавлены к БД', 200
    if request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user == None:
            return 'Отсутствует пользователь с введенным ID', 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f'Пользователь с ID {user_id} удалён.', 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    import utils
    from models import Order
    if request.method == 'GET':
        all_order_list = []
        for order in Order.query.all():
            all_order_list.append(order.to_dict())
        return jsonify(all_order_list)
    if request.method == 'POST':
        try:
            order = json.load(request.data)
            utils.add_order(order)
            return 'Новый заказ создан.', 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    from models import Order
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order == None:
            return 'Отсутствует заказ с введенными данными'
        return jsonify(order.to_dict())
    if request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        month_start, day_start, year_start = [int(_) for _ in order_data['start_date'].split('/')]
        month_end, day_end, year_end = [int(_) for _ in order_data['end_date'].split('/')]
        if order == None:
            return 'Отсутствует заказ с введенным номером', 404
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.date(year=year_end, month=month_end, day=day_end)
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f'Данные заказа №{order_id} изменены.', 200
    if request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order == None:
            return 'Отсутствует заказ с введенным номером.', 404
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f'Заказ №{order_id} удалён из БД', 200


@app.route('/offers', methods=['GET', 'POST'])
def offer():
    import utils
    from models import Offer
    if request.method == 'GET':
        all_offer_list = []
        for offer in Offer.query.all():
            all_offer_list.append(offer.to_dict())
        return jsonify(all_offer_list)
    if request.method == 'POST':
        try:
            offer = json.load(request.data)
            utils.add_offer(offer)
            return 'Новое предложение создано', 200
        except Exception as e:
            return e


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    from models import Offer
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer == None:
            return 'Данные не найдены'
        return jsonify(offer.to_dict())
    if request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer == None:
            return 'Отсутствует предложение с введенным номером', 404
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f'Данные предложения с №{offer_id} изменены и добавлены к БД', 200
    if request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer == None:
            return 'Отсутствует предложение с введенным номером', 404
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f'Предложение с №{offer_id} удалёно', 200


if __name__ == '__main__':
    app.run()
