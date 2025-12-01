import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_encounter_condition.json"
BASE_URL = "https://pokeapi.co/api/v2/encounter-condition/"

def grab_enc_countdition():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for ec_id in tqdm(range(1, 15 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(ec_id))

        if data is None:
            continue

        description = ''
        if 'names' in data:
            for get_lang in data['names']:
                if get_lang.get('language', {}).get('name') == 'en':
                    description = get_lang.get('name', '').replace('-', ' ').title()
                    break
        
        values = []
        for item in data['values']:
            v = item['name'].replace('-', ' ').title()
            values.append(v)
                
        existing_dict[ec_id] = {
            "id": ec_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "description": description,
            "values": values,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_enc_countdition()