import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_berry_flavor.json"
BASE_URL = "https://pokeapi.co/api/v2/berry-flavor/"

def grab_flava():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for flav_id in tqdm(range(1, 6 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(flav_id))

        if data is None:
            continue

        # Map berry data with potency
        berries_with_potency = [
            {
                "name": b['berry']['name'].lower(),
                "display_name": b['berry']['name'].replace('-', ' ').title(),
                "potency": b.get('potency', 0)
            }
            for b in data.get('berries', [])
        ]
        
        existing_dict[flav_id] = {
            "id": flav_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "berries": berries_with_potency,
            "contest_type": data['contest_type']['name'].lower() if data.get('contest_type') else None,
            "contest_display_type": data['contest_type']['name'].replace('-', ' ').title() if data.get('contest_type') else None,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_flava()