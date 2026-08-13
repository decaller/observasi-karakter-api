import json
import re

result_json_path = '/home/abuhafi/Project/observasi-karakter-api/api-tb40-explore/api/v0.1/tb40/result.json'
data2_path = '/home/abuhafi/Project/observasi-karakter-api/mockup/data2.json'

with open(result_json_path, 'r') as f:
    result_data = json.load(f)

with open(data2_path, 'r') as f:
    data2 = json.load(f)

def clean_string(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

ranked40 = result_data['parts']['tb40']['tb40ResultRanked']['40']

pillars_by_clean_name = {}
for p in ranked40:
    name = p['name']
    clean_name = clean_string(name)
    pillars_by_clean_name[clean_name] = p

unmatched_pillars = list(pillars_by_clean_name.keys())

for cat_id, cat_data in data2['categories'].items():
    for trait in cat_data['traits']:
        trait['pillars'] = []
        trait_str = clean_string(json.dumps(trait))
        matched = []
        for p_name in list(unmatched_pillars):
            if p_name in trait_str:
                matched.append(p_name)
                p = pillars_by_clean_name[p_name]
                trait['pillars'].append({
                    'pilar40': p['data'].get('pilar40'),
                    'questionIndex': p.get('questionIndex')
                })
                unmatched_pillars.remove(p_name)
        print(f"Trait: {trait['name']} -> Matched {len(matched)} pillars: {matched}")

print(f"Unmatched Pillars: {len(unmatched_pillars)}")
print(f"Unmatched Pillars list: {unmatched_pillars}")
