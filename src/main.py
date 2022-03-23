"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from ast import Return
import json
from operator import and_
import os
from traceback import print_last
from urllib.parse import uses_relative
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Card,Planet,Vehicles,Favorite,Character
from flask_migrate import Migrate
import requests
from sqlalchemy.sql import exists 


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
BASE_URL = "https://www.swapi.tech/api/"

# Handle/serialize errors like a JSON o
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code  #, error.status_code
    # generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)
# @app.route('/user', methods=['GET'])
# def handle_hello():

    # response_body = {
        # "msg": "Hello, this is your G
    # }

#    return jsonify(response_body), 200
@app.route('/starships/', methods=['GET'])
def get_all_starships():
    vehicles = Vehicles.query.all()
    return jsonify(list(map(
        lambda planet: planet.serialize(), vehicles))), 200

@app.route('/starships/<int:position>', methods=['GET'])
def get_all_startship(position):
    starship = Vehicles.query.get(position)
    if starship is None:
        return jsonify({
            "msg": "not found"
        }), 404
    ##one_person=[]
    ##one_person.append(character.serialize())
    ##return jsonify(one_person)  #'something'
    return jsonify(starship.serialize()), 200
###****************************************************************
@app.route('/planets/', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify(list(map(
        lambda planet: planet.serialize(), planets))), 200
            
 
@app.route('/planet/<int:position>', methods=['GET'])
def get_one_planet(position):
    planet = Planet.query.get(position)
    if planet is None:
        return jsonify({
            "msg": "not found"
        }), 404
    ##one_person=[]
    ##one_person.append(character.serialize())
    ##return jsonify(one_person)  #'something'
    return jsonify(planet.serialize()), 200
##********************************************************************
@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    character = Character.query.get(id)
    if character is None:
        return jsonify({
            "msg": "not found"
        }), 404
    ##one_person=[]
    ##one_person.append(character.serialize())
    ##return jsonify(one_person)  #'something'
    return jsonify(character.serialize()), 200

@app.route('/characters_all', methods=['GET'])
def get_all_chacters():
    all_planets = Character.query.all()
    dict_planets=[]
    ##for x in all_planets:
    ##    dict_planets.append(x.serialize())
    ##return jsonify(dict_planets)
    dict_planets = list(map(lambda x: x.serialize(), all_planets))
    
    return jsonify(dict_planets)

##**********************************************************************
@app.route('/user', methods=['GET'])
def get_all_user():
    all_users = User.query.all()
    return jsonify(list(map(lambda user: user.serialize(), all_users))), 200

    # all_users = User.query.all()
    # dict_users=[]
    # ##@for x in all_user:
    # ##    dict_users.append(x.serialize())
    # dict_users = list(map(lambda x: x.serialize(), all_users))
    # #json_text=jsonify(dict_users)
    # return jsonify(dict_users)
    
    
    


@app.route('/user', methods=['POST'])
def add_one_user():
     dictionary={}
     body = request.json
     decoded_object = json.loads(request.data)
     user = User.create(
         email=body["email"],
         password=body["password"],
         is_active= body["is_active"],
         name=body["name"],
         nick_name = body["nick_name"] 
        )
     
     dictionary = user.serialize()
     ##return jsonify(decoded_object), 201
     return jsonify(dictionary), 201

@app.route('/user/<int:id1>', methods=['DELETE'])
def delete_one_user(id1):
    #user = User.query.filter_by(id=id1).first()
    ##user = User.query.get(id1)
    ##peter = User.query.filter_by(username='peter').first()
    #User.query.filter(User.email.endswith('@example.com')).all()
    # User.query.order_by(User.username).all()
    #User.query.limit(1).all()
    # User.query.get(1)
    
    user = User.query.get_or_404(id1)
    db.session.delete(user)
    db.session.commit()
    #return '',204 
    return jsonify({"msg": f"user id:{id1} has been deleted succesfully"}), 204
       
                        
##///****************************************************************************


@app.route('/registro_usuario/', methods=['POST'])
def add_one_favorite():
     dictionary={}
     body = request.json
     decoded_object = json.loads(request.data)
     user_id=body["user_id"],
     exists = db.session.query(User.id).filter_by(id=User.id).first() is not None 
     if exists:
        return jsonify({"msg":f"The id:{user_id} already exist in database, please add another id"})
     else:
         favorite = Favorite.create(
             user_id=body["user_id"],
             card_id=body["card_id"]
             )
             
     dictionary = favorite.serialize()
     ##return jsonify(decoded_object), 201
     
     return jsonify(dictionary), 201       
    
@app.route('/Favorite', methods=['GET'])
def get_all_favorite():
    all_favorites = Favorite.query.all()
    dict_favorite=[]
    ##@for x in all_user:
    ##    dict_users.append(x.serialize())
    dict_favorite = list(map(lambda x: x.serialize(), all_favorites))
    json_text=jsonify(dict_favorite)
    
    return json_text


@app.route('/Favorite/user_id/<id>', methods=['GET'])
def get_user_favorite(id):
    ###all_favorite_user = Favorite.query.all(user_id)
     #User.query.filter(User.email.endswith('@example.com')).all()
    all_favorite_user=Favorite.query.filter(Favorite.user_id==id).all()
    ##User.query.filter(User.addresses.any(address=address)) # Returns all users who have a particular address listed as one of their addresses
    ##all_favorite_card = Favorite.query.all(card_id)
    dic_favorite_user=[]
    dic_favorite_card=[]
    for x in all_favorite_user:
        dic_favorite_user.append(x.serialize())
        #dic_favorite_card.append(x.serializa())
    json_text=jsonify(dic_favorite_user)
    ##dic_favorite_user = list(map(lambda x: x.serialize(), all_favorite_card))

    return json_text    

app.route('favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_favorite_planet():
    if request.is_json:
        #request_body = request.get_json()
        #user_id=request.json['user_id']
        #user_id=request.json['card_id']
        #new_favorite=Favorite(user_id,card_id)
        #db.session.add(new_favorite)
        #b.session.commit()
        dictionary={}
        request_body = request.json
        new_planet_favorite=Favorite.create(
            user_id=request_body['user_id'], 
            card_id=request_body['card_id']
            )
        dictionary = Favorite.serialize()
        return jsonify(dictionary), 201
    else:
        return jsonify({"msg": f"Please check your data entry format"})     
       
   
        
###777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777
@app.route('/delete_favorite/<int:user_id1>/<int:planet_id>', methods=['DELETE'])
def deletefavorite(user_id1,planet_id):
    ##existing = User.query.join(User.spaces).filter(User.username=='Bob', Space.name=='Mainspace').first()
    existing = User.query.filter(Favorite.user_id==user_id1, Favorite.card_id==planet_id).first()
    print(existing.user_id)
    if existing != None:
        print('Exists')


 ###27.0.0.1:3000/delete_favorite_planet_to_active_user?favorite=user_id&planet=planet_id
##def deletefavorite():
     ##@RequestMapping(method = RequestMethod.GET, value = "/custom")
    # def delete_favorite_planet():
    #  ##user_forite_planet_data=Favorite.query.filter(Favorite.user_id==user_id).get_or_404(planet_id)
    ######user_forite_planet_data=Favorite.query.filter(Favorite.user_id==planet_id)
    # return jsonify(user_forite_planet_data)
    # if user_forite_planet_data is None:
        # return jsonify({
        # "msg": "not found"
        # }), 404
        # ##one_person=[]
    # #data = request.query.get_or_404(planet_id)
    # db.session.delete(user_forite_planet_data)
    # db.session.commit()
    



######*****************************************************************************************
@app.route('/Cards', methods=['GET'])
def get_all_cards():
    all_cards = Card.query.all()
    dict_cards=[]
    ##@for x in all_user:
    ##    dict_users.append(x.serialize())
    dict_cards = list(map(lambda x: x.serialize(), all_cards))
    json_text=jsonify(dict_cards)
    
    return json_text

#####******************************************************************************************
@app.route('/characters', methods=["GET", "POST"])
def handle_characters():
    if request.method == "GET":
        characters = Character.query.all()
        return jsonify(list(map(
            lambda character: character.shortalize(),
            characters
        ))), 200
    else:
        body = request.json
        character = Character.create(
            name=body["name"],
            eye_color=body['eye_color'],
            skin_color= body['skin_color'],           
            birth_year=body["birth_year"],
            gender= body["gender"],
            mass=body["mass"],
            height=body["height"],
            hair_color = body["hair_color"],
            homeworld=body["homeworld"],
            url=body["url"] 
            
        )
        dictionary = character.serialize()
        return jsonify(dictionary), 201



@app.route('/populate-characters', methods=["POST"])
def populate_characters():

    # solicitud de todos los characters
    response = requests.get(
        f"{BASE_URL}{'people'}/?page=1&limit=10"  #/?page=1&limit=10
    )

    # cuerpo de esa solicitud con results que es
    # una lista de characters con data resumida
    body = response.json()
    all_characters = []
    
    # ciclo a traves de la lista body['results']
    # donde cada result es un diccionario resumido
    # de un character, segun swapi
    for result in body['results']:
        
        # solicitud del detalle del character result
        response = requests.get(result['url'])
        body = response.json()

        # agregamos a la lista las propiedades de este
        # character
        all_characters.append(body['result']['properties'])
    
    instances = []
    
    # recorremos la lista all_characters que son
    # diccionarios de propiedades de cada personaje
    for character in all_characters:
        
        # creamos la instancia y se guarda en bdd
        instance = Character.create(character)

        # agregamos el OBJETO character a la lista
        instances.append(instance)

    # mapeamos la lista instances para obtener una lista
    # de diccionarios que represente a cada objeto
    # character; convertimos el objeto map en una lista
    # y jsonificamos y devolvemos el resultado
    return jsonify(list(map(
        lambda inst: inst.serialize(),
        instances
    ))), 200

@app.route('/populate-planets', methods=["POST"])
def populate_planets():

    # solicitud de todos los characters
    response = requests.get(
        f"{BASE_URL}{'planets'}/?page=1&limit=10"  #/?page=1&limit=10
    )

    body = response.json()
    all_planets = []
    
    # ciclo a traves de la lista body['results']
    # donde cada result es un diccionario resumido
    # de un character, segun swapi
    for result in body['results']:
        # solicitud del detalle del character result
        response = requests.get(result['url'])
        body = response.json()
        # agregamos a la lista las propiedades de este
        # character
        all_planets.append(body['result']['properties'])
    
    instances = []
    
    # recorremos la lista all_characters que son
    # diccionarios de propiedades de cada personaje
    for planet in all_planets:
        
        # creamos la instancia y se guarda en bdd
        instance = Planet.create(planet)

        # agregamos el OBJETO character a la lista
        instances.append(instance)

    # mapeamos la lista instances para obtener una lista
    # de diccionarios que represente a cada objeto
    # character; convertimos el objeto map en una lista
    # y jsonificamos y devolvemos el resultado
    return jsonify(list(map(
        lambda inst: inst.serialize(),
        instances
    ))), 200

@app.route('/populate-starships', methods=["POST"])
def populate_starships():

    # solicitud de todos los characters
    response = requests.get(
        f"{BASE_URL}{'starships'}/?page=1&limit=10"  #/?page=1&limit=10
    )

    body = response.json()
    all_starships = []
    
    # ciclo a traves de la lista body['results']
    # donde cada result es un diccionario resumido
    # de un character, segun swapi
    for result in body['results']:
        # solicitud del detalle del character result
        response = requests.get(result['url'])
        body = response.json()
        # agregamos a la lista las propiedades de este
        # character
        all_starships.append(body['result']['properties'])
    
    instances = []
    
    # recorremos la lista all_characters que son
    # diccionarios de propiedades de cada personaje
    for starship in all_starships:
        
        # creamos la instancia y se guarda en bdd
        instance = Vehicles.create(starship)
        # agregamos el OBJETO character a la lista
        instances.append(instance)
    # mapeamos la lista instances para obtener una lista
    # de diccionarios que represente a cada objeto
    # character; convertimos el objeto map en una lista
    # y jsonificamos y devolvemos el resultado
    return jsonify(list(map(
        lambda inst: inst.serialize(),
        instances
    ))), 200
   # this only runs if `$ python src/main.py` is executed







@app.route('/search', methods=['GET'])
def search():
    ##args = request.args
    id_user=request.args.get("user_id", default="", type=str)
    id_planet=request.args.get("planet_id", default="Caracas", type=str) 
    query = Favorite.query.get((id_user,id_planet))
    query1=db.session.query(Favorite).get((id_user,id_planet))
    
    if query is None:
        return jsonify({
            "msg": "not found"
            }), 404
    return jsonify({"msg":f"Some of them are wrong, pls check, id number:{id_user} or id Planet:{id_planet}"}), 200

@app.route('/delete_favorites', methods=['DELETE'])
def delete_FAVORITE_PLANET():
    id_user=request.args.get("user_id", default="", type=str)
    id_planet=request.args.get("planet_id", default="Caracas", type=str)
    query = Favorite.query.get((id_user,id_planet))
    query1=db.session.query(Favorite).get((id_user,id_planet))
    if query is None:
        return jsonify({
            "msg": "not found"
            }), 404
    ##user = User.query.get_or_404(id1)
    db.session.delete(query1)
    db.session.commit()
    return jsonify( { "msg": "favorite id{id_planet}was deleted "}), 204    


@app.route('/delete_favorite_people', methods=['DELETE'])
def delete_favorite_people():
    id_user=request.args.get("user_id", default="", type=str)
    id_people=request.args.get("people_id", default="", type=str)
    query = Favorite.query.get((id_user,id_people))
    query1=db.session.query(Favorite).get((id_user,id_people))
    if query is None:
        return jsonify({
            "msg": "not found"
            }), 404
    ##user = User.query.get_or_404(id1)
    db.session.delete(query1)
    db.session.commit()
    return print( { "msg": "favorite id{id_people}was deleted "}), 204 
     


    
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
