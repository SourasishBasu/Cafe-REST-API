from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Records
@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    all_cafes = {}
    for cafe in cafes:
        cafe_eg = {"can_take_calls": cafe.can_take_calls, "coffee_price": cafe.coffee_price, "has_sockets": cafe.has_sockets,
              "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_toilet, "id": cafe.id, "img_url": cafe.img_url,
              "location": cafe.location, "map_url": cafe.map_url, "seats": cafe.seats }
        all_cafes[cafe.name] = cafe_eg

    return jsonify(all_cafes)


@app.route("/search")
def search_cafe():
    cafes = Cafe.query.filter_by(location=request.args.get("loc")).all()
    all_cafes = {}
    if not cafes:
        return jsonify({"error": {"Not Found": "Sorry, we don't have a cafe at that location"}}), 404
    else:
        for cafe in cafes:
            cafe_eg = {"can_take_calls": cafe.can_take_calls, "coffee_price": cafe.coffee_price,
                       "has_sockets": cafe.has_sockets,
                       "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_toilet, "id": cafe.id, "img_url": cafe.img_url,
                       "location": cafe.location, "map_url": cafe.map_url, "seats": cafe.seats}
            all_cafes[cafe.name] = cafe_eg

        return jsonify(all_cafes)


@app.route("/random")
def get_random_cafe():
    rand_id = random.randint(1,21) 
    cafe = Cafe.query.get(rand_id)
    return jsonify(cafe={"can_take_calls": cafe.can_take_calls, "coffee_price":cafe.coffee_price, "has_sockets":cafe.has_sockets,
                         "has_toilet":cafe.has_toilet, "has_wifi":cafe.has_toilet, "id":cafe.id, "img_url":cafe.img_url,
                         "location":cafe.location, "map_url":cafe.map_url, "name":cafe.name, "seats":cafe.seats,})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def create_record():
    if request.method == "POST":
        new_cafe = Cafe(name=request.form["name"], map_url=request.form["map_url"], img_url=request.form["img_url"],
                        location=request.form["location"], has_sockets=bool(request.form["has_sockets"]),
                        seats=request.form["seats"], has_wifi=bool(request.form["has_wifi"]),
                        has_toilet=bool(request.form["has_toilet"]), can_take_calls=bool(request.form["can_take_calls"]),
                        coffee_price=request.form["coffee_price"])
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify({"response": {"Success": "Successfully added the new cafe"}})


# HTTP PATCH - Update Record
@app.route("/update/<cafe_id>", methods=["PATCH"])
def change_data(cafe_id):
    new_price = request.args.get("new_price")
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify({"success": "Successfully updated the price."}), 200
    else:

        return jsonify({"error": {"Not Found": "Sorry a cafe with that ID was not found in the Cafe database"}}), 404 # Return custom error code


# HTTP DELETE - Delete Record
@app.route("/delete/<cafe_id>", methods=["DELETE"])
def del_cafe(cafe_id):
    if request.args.get("key") == "valid_key": # Change secret API key for validation during DELETE operation here
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify({"success": "Successfully deleted the cafe details."}), 200
        else:
            return jsonify({"error": {"Not Found": "Sorry a cafe with that ID was not found in the Cafe database"}}), 404
    else:
        return jsonify({"error": "Sorry you are not allowed to perform this operation"}), 403


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000) # Change port here
