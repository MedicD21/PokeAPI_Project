✅ Remaining Scripts to Build (Full Checklist)

1. Item-Related

You already finished:
✔ categories
✔ attributes

Still left:

1.1 Item Fling Effects

Endpoint: /item-fling-effect/
Collect:

id

name

effect entries (EN)

items belonging to this effect

2. Item Pockets

Endpoint: /item-pocket/
Collect:

id

name

categories inside pocket

display name

3. Moves

Moves are big. They need several connected scripts:

3.1 Moves

Endpoint: /move/
Collect major fields:

id

name

type

damage class

accuracy

power

PP

priority

effect

flavor text

meta info (crit rate, drain, ailment, chance, etc.)

stat changes

learned by Pokémon

machines

generation

3.2 Move Damage Classes

Endpoint: /move-damage-class/

Collect:

id

name

description

list of moves with this class

3.3 Move Categories (a.k.a Meta Categories)

Endpoint: /move-category/

Collect:

id

name

description

moves under this category

3.4 Move Ailments

Endpoint: /move-ailment/

Collect:

id

name

description

moves causing this ailment

3.5 Move Targets

Endpoint: /move-target/

Collect:

id

name

description

moves with this targeting type

3.6 Move Learn Methods

Endpoint: /move-learn-method/

Collect:

id

name

description

version groups supporting that method

(Useful for connecting Pokémon → move learn sources later.)

4. Types
   4.1 Pokémon Types

Endpoint: /type/

Collect:

id

name

damage relations

moves of this type

Pokémon of this type

generation

game indices

5. Pokémon species

This is the species endpoint for flavor text + forms data.
You will need this later to connect evolutions and gender differences.

5.1 Pokémon Species

Endpoint: /pokemon-species/

Collect:

id

name

genera

color

shape

habitat

growth rate

capture rate

gender rate

base happiness

flavor text (multiple languages)

evolves from species

evolution chain url

varieties (forms)

6. Pokémon (full details)

This is the actual base Pokémon data (stats, abilities, forms, sprites).
You already started names — this finishes it.

6.1 Pokémon Data

Endpoint: /pokemon/

Collect:

id

name

height

weight

stats

abilities

types

held items

game indices

past types

sprites

moves learned (with version/method)

7. Evolution Chains

Endpoint: /evolution-chain/

Collect:

id

base species

evolution details (level, item, happiness, trade, move, time, etc.)

This connects back to species.

8. Egg Groups

Endpoint: /egg-group/

Collect:

id

name

Pokémon species in that group

9. Growth Rates

Endpoint: /growth-rate/

Collect:

id

name

formula

experience tables

10. Pokémon Colors

Endpoint: /pokemon-color/

Collect:

id

name

Pokémon species

(This is simple but useful for filtering UI themes later.)

11. Pokémon Habitats

Endpoint: /pokemon-habitat/

12. Pokémon Shapes

Endpoint: /pokemon-shape/

13. Pokémon Genders

Endpoint: /gender/

Includes:

Pokémon with gender differences

rates

🎉 Optional (future polish)

These aren’t required but are nice-to-haves for a perfect database:

• Machines (TM/TR list)

Endpoint: /machine/
Link TM → Move → Item

• Version Groups

Better organize by generation.

• Regions

Map Pokémon to regions.

⭐ Total Scripts Remaining

19 essential scripts

- optional 3–5 future scripts
