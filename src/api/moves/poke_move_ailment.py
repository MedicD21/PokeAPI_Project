import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

# Move Ailments 22 1-24,42

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_move_ailment.json"
BASE_URL = "https://pokeapi.co/api/v2/move-ailment/"

AILMENT_COUNT = 43

def grab_move_ailment(): 
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {ail["id"]: ail for ail in exist_data}
    
    def fetch_ailment(start, end, tag="Fetching Ailment..."):
        for ail_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(ail_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" No data for Ailment {ail_id}, skipping...")
                continue
            
            ail_name = data['name'].lower()
            tqdm.write(f" Ailment {ail_name} loading...")
            
            moves = [mn['name'].lower() for mn in data['moves']]
            
            existing_dict[ail_id] = {
                "id": ail_id,
                "name": ail_name,
                "display_name": ail_name.replace("-", " ").title(),
                "moves": moves,
                "display_move": [m.replace("-", " ").title() for m in moves],
            }
            
    fetch_ailment(1, AILMENT_COUNT, "Fetching Ailments...")
    
    outlist = (sorted(existing_dict.values(), key=lambda x: x["id"]))
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
    tqdm.write(f" All Ailments save to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    grab_move_ailment()