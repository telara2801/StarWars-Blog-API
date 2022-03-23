import requests



class Exceute_API():
    def Execute(self):

        params={
            'access_key':'889878iiouo'
        }
        
        #url="https://www.swapi.tech/api/people/{0}".format(people_id)
        url="https://www.swapi.tech/api/people/"
        results=requests.get(url)
        print(results.json())
        return results.json()


