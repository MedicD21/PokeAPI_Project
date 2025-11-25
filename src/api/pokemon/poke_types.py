import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_types.json"
BASE_URL = "https://pokeapi.co/api/v2/type/"

def grap_types():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for type_id in tqdm(range(1, 22 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(type_id))

        if data is None:
            continue
        
        gen = data['generation']['name'].lower()
        game_indices = data['game_indices']
        damage_relations = data['damage_relations']
        if data['move_damage_class'] and data['move_damage_class']['name']:
            move_damage_class = data['move_damage_class']['name'].lower()
        else:
            move_damage_class = None
            
            
        moves = [m['name'].lower() for m in data['moves']]
        pokemon = [p['pokemon']['name'].lower() for p in data['pokemon']]
        past_damage_relations = data.get('past_damage_relations', [])


        existing_dict[type_id] = {
            "id": type_id,
            "name": data.get('name', '').lower(),
            "display_name": data.get('name', '').replace('-', ' ').title(),
            "generation": gen,
            "game_indices": game_indices,
            "damage_relations": damage_relations,
            "move_damage_class": move_damage_class,
            "moves": moves,
            "display_moves": [m.replace("-", " ").title() for m in moves],
            "pokemon": pokemon,
            "past_damage_relations": past_damage_relations,
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grap_types()