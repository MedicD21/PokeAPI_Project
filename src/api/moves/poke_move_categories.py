import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_move_categories.json"
BASE_URL = "https://pokeapi.co/api/v2/move-category/"

def grab_move_cat():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for cat_id in tqdm(range(0, 14 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(cat_id))

        if data is None:
            tqdm.write(f"⚠️ No data for category {cat_id}, skipping...")
            continue
        
        cat_name = data.get('name', '').lower()
        
        move_list = [m['name'].lower() for m in data.get('moves', [])]
        
        description = next(
            (d['description'] for d in data.get('descriptions', [])
            if d['language']['name'] == 'en'),
            None
        )

        # TODO: map fields from 'data' into a cleaned object
        existing_dict[cat_id] = {
            "id": cat_id,
            "name": cat_name,
            "display_name": cat_name.replace('-', ' ').title(),
            "moves": move_list,
            "display_moves": [m.replace("-", " ").title() for m in move_list],
            "description": description,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_move_cat()