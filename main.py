from entry_mode import EntryMode
from challenge_mode import ChallengeMode
from computer_choice import ComputerChoice

entry_mode = EntryMode()
challenge_mode = ChallengeMode()
computer_choice = ComputerChoice()


def user_action():
    run = True
    while run:
        action = input("Type '1' for fridge entry, '2' for challenge mode, or '3' for computer's choice: ").strip()
        try:
            action = int(action)
        except ValueError:
            print("Please type a number!")
        else:
            if action == 1:
                run = False
                entry_mode.fridge_entry()
            elif action == 2:
                run = False
                challenge_mode.challenge_mode()
                challenge_mode.reset_challenge_mode()
            elif action == 3:
                run = False
                computer_choice.pick_prompt()
                computer_choice.reset_computer_choices()
            else:
                print("Please type a valid number!")


def another_action_prompt():
    run = True
    while run:
        run_again_prompt = input("Would you like to do something else? Type 'Y' for Yes or 'N' for No: ")
        try:
            run_again_prompt = run_again_prompt.upper()
        except ValueError:
            print("Please type a letter!")
        else:
            if run_again_prompt == "N":
                return False
            elif run_again_prompt == "Y":
                return True
            else:
                print("Please type a valid letter!")


running = True
while running:
    print("Welcome To Fridge Cleaner 🍕\n"
          "Are you ready to prepare some kick ass meals while reducing food waste and saving money?")
    user_action()
    if not another_action_prompt():
        running = False
