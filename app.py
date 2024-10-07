import streamlit as st
import ast
from PIL import Image
import re
from src.recommendation.get_top_recipes import get_top_recipes
from src.recommendation.get_ingredient_names import get_ingredient_names

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

            if not top_recipes.empty:
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

                        ingredients_bullets = "\n".join(
                            f"- {ingredient}" for ingredient in recipe_ingredients
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
                            st.image(row["Image URL"], use_column_width=True)

                    st.write("---")
            else:
                st.write("No recipes found with the given ingredients.")
    else:
        st.warning("Please enter some ingredients.")
