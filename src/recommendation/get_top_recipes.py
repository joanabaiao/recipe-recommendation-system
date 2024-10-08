import pandas as pd

import joblib
from sklearn.metrics.pairwise import cosine_similarity
from src.recommendation.get_ingredient_names import get_ingredient_names

from src.constants import *

tfidf_vectorizer = joblib.load(TDIDF_MODEL_PATH)
tfidf_matrix = joblib.load(TDIDF_MATRIX_PATH)
df_recipes = pd.read_excel(PROCESSED_RECIPES_PATH)


# Get the top recipes based on cosine similarity
def get_top_recipes(ingredients, n_recipes=5):

    ing_list, ing_str = get_ingredient_names(ingredients)
    tfidf_ing = tfidf_vectorizer.transform([ing_str])
    cos_sim = cosine_similarity(tfidf_ing, tfidf_matrix)

    df_recipes["Cosine Similarity"] = cos_sim.flatten()

    top_recipes = df_recipes.sort_values(by="Cosine Similarity", ascending=False).head(
        n_recipes
    )
    top_recipes = top_recipes[top_recipes["Cosine Similarity"] > 0]

    return top_recipes


################################################################


if __name__ == "__main__":
    test_ingredients = ["codfish"]
    n = 5

    top_recipes = get_top_recipes(test_ingredients, n)
    print(top_recipes[["Recipe title", "Cosine Similarity"]])
