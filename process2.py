import json

result_json_path = '/home/abuhafi/Project/observasi-karakter-api/api-tb40-explore/api/v0.1/tb40/result.json'
data2_path = '/home/abuhafi/Project/observasi-karakter-api/mockup/data2.json'

with open(result_json_path, 'r') as f:
    result_data = json.load(f)

with open(data2_path, 'r') as f:
    data2 = json.load(f)

ranked18 = result_data['parts']['tb40']['tb40ResultRanked']['18']

for i, t in enumerate(ranked18):
    pillar_no = t['pillar']['no']
    name = t['data']['nama_lengkap']
    print(f"Ranked18 - No {pillar_no}: {name}")

print("---")
for cat_id, cat_data in data2['categories'].items():
    for i, trait in enumerate(cat_data['traits']):
        print(f"Data2 - {trait['id']}: {trait['name']}")

