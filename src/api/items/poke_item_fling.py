import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_item_fling.json"
BASE_URL = "https://pokeapi.co/api/v2/item-fling-effect/"
FLING_COUNT = 7

def grab_fling_effects():
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {fling["id"]: fling for fling in exist_data}
    
    def fetch_fling(start, end, tag="Fetching"):
        for fling_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(fling_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" ⚠️ No data for Fling Effect {fling_id} 🚫")
                continue
            
            fling_name = data['name'].lower()
            tqdm.write(f" {fling_name} loading....")
            
            #items with this fling effect
            items = [i['name'].lower() for i in data['items']]
            
            #effect entry
            effect_entry = next((ee['effect'] for ee in data['effect_entries'] if ee['language']['name'] == 'en'),
                                None
                                )
                    
            existing_dict[fling_id] = {
                "id": fling_id,
                "name": fling_name,
                "display_name": fling_name.replace("-", " ").title(),
                "items": items,
                "effect_entry": effect_entry,
            }
                    
    fetch_fling(1, FLING_COUNT, "Fetching Fling Effects...")
    tqdm.write(f" Fling Effects Complete")
    
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
    
    tqdm.write(f" Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_fling_effects()