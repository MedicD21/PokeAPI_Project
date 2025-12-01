import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "poke_species.json"
BASE_URL = "https://pokeapi.co/api/v2/pokemon-species/"

def grab_species():

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {x['id']: x for x in exist_data}

    for species_id in tqdm(range(1, 1026 + 1), desc="Fetching..."):
        data = get(BASE_URL + str(species_id))

        if data is None:
            continue

        # Extract English name
        english_name = data.get('name', '').replace('-', ' ').title()
        for name_entry in data.get('names', []):
            if name_entry.get('language', {}).get('name') == 'en':
                english_name = name_entry.get('name', english_name)
                break
        
        # Extract genus (e.g., "Seed Pokémon")
        genus = None
        for genus_entry in data.get('genera', []):
            if genus_entry.get('language', {}).get('name') == 'en':
                genus = genus_entry.get('genus')
                break
        
        # Get latest English flavor text
        flavor_text = None
        flavor_entries = [entry for entry in data.get('flavor_text_entries', []) 
                         if entry.get('language', {}).get('name') == 'en']
        if flavor_entries:
            flavor_text = flavor_entries[-1].get('flavor_text', '').replace('\n', ' ').replace('\f', ' ')
        
        # Extract egg groups
        egg_groups = [egg.get('name') for egg in data.get('egg_groups', [])]
        
        # Get evolution chain ID
        evo_chain_id = None
        if data.get('evolution_chain', {}).get('url'):
            evo_chain_id = int(data['evolution_chain']['url'].rstrip('/').split('/')[-1])
        
        # Get evolves from species
        evolves_from = None
        if data.get('evolves_from_species'):
            evolves_from = data['evolves_from_species'].get('name')
        
        # Get pokedex numbers
        pokedex_numbers = []
        for entry in data.get('pokedex_numbers', []):
            pokedex_numbers.append({
                'number': entry.get('entry_number'),
                'pokedex': entry.get('pokedex', {}).get('name')
            })
        
        # Get varieties (different forms)
        varieties = []
        for variety in data.get('varieties', []):
            varieties.append({
                'is_default': variety.get('is_default', False),
                'pokemon': variety.get('pokemon', {}).get('name')
            })
        
        # Get form descriptions (for Pokemon with multiple forms)
        form_descriptions = []
        for form_desc in data.get('form_descriptions', []):
            if form_desc.get('language', {}).get('name') == 'en':
                form_descriptions.append(form_desc.get('description', ''))
        
        # Get Pal Park encounters (Gen 4 feature)
        pal_park = []
        for encounter in data.get('pal_park_encounters', []):
            pal_park.append({
                'area': encounter.get('area', {}).get('name'),
                'base_score': encounter.get('base_score'),
                'rate': encounter.get('rate')
            })
        
        existing_dict[species_id] = {
            "id": species_id,
            "name": data.get('name', '').lower(),
            "display_name": english_name,
            "genus": genus,
            "flavor_text": flavor_text,
            "generation": data.get('generation', {}).get('name'),
            "is_legendary": data.get('is_legendary', False),
            "is_mythical": data.get('is_mythical', False),
            "is_baby": data.get('is_baby', False),
            "has_gender_differences": data.get('has_gender_differences', False),
            "forms_switchable": data.get('forms_switchable', False),
            "color": data.get('color', {}).get('name'),
            "shape": data.get('shape', {}).get('name') if data.get('shape') else None,
            "habitat": data.get('habitat', {}).get('name') if data.get('habitat') else None,
            "growth_rate": data.get('growth_rate', {}).get('name'),
            "egg_groups": egg_groups,
            "gender_rate": data.get('gender_rate'),  # -1 = genderless, 0 = always male, 8 = always female
            "capture_rate": data.get('capture_rate'),
            "base_happiness": data.get('base_happiness'),
            "hatch_counter": data.get('hatch_counter'),
            "evolution_chain_id": evo_chain_id,
            "evolves_from_species": evolves_from,
            "pokedex_numbers": pokedex_numbers,
            "varieties": varieties,
            "form_descriptions": form_descriptions if form_descriptions else None,
            "pal_park_encounters": pal_park if pal_park else None,
            "order": data.get('order')
        }

    outlist = sorted(existing_dict.values(), key=lambda x: x['id'])

    with open(OUTPUT_FILE, 'w') as file:
        json.dump(outlist, file, indent=4)

    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    grab_species()