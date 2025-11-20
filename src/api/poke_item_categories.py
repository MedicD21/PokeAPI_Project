import json
from tqdm import tqdm
from pathlib import Path
from .client import get

#2180 items 1-2229, 10001-10002 

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_item_categories.json"
BASE_URL = "https://pokeapi.co/api/v2/item-category/"
ITEM_CAT_COUNT = 55

def grab_item_categories():
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {cat["id"]: cat for cat in exist_data}
    exist_ids = set(existing_dict.keys())
    
    def fetch_cat(start, end, tag="Fetching"):
        for cat_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(cat_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" ⚠️ No data for category {cat_id} 🚫 ")
                continue
            
            cat_name = data['name'].lower()
            tqdm.write(f" {cat_name} loading...")
            
            #items
            items = [i['name'].lower() for i in data['items']]
            
            #pocket    
            pocket = data['pocket']['name'].lower()
            
            #save
            existing_dict[cat_id] = {
                "id": cat_id,
                "category": cat_name,
                "display_category": cat_name.replace("-", " ").title(),
                "items": items,
                "pocket": pocket,
            }
            
    fetch_cat(1, ITEM_CAT_COUNT, "Fetching Categories...")
    tqdm.write(f" Categories Complete ")
    
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
        
    tqdm.write(f" All Categories Pulled and saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    grab_item_categories()
            
            