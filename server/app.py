from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()  # Gets all Heroes from db

    # Converts each hero to a dict but only includes the id, name and super_name then converts to json
    return jsonify(
        [hero.to_dict(only=("id", "name", "super_name")) for hero in heroes]
    ), 200  # Success status code


@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.filter_by(id=id).first()

    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict()), 200


@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify(
        [power.to_dict(only=("id", "name", "description")) for power in powers]
    ), 200


# Gets one power
@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.filter_by(id=id).first()

    if not power:
        return jsonify({"error": "Power not found"}), 404

    return jsonify(power.to_dict(only=("id", "name", "description"))), 200


@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.filter_by(id=id).first()

    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()

    try:
        # Update the description (validation will run automatically)
        power.description = data.get("description")
        db.session.commit()
        return jsonify(power.to_dict(only=("id", "name", "description"))), 200
    except ValueError as error:
        # If validation fails, return the error
        return jsonify({"errors": [str(error)]}), 400


@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()

    try:
        # Create the new HeroPower
        new_hero_power = HeroPower(
            strength=data.get("strength"),
            hero_id=data.get("hero_id"),
            power_id=data.get("power_id"),
        )

        db.session.add(new_hero_power)
        db.session.commit()

        # Return the new HeroPower with nested hero and power
        return jsonify(new_hero_power.to_dict()), 201

    except ValueError as e:
        # Validation errors (strength not valid)
        return jsonify({"errors": [str(e)]}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
