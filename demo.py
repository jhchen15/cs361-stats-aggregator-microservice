import requests

endpoints = {
    '/sum': 'http://127.0.0.1:8000/sum',
    '/avg': 'http://127.0.0.1:8000/avg',
    '/minmax': 'http://127.0.0.1:8000/minmax'
}

test_list = {
    'vals': [5, 7, 9, 44, 13.7523, -10],
    'payload_type': 'list'
}

test_dict = {
    'vals': [{'name': 'rufus', 'age': 5},
             {'name': 'todd', 'age': 6},
             {'name': 'marx', 'age': 7}],
    'payload_type': 'dict',
    'key': 'age'
}

print("------------------- TESTING ENDPOINTS WITH INPUT LIST -------------------")
for endpoint, url in endpoints.items():
    response = requests.post(url=url, json=test_list)
    print(f"Testing endpoint {endpoint} at {url}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Payload: {response.json()}\n")


print("------------------- TESTING ENDPOINTS WITH INPUT DICT -------------------")
for endpoint, url in endpoints.items():
    response = requests.post(url=url, json=test_dict)
    print(f"Testing endpoint {endpoint} at {url}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Payload: {response.json()}\n")
