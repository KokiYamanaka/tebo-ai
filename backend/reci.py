from recipe_title import RecipeTitleGenerator
from vector_recipe import SimilarTitle
from rank import RankedRecipe
from render import RecipeEnricher
import gc 

def get_recipe(user_input: str):
    try:
        # # Step 1: Generate title
        # title_generator = RecipeTitleGenerator()
        # title = title_generator.to_title(user_input)
        # del title_generator

    
        # Step 2: Find similar titles
        similar_title_instance = SimilarTitle()
        similar_titles = similar_title_instance.get_top_k(user_input)
        # del title
        gc.collect()

        # Step 3: Rank recipes
        rank_inst = RankedRecipe(top_k_recipes=similar_titles)
        ordered_titles = rank_inst.get_sorted_titles(top_n=4)
        reordered_recipes = [
            d for title in ordered_titles for d in similar_titles if d["title"] == title
        ]
        del similar_titles, ordered_titles, rank_inst
        gc.collect()

        # Step 4: Add metadata
        metadata_instance = RecipeEnricher(reordered_recipes)
        final_recipes = metadata_instance.enrich()
        del metadata_instance, reordered_recipes
        gc.collect()

        return {"results": final_recipes}

    finally:
        gc.collect()
    
# res = get_recipe("chicken spicy")  
# print(res)