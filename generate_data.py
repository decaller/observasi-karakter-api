import json
import os

result_json_path = '/home/abuhafi/Project/observasi-karakter-api/api-tb40-explore/api/v0.1/tb40/result.json'
data2_path = '/home/abuhafi/Project/observasi-karakter-api/mockup/data2.json'
data3_path = '/home/abuhafi/Project/observasi-karakter-api/mockup/data3.json'

with open(result_json_path, 'r') as f:
    result_data = json.load(f)

with open(data2_path, 'r') as f:
    data2 = json.load(f)

ranked40 = result_data['parts']['tb40']['tb40ResultRanked']['40']

# Map pillars by their parent trait 'no'
pillars_by_trait_no = {}
data3 = {}

for p in ranked40:
    parent_no = p['parents'][0]['no']
    if parent_no not in pillars_by_trait_no:
        pillars_by_trait_no[parent_no] = []
        
    pilar40 = p['data'].get('pilar40')
    q_index = p.get('questionIndex')
    
    pillars_by_trait_no[parent_no].append({
        'pilar40': pilar40,
        'questionIndex': q_index
    })
    
    # Construct data3 entry
    data3[str(q_index)] = {
        'pilar40': pilar40,
        'questionIndex': q_index,
        'nama_lengkap': p['data'].get('nama_lengkap'),
        'definisi': p['data'].get('definisi'),
        'lalai_nama_lengkap': p['data'].get('lalai_nama_lengkap'),
        'lalai_definisi': p['data'].get('lalai_definisi'),
        'lalai_perbaiki': p['data'].get('lalai_perbaiki'),
        'lebih_nama_lengkap': p['data'].get('lebih_nama_lengkap'),
        'lebih_definisi': p['data'].get('lebih_definisi'),
        'lebih_perbaiki': p['data'].get('lebih_perbaiki'),
        'profesi': p['data'].get('profesi'),
        'jurusan': p['data'].get('jurusan')
    }

# Update data2
for cat_id, cat_data in data2['categories'].items():
    for trait in cat_data['traits']:
        trait_id = trait['id'] # e.g. "sub_1"
        trait_no = trait_id.split('_')[1] # "1"
        
        if trait_no in pillars_by_trait_no:
            trait['pillars'] = pillars_by_trait_no[trait_no]
        else:
            trait['pillars'] = []

# Write back data2
with open(data2_path, 'w') as f:
    json.dump(data2, f, indent=2)

# Write data3
with open(data3_path, 'w') as f:
    json.dump(data3, f, indent=2)

print(f"Successfully processed {len(ranked40)} pillars and updated data2.json. Created data3.json with {len(data3)} items.")
