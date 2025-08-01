from .schema import Ingredient, IngredientSummary 
from .transform_recipes import RecipeProcessor 
from google import genai
from typing import Optional

GEMINI_API_KEY = ""  # Replace with your actual API key

def structure_llm(recipe_data : str, api_key: str = GEMINI_API_KEY , model: str = "gemini-1.5-flash") -> Optional[str]:
    """
    Sends a prompt to Gemini and parses the structured JSON output based on the IngredientSummary schema.

    Args:
        prompt (str): The instruction to send to Gemini.
        api_key (str): Your Gemini API key.
        model (str): The Gemini model to use. Default is "gemini-2.0-flash".

    Returns:
        Optional[str]: The raw JSON response text or None if an error occurred.
    """
    
    # get ingredients, quantities, servings data out
    prompt = "# Task Description\nAct as a precise data-cleaning, translation, categorization, and cost estimation assistant for Japanese recipes. You will be provided with multiple recipes, each listing ingredients in Japanese using \"name\" and \"quantity\" fields.\n\n## Tasks\n- Translate each ingredient name into accurate English for cooking.\n- Convert quantity units into natural English equivalents. Examples: \"大さじ1\" → \"1 tablespoon\", \"適量\" → \"to taste\".\n- Combine ingredient lists across all recipes.\n- Merge duplicates or similar ingredients, such as: \"鶏胸肉\" and \"鶏胸肉（皮なし）\" → \"Skinless Chicken Breast\".\n\n## Aggregation Rules\n- **High Accuracy Required (Meat & Vegetables):** Sum exact quantities from all recipes. For items counted in 'pieces', 'sheets', etc., sum precisely. If a vegetable lacks quantity, assume default \"2 pieces\".\n- **Acceptable Minor Inaccuracies (Seasonings, Oils & Fats, Others):** For specific measurements (teaspoons, tablespoons), sum precisely. For vague quantities ('a little', 'to taste'), consolidate similarly vague mentions. Combine specific and vague quantities descriptively if both appear (e.g., \"1 piece + 1/2 teaspoon and a little more\"). Prioritize summing specific measurements first.\n\n## Store Package Estimation\nFor each item:\n- Estimate typical store package size available in Vancouver, Canada, as \"store_package_quantity\".\n- Estimate full price of the store package in CAD as \"store_package_price\".\n\n## Baseline Grocery Prices (updated June 2025)\n| Item | Quantity | Price (CAD) |\n| :--- | :--- | :--- |\n| Milk, 2% | 2 Litres | $4.84 |\n| Large White Eggs | 12 pack | $3.93 |\n| Yellow Onions | 3 lb bag | $3.47 |\n| Silver Swan Soy Sauce | 1 Litre | $2.77 |\n| Delicious Kitchen Jasmine Rice | 8 kg | $18.97 |\n\n## Classification\nClassify each item into: \"Meat\", \"Vegetables\", \"Seasonings\", \"Oils & Fats\", or \"Others\".\n\n## Output Format\nReturn a clean JSON object using this structure:\n```\n{\n  \"Meat\": [\n    {\"name\": \"Skinless Chicken Breast\", \"quantity\": \"350g\", \"store_package_quantity\": \"1kg\", \"store_package_price\": \"10.99 CAD\"}\n  ],\n  \"Vegetables\": [...],\n  \"Seasonings\": [...],\n  \"Oils & Fats\": [...],\n  \"Others\": [...],\n  \"Total_Store_Cost_CAD\": \"35.42 CAD\",\n  \"Total_Store_Cost_Excluding_Seasonings_CAD\": \"27.10 CAD\"\n}\n```\n\n## Special Notes\n- Do not include recipe metadata (titles, steps).\n- Merge known equivalents:\n  - \"鶏胸肉\" = \"Skinless Chicken Breast\"\n  - Any item containing \"塩麹\" = \"Salt Koji\"\n  - \"シュガーカットゼロ\" or \"砂糖代替品\" = \"Sugar Substitute\"\n- Do not calculate partial prices; use full store package prices for totals.\n\n## Recipes Provided\n"

    prompt += str(recipe_data) 


    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": IngredientSummary,
            },
        )

        return response.parsed  # This is a parsed Pydantic object (IngredientSummary)

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def get_ingredient_summary(get_recipe_endpoint_data):

    # get extra metadata from endpoint payload
    processor = RecipeProcessor(get_recipe_endpoint_data)
    processor.run()
    transf_data = processor.get_results()
    
    # get aggregrated ingredient 
    result = structure_llm(recipe_data=transf_data)

    # convert to python dict  
    return result.model_dump()

