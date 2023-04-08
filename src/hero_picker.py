import json

# From Repository: https://github.com/odota/dotaconstants
HERO_FILE = "../../dotaconstants/build/heroes.json"

def get_hero(hero_id, hero_file=HERO_FILE):
    """Takes in a hero_id and returns the name of the Hero associated with it."""

    hero_name = ""
    hero_id = str(hero_id)

    try:
        with open(hero_file, 'r') as hero_data:
            hero = json.load(hero_data)
            # For debugging to read the json file
            # print(json.dumps(hero_data[str(id)], indent=2))
            hero_name = hero[hero_id]["localized_name"]
    except FileNotFoundError as fnf:
        print(f"[X] Can't find dotaconstants github repo: {fnf}")
    return hero_name

def main():
    """Main function for testing purposes."""
    try:
        HERO_ID = input("Enter a hero ID: ")
        hero = get_hero(hero_id=HERO_ID, hero_file=HERO_FILE)
        if hero:
            print(f"Hero ID {HERO_ID} is {hero}.")
    except Exception as e:
        print(f"[X] An error occurred: {e}")

if __name__ == "__main__":
    main()
