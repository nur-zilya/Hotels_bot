import requests
import json
import re
from config_data import config


city_url = "https://hotels4.p.rapidapi.com/locations/v3/search"

headers = {
	"X-RapidAPI-Key": "e418064698msh6828f10f851a96ep1f2a6djsn6cef63b16a1a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def destination_id():
    pattern = '<[^>]*>'
    querystring = {"query": city, "locale": "en_US", "currency":"USD"}
    response = requests.request("GET", city_url, headers=headers, params=querystring)
    data = json.loads(response.text)
    with open('step_1.json', 'w') as file:
        json.dump(data, file, indent=4)
    possible_cities = {}
    for i in data['suggestions'][0]['entities']:
        possible_cities[i['destinationId']] = re.sub(pattern, '', i['caption'])
    return possible_cities









