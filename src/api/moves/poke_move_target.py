import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_move_target.json"
BASE_URL = "https://pokeapi.co/api/v2/move-target/"

def grab_move_target():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for targ_id in tqdm(range(1, 17 + 1), desc="Fetching..."):
        data = get(BASE_URL + str (targ_id))

        if data is None:
            continue
        
        description = next(
            (d['description'] for d in data.get('descriptions', [])
             if d['language']['name'] == 'en'),
            None
        )
        
        moves_list = [m['name'].lower() for m in data.get('moves', [])]

        # TODO: map fields from 'data' into a cleaned object
        existing_dict [targ_id] = {
            "id": targ_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "moves": moves_list,
            "display_moves": [m.replace("-", " ").title() for m in moves_list],
            "description": description,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_move_target()