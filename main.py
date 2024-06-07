import requests
import pprint

url = 'http://5.63.153.31:5051/v1/account'

headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
}

json = {
    'login': 'IM_test_user_5',
    'email': 'IM_test_user_5@mail.com',
    'password': 'pass123456',
}

response = requests.post(
    url=url,
    headers=headers,
    json=json
)




url = 'http://5.63.153.31:5051/v1/account/1efe497a-e32c-4b3c-804c-a7c0c7a001d9'

headers = {
    'accept': 'text/plain',
}



response = requests.put(
    url=url,
    headers=headers,

)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['roles'][1])