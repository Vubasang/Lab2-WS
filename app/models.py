import os
from hashlib import scrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_order = db.Column(db.String(30), nullable=False)
    link_to_client = db.Column(db.String(30), nullable=False)
    text_order_definition = db.Column(db.String(30))
    delivery_address = db.Column(db.String(30))
    cost_order = db.Column(db.String(30))

    # def __str__(self):
    #     result = f'{self.last_name} {self.first_name:.1}.'
    #     if self.second_name:
    #         result += f'{self.second_name:.1}.'
    #     return result
    #
    # def to_dict(self):
    #     return {'id': self.id, 'last_name': self.last_name, 'first_name': self.first_name, 'second_name': self.second_name}
    def __str__(self):
        return self.number_order

    def to_dict(self):
        return {'id': self.id, 'number_order': self.number_order, 'link_to_client': self.link_to_client,
                'text_order_definition': self.text_order_definition, 'delivery_address': self.delivery_address,
                'cost_order': self.cost_order}


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_client = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.type_client

    def to_dict(self):
        return {'id': self.id, 'type_client': self.type_client, 'customer_name': self.customer_name,
                'delivery_address': self.delivery_address, 'comment': self.comment}


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
