import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json
import time
import os
import pickle

from utils.recipe_scraper_class import RecipeScraper
from constants import *


def get_recipes_details(recipe_urls):

    recipe_data = []
    for idx, url in enumerate(recipe_urls["recipe_urls"], start=1):
        print(f"Processing recipe {idx}: {url}")
        recipe_scraper = RecipeScraper(url)
        recipe_scraper.get_recipe_info()
        recipe_data.append(recipe_scraper.to_dict())

        # Sleep for 10 minutes every 400 requests
        if idx % 400 == 0:
            print("\nReached 400 requests. Sleeping for 10 minutes...\n")
            time.sleep(600)  # Sleep for 600 seconds (10 minutes)

    df_recipes_info = pd.DataFrame(recipe_data)

    return df_recipes_info


################################################################


def main():
    recipe_urls = pd.read_csv(URLS_PATH)
    print(f"Number of recipes: {len(recipe_urls)}")

    df_recipes = get_recipes_details(recipe_urls)
    df_recipes.to_excel(RAW_RECIPES_PATH, index=False)
    print(f"Recipes details successfully saved to: {RAW_RECIPES_PATH}")


if __name__ == "__main__":
    main()
