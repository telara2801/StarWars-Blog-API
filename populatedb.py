import requests
##from urllib import requests
from src.models import Person

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

BASE_URL="https://www.swapi.tech/api/"
response=requests.get(
    f"{BASE_URL}{'people'}"
)
body=response.json()
#print(body)
all_persons=[]
for result in body['results']:
    ##print(result)
    response=requests.get(result['url'])
    body=response.json()
    all_persons.append(body)

##print(all_character)    

for person in all_persons:
    ##data={**person['result']['properties']}
    data={**person['result']['properties']}
    print(data)
    instance=Person(
        name=data['name'],
        mass=data['mass'],
        skin_color=data['skin_color'],
        eye_color=data['eye_color'],
        birth_year=data['birth_year'],
        gender=data['gender'],
        height=data['height'],
        hair_color=data['hair_color']
    )
    print("ooooooooooo"+data['name'])
    if isinstance(instance,Person):
        print(f"created {instance.name} with id:{instance.id}")
        db.session.add(instance)
        db.session.commit()
        continue 
    else:
        print("verificar, algo paso")