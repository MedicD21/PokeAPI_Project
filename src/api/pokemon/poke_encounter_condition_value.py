import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_encounter_condition_value.json"
BASE_URL = "https://pokeapi.co/api/v2/encounter-condition-value/"

def grab_ecv():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for ecv_id in tqdm(range(1, 106 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(ecv_id))

        if data is None:
            continue

        
        condition = data['condition']['name'].replace('-', ' ').title()
        
        description = ''
        if 'names' in data:
            for descrip in data['names']:
                if descrip.get('language', {}).get('name') == 'en':
                    description = descrip.get('name', '').replace('-', '')
                    break
            
            
        
        
        
        
        existing_dict[ecv_id] = {
            "id": ecv_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "condition_type": condition,
            "description": description,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_ecv()