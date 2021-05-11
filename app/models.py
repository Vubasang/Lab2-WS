import os
from hashlib import scrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_order = db.Column(db.String(30), nullable=False)
    #link_to_client = db.Column(db.String(30), nullable=False)
    text_order_definition = db.Column(db.String(30))
    delivery_address = db.Column(db.String(30))
    cost_order = db.Column(db.String(30))

    client = db.relationship('Client', backref='orders', lazy=True)
    link_to_client = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __str__(self):
        return self.number_order

    def to_dict_without_clients(self):
        return {'id': self.id, 'number_order': self.number_order, 'link_to_client': self.link_to_client,
                'text_order_definition': self.text_order_definition, 'delivery_address': self.delivery_address,
                'cost_order': self.cost_order}

    def to_dict(self):
        return {'id': self.id, 'number_order': self.number_order,'text_order_definition': self.text_order_definition,
                'delivery_address': self.delivery_address, 'cost_order': self.cost_order,
                'client': self.client.to_dict_without_orders()}


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_client = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.type_client

    def to_dict_without_orders(self):
        return {'id': self.id, 'type_client': self.type_client, 'customer_name': self.customer_name,
                'delivery_address': self.delivery_address, 'comment': self.comment}

    def to_dict(self):
        orders = []
        for s in self.orders:
            orders.append(s.to_dict_without_clients())
        return {'id': self.id, 'type_client': self.type_client, 'customer_name': self.customer_name,
                'delivery_address': self.delivery_address, 'comment': self.comment, 'orders': orders}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password_salt = db.Column(db.String(16), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    def hash_password(self, password: str):
        self.password_salt = os.urandom(16)
        self.password_hash = scrypt(password.encode('utf-8'), salt=self.password_salt, n=16384, r=8, p=1)

    def hash_verify(self, password: str):
        return self.password_hash == scrypt(password.encode('utf-8'), salt=self.password_salt, n=16384, r=8, p=1)