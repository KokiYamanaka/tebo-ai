import os

# Base path of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Recipe title vector search
VECTOR_DATABASE_PATH = os.path.join(BASE_DIR, "data", "vector_recipe.index")
METADATA_PATH = os.path.join(BASE_DIR, "data", "metadata_recipe.pkl")

# Ingredient vector search
INGREDIENT_VECTOR_DATABASE_PATH = os.path.join(BASE_DIR, "data", "vector_ingredient.pkl")

# Recipe metadata (id, title, ingredients)
RECIPE_METATDATA_PATH = os.path.join(BASE_DIR, "data", "recipes_meat_2000.json")
