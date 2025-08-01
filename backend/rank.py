import numpy as np

from path import INGREDIENT_VECTOR_DATABASE_PATH, RECIPE_METATDATA_PATH


import pickle

 
from typing import List
import json 
 
class SimilarityCalculator:
    """This class calculates the similarity score between two ingredients based on their vector representations."""

    _ingredient_vectors = None  # class-level cache

    def __init__(self):
        # Load vectors only once across all instances
        if SimilarityCalculator._ingredient_vectors is None:
            with open(INGREDIENT_VECTOR_DATABASE_PATH, "rb") as f:
                SimilarityCalculator._ingredient_vectors = pickle.load(f)

        self.ingredient_vectors = SimilarityCalculator._ingredient_vectors

    def get_similarity_score(self, ingr_source: str, ingr_target: str) -> float:
        vec_source = self.ingredient_vectors.get(ingr_source)
        vec_target = self.ingredient_vectors.get(ingr_target)

        if vec_source is None or vec_target is None:
            raise ValueError(f"Missing vector for: {ingr_source} or {ingr_target}")

        vec_source = np.array(vec_source).reshape(1, -1)
        vec_target = np.array(vec_target).reshape(1, -1)

        # cosine similarity
        return float(
            np.dot(vec_source, vec_target.T) /
            (np.linalg.norm(vec_source) * np.linalg.norm(vec_target))
        )


class OverlapIngRate:
    """This class calculates the overlap rate between two sets of ingredients."""
    def __init__(
        self,
        recipe_source: List[str],
        recipe_target: List[str],
        threshold: float = 0.8 # threshold for ingredient similarity score
    ):
        self.recipe_source = recipe_source
        self.recipe_target = recipe_target
        self.sim = SimilarityCalculator()
        self.threshold = threshold

    def get_overlap_rate(self) -> float:
        used_target_idxs = set()
        match_count = 0

        # for each ingredient in recipe_source...
        for ingr_src in self.recipe_source:
            best_score = 0.0
            best_j = None

            # ...compare against each unused ingredient in recipe_target
            for j, ingr_tgt in enumerate(self.recipe_target):
                if j in used_target_idxs:
                    continue
                try:
                    score = self.sim.get_similarity_score(ingr_src, ingr_tgt)
                except ValueError:
                    continue  # skip if either vector is missing

                # keep the best-scoring candidate above threshold
                if score > best_score and score >= self.threshold:
                    best_score = score
                    best_j = j

            # if we found a match, lock that target and count it
            if best_j is not None:
                used_target_idxs.add(best_j)
                match_count += 1

        # avoid division by zero
        if not self.recipe_source:
            return 0.0

        return match_count / len(self.recipe_source)

class RankedRecipe:
    """This class ranks recipes based on their overlap rate with a given recipe."""
    def __init__(self, top_k_recipes: List[str]):
        # vector search recipe titles
        self.top_k_recipes = self.extract_titles(top_k_recipes)
        # recipes titles and their metadata (id, title, ingredients)
        self.title_to_ingredients = self._create_recipe_ingredients(self.top_k_recipes) 
        # get the first recipe as source and the rest as targets
        self.recipe_src , self.recipe_targets = self._separate_source_target()
        # get overlap rates between source and targets 
        self.overlap_rates  = self._get_overlap_rates()

    def extract_titles(self,top_k_recipes) -> list[str]:
        return [item["title"] for item in top_k_recipes if "title" in item]
    
    def _create_recipe_ingredients(self, recipe_titles: dict) -> List[str]:
        """Extracts ingredients from a recipe dictionary."""
        
        with open(RECIPE_METATDATA_PATH, "r", encoding="utf-8") as f:
            recipe_data = json.load(f)

        # Build a lookup table for fast access
        title_lookup = {r["title"]: r["ingredients"] for r in recipe_data}

        # Reconstruct ordered dict based on input list
        title_to_ingredients = {
            title: title_lookup[title]
            for title in recipe_titles
            if title in title_lookup
        }   

        return title_to_ingredients

    def _separate_source_target(self):
        """Separates the first recipe as the source and the rest as targets."""
        if not self.title_to_ingredients:
            raise ValueError("No recipes available to separate.")

        # Get the first item as source
        var_source = {list(self.title_to_ingredients.items())[0][0]: list(self.title_to_ingredients.items())[0][1]}

        # Get the rest as targets
        var_target = dict(list(self.title_to_ingredients.items())[1:])

        return var_source,  var_target

    def _get_overlap_rates(self) -> dict:
        """Calculates overlap rates between the source recipe and each target recipe."""
        fix_recipe_title = list(self.recipe_src.keys())[0]
        fix_recipe_ingredients = list(self.recipe_src.values())[0]
   
        overlap_results = []
        for title, ingredients in self.recipe_targets.items(): 
            overlap_inst = OverlapIngRate(recipe_source=fix_recipe_ingredients,recipe_target=ingredients)
            overlap_rate = overlap_inst.get_overlap_rate() 
            overlap_results.append({"source": fix_recipe_title, "target": title, "overlap_rate": overlap_rate})
    
        return overlap_results
    
    def get_sorted_titles(self,top_n) -> list:
        if not self.overlap_rates:
            return []

        # Get the source title from the first result
        source_title = self.overlap_rates[0]["source"]

        # Sort target recipes by overlap_rate in descending order
        sorted_targets = sorted(self.overlap_rates, key=lambda x: x["overlap_rate"], reverse=True)

        # Compute how many targets to include (subtract 1 for the source)
        num_targets = max(top_n - 1, 0)

        # Extract the target titles
        target_titles = [item["target"] for item in sorted_targets[:num_targets]]

        # Return final list with source at front
        return [source_title] + target_titles 
    
# if __name__ == "__main__":
#     # Example usage
#     top_k_recipes = [
#     "トマトソースの煮込みハンバーグ", 
#     "【基本】フライパンで簡単♪親子丼の黄金比",
#     "✿そぼろ三色丼ぶり✿", 
#     "餃子の焼き方", 
#     "こっくりおいしい豚バラ大根",
#     "簡単おいしい♪基本のハンバーグ"

#     ]   
#     inst = RankedRecipe(top_k_recipes)
#     print(inst.get_sorted_titles()) 
 

 