from flask import Flask, jsonify, request
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# ------------------ RESTAURANTS ------------------

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify(
        [r.to_dict(only=("id", "name", "address")) for r in restaurants]
    ), 200


@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "restaurant_pizzas": [
            {
                "id": rp.id,
                "price": rp.price,
                "pizza_id": rp.pizza.id,
                "pizza": {
                    "id": rp.pizza.id,
                    "name": rp.pizza.name,
                    "ingredients": rp.pizza.ingredients
                }
            }
            for rp in restaurant.restaurant_pizzas
        ]
    }

    return jsonify(data), 200


@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()
    return "", 204


# ------------------ PIZZAS ------------------

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify(
        [p.to_dict(only=("id", "name", "ingredients")) for p in pizzas]
    ), 200


# ------------------ RESTAURANT PIZZAS ------------------

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        restaurant_pizza = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        response = {
            "id": restaurant_pizza.id,
            "price": restaurant_pizza.price,
            "restaurant_id": restaurant_pizza.restaurant.id,
            "restaurant": restaurant_pizza.restaurant.to_dict(
                only=("id", "name", "address")
            ),
            "pizza_id": restaurant_pizza.pizza.id,
            "pizza": restaurant_pizza.pizza.to_dict(
                only=("id", "name", "ingredients")
            )
        }

        return jsonify(response), 201

    except:
        return jsonify({"errors": ["validation errors"]}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
