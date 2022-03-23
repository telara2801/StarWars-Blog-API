from datetime import timezone
from email.policy import default
from pickle import FALSE
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists 

db = SQLAlchemy()


class Base(db.Model):
    __abstract__=True
    created=db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated=db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())

        
        

    def __init__(self, **kwargs): # keyword arguments
        """
        kwargs = {
        "name": "Luke",
        "eye_color": "brown",
        ...
        }
        """
        for (key, value) in kwargs.items(): #
            if key in ('created', 'updated'): continue
            if hasattr(self, key): #
                attribute_type = getattr(self.__class__, key).type
                try:
                    attribute_type.python_type(value)
                    setattr(self, key, value)
                except Exception as error:
                    print("ignoring key ", key, " with ", value, " for ", attribute_type.python_type, " because ", error.args)

    @classmethod
    def create(cls, **data):
        # crear la instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        # guardar en bdd
        db.session.add(instance)
        try:
            ##Cambio de tulio es el existe valiadtion
            db.session.commit()
            print(f"created: {instance.id}")
            return instance
        except Exception as error:
            db.session.rollback()
            #return jsonify({"msg":f"The id alreade exist in database{User.id}, please add another id"})
            raise Exception(error.args)    

                                                            

class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.String(80))
    name = db.Column(db.String(120), nullable=False)
    nick_name = db.Column(db.String(80), nullable=False)
   ### fovorites = db.relationship("Favorite", cascade="all, delete-orphan")
       
    def __repr__(self):
        return '<User %r>' % self.name
    
    
                
    def serialize(self):
        return {
            "id": self.id,
            "email":self.email,
            "password":self.password,
            "is_active":self.is_active,
            "name":self.name,
            "nick_name":self.nick_name     
            # do not serialize the password, its a security breach
        }


class Card(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(250))
    img = db.Column(db.String(250))
    nature = db.Column(db.String(50), nullable=FALSE)

    __mapper_args__ = {
        'polymorphic_identity':'Card',
        'polymorphic_on':nature
    }

    def __repr__(self):
        return f" {self.id},{self.name}, {self.nature}"
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "img":self.img,
            "nature":self.nature
                # do not serialize the password, its a security breach
        }
    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.nature}"

    def __init__(self, **kwargs): # keyword arguments
        """
        kwargs = {
            "name": "Luke",
            "eye_color": "brown",
            ...
        }
        """
        for (key, value) in kwargs.items(): #
            if key in ('created', 'updated'): continue
            if hasattr(self, key): #
                attribute_type = getattr(self.__class__, key).type
                try:
                    attribute_type.python_type(value)
                    setattr(self, key, value)
                except Exception as error:
                    print("ignoring key ", key, " with ", value, " for ", attribute_type.python_type, " because ", error.args)
   
    @classmethod
    def create(cls, data):
    # crear la instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)): 
            print("FALLA EL CONSTRUCTOR")
            return None
        # guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            print(f"created: {instance.name}")
            return instance
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)    


class Favorite(Base):
    id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    card_id= db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)

    def __repr__(self):
        return f"< user_id: {self.user_id}, Card_id: {self.card_id}>"
   
    def serialize(self):
        return {
            "user_id": self.user_id,
            "card_id": self.card_id
        }       



class Planet(Card):
    id=db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
    population = db.Column(db.String(190), nullable=False)
    climate = db.Column(db.String(200))
    rotation_period = db.Column(db.String(190))
    orbital_period = db.Column(db.String(190))
    diameter = db.Column(db.String(200))
    terrain=db.Column(db.String(200))
    gravity=db.Column(db.String(200))
    surface_water=db.Column(db.String(200))
    url=db.Column(db.String(200)) 
  
    __mapper_args__ = {'polymorphic_identity': 'planet'}


    def __repr__(self)-> str:
         return f"<Planet {self.name}, Population {self.population}>"
  
                 
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "orbital_period":self.orbital_period,
            "diameter":self.diameter,
            "terrain":self.terrain,
            "gravity":self.gravity,
            "surface_water":self.surface_water,
            "name":self.name,
            "url":self.url
             # do not serialize the password, its a security breach
        }


class Vehicles(Card):
    id=db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
    model = db.Column(db.String(200))
    passengers= db.Column(db.String(200))
    cargo_capacity= db.Column(db.String(200))
    length= db.Column(db.String(230))
    consumables= db.Column(db.String(230))
    starship_class= db.Column(db.String(230))
    manufacturer= db.Column(db.String(230))
    cost_in_credits= db.Column(db.String(230))
    crew= db.Column(db.String(230))
    max_atmosphering_speed= db.Column(db.String(230))
    hyperdrive_rating= db.Column(db.String(230))
    MGLT= db.Column(db.String(230))
    pilots= db.Column(db.String(230))
    url= db.Column(db.String(230))


    __mapper_args__ = {'polymorphic_identity': 'vehicle'}

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class":self.starship_class,
            "manufacturer":self.manufacturer,
            "cost_in_credits":self.cost_in_credits,
            "length":self.length,
            "crew":self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed":self.max_atmosphering_speed,
            "hyperdrive_rating":self.hyperdrive_rating,
            "MGLT":self.MGLT,
            "cargo_capacity": self.cargo_capacity,
            "consumables":self.consumables,
            "pilots":self.pilots,
            "url":self.url
                 # do not serialize the password, its a security breach
        }
    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.pilots}, {self.crew}"    

class Character(Card):
    id=db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
    eye_color = db.Column(db.String(40), nullable=False)
    skin_color= db.Column(db.String(40), nullable=False)
    birth_year= db.Column(db.String(10), nullable=False)
    gender= db.Column(db.String(20), nullable=False)
    mass=db.Column(db.String(20))
    height=db.Column(db.String(20))
    hair_color = db.Column(db.String(40), nullable=False)
    homeworld=db.Column(db.String(120))
    url=db.Column(db.String(120))
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'character',
    }

           
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "gender":self.gender,
            "mass":self.mass,
            "height":self.height,
            "hair_color":self.hair_color,
            "homeworld":f"http://127.0.0.1:3000/planets/{self.id}",
            "url": f"http://127.0.0.1:3000/{self.nature}s/{self.id}"    
             # do not serialize the password, its a security breach
        }
    
##    def __init__(self, **kwargs): # keyword arguments
##        """
##            kwargs = {
##            "name": "Luke",
##            "eye_color": "brown",
##            ...
##                }
##        """
##        for (key, value) in kwargs.items():
##            if hasattr(self, key):
##                setattr(self, key, value)
            
   # self.key = value
    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.name}, {self.nature}, {self.eye_color}"
        
##    @classmethod
##    def create(cls, data):
##        #Crear la instancia
##        instance=cls(**data)
##        if (not isinstance(instance,cls) ):
##            print("Falla en el constructor")
##            return None
##         #guardar en base de datos    
##        db.session.add(instance)
##        try:
##            db.session.commit()
##            return instance
##        except Exception as error:
##            db.session.rollback()
##            print(error.args)
##            raise Exception(error.args)
       
    
       
    def shortalize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": f"http://127.0.0.1:3000/{self.nature}s/{self.id}"
            }