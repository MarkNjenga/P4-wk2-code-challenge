from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', lazy=True)

    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []

        restaurant_dict = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
        }

        if 'restaurant_pizzas' not in exclude:
            restaurant_dict['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]

        return restaurant_dict
    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant')
    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', lazy=True)

    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []

        pizza_dict = {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
        }

        if 'restaurant_pizzas' not in exclude:
            pizza_dict['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]

        return pizza_dict
    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza')
    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    # add relationships
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    def __init__(self, price, pizza_id, restaurant_id):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30")
        self.price = price
        self.pizza_id = pizza_id
        self.restaurant_id = restaurant_id

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "pizza_id": self.pizza_id,
            "restaurant_id": self.restaurant_id,
        }

        
    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
