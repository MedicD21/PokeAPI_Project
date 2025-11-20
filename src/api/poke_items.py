import json
from tqdm import tqdm
from pathlib import Path
from .client import get

#2180 items 1-2229, 10001-10002 

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_items.json"
BASE_URL = "https://pokeapi.co/api/v2/item/"
ITEMS_COUNT = 2229
OITEMS_START = 10001
OITEMS_END = 10002

def grab_item():
    
    item_list = []
    exist_data = []
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    
    exist_ids = { entry["id"] for entry in exist_data}
    
    
    def fetch_items(start, end, tag="Fetching"):
        for item_id in tqdm(range(start, end + 1), desc=tag):
            
            if item_id in exist_ids:
                tqdm.write(f" Item {item_id} already exists. Skipping...")
                continue
            url = BASE_URL + str(item_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" No data for item {item_id}")
                continue
            
            item_name = data['name'].lower()
            tqdm.write(f" Getting {item_name} info...")
            
            #Gets non nested item info
            fling_effect = data['fling_effect']
            fling_power = data['fling_power']
            baby_trig = data['baby_trigger_for']
            cost = data['cost']
            held_by = data['held_by_pokemon']
            
            
            machines = []
            for machine in data['machines']:
                machine_game = machine['version_group']['name'].lower()
                machines.append({
                    "in_game": machine_game,
                    })
            
            attributes = []
            for att in data['attributes']:
                att_name = att['name']
                attributes.append({
                    "attributes": att_name,
                    })
                
            category = data['category']['name']
            
            effect_entries = []
            for ef in data['effect_entries']:
                if ef['language']['name'] == 'en':
                    effect_entries.append({
                        "effect": ef['effect'],
                        "short_effect": ef['short_effect'],
                    })
            
            flavor_entries = []
            for ft in data['flavor_text_entries']:
                if ft['language']['name'] == 'en':
                    flavor_text = ft["text"]
                    game = ft['version_group']['name'].lower()
                    flavor_entries.append({
                        "flavor_text": flavor_text,
                        "in_game": game,
                    })
                    
            game_indices = []
            for gi in data['game_indices']:
                game_index = gi['game_index']
                gen = gi['generation']['name']
                game_indices.append({
                    "game_index": game_index,
                    "generation": gen,
                })
                
            sprites = data['sprites']['default']
            
            item_list.append({
                "id": item_id,
                "name": item_name,
                "category": category,
                "cost": cost,
                "fling_effect": fling_effect,
                "fling_power": fling_power,
                "baby_trigger_for": baby_trig,

                "attributes": attributes,                # list of attribute names
                "machines": machines,                    # list of in_game TM/TR availability
                "held_by_pokemon": held_by,              # raw list from PokeAPI

                "effect_entries": effect_entries,        # list of effect / short effect pairs
                "flavor_texts": flavor_entries,          # list of flavor text across games
                "game_indices": game_indices,            # index + generation
                "sprites": sprites                       # default sprite
            })
     
    fetch_items(1, ITEMS_COUNT, "Fetching items...")
    tqdm.write(f" Bulk Complete")
    
    fetch_items(OITEMS_START, OITEMS_END, "Fetching the rest...")
    tqdm.write(f" Grabbed the last couple ")
    
    outlist = exist_data + item_list
    outlist = sorted(outlist, key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
        
    tqdm.write(f" All Items pulled and saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    grab_item()
            