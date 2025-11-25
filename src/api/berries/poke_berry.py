import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_berries.json"
BASE_URL = "https://pokeapi.co/api/v2/berry/"

def grab_berries():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for berry_id in tqdm(range(1, 65 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(berry_id))

        if data is None:
            continue
        nat_gift_power = data['natural_gift_power']
        size = data['size']
        smooth = data['smoothness']
        soil = data['soil_dryness']
        m_har = data['max_harvest']
        grow_time = data['growth_time']
        
        firmness = data['firmness']['name'].lower()
        flavors = {}
        for flavor in data['flavors']:
            flavors[flavor['flavor']['name'].lower()] = flavor['potency']
        
        item = data['item']['name'].lower()
        
        nat_gift_type = data['natural_gift_type']['name'].lower()
        
        
        
        
        existing_dict[berry_id] = {
            "id": berry_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "size": size,
            "smoothness": smooth,
            "soil_dryness": soil,
            "max_harvest": m_har,
            "growth_time": grow_time,
            "firmness": firmness,
            "display_firmness": firmness.replace("-", " ").title(),
            "flavors": flavors,
            "item": item,
            "display_item": item.replace("-", " ").title(),
            "natural_gift_type": nat_gift_type,
            "natural_gift_power": nat_gift_power,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_berries()