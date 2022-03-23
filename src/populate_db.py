import requests
from models import Character

BASE_URL = "https://www.swapi.tech/api/"
def populate_chars():
    response = requests.get(
        f"{BASE_URL}{'people'}"
    )
    body = response.json()
    all_characters = []
    for result in body['results']:
        response = requests.get(result['url'])
        body = response.json()
        all_characters.append(body)
    return all_characters

print(populate_chars())

