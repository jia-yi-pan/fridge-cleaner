import json
import os

class FridgeData:
    def __init__(self, access_mode):
        self.access_mode = access_mode
        self.ingredients_file = "fridge_ingredients_data.json"
        self.meals_file = "fridge_meals_data.json"
        self.current_file_name = ""
        self.fridge_data = {}
        self.full_ingredient_list = []

    def open_fridge_files(self, fridge_file):
        if fridge_file == "meal":
            self.current_file_name = self.meals_file
        else:
            self.current_file_name = self.ingredients_file
        with open(f"{self.current_file_name}", "r") as data_file:
            data = json.load(data_file)
        return data

    def save_new_entry(self, new_data, entry_type="ingredient"):
        try:
            self.fridge_data = self.open_fridge_files(entry_type)
        except FileNotFoundError:
            with open(f"{self.current_file_name}", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            if os.stat(f"{self.current_file_name}").st_size == 0:
                with open(f"{self.current_file_name}", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
        else:
            self.fridge_data.update(new_data)
            with open(f"{self.current_file_name}", "w") as data_file:
                json.dump(self.fridge_data, data_file, indent=4)

    def find_items(self, item_type="ingredient"):
        try:
            self.fridge_data = self.open_fridge_files(item_type)
        except FileNotFoundError:
            print("Your fridge is empty! Time to eat out!")
            return False
        except json.decoder.JSONDecodeError:
            if os.stat(f"fridge_ingredients_data.json").st_size == 0:
                print("Your fridge is empty! Time to eat out!")
                return False
        else:
            # value error when empty
            if len(self.fridge_data.keys()) == 0:
                print("Your fridge is empty! Time to eat out!")
                return False
            if self.access_mode == "challenge":
                for ingredient, details in self.fridge_data.items():
                    self.full_ingredient_list.append(ingredient)
            return True

    def remove_used_item(self, list_for_chef):
        for ingredient in list_for_chef:
            self.fridge_data.pop(ingredient)
        with open("fridge_ingredients_data.json", "w") as data_file:
            json.dump(self.fridge_data, data_file, indent=4)