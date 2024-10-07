import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import re
from nltk.tokenize import word_tokenize
import pandas as pd
import ast
import nltk
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter

from src.constants import *

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def get_ingredient_names(ingredients_list):
    ingredient_names = []
    ingredient_names_str = ""
    
    if not isinstance(ingredients_list, list):
        ingredients_list = ast.literal_eval(ingredients_list)

    for item in ingredients_list:

        item = item.lower()  # Convert to lower case
        item = re.sub(r"\(.*?\)", "", item)  # Remove content within parentheses
        item = re.sub(r"\s+", " ", item).strip()  # Remove additional white space

        tokens = word_tokenize(item)  # Tokenize the item
        tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatize tokens
        filtered_tokens = [
            word
            for word in tokens
            if word.isalpha()  # Keep only alphabetic tokens
            and word not in stop_words  # Remove stopwords
            and word not in MEASUREMENT_UNITS  # Remove measurement units
            and word not in WORDS_TO_REMOVE  # Remove additional words
        ]

        if filtered_tokens:
            ingredient = " ".join(filtered_tokens)
            ingredient_names.append(ingredient.strip())
            ingredient_names_str = ingredient_names_str + ingredient.strip() + " "

    return ingredient_names, ingredient_names_str


################################################################


def main():

    df_recipes = pd.read_excel(RAW_RECIPES_PATH)
    df_recipes.dropna(subset=["Ingredients"], inplace=True)

    df_recipes[['Ingredients_processed', 'Ingredients_processed_str']] = df_recipes['Ingredients'].apply(
            lambda x: pd.Series(get_ingredient_names(x))
    )

    df_recipes.to_excel(PROCESSED_RECIPES_PATH, index=False)
    print(f"Recipes details successfully saved to: {PROCESSED_RECIPES_PATH}")


if __name__ == "__main__":
    main()
