import json
import requests


j = dir(json)
r = dir(requests)

print("JSON module attributes and methods:")
for item in j:
    print(item)
print("\nRequests module attributes and methods:")
for item in r:
    print(item)
    

