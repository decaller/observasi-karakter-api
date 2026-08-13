import json
with open('/home/abuhafi/Project/observasi-karakter-api/api-tb40-explore/api/v0.1/tb40/result.json', 'r') as f:
    d = json.load(f)

for t in d['parts']['tb40']['tb40ResultRanked']['18']:
    print(f"Cat: {t['parents'][0]['no']}, TraitNo: {t['pillar']['no']}, Name: {t['data'].get('nama_lengkap', t['name'])}")
