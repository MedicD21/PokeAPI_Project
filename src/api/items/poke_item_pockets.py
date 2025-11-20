import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

#8 atrributes

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_item_pockets.json"
BASE_URL = "https://pokeapi.co/api/v2/item-pocket/"
pock_COUNT = 8

def grab_pockets():
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {pock["id"]: pock for pock in exist_data}
    
    def fetch_pock(start, end, tag="Fetching"):
        for pock_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(pock_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" ⚠️ No data for Pocket {pock_id} 🚫")
                continue
            
            pock_name = data['name'].lower()
            tqdm.write(f" {pock_name} loading....")
            
            #category
            category = [i['name'].lower() for i in data['categories']]
                    
            existing_dict[pock_id] = {
                "id": pock_id,
                "name": pock_name,
                "display_name": pock_name.replace("-", " ").title(),
                "categories": category,
            }
                    
    fetch_pock(1, pock_COUNT, "Fetching Pockets...")
    tqdm.write(f" Pockets Complete")
    
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
    
    tqdm.write(f" Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_pockets()