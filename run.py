import sys
import subprocess

# Map of shortcuts → module paths
SCRIPTS = {
    "items": "src.api.items.poke_items",
    "abilities": "src.api.abilities.poke_abilities",
    "names": "src.api.pokemon.poke_names",
    "moves": "src.api.moves.poke_moves",
    "machines": "src.api.items.poke_machines",
    "types": "src.api._types.poke_types",
    "item_categories": "src.api.items.poke_item_categories",
    "item_attributes": "src.api.items.poke_item_attributes",
    "berries": "src.api.items.poke_berries",
    "encounters": "src.api.pokemon.pokemon_encounter_methods",
    "encounter-condition": "src.api.pokemon.poke_encounter_condition",
    "encounter-condition-value": "src.api.pokemon.poke_encounter_condition_value",
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py <script>")
        print("Available scripts:", ", ".join(SCRIPTS))
        return

    script = sys.argv[1]

    if script not in SCRIPTS:
        print(f"Unknown script: {script}")
        print("Available options:", ", ".join(SCRIPTS))
        return

    module_path = SCRIPTS[script]
    cmd = ["python3", "-m", module_path]

    print(f"▶ Running {module_path} …")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
