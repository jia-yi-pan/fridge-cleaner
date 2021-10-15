from recipe_requester import RecipeRequester
from fridge_data import FridgeData

fridge_data = FridgeData(access_mode="challenge")
recipe_requester = RecipeRequester()

class ChallengeMode:
    def __init__(self):
        self.chosen_level = 0

    def pick_difficulty_prompt(self):
        run = True
        while run:
            chosen_level = input(
                "Choose your difficultly level? Enter '1' for easy, '2' for medium, '3' for hard: ").strip()
            try:
                chosen_level = int(chosen_level)
            except ValueError:
                print("Please type a number!")
            else:
                if 0 < chosen_level < 4:
                    run = False
                    self.chosen_level = chosen_level
                else:
                    print("That is not a valid number, please try again.")

    def challenge_mode(self):
        import random
        print("Welcome to Challenge Mode!")
        print("Instructions: You will be challenged to incorporate certian ingredients in your dish based on your chosen difficulty level.")
        self.pick_difficulty_prompt()
        if fridge_data.find_items():
            list_for_chef = []
            if len(fridge_data.full_ingredient_list) < self.chosen_level:
                list_for_chef = fridge_data.full_ingredient_list
                print(f"Your fridge only has {len(fridge_data.full_ingredient_list)} ingredient(s) and you requested {self.chosen_level}!"
                      f"\nComputer can only challenge you on what you have! Your updated task is to make something with: {list_for_chef}")
            else:
                full_ingredient_list = fridge_data.full_ingredient_list
                for num in range(self.chosen_level):
                    random_ingredient = random.choice(full_ingredient_list)
                    list_for_chef.append(random_ingredient)
                    full_ingredient_list.remove(random_ingredient)
                print(f"We challenge you to make something delicious and nutritious with: {list_for_chef}")
            self.challenge_decision_prompt(list_for_chef)

    def challenge_decision_prompt(self, list_for_chef):
        run = True
        while run:
            decision = input("Will you accept this challenge? If you choose to accept, Computer shall update the fridge inventory accordingly."
                             "\nType 'A' for Accept 'D' for Decline: ").upper().strip()
            if decision == "A":
                run = False
                print(f"Computer will remove {list_for_chef} from your fridge!")
                fridge_data.remove_used_item(list_for_chef)
            elif decision == "D":
                run = False
                print("Thank you for your answer. The fridge inventory will be kept as is.")
            else:
                print("That is not a valid answer, please try again.")

    def reset_challenge_mode(self):
        fridge_data.full_ingredient_list = []
