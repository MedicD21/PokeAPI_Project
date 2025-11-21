import json
from tqdm import tqdm
from pathlib import Path
from ..client import get

# MOVE RANGES:
# 1–919 = normal moves
# 10001–10256 = special/dynamax/extra moves

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "pokemon_moves.json"
BASE_URL = "https://pokeapi.co/api/v2/move/"

MOVE_MAIN_END = 919
MOVE_SPECIAL_START = 10001
MOVE_SPECIAL_END = 10018


def grab_moves():

    # Load existing JSON
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r") as file:
            exist_data = json.load(file)
    else:
        exist_data = []

    existing_dict = {entry["id"]: entry for entry in exist_data}

    def fetch_moves(start, end, tag="Fetching Moves..."):
        for move_id in tqdm(range(start, end + 1), desc=tag):

            url = BASE_URL + str(move_id)
            data = get(url)

            if data is None:
                tqdm.write(f" ⚠️ No data for move {move_id}, skipping...")
                continue

            move_name = data["name"].lower()
            tqdm.write(f" Move {move_name} loading...")

            # Basic fields
            accuracy = data["accuracy"]
            pp = data["pp"]
            priority = data["priority"]
            power = data["power"]
            effect_chance = data["effect_chance"]

            gen = data["generation"]["name"].lower()
            type_ = data["type"]["name"].lower()

            target = data["target"]["name"].lower()
            dmg_class = data["damage_class"]["name"].lower()

            # Contest fields (may be null)
            contest_type = (
                data["contest_type"]["name"].lower()
                if data["contest_type"]
                else None
            )

            # Contest combos are objects, not lists
            contest_combos = data["contest_combos"]

            # Contest effect (url reference)
            contest_effect = (
                data["contest_effect"]["url"] if data["contest_effect"] else None
            )

            # Effect entries (EN only)
            effect_entries = []
            for ee in data["effect_entries"]:
                if ee["language"]["name"] == "en":
                    effect_entries.append(
                        {
                            "effect": ee["effect"].replace("\n", " ").strip(),
                            "short_effect": ee["short_effect"]
                            .replace("\n", " ")
                            .strip(),
                        }
                    )

            # Flavor text entries (EN only)
            flavor_texts = []
            for ft in data["flavor_text_entries"]:
                if ft["language"]["name"] == "en":
                    flavor_texts.append(
                        {
                            "flavor_text": ft["flavor_text"]
                            .replace("\n", " ")
                            .strip(),
                            "in_game": ft["version_group"]["name"].lower(),
                        }
                    )

            # Pokemon that learn the move
            learned_by = [p["name"] for p in data["learned_by_pokemon"]]

            # Machines that teach this move
            machines = []
            for m in data["machines"]:
                url_ = m["machine"]["url"]
                machines.append(
                    {
                        "machine_id": url_.split("/")[-2],
                        "in_game": m["version_group"]["name"].lower(),
                    }
                )

            # Stat changes
            stat_changes = []
            for sc in data["stat_changes"]:
                stat_changes.append(
                    {
                        "change": sc["change"],
                        "stat": sc["stat"]["name"],
                    }
                )

            # METADATA (object, not list)
            meta_raw = data["meta"]
            if meta_raw:
                meta = {
                    "ailment": meta_raw["ailment"]["name"]
                    if meta_raw["ailment"]
                    else None,
                    "category": meta_raw["category"]["name"]
                    if meta_raw["category"]
                    else None,
                    "crit_rate": meta_raw["crit_rate"],
                    "drain": meta_raw["drain"],
                    "flinch_chance": meta_raw["flinch_chance"],
                    "healing": meta_raw["healing"],
                    "min_hits": meta_raw["min_hits"],
                    "max_hits": meta_raw["max_hits"],
                    "min_turns": meta_raw["min_turns"],
                    "max_turns": meta_raw["max_turns"],
                    "stat_chance": meta_raw["stat_chance"],
                }
            else:
                meta = None

            # Flags → extract names
            #flags = [f["name"] for f in data["flags"]]

            # Past values (optional but important)
            past_values = data["past_values"]

            existing_dict[move_id] = {
                "id": move_id,
                "name": move_name,
                "display_name": move_name.replace("-", " ").title(),
                "type": type_,
                "generation": gen,
                "damage_class": dmg_class,
                "power": power,
                "accuracy": accuracy,
                "pp": pp,
                "priority": priority,
                "effect_chance": effect_chance,
                "target": target,
                #"flags": flags,
                "effect_entries": effect_entries,
                "stat_changes": stat_changes,
                "flavor_texts": flavor_texts,
                "learned_by_pokemon": learned_by,
                "machines": machines,
                "meta": meta,
                "contest_type": contest_type,
                "contest_combos": contest_combos,
                "contest_effect": contest_effect,
                "past_values": past_values,
            }

    # Fetch main moves
    fetch_moves(1, MOVE_MAIN_END, "Fetching Main Moves...")

    # Fetch special moves
    fetch_moves(MOVE_SPECIAL_START, MOVE_SPECIAL_END, "Fetching Special Moves...")

    # Save sorted output
    outlist = sorted(existing_dict.values(), key=lambda x: x["id"])

    with open(OUTPUT_FILE, "w") as file:
        json.dump(outlist, file, indent=4)

    tqdm.write(f" All moves saved → {OUTPUT_FILE}")


if __name__ == "__main__":
    grab_moves()
