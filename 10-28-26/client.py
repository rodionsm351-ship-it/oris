import requests

url = "http://127.0.0.1:5000/notes"

# r = requests.post(url, json={"text": "Привет"})
# print(r.status_code)          # 201 {'id': 1, 'text': 'Привет'}

# r = requests.post(url, json={"text": ""})
# print(r.status_code, r.json())          # 400 ...

# r = requests.post(url, data={"text": "x"})   # form-data, не JSON
# print(r.status_code, r.json())          # 400

r = requests.post(url, json={"text": "Привет", "author": "Иван"})
print(r.status_code, r.json())

r = requests.put(url + "/2", json={"text": "Привет, мир!", "author": "Петя"})
print(r.status_code, r.json())

r = requests.patch(url + "/3", json={"text": "Hello"})
print(r.status_code, r.json())

r = requests.get(url + "?author=Иван&limit=1&offset=0")
print(r.status_code, r.json())

r = requests.post(url + "/1/like")
print(r.status_code, r.json())

r = requests.get(url + "?sort_by=id&order_by=asc")
print(r.status_code, r.json())