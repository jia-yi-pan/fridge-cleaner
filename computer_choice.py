from datetime import datetime, timedelta
from recipe_requester import RecipeRequester
from fridge_data import FridgeData

fridge_data = FridgeData(access_mode="computer")

class ComputerChoice:
    def __init__(self):
        self.picked_option = ""
        self.expiring_ingredients = []
        self.expiring_meals = []
        self.upcoming_expiration = ""

    def pick_prompt(self):
        run = True
        while run:
            self.picked_option = input("What would you like chosen for you? "
                                "Type (I) for ingredient, (M) for meal, or (R) for recipe: ").strip()
            try:
                self.picked_option = self.picked_option.upper()
            except ValueError:
                print("Please type a letter!")
            else:
                if self.picked_option == "I":
                    run = False
                    self.pick_ingredient()
                elif self.picked_option == "M":
                    run = False
                    self.pick_meal()
                elif self.picked_option == "R":
                    run = False
                    self.pick_recipe()
                else:
                    print("Please type a valid letter!")

    def find_expiring_soon(self, list_to_append):
        base_dt = datetime.now()
        fridge_dates_dict = {}

        def find_date_difference(date):
            converted_dt_object = datetime.strptime(date, "%m/%d/%Y")
            delta = converted_dt_object - base_dt if base_dt < converted_dt_object else timedelta.max
            return delta
        for entry, details in fridge_data.fridge_data.items():
            fridge_dates_dict[entry] = details["Approximate Expiration"]
        expiry_dates_list = list(fridge_dates_dict.values())
        closest_date = min(expiry_dates_list, key=find_date_difference)
        for entry, details in fridge_dates_dict.items():
            if fridge_dates_dict[entry] == closest_date:
                list_to_append.append(entry)
        self.upcoming_expiration = fridge_dates_dict[list_to_append[0]]

    def pick_ingredient(self):
        if fridge_data.find_items():
            self.find_expiring_soon(self.expiring_ingredients)
            print(
                f"You have {len(self.expiring_ingredients)} item(s) expiring on {self.upcoming_expiration}: {self.expiring_ingredients}")
            if self.picked_option == "I":
                self.follow_through_prompt(self.expiring_ingredients)
            return True
        return False

    def pick_meal(self):
        if fridge_data.find_items("meal"):
            self.find_expiring_soon(self.expiring_meals)
            print(
                f"You have {len(self.expiring_meals)} item(s) expiring on {self.upcoming_expiration}: {self.expiring_meals}")
            self.follow_through_prompt(self.expiring_meals)

    def pick_recipe(self):
        if self.pick_ingredient():
            print(f"Let's make something delicious with these ingredients!")
            recipe_requester = RecipeRequester()
            for ingredient in self.expiring_ingredients:
                recipe_requester.ingredient_list.append(ingredient)
            recipe_requester.choose_random_recipe()
            recipe_requester.open_recipe_link()
            self.follow_through_prompt(self.expiring_ingredients)

    def follow_through_prompt(self, chosen_list):
        run = True
        while run:
            decision = input(f"Do you plan to consume or make something with {chosen_list} today? If yes, Computer shall update the fridge inventory accordingly."
                             "\nType 'Y' for Yes or 'N' for No: ").upper().strip()
            if decision == "Y":
                run = False
                print(f"Computer will remove {chosen_list} from your fridge!")
                fridge_data.remove_used_item(chosen_list)
            elif decision == "N":
                run = False
                print("Thank you for your answer. The fridge inventory will be kept as is.")
            else:
                print("That is not a valid answer, please try again.")

    def reset_computer_choices(self):
        fridge_data.fridge_data = {}
        self.expiring_ingredients = []
        self.expiring_meals = []
        self.upcoming_expiration = ""






