import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

#2180 items 1-2229, 10001-10002 

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_items.json"
BASE_URL = "https://pokeapi.co/api/v2/item/"
ITEMS_COUNT = 2229
OITEMS_START = 10001
OITEMS_END = 10002

def grab_item():
    
    # load existing file
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    # convert to dict for upsert behavior
    existing_dict = {item["id"]: item for item in exist_data}

    # fast lookup for skip logic
    exist_ids = set(existing_dict.keys())
    
    def fetch_items(start, end, tag="Fetching"):
        for item_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(item_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" ⚠️ No data for item {item_id} 🚫 ")
                continue
            
            item_name = data['name'].lower()
            
            tqdm.write(f" Getting {item_name} info...")
            
            #Gets non nested item info
            fling_effect = data['fling_effect']
            fling_power = data['fling_power']
            baby_trig = data['baby_trigger_for']
            cost = data['cost']
            
            held_by = []
            for hb in data['held_by_pokemon']:
                pokemon_name = hb['pokemon']['name']
                for v in hb['version_details']:
                    held_by.append({
                        "pokemon": pokemon_name,
                        "rarity": v['rarity'],
                        "in_game": v['version']['name'].lower(),
                        })

            
            
            machines = []
            for machine in data['machines']:
                url_ = machine["machine"]["url"]
                machines.append({
                    "machine_id": url_.split("/")[-2] if url_ else None,
                    "in_game": machine["version_group"]["name"].lower(),
                    })

            
            attributes = []
            for att in data['attributes']:
                att_name = att['name']
                attributes.append({
                    "name": att_name,
                    })
                
            category = data['category']['name'].lower()
            
            effect_entries = []
            for ef in data['effect_entries']:
                if ef['language']['name'] == 'en':
                    effect_entries.append({
                        "effect": ef['effect'].replace("\n", " ").strip(),
                        "short_effect": ef['short_effect'].replace("\n", " ").strip(),
                    })
            
            flavor_entries = []
            for ft in data['flavor_text_entries']:
                if ft['language']['name'] == 'en':
                    flavor_entries.append({
                        "flavor_text": ft["text"].replace("\n", " ").strip(),
                        "in_game": ft['version_group']['name'].lower(),
                    })

                    
            game_indices = []
            for gi in data['game_indices']:
                game_index = gi['game_index']
                gen = gi['generation']['name']
                game_indices.append({
                    "game_index": game_index,
                    "generation": gen,
                })
                
            sprites = data['sprites']
            
            existing_dict[item_id] = {
                "id": item_id,
                "name": item_name,
                "display_name": item_name.replace("-", " ").title(),
                "category": category,
                "display_category": category.replace("-", " ").title(),
                "cost": cost,
                "fling_effect": fling_effect,
                "fling_power": fling_power,
                "baby_trigger_for": baby_trig,
                "attributes": attributes,                # list of attribute names
                "machines": machines,                    # list of in_game TM/TR availability
                "held_by_pokemon": held_by,              
                "effect_entries": effect_entries,        # list of effect / short effect pairs
                "flavor_texts": flavor_entries,          # list of flavor text across games
                "game_indices": game_indices,            # index + generation
                "sprites": sprites                       # default sprite
            }
     
    fetch_items(1, ITEMS_COUNT, "Fetching items...")
    tqdm.write(f" Bulk Complete")
    
    fetch_items(OITEMS_START, OITEMS_END, "Fetching the rest...")
    tqdm.write(f" Grabbed the last couple ")
    
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
        
    tqdm.write(f" All Items pulled and saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    grab_item()
            