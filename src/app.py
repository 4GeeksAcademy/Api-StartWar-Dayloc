"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Favorito

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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), 200

# Endpoint para crear un usuario
@app.route('/user', methods=['POST'])
def create_user():
    request_data = request.get_json()
    new_user = User(
        email=request_data.get('email'),
        password=request_data.get('password'),
        is_active=request_data.get('is_active', True)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

# Endpoint para obtener todos los personajes
@app.route('/personajes', methods=['GET'])
def get_people():
    people = Personaje.query.all()
    people_list = [person.serialize() for person in people]
    return jsonify(people_list), 200

# Endpoint para obtener todos los planetas
@app.route('/planetas', methods=['GET'])
def get_planets():
    planets = Planeta.query.all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200

# Endpoint para agregar un personaje a favoritos de un usuario
@app.route('/user/<int:user_id>/favoritos/personaje/<int:personaje_id>', methods=['POST'])
def add_favorite_personaje(user_id, personaje_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        raise APIException('Personaje not found', status_code=404)
    
    favorito = Favorito.query.filter_by(usuario_id=user_id, personaje_id=personaje_id).first()
    if favorito:
        return jsonify({'message': 'El personaje ya está en favoritos'}), 200

    new_favorito = Favorito(usuario_id=user_id, personaje_id=personaje_id)
    db.session.add(new_favorito)
    db.session.commit()

    return jsonify(new_favorito.serialize()), 201

# Endpoint para agregar un planeta a favoritos de un usuario
@app.route('/user/<int:user_id>/favoritos/planeta/<int:planeta_id>', methods=['POST'])
def add_favorite_planeta(user_id, planeta_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    
    planeta = Planeta.query.get(planeta_id)
    if not planeta:
        raise APIException('Planeta not found', status_code=404)
    
    favorito = Favorito.query.filter_by(usuario_id=user_id, planeta_id=planeta_id).first()
    if favorito:
        return jsonify({'message': 'El planeta ya está en favoritos'}), 200

    new_favorito = Favorito(usuario_id=user_id, planeta_id=planeta_id)
    db.session.add(new_favorito)
    db.session.commit()

    return jsonify(new_favorito.serialize()), 201

# Endpoint para obtener los favoritos de un usuario
@app.route('/user/<int:user_id>/favoritos', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    
    favoritos = Favorito.query.filter_by(usuario_id=user_id).all()
    favoritos_list = [favorito.serialize() for favorito in favoritos]
    return jsonify(favoritos_list), 200

# Punto de entrada para ejecutar la aplicación Flask
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
