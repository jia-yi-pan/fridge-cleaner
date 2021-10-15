import requests
from selenium import webdriver
import random

CHROME_DRIVER_PATH = r"C:\Users\thepa\OneDrive\Desktop\Coding\chromedriver.exe"
GOOGLE_URL = "https://www.google.com/"

INGREDIENTS_URL = "https://api.spoonacular.com/recipes/findByIngredients"
RECIPE_URL = "https://api.spoonacular.com/recipes/"
API_KEY = "GET FREE API KEY @ https://spoonacular.com/food-api"

class RecipeRequester:
    def __init__(self):
        self.ingredient_list = []
        self.recipes_list = []
        self.selected_recipe = ""
        self.selected_recipe_id = ""
        self.selected_recipe_link = ""

    def get_recipes(self):
        if len(self.ingredient_list) > 1:
            ingredients_query = ",".join(self.ingredient_list)
        else:
            ingredients_query = self.ingredient_list[0]

        query = {
            "apiKey": API_KEY,
            "ingredients": ingredients_query
        }

        results = requests.get(url=INGREDIENTS_URL, params=query).json()
        self.recipes_list = [{recipe["title"]: recipe["id"]} for recipe in results]

    def choose_random_recipe(self):
        self.get_recipes()
        random_recipe = random.choice(self.recipes_list)
        for k,v in random_recipe.items():
            self.selected_recipe = k
            self.selected_recipe_id = str(v)

    def find_recipe_link(self):
        query = {
            "apiKey": API_KEY,
        }
        results = requests.get(url=f"https://api.spoonacular.com/recipes/{self.selected_recipe_id}/information", params=query).json()
        self.selected_recipe_link = results["spoonacularSourceUrl"]

    def open_recipe_link(self):
        self.find_recipe_link()
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        driver.maximize_window()
        driver.get(self.selected_recipe_link)




