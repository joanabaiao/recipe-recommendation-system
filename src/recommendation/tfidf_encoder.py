import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle 
import os
import joblib

from src.constants import *

# Load the parsed recipe dataset.
df_recipes = pd.read_excel(PROCESSED_RECIPES_PATH)

# TF-IDF feature extractor 
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df_recipes["Ingredients_processed_str"])

# Save the TF-IDF vectorizer and matrix
joblib.dump(vectorizer, TDIDF_MODEL_PATH)
joblib.dump(tfidf_matrix, TDIDF_MATRIX_PATH)

    
feature_names = vectorizer.get_feature_names_out()
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

print("TF-IDF Matrix:")
print(tfidf_df.head())

