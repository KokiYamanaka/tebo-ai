from typing import Dict 
import json 
import subprocess


from dotenv import load_dotenv
import os 

load_dotenv()  
INSTACART_API_KEY = os.getenv("INSTACART_API_KEY")


def format_ingredients_to_instacart(aggregrated_ingredients :Dict) -> str : 

    full_payload = {
    "title": "3 Protein Shopping List",
    "image_url": "https://example.com/3-proteins.jpg",
    "link_type": "shopping_list",
    "expires_in": 7,
    "instructions": ["Get these proteins for the week."],
    "line_items": aggregrated_ingredients["line_items"],
    "landing_page_configuration": {
        "partner_linkback_url": "https://myapp.example.com/after-shopping",
        "enable_pantry_items": True
        }
    }
    
    full_data_str = json.dumps(full_payload, ensure_ascii=False)
    return full_data_str 

def get_instacart_url(format_ingredients:str) -> str : 
    #Run curl with that string
    curl_command = f"""
    curl --request POST \\
    --url https://connect.dev.instacart.tools/idp/v1/products/products_link \\
    --header 'Accept: application/json' \\
    --header 'Authorization: Bearer {INSTACART_API_KEY}'\\
    --header 'Content-Type: application/json' \\
    --data '{format_ingredients}'
    """
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

    # return string -> convert to json 
    data = json.loads(result.stdout) 
    instacart_url = data['products_link_url']
    return instacart_url 



# aag_ingr = {'line_items': [{'name': 'Salmon', 'quantity': 3, 'unit': 'pieces', 'display_text': 'Raw salmon, 3 pieces', 'line_item_measurements': [{'quantity': 3, 'unit': 'pieces'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Soy Sauce Fermentation Paste', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Salt koji, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Shimeji Mushrooms', 'quantity': 60, 'unit': 'grams', 'display_text': 'Shimeji mushrooms, 60 grams', 'line_item_measurements': [{'quantity': 60, 'unit': 'grams'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Green Onion', 'quantity': 1, 'unit': 'half', 'display_text': 'Half a bunch of green onion', 'line_item_measurements': [{'quantity': 1, 'unit': 'half bunch'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Chicken Breast', 'quantity': 200, 'unit': 'grams', 'display_text': 'Chicken breast, 200 grams', 'line_item_measurements': [{'quantity': 200, 'unit': 'grams'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Potato Starch', 'quantity': 1, 'unit': 'appropriate amount', 'display_text': 'Potato starch, appropriate amount', 'line_item_measurements': [{'quantity': 1, 'unit': 'appropriate amount'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Sake', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Sake, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Noodle Soup Base', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Noodle soup base, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Soy Sauce', 'quantity': 1, 'unit': 'teaspoon', 'display_text': 'Soy sauce, 1 teaspoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'teaspoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Yuzu Kosho', 'quantity': 1, 'unit': 'appropriate amount', 'display_text': 'Yuzu Kosho, to taste', 'line_item_measurements': [{'quantity': 1, 'unit': 'appropriate amount'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Cooked Rice', 'quantity': 2, 'unit': 'cups', 'display_text': 'Cooked rice, 2 cups', 'line_item_measurements': [{'quantity': 2, 'unit': 'cups'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Miso Canned Mackerel', 'quantity': 1, 'unit': 'can', 'display_text': 'Miso canned mackerel, 1 can', 'line_item_measurements': [{'quantity': 1, 'unit': 'can'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Perilla or Green Onion', 'quantity': 1, 'unit': 'appropriate amount', 'display_text': 'Perilla leaves or green onion, to taste', 'line_item_measurements': [{'quantity': 1, 'unit': 'appropriate amount'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Oyster Sauce', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Oyster sauce, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Soy Sauce', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Soy sauce, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Cooking Sake', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Cooking sake, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Mirin', 'quantity': 1, 'unit': 'tablespoon', 'display_text': 'Mirin, 1 tablespoon', 'line_item_measurements': [{'quantity': 1, 'unit': 'tablespoon'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'Ginger Tube', 'quantity': 3, 'unit': 'cm', 'display_text': 'Ginger paste, 3cm', 'line_item_measurements': [{'quantity': 3, 'unit': 'cm'}], 'filters': {'brand_filters': [], 'health_filters': []}}, {'name': 'White Sesame', 'quantity': 1, 'unit': 'pinch', 'display_text': 'White sesame, a pinch', 'line_item_measurements': [{'quantity': 1, 'unit': 'pinch'}], 'filters': {'brand_filters': [], 'health_filters': []}}]}
# ing_str = format_ingredients_to_instacart(aag_ingr)
# res = get_instacart_url(ing_str)
# print(res)