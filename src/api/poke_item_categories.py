import json
from tqdm import tqdm
from pathlib import Path
from .client import get

#2180 items 1-2229, 10001-10002 

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_items.json"
BASE_URL = "https://pokeapi.co/api/v2/item/"