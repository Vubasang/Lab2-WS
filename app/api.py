from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.models import db, Client, Order, User


# class UsersResource(Resource):
#     def post(self):
#         data = request.get_json()
#         user = User.query.filter_by(username=data['username']).first()
#         if user and user.hash_verify(data['password']):
#             token = ''  # TODO: create token
#             return {
#                 'success': True,
#                 'token': token
#             }
#         return {'success': False}

class ClientsResource(Resource):
    @jwt_required()
    def get(self):
        result = Client.query.all()
        return [b.to_dict() for b in result]

    def post(self):
        data = request.get_json()
        db.session.add(Client(type_client=data['type_client'], customer_name=data['customer_name'],
                              delivery_address=data['delivery_address'], comment=data['comment']))
        db.session.commit()
        return {'success': True}

class ClientResource(Resource):
    def get(self, client_id):
        client = Client.query.get_or_404(client_id)
        return client.to_dict()

    def put(self, client_id):
        data = request.get_json()
        client = Client.query.get(client_id)
        client.title = data.get('type_client')
        client.order = data.get('customer_name')
        client.title = data.get('delivery_address')
        client.title = data.get('comment')
        db.session.add(client)
        db.session.commit()
        return {'success': True}

    def delete(self, client_id):
        client = Client.query.get(client_id)
        db.session.delete(client)
        db.session.commit()
        return {'success': True}

class OrdersResource(Resource):
    @jwt_required()
    def get(self):
        result = Order.query.all()
        return [b.to_dict() for b in result]

    def post(self):
        data = request.get_json()
        db.session.add(Order(last_name=data['last_name'], first_name=data['first_name'], second_name=data['second_name']))
        db.session.commit()
        return {'success': True}

class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return order.to_dict()

    def put(self, order_id):
        data = request.get_json()
        order = Order.query.get(order_id)
        order.number_order = data.get('number_order')
        order.link_to_client = data.get('link_to_client')
        order.text_order_definition = data.get('text_order_definition')
        order.delivery_address = data.get('delivery_address')
        order.cost_order = data.get('cost_order')
        db.session.add(order)
        db.session.commit()
        return {'success': True}

    def delete(self, order_id):
        order = Order.query.get(order_id)
        db.session.delete(order)
        db.session.commit()
        return {'success': True}
