import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_move_learn.json"
BASE_URL = "https://pokeapi.co/api/v2/move-learn-method/"

def grab_learn_method():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for learn_id in tqdm(range(1, 20 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(learn_id))

        if data is None:
            continue


#######start here 
        # TODO: map fields from 'data' into a cleaned object
        existing_dict[learn_id] = {
            "id": learn_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            # Add more fields here
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_learn_method()