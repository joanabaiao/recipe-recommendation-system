import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import json
import time

class RecipeScraper:
    def __init__(self, url):
        self.url = url
        self.page = None
        self.soup = None
        
        self.name = None
        self.ingredients = []
        self.serves = None
        self.cooking_time = None
        self.difficulty = None

    def fetch_page(self):
        """
        Fetches the webpage content from the provided URL.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            self.page = response.content
            self.soup = BeautifulSoup(self.page, 'html.parser')
            
        elif response.status_code == 429:
                print(f"\tRate limited. Waiting 30 seconds before retrying {self.url}")
                time.sleep(30)
                self.fetch_page()
                
        else:
            raise Exception(f"Failed to retrieve page: {response.status_code}")

    def extract_cooking_time(self):
        """
        Extracts the cooking time from the recipe webpage.
        """
        cooking_time_tag = self.soup.find('div', {'class': 'recipe-detail time'})
        if cooking_time_tag:
            self.cooking_time = cooking_time_tag.text.split('In')[1].strip()

    def extract_difficulty(self):
        """
        Extracts the difficulty level from the recipe webpage.
        """
        difficulty_tag = self.soup.find('div', {'class': 'col-md-12 recipe-details-col remove-left-col-padding-md'})
        if difficulty_tag:
            self.difficulty = difficulty_tag.text.split('Difficulty')[1].strip()

    def extract_recipe_data(self):
        """
        Extracts recipe name, serves, and ingredients from JSON-LD structured data.
        """
        script_tag = self.soup.find('script', type='application/ld+json')
        if script_tag:
            try:
                json_data = json.loads(script_tag.string)
                self.name = json_data.get('name')
                self.serves = json_data.get('recipeYield')
                self.ingredients = json_data.get('recipeIngredient')
                #'instructions': BeautifulSoup(json_data.get('recipeInstructions', ''), 'html.parser').get_text(),
                #'cuisine': json_data.get('recipeCuisine'),
                #'keywords': json_data.get('keywords'),
                #'description': json_data.get('description'),
                #'suitable_for_diet': json_data.get('suitableForDiet'),
                #'author': json_data.get('author', {}).get('name'),
                #'nutrition': json_data.get('nutrition'),
                #'date_published': json_data.get('datePublished'),
                #'images': json_data.get('image'),
                #'video': json_data.get('video', 'contentUrl')
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")

    def get_recipe_info(self):
        """
        Main function to fetch and extract all necessary recipe information.
        """
        self.fetch_page()
        self.extract_cooking_time()
        self.extract_difficulty()
        self.extract_recipe_data()

    def to_dict(self):
        """
        Converts recipe information into a dictionary format.
        """
        return {
            'Recipe Name': self.name,
            'Ingredients': self.ingredients,
            'Serves': self.serves,
            'Cooking Time': self.cooking_time,
            'Difficulty': self.difficulty,
            'URL': self.url
        }