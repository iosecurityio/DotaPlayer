import json

# From Repository: https://github.com/odota/dotaconstants
HERO_FILE = "../../git/dotaconstants/build/heroes.json"
HERO_ID = "100"

def get_hero(hero_id, hero_file=HERO_FILE):
    """Takes in a hero_id and returns the name of the Hero associated with it."""

    hero_name = ""
    hero_id = str(hero_id)

    try:
        with open(hero_file, 'r') as hero_data:
            hero = json.load(hero_data)
            # print(json.dumps(hero_data[str(id)], indent=2))
            hero_name = hero[hero_id]["localized_name"]
    except FileNotFoundError as fnf:
        print(fnf)
    return hero_name


if __name__ == "__main__":
    hero = get_hero(hero_id=HERO_ID, hero_file=HERO_FILE)
    print(hero)
