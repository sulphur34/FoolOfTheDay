import json
import os
import random


class FoolData:

    def __init__(self):
        self.members_list = {1: "Ivan", 2: "Alexander", 3: "Sergey"}
        self.statistics = {"Ivan": {"fool": 0, "good": 0}, "Alexander": {"fool": 0, "good": 0},
                           "Sergey": {"fool": 0, "good": 0}}

        self.filepath = os.path.join(os.getcwd(), 'statistics.json')
        with open(self.filepath, 'w') as jsonfile:
            if os.stat("file").st_size == 0:
                json.dump(self.statistics, jsonfile)

    def get_statistics(self):
        with open(self.filepath, 'r') as jsonfile:
            data = json.load(jsonfile)
            return data

    def save_statistics(self, fool, good):
        data = self.get_statistics()
        data[fool]["fool"] += 1
        data[good]["good"] += 1
        with open(self.filepath, 'w') as jsonfile:
            json.dump(data, jsonfile)

    def game(self):
        rand = random.Random()
        fool = self.members_list[rand.randint(1, 3)]
        good = self.members_list[rand.randint(1, 3)]
        self.save_statistics(fool, good)
        return fool, good

    def clean_statistics(self):
        with open(self.filepath, 'w') as jsonfile:
            json.dump(self.statistics, jsonfile)
