import json
from tqdm import tqdm
from pathlib import Path
from .client import get

#2180 items 1-2229, 10001-10002 

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_abilities.json"
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
            
            