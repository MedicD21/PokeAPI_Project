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
    
    if OUTPUT_FILE.exists()
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
            
            acc = data['accuracy'].int()
            pp = data['pp'].int()
            priority = data['priority']
            power = data['power']
            dmg_class = data['damage_class']
            eff_chance = data['effect_chance']
            gen = data['generation']
            type = data['type']
            target = data['target']['name']
            contest_type = data['contest_type']['name']
            
            
    
    
