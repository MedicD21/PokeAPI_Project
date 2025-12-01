import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_encounter_method.json"
BASE_URL = "https://pokeapi.co/api/v2/encounter-method/"

def grab_encount_meth():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for em_id in tqdm(range(1, 38 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(em_id))

        if data is None:
            continue

        description = ""
        if 'names' in data:
            for name_entry in data['names']:
                if name_entry.get('language', {}).get('name') == 'en':
                    description = name_entry.get('name', '')
                    break
        
        existing_dict[em_id] = {
            "id": em_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "description": description,
            "order": data.get('order', 0)
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_encount_meth()