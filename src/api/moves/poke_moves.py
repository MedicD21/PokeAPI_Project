import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

# 937 Total Moves
# 1 - 919 and 10001 - 10084

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_moves.json"
BASE_URL = "https://pokeapi.co/api/v2/move/"

moveCOUNT = 937
moveSTART = 10001
moveEND = 10084

def grab_moves():
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {move["id"]: move for move in exist_data}
    
    def fetch_moves(start, end, tag="Fetching..."):
        for move_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(move_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f"⚠️ No data for Fling Effect {move_id} 🚫 ")
                continue
                
            move_name = data['name'].lower()
            tqdm.write(f" {move_name} loading... ")
            
            acc = data['accuracy']
            pp = data['pp']
            priority = data['priority']
            power = data['power']
            dmg_class = data['damage_class']
            eff_chance = data['effect_chance']
            gen = data['generation']['name']
            type = data['type']['name']
            target = data['target']['name']
            contest_type = data['contest_type']['name']
            
            contest_combos = ['normal', 'super']
            contest_effect = ['url']
            
            #effect_changes = 
            
            effect_entries = []
            for ee in data['effect_entries']:
                effect_entries.append({
                    "effect": ee['effect'],
                    "short_effect": ee['short_effect'],
                })
                
            flavor_text_entries = []
            for ft in data['flavor_text_entries']:
                flavor_text_entries.append({
                    "flavor_text": ft['flavor_text'],
                    "in_game": ft['version_group']['name'],
                })
                
            learned_by = []
            for p in data['learned_by_pokemon']:
                learned_by.append({
                    "learned_by_pokemon": p['name']
                }) 
                
            machines = data['machines']
            
            stat_changes = []
            for sc in data['stat_changes']:
                stat_changes.append({
                    "change": sc['change'],
                    "stat": sc['stat']['name'],
                }) 
                
            meta = []
            for m in data['meta']:
                meta.append({
                    "ailment": m['ailment'],
                    "category": m['category']['damage'],
                    "crit_rate": m['crit_rate'],
                    "drain": m['drain'],
                    "flinch_chance": m['flinch_chance'],
                    "healing": m['healing'],
                    "min_hits": m['min_hits'],
                    "max_hits": m['max_hits'],
                    "min_turns": m['min_turns'],
                    "max_turns": m['max_turns'],
                    "stat_chance": m['stat_chance'],
                })
            
            flags = []
            for f in data['flags']:
                flags.append(f)
                         
                    
            
            existing_dict[move_id] = {
                "id": move_id,
                "name": move_name,
                "display_name": move_name.replace("-", " ").title(),
                "type": type,
                "generation": gen,
                "damage_class": dmg_class,
                "power": power,
                "accuracy": acc,
                "pp": pp,
                "priority": priority,
                "effect_chance": eff_chance,
                "target": target,
                "flags": flags,
                "effect_entries": effect_entries,
                "stat_changes": stat_changes,
                "flavor_text_entries": flavor_text_entries,
                "learned_by": learned_by,
                "machines": machines,
                "meta": meta,
                "contest_type": contest_type,
                "contest_combos": contest_combos,
                "contest_effect": contest_effect,
            }
            
    fetch_moves(1, 919, tag="Fetching Moves 1-919")
    fetch_moves(10001, 10084, tag="Fetching Moves 10001-10084")
    # Convert the existing_dict back to a list
    move_list = list(existing_dict.values())
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(move_list, file, indent=4)
if __name__ == "__main__":
    grab_moves()
    
    
                
            
    
    
