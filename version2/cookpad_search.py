# struct 
from typing import List, Dict, Any

# web parser
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# EXTERNAL TOOL 
from recipe_scrapers import scrape_me
 


# ==========================================
# SECTION: RECIPE NAMES -> RECIPE URL COOKPAD 
# ==========================================

# get first cook pad recipe after search 
def get_first_cookpad_link(search_keyword: str) -> str: 
    encoded = quote(search_keyword)
    url = f"https://cookpad.com/search/{encoded}"
    headers = {"User-Agent": "Mozilla/5.0"}  # polite header
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    first = soup.select_one("a.block-link__main")
    if first:
        return f"https://cookpad.com{first['href']}"
    return None

# auto translate cookpad ja -> eng  
def make_google_translate_link(japanese_url: str) -> str:
    base = "https://translate.google.com/translate"
    params = f"?sl=ja&tl=en&u={japanese_url}"
    return base + params

# use 
def get_all_cookpad_link(recipe_names:List[str]) -> List[str]:
    recipe_links = []
    for recipe_name in recipe_names: 
        # first cook pad -> auto translate page 
        recipe_links.append((get_first_cookpad_link(recipe_name))) 
    return recipe_links 

 



# ==========================================
# SECTION: RECIPE URL COOKPAD -> RECIPE WITH INSTRUCTIONS + INGREDIENTS 
# ==========================================
# def 
def extract_ingredients(recipe_url:str) -> Dict[str, Any]: 
    scraper = scrape_me(recipe_url)
    scraper.title()
    scraper.instructions()
    extract_recipe_info = scraper.to_json()   
    return extract_recipe_info 

# use 
def extract_aggregrated_ingredients(recipe_urls:List[str]) ->  List[Dict[str, Any]]: 
    all_recipe_info = []
    for recipe_url in recipe_urls:
        recipe_info = extract_ingredients(recipe_url)
        all_recipe_info.append(recipe_info) 
    return all_recipe_info 

 

# recipe_urls  = ['https://cookpad.com/jp/recipes/21228423', 'https://cookpad.com/jp/recipes/18997429', 'https://cookpad.com/jp/recipes/24834680', 'https://cookpad.com/jp/recipes/21786154']
# recipe_info = extract_aggregrated_ingredients(recipe_urls)
# print(recipe_info)