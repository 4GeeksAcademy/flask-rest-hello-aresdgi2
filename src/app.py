import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Galaxy, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# En princpio, esta API será usada con autentificacion. Vamos a emular que un usuario ya se ha identificado. 
current_logged_user_id = 1

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get users
@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

# get galaxies
@app.route('/galaxy', methods=['GET'])
def get_galaxies():
    galaxies = Galaxy.query.all()
    all_galaxies = list(map(lambda x: x.serialize(), galaxies))
    return jsonify(all_galaxies), 200

# get planets
@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

@app.route('/character', methods=['GET'])
def get_character():
    allCharacters = Character.query.all()
    result = [element.serialize() for element in allCharacters]
    return jsonify(result), 200

# add user
@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Invalid input"}), 400

    new_user = User(
        username=body['username'],
        email=body['email'],
        # agrega otros campos según sea necesario
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

# delete user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200

# add galaxy
@app.route('/galaxy', methods=['POST'])
def add_galaxy():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Invalid input"}), 400

    new_galaxy = Galaxy(
        name=body['name'],
        description=body['description'],
        # agrega otros campos según sea necesario
    )
    db.session.add(new_galaxy)
    db.session.commit()
    return jsonify(new_galaxy.serialize()), 201

# delete galaxy
@app.route('/galaxy/<int:galaxy_id>', methods=['DELETE'])
def delete_galaxy(galaxy_id):
    galaxy = Galaxy.query.get(galaxy_id)
    if not galaxy:
        return jsonify({"msg": "Galaxy not found"}), 404

    db.session.delete(galaxy)
    db.session.commit()
    return jsonify({"msg": "Galaxy deleted"}), 200

# add planet
@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Invalid input"}), 400

    new_planet = Planet(
        name=body['name'],
        description=body['description'],
        galaxy_id=body['galaxy_id']
        # agrega otros campos según sea necesario
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# delete planet
@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted"}), 200

# add character
@app.route('/character', methods=['POST'])
def add_character():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Invalid input"}), 400

    new_character = Character(
        name=body['name'],
        description=body['description'],
        planet_id=body['planet_id']
        # agrega otros campos según sea necesario
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

# delete character
@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404

    db.session.delete(character)
    db.session.commit()
    return jsonify({"msg": "Character deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
