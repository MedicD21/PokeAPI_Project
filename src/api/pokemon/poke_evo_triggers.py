import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_evo_triggers.json"
BASE_URL = "https://pokeapi.co/api/v2/evolution-trigger/"

def grab_evo_trigger():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for evo_trig_id in tqdm(range(1, 15 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(evo_trig_id))

        if data is None:
            continue

        poke_species = []
        if 'pokemon_species' in data:
            for pname in data['pokemon_species']:
                poke_species.append(pname['name'].replace('-', ' '))
                
        description = ''
        if 'names' in data:
            for descrip in data['names']:
                if descrip.get('language', {}).get('name') == 'en':
                    description = descrip.get('name', '').replace('-', '')
                    break
        
        
        
        
        existing_dict[evo_trig_id] = {
            "id": evo_trig_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "pokemon_species": poke_species,
            "description": description,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_evo_trigger()