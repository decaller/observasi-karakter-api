import json
import re

with open('mockup/data3.json', 'r') as f:
    data3 = json.load(f)

pillar_dict = {}
for key, val in data3.items():
    name = val["nama_lengkap"].split(" / ")[0].strip().lower()
    pillar_id = str(val.get("pilar40", key))
    pillar_dict[name] = pillar_id

# Manually add some known aliases for better matching
# Some strings use single quotes instead of curly quotes, or slight variations
aliases = {
    "tawaadhu'": "24",
    "tawaadhu’": "24",
    "qanaa'ah": "20",
    "qanaa’ah": "20",
    "hayaa'": "15",
    "hayaa’": "15",
    "izzah": "17",
    "'izzah": "17",
    "‘izzah": "17",
    "aziimah": "5",
    "'aziimah": "5",
    "‘aziimah": "5",
    "syajaa'ah": "18",
    "syajaa’ah": "18",
    "fashaahah": "26",
    "husnuzhan": "9"
}
for k, v in aliases.items():
    pillar_dict[k] = v

data_profesi = {}

def extract_list(text):
    if not text:
        return []
    # Split by comma or semicolon
    parts = re.split(r'[,;]', text)
    res = []
    for p in parts:
        p = p.strip()
        if p and not p.lower() in ['dsb.', 'dll.']:
            res.append(p)
    return res

for key, val in data3.items():
    p_id = str(val.get("pilar40", key))
    
    # Extract profesi & jurusan
    prof_text = val.get("profesi", "")
    jur_text = val.get("jurusan", "")
    
    prof_list = extract_list(prof_text)
    jur_list = extract_list(jur_text)
    
    for prof in prof_list:
        if prof not in data_profesi:
            data_profesi[prof] = {
                "related_pillars": [],
                "related_jurusans": []
            }
        if p_id not in data_profesi[prof]["related_pillars"]:
            data_profesi[prof]["related_pillars"].append(p_id)
        
        for j in jur_list:
            if j not in data_profesi[prof]["related_jurusans"]:
                data_profesi[prof]["related_jurusans"].append(j)

    # Link IDs
    def extract_ids(text):
        if not text: return []
        found = set()
        text_lower = text.lower()
        for p_name, p_val in pillar_dict.items():
            if p_name in text_lower:
                found.add(p_val)
        return list(found)

    val["lalai_perbaiki_ids"] = extract_ids(val.get("lalai_perbaiki", ""))
    val["lebih_perbaiki_ids"] = extract_ids(val.get("lebih_perbaiki", ""))
    
    # Save back
    data3[key] = val

# Save updated data3.json
with open('mockup/data3.json', 'w') as f:
    json.dump(data3, f, indent=2)

# Save data_profesi.json
with open('mockup/data_profesi.json', 'w') as f:
    json.dump(data_profesi, f, indent=2)

print("Data refactored successfully!")
