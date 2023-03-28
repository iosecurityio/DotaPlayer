#discord_dota.py -> Discord Bot for Dota 2
import hero_picker as hp
import json
import pandas as pd
import requests
from colorama import Fore, init
init(autoreset=True)    # Turns on colored terminal output; resets each line

player_name = "dendi" # Arbitrary name you want to give the player
player_id = "70388657"  # The actual player ID from an Open DOTA profile


class DotaPlayer:
    """Creates a Dota Player object when you input a name and opendota ID; 
    Interacts with OpenDotaAPI

    You can retrieve this key on their website by finding the player
    - https://opendota.com

    Parameters:
    name -> string input of a name you want to assign
    pid -> the unique player id from opendota
    """

    API_URL = "http://api.opendota.com/api/"
    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, name, pid):
        self.name = name.title()
        self.id = pid
        self.mmr_estimate = 0
        self.steam_name = ""
        self.information = {}
        self.avatar = ""
        self.profile = ""
        self.matches = None
        self.wordcloud = None
        self.get_player_info()

    def get_player_info(self):
        """Contact OpenDota API to Populate Player Information"""

        endpoint = "players/"
        target = f"{self.API_URL}{endpoint}{self.id}"
        print(Fore.YELLOW + f"[*] Getting information for {self.name}...")
        try:
            resp = requests.get(target, headers=self.HEADERS)
            self.information = resp.json()
            # print(json.dumps(resp.json(), indent=2))
            self.mmr_estimate = self.information["mmr_estimate"]["estimate"]
            self.steam_name = self.information["profile"]["personaname"]
            self.avatar = self.information["profile"]["avatarfull"]
            self.profile = self.information["profile"]["profileurl"]
            return self.information
        except ConnectionError as conn_error:
            print(Fore.RED + f"[!] Failed to connect to server :(\n{conn_error}")
        except KeyError as key_error:
            print(Fore.RED + f"[!] Failed to connect to server :(\n{key_error}")
        except NameError as name_error:
            print(Fore.RED + f"[!] Failed to connect to server :(\n{name_error}")
            
    def get_matches(self, limit=1):
        """Retrieves the statistics of the last Dota Game played"""

        if limit <= 0:
            print(Fore.RED + f"[!] Illegal Recent Game Quantity!")
            exit()

        endpoint = "players/"
        matchlimit = f"/matches?limit={str(limit)}"
        target = f"{self.API_URL}{endpoint}{self.id}{matchlimit}"
        titles = ["Result", "Hero", "Avg_Rank", "Duration",
                  "Kills", "Deaths", "Assists", "+/-"]
        statlist = []

        try:
            resp = requests.get(target, headers=self.HEADERS)
            # Set your 'matches' variable to the response with the JSON data
            self.matches = resp.json()
        except Exception as E:
            print(Fore.RED + f"[!] Couldn't get last game because {E}\n")
            exit()

        for match in self.matches:
            stats = []
            if match["player_slot"] <= 127:
                radiant = True
            else:
                radiant = False

            result = match["radiant_win"]
            if result and radiant:
                stats.append("Win")
            elif not result and not radiant:
                stats.append("Win")
            else:
                stats.append("Loss")

            hero_id = match['hero_id']
            hero = hp.get_hero(str(hero_id))
            stats.append(hero)
            stats.append(match["average_rank"])
            stats.append(self.convert_time(match["duration"]))
            stats.append(match["kills"])
            stats.append(match["deaths"])
            stats.append(match["assists"])
            stats.append(int(match["kills"])-int(match["deaths"]))
            statlist.append(stats)
            radiant = None

        print(Fore.CYAN + f"[-] Recent {limit} Game History for {self.name}:")
        # Print JSON Response to terminal for debugging
        # print(json.dumps(self.matches, indent=2))
        matchlist = pd.DataFrame(statlist, columns=titles)
        formatted = matchlist.to_string(index=False)
        print(formatted)
        output = f"Recent {limit} Game History for {self.name}:\n\n"
        output += formatted
        return output

    def convert_time(self, seconds):
        """Converts seconds to a string of hh:mm:ss"""

        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def get_mmr(self, to_discord=False):
        """Returns the objects MMR. Setting to_discord will stringify it"""

        print(Fore.YELLOW + f"MMR for {self.name} is " +
              Fore.GREEN + f"{self.mmr_estimate}")
        result = f"{self.name.title()}'s MMR is {self.mmr_estimate}!"
        if to_discord:
            return result
        else:
            return self.mmr_estimate

    def get_wordcloud(self):
        """Returns two dicts of words used in Team Chat and All Chat"""

        players = "players/"
        wc = "/wordcloud"
        target = f"{self.API_URL}{players}{self.id}{wc}"

        try:
            resp = requests.get(target, headers=self.HEADERS)
            self.wordcloud = resp.json()
            return resp.json()
        except Exception as E:
            print(f"Broken -> {E}")

    def get_wordcount(self, cloud, word) -> str:
        """Takes in a wordcloud and a word to look for and returns a string output of wordcount"""

        count = 0
        for chat, val in cloud.items():
            for k, v in val.items():
                if k == word:
                    count = v
        p = f"{self.name}'s current word count for '{word}' is: " + \
            Fore.RED + f"{count}"
        print(p)
        discord_msg = f"{self.name}'s current word count for the word \"{word}\" is: {count}"
        return discord_msg


if __name__ == "__main__":
    try:
        player = DotaPlayer(player_name, player_id)
        player.get_matches(5)
        player.get_mmr()
    except Exception as e:
        print(f"No worky: {e}")
