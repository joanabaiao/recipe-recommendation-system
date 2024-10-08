import streamlit as st
import ast
from PIL import Image
import re
from nltk.stem import WordNetLemmatizer

from src.recommendation.get_top_recipes import get_top_recipes
from src.recommendation.get_ingredient_names import get_ingredient_names

lemmatizer = WordNetLemmatizer()


def ingredients_to_bold(ingredients_list, recipe_ingredients, lemmatizer):

    ingredients_list_words = [lemmatizer.lemmatize(word) for word in ingredients_list]
    recipe_ingredients_words = [
        [lemmatizer.lemmatize(word) for word in ingredient.split(" ")]
        for ingredient in recipe_ingredients
    ]
    recipe_ingredients_bold = []
    for count, recipe_ing in enumerate(recipe_ingredients_words):
        ing_input = False
        for input_ing in ingredients_list_words:
            if input_ing in recipe_ing:
                ing_input = True

        if ing_input:
            recipe_ingredients_bold.append(f"**{recipe_ingredients[count]}**")
        else:
            recipe_ingredients_bold.append(recipe_ingredients[count])

    return recipe_ingredients_bold


################################################################################################

# Display the image
image1 = Image.open("docs/recipe.jpg")
st.image(image1)

st.title("Recipe Recommendation System")

# User input for ingredients
ingredients_input = st.text_input("Enter ingredients (comma-separated):")
num_recipes = st.number_input(
    "Number of recipes to display:", min_value=1, max_value=20, value=5
)

if st.button("Recommend recipes"):
    if ingredients_input:
        with st.spinner("Searching for recipes..."):
            ingredients_list = [
                ingredient.strip() for ingredient in ingredients_input.split(",")
            ]
            top_recipes = get_top_recipes(ingredients_list, n_recipes=int(num_recipes))

            if top_recipes.empty:
                st.subheader("No recipes found")
                st.write(
                    "Sorry, we couldn't find any recipes that match your ingredients."
                )

            else:
                st.subheader("Recommended Recipes:")
                for i, (index, row) in enumerate(top_recipes.iterrows(), start=1):

                    # Recipe name
                    st.markdown(
                        f"<h4 style='font-size: 22px;'>{i}. <a href='{row['Recipe URL']}' target='_blank'>{row['Recipe title']}</a></h4>",
                        unsafe_allow_html=True,
                    )

                    col1, col2 = st.columns([2, 1])

                    with col1:

                        # Ingredients as bullet points
                        recipe_ingredients = row["Ingredients"]
                        if not isinstance(recipe_ingredients, list):
                            recipe_ingredients = ast.literal_eval(recipe_ingredients)

                        recipe_ingredients_bold = ingredients_to_bold(
                            ingredients_list, recipe_ingredients, lemmatizer
                        )

                        ingredients_bullets = "\n".join(
                            f"- {ingredient}" for ingredient in recipe_ingredients_bold
                        )  # Create bullet points
                        st.markdown(f"**Ingredients:**\n{ingredients_bullets}")

                        # Display additional information
                        if row["Serves"]:
                            servings = re.search(
                                r"(serves|makes)\s+(\d+)", row["Serves"], re.IGNORECASE
                            ).group(2)
                            st.write(f"**Servings:** {servings}")

                        if row["Cooking time"]:

                            time_str = re.sub(
                                r"(\d+)\s*hr", r"\1 hour", row["Cooking time"]
                            )
                            time_str = re.sub(r"(\d+)\s*mins", r"\1 minutes", time_str)

                            st.write(f"**Cooking time:** {time_str}")

                        if row["Difficulty"]:
                            st.write(
                                f"**Difficulty:** {row['Difficulty'].capitalize()}"
                            )

                    with col2:
                        if row["Image URL"]:
                            try:
                                st.image(row["Image URL"], use_column_width=True)
                            except Exception as e:
                                print(f"Error displaying image: {e}")

                    st.write("---")

    else:
        st.warning("Please enter some ingredients.")
