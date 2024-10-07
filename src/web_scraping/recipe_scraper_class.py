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

        self.title = None
        self.ingredients = []
        self.serves = None
        self.cooking_time = None
        self.difficulty = None
        self.image_url = None

    def fetch_page(self):
        """
        Fetches the webpage content from the provided URL.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            self.page = response.content
            self.soup = BeautifulSoup(self.page, "html.parser")

        elif response.status_code == 429:
            print(f"\tRate limited. Waiting 30 seconds before retrying {self.url}")
            time.sleep(30)
            self.fetch_page()

        else:
            raise Exception(f"Failed to retrieve page: {response.status_code}")

    def parse_recipe(self):
        try:
            TITLE_CSS_SELECTOR = "div.pb-32 h1.type-h2"
            INGREDIENTS_CSS_SELECTOR = "div.ingredients-rich-text p.type-body"
            IMAGE_CSS_SELECTOR = (
                "img.media.recipe-page__image.astro-awyk7vzs.astro-ntkhkmnr"
            )
            DETAILS_CSS_SELECTOR = "div.recipe-facts__container .recipe-fact__item"
            SUB_DETAILS_CSS_SELECTOR = "h6.type-subtitle-sm"

            # Extract title
            try:
                self.title = self.soup.select_one(TITLE_CSS_SELECTOR).get_text(
                    strip=True
                )
            except AttributeError:
                self.title = None

            # Extract details (cooking time, difficulty and serves)
            try:
                facts = self.soup.select(DETAILS_CSS_SELECTOR)
                for fact in facts:
                    text = (
                        fact.select_one(SUB_DETAILS_CSS_SELECTOR)
                        .get_text(strip=True)
                        .lower()
                    )
                    lower_text = text.lower()

                    if "serves" in lower_text or "makes" in lower_text:
                        self.serves = text

                    elif "hr" in lower_text or "min" in lower_text:
                        self.cooking_time = text
                    else:
                        self.difficulty = text

            except AttributeError:
                self.cooking_time = None
                self.serves = None
                self.difficulty = None

            # Extract ingredients
            try:
                ingredient_elements = self.soup.select(INGREDIENTS_CSS_SELECTOR)
                self.ingredients = [
                    ingredient.get_text(strip=True)
                    for ingredient in ingredient_elements
                ]
            except Exception as e:
                self.ingredients = []

            # Extract image URL
            try:
                self.image_url = self.soup.select_one(IMAGE_CSS_SELECTOR)["src"]
            except (AttributeError, TypeError):
                self.image_url = None

        except Exception as e:
            print(f"Error parsing the recipe from {self.url}: {e}")

    def to_dict(self):
        return {
            "Recipe title": self.title,
            "Ingredients": self.ingredients,
            "Serves": self.serves,
            "Cooking time": self.cooking_time,
            "Difficulty": self.difficulty,
            "Image URL": self.image_url,
            "Recipe URL": self.url,
        }

    def get_recipe_info(self):
        self.fetch_page()
        self.parse_recipe()
