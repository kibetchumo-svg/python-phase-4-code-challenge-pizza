from models import db, Restaurant, Pizza, RestaurantPizza
from app import app

print("Deleting data...")
with app.app_context():
    db.drop_all()
    db.create_all()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="address1")
    sanjay = Restaurant(name="Sanjay's Pizza", address="address2")
    kiki = Restaurant(name="Kiki's Pizza", address="address3")
    db.session.add_all([shack, sanjay, kiki])
    db.session.commit()

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    ricotta = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    db.session.add_all([cheese, pepperoni, ricotta])
    db.session.commit()

    print("Creating RestaurantPizza...")
    rp1 = RestaurantPizza(restaurant_id=shack.id, pizza_id=cheese.id, price=1)
    rp2 = RestaurantPizza(restaurant_id=sanjay.id, pizza_id=pepperoni.id, price=10)
    rp3 = RestaurantPizza(restaurant_id=kiki.id, pizza_id=ricotta.id, price=5)
    db.session.add_all([rp1, rp2, rp3])
    db.session.commit()

    print("Seeding done!")
