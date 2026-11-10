import requests

url = "http://127.0.0.1:5000/notes"

r = requests.post(url, json={"text": "Hello", "author": "Alice"})
r = requests.post(url, json={"text": "Goodbye", "author": "Alice"})
r = requests.post(url, json={"text": "Hello", "author": "Bob"})
r = requests.post(url, json={"text": "Goodbye", "author": "Alla"})

r = requests.get(url)
print(r.status_code, r.json())

r = requests.get(url + "/1")
print(r.status_code, r.json())

r = requests.get(url + "?author=Alice")
print(r.status_code, r.json())

r = requests.get(url + "?author=Alice&sort_by=likes&order_by=desc&limit=1")
print(r.status_code, r.json())

r = requests.get(url + "/authors")
print(r.status_code, r.json())

r = requests.put(url + "/1", json={"author": "Put author", "text": "Updated text"})
print(r.status_code, r.json())

r = requests.patch(url + "/2", json={"text": "Patched text"})
print(r.status_code, r.json())

r = requests.delete(url + "/2")
print(r.status_code)

r = requests.delete(url + "?author=Bob")
print(r.status_code, r.json())