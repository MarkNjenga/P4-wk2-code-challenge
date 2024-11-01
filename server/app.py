#!/usr/bin/env python3
from sqlalchemy.orm import Session
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurant_dicts = [r.to_dict(exclude=['restaurant_pizzas']) for r in restaurants]

        return make_response(jsonify(restaurant_dicts), 200)
api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            return make_response(jsonify(restaurant.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()  
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

api.add_resource(RestaurantByID, '/restaurants/<int:id>')
class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_dicts = [p.to_dict(exclude=['restaurant_pizzas']) for p in pizzas]

        return make_response(jsonify(pizza_dicts), 200)

api.add_resource(Pizzas, '/pizzas')
class RestaurantByID(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            return make_response(jsonify(restaurant.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()  
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        if not 1 <= data.get('price', 0) <= 30:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)

        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        pizza = db.session.get(Pizza, pizza_id)
        restaurant = db.session.get(Restaurant, restaurant_id)

        if pizza and restaurant:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=pizza_id,
                restaurant_id=restaurant_id
            )
            db.session.add(restaurant_pizza)
            db.session.commit()

            response_data = {
                "id": restaurant_pizza.id,
                "pizza": pizza.to_dict(),
                "pizza_id": pizza_id,
                "price": restaurant_pizza.price,
                "restaurant": restaurant.to_dict(),
                "restaurant_id": restaurant_id
            }
            return make_response(jsonify(response_data), 201)
        else:
            return make_response(jsonify({"errors": ["Invalid pizza or restaurant ID"]}), 400)

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
