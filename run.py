import sys
import subprocess

# Map of shortcuts → module paths
SCRIPTS = {
    "items": "src.api.poke_items",
    "abilities": "src.api.poke_abilities",
    "names": "src.api.poke_names",
    "moves": "src.api.poke_moves",
    "machines": "src.api.poke_machines",
    "types": "src.api.poke_types",
    "items_categories": "src.api.poke_item_categories",
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