# if __name__ == "__main__":
#     sample_data = {
#     "results": [
#         {
#         "id": "18925863",
#         "score": 0.881210506,
#         "category": "お肉のおかず",
#         "title": "鶏肉の塩麹焼き",
#         "url": "https://cookpad.com/jp/recipes/18925863-%E9%B6%8F%E8%82%89%E3%81%AE%E5%A1%A9%E9%BA%B9%E7%84%BC%E3%81%8D",
#         "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/18925863-%E9%B6%8F%E8%82%89%E3%81%AE%E5%A1%A9%E9%BA%B9%E7%84%BC%E3%81%8D",
#         "image_url": "https://img-global-jp.cpcdn.com/recipes/3410371/480x680cq50/%E9%B6%8F%E8%82%89%E3%81%AE%E5%A1%A9%E9%BA%B9%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
#         "title_en": "Shio-koji grilled chicken"
#         },
#         {
#         "id": "17917280",
#         "score": 0.832703412,
#         "category": "お肉のおかず",
#         "title": "鶏のごま味噌焼き♪",
#         "url": "https://cookpad.com/jp/recipes/17917280-%E9%B6%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%84%BC%E3%81%8D",
#         "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/17917280-%E9%B6%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%84%BC%E3%81%8D",
#         "image_url": "https://img-global-jp.cpcdn.com/recipes/4030490/480x680cq50/%E9%B6%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
#         "title_en": "Grilled chicken with sesame miso♪"
#         },
#         {
#         "id": "18558237",
#         "score": 0.820684791,
#         "category": "お肉のおかず",
#         "title": "鶏胸肉のホイル焼き",
#         "url": "https://cookpad.com/jp/recipes/18558237-%E9%B6%8F%E8%83%B8%E8%82%89%E3%81%AE%E3%83%9B%E3%82%A4%E3%83%AB%E7%84%BC%E3%81%8D",
#         "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/18558237-%E9%B6%8F%E8%83%B8%E8%82%89%E3%81%AE%E3%83%9B%E3%82%A4%E3%83%AB%E7%84%BC%E3%81%8D",
#         "image_url": "https://img-global-jp.cpcdn.com/recipes/4238875/480x680cq50/%E9%B6%8F%E8%83%B8%E8%82%89%E3%81%AE%E3%83%9B%E3%82%A4%E3%83%AB%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
#         "title_en": "Chicken breast grilled in foil"
#         },
#         {
#         "id": "18187363",
#         "score": 0.87925142,
#         "category": "お肉のおかず",
#         "title": "鶏の照り焼き",
#         "url": "https://cookpad.com/jp/recipes/18187363-%E9%B6%8F%E3%81%AE%E7%85%A7%E3%82%8A%E7%84%BC%E3%81%8D",
#         "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/18187363-%E9%B6%8F%E3%81%AE%E7%85%A7%E3%82%8A%E7%84%BC%E3%81%8D",
#         "image_url": "https://img-global-jp.cpcdn.com/recipes/2154458/480x680cq50/%E9%B6%8F%E3%81%AE%E7%85%A7%E3%82%8A%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
#         "title_en": "Chicken teriyaki"
#         }
#     ]
#     }
#     res = get_ingredient_summary(sample_data) 
#     print(res) 

