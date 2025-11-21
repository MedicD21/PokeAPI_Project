import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

# Move Ailments 22 1-24,42

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_move_battle_style.json"
BASE_URL = "https://pokeapi.co/api/v2/move-battle-style/"

BATTLE_STYLE_COUNT = 3

def grab_move_battle_styles(): 
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {style["id"]: style for style in exist_data}
    
    def fetch_battle_style(start, end, tag="Fetching Battle Styles..."):
        for style_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(style_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" No data for Battle Style {style_id}, skipping...")
                continue
            
            style_name = data['name'].lower()
            tqdm.write(f" Battle Style {style_name} loading...")
            
            existing_dict[style_id] = {
                "id": style_id,
                "name": style_name,
                "display_name": style_name.replace("-", " ").title(),
            }
            
    fetch_battle_style(1, BATTLE_STYLE_COUNT, "Fetching Battle Styles...")
    
    outlist = (sorted(existing_dict.values(), key=lambda x: x["id"]))
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
    tqdm.write(f" All Battle Styles save to {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_move_battle_styles()