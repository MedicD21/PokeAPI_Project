import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_evo_chain.json"
BASE_URL = "https://pokeapi.co/api/v2/evolution-chain/"

def parse_evolution_details(evo_details):
    """Parse evolution details into a clean format"""
    if not evo_details:
        return []
    
    parsed = []
    for detail in evo_details:
        parsed_detail = {
            "trigger": detail.get('trigger', {}).get('name'),
            "min_level": detail.get('min_level'),
            "min_happiness": detail.get('min_happiness'),
            "min_affection": detail.get('min_affection'),
            "min_beauty": detail.get('min_beauty'),
            "item": detail.get('item', {}).get('name') if detail.get('item') else None,
            "held_item": detail.get('held_item', {}).get('name') if detail.get('held_item') else None,
            "known_move": detail.get('known_move', {}).get('name') if detail.get('known_move') else None,
            "known_move_type": detail.get('known_move_type', {}).get('name') if detail.get('known_move_type') else None,
            "location": detail.get('location', {}).get('name') if detail.get('location') else None,
            "time_of_day": detail.get('time_of_day') if detail.get('time_of_day') else None,
            "gender": detail.get('gender'),
            "relative_physical_stats": detail.get('relative_physical_stats'),
            "needs_overworld_rain": detail.get('needs_overworld_rain'),
            "party_species": detail.get('party_species', {}).get('name') if detail.get('party_species') else None,
            "party_type": detail.get('party_type', {}).get('name') if detail.get('party_type') else None,
            "trade_species": detail.get('trade_species', {}).get('name') if detail.get('trade_species') else None,
            "turn_upside_down": detail.get('turn_upside_down'),
        }
        # Remove null values to keep data clean
        parsed_detail = {k: v for k, v in parsed_detail.items() if v is not None}
        parsed.append(parsed_detail)
    
    return parsed

def parse_chain_recursive(chain_data):
    """Recursively parse the evolution chain"""
    if not chain_data:
        return None
    
    species_name = chain_data.get('species', {}).get('name')
    species_id = None
    if chain_data.get('species', {}).get('url'):
        species_id = int(chain_data['species']['url'].rstrip('/').split('/')[-1])
    
    evolution = {
        "species": species_name,
        "species_id": species_id,
        "is_baby": chain_data.get('is_baby', False),
        "evolution_details": parse_evolution_details(chain_data.get('evolution_details', [])),
        "evolves_to": []
    }
    
    # Recursively process all evolutions
    for evo in chain_data.get('evolves_to', []):
        evolution['evolves_to'].append(parse_chain_recursive(evo))
    
    return evolution

def grab_evo_chain():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for evo_chain_id in tqdm(range(1, 550 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(evo_chain_id))

        if data is None:
            continue

        baby_trigger_item = None
        if 'baby_trigger_item' in data and data['baby_trigger_item'] is not None:
            baby_trigger_item = data['baby_trigger_item']['name']
        
        # Parse the chain recursively
        chain = parse_chain_recursive(data.get('chain'))
        
        existing_dict[evo_chain_id] = {
            "id": evo_chain_id,
            "baby_trigger_item": baby_trigger_item,
            "chain": chain
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_evo_chain()