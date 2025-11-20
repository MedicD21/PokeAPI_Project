import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

#8 atrributes

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_item_attributes.json"
BASE_URL = "https://pokeapi.co/api/v2/item-attribute/"
ATT_COUNT = 8

def grab_attributes():
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []
        
    existing_dict = {att["id"]: att for att in exist_data}
    
    def fetch_att(start, end, tag="Fetching"):
        for att_id in tqdm(range(start, end + 1), desc=tag):
            
            url = BASE_URL + str(att_id)
            data = get(url)
            
            if data is None:
                tqdm.write(f" ⚠️ No data for Attribute {att_id} 🚫")
                continue
            
            att_name = data['name'].lower()
            tqdm.write(f" {att_name} loading....")
            
            #items
            items = [i['name'].lower() for i in data['items']]
            
            #description
            descrip = next(
                (d['description'] for d in data['descriptions'] if d['language']['name'] == 'en'),
                None
            )
                    
            existing_dict[att_id] = {
                "id": att_id,
                "name": att_name,
                "display_name": att_name.replace("-", " ").title(),
                "items": items,
                "description": descrip,
            }
                    
    fetch_att(1, ATT_COUNT, "Fetching Attributes...")
    tqdm.write(f" Attributes Complete")
    
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])
    
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)
        
    tqdm.write(f" All Attributes pulled and saved to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    grab_attributes()
    
