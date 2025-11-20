import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_item_machines.json"
BASE_URL = "https://pokeapi.co/api/v2/machine/"
MAC_COUNT = 2102

def grab_machines():
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {mac["id"]: mac for mac in exist_data}
    
    def fetch_mac(start, end, tag="Fetching"):
        for mac_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(mac_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" ⚠️ No data for Machine {mac_id} 🚫")
                continue
            
            mach_name = data['item']['name'].lower() if data['item'] else None
            tqdm.write(f"ID#{mac_id} {mach_name} loading....")
            
            move_name = data['move']['name'].lower() if data ['move'] else None
            in_game = data['version_group']['name'].lower()
           
                    
            existing_dict[mac_id] = {
                "id": mac_id,
                "machine_item": mach_name,
                "move": move_name,
                "in_game": in_game,
            }
                    
    fetch_mac(1, MAC_COUNT, "Fetching Machines...")
    tqdm.write(f" Machines Complete")
    
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
    
    tqdm.write(f" Data saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    grab_machines() 
    