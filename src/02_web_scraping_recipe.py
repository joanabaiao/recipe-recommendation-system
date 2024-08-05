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

urls_file_path = os.path.join(RAW_DATA_DIR, "recipe_urls.csv")
    
recipe_urls = pd.read_csv(urls_file_path)
print(f"Number of recipes: {len(recipe_urls)}")

# Get data for all the links
recipe_data = []
for idx, url in enumerate(recipe_urls['recipe_urls'], start=1):
    print(f"Processing recipe {idx}: {url}")
    recipe_scraper = RecipeScraper(url)
    recipe_scraper.get_recipe_info()
    recipe_data.append(recipe_scraper.to_dict())
    
    # Sleep for 10 minutes every 400 requests
    if idx % 400 == 0:
        print("\nReached 400 requests. Sleeping for 10 minutes...\n")
        time.sleep(600)  # Sleep for 600 seconds (10 minutes)

recipe_info_df = pd.DataFrame(recipe_data)

with open('df.pkl', 'wb') as f:
    pickle.dump(recipe_info_df, f)
    
# Save data
file_path="data/raw/recipes_info.xlsx"
recipe_info_df.to_excel(file_path, index=False)
print(f"URLs saved to {file_path}")