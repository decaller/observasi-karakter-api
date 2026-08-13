import json
import re

with open('mockup/data3.json', 'r') as f:
    data = json.load(f)

for key, val in data.items():
    name = val["nama_lengkap"].split(" / ")[0].strip()
    p_id = val.get("pilar40")
    print(f"Key: {key}, Pilar40: {p_id}, Name: {name}")
