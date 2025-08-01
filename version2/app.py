from pydantic import BaseModel, HttpUrl
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# first endpoint 
from llm import get_recipe_names 
from cookpad_search import get_first_cookpad_link ,  get_all_cookpad_link,extract_aggregrated_ingredients 
from llm import get_unique_aggregated_line_items, convert_ingredients_to_lineitems
from instacart import format_ingredients_to_instacart,  get_instacart_url 
app = FastAPI()
# CORS setup (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow only your domain later
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
@app.post("/")
def read_root():
    return {"msg": "API is running"}

# schema - endpoint 1 
# input
class EatingConstraint(BaseModel):
    constraint: str 
# output
class RecipeUrls(BaseModel):
    urls: List[HttpUrl]

# definition 
def get_recipe_url(user_eating_constraint:str):
    recipe_names  = get_recipe_names(user_eating_constraint)
    recipe_links  = get_all_cookpad_link(recipe_names)
    return recipe_links 


# endpoint
@app.post("/recipes/recommend", response_model=RecipeUrls)
async def recommend_recipes(input: EatingConstraint):
    user_input_constraint = input.constraint
    recipe_links = get_recipe_url(user_input_constraint)
    
    # filter out None values
    clean_links = [link for link in recipe_links if link is not None]
    
    # if fewer than 4, pad with placeholder urls
    while len(clean_links) < 4:
        clean_links.append("https://example.com/placeholder")

    return {"urls": clean_links}


# ==========================================
# SECTION: ENDPOINT 1 
# ==========================================
class RecipeUrlsIn(BaseModel):
    urls: List[HttpUrl]

 



@app.post("/cart")
async def process_recipes(input: RecipeUrlsIn):
    # you receive the urls from previous step
    received_urls = input.urls

    received_urls = [str(url) for url in input.urls]

    all_recipe_info = extract_aggregrated_ingredients(received_urls)
    all_ingredients = get_unique_aggregated_line_items( all_recipe_info )
    format_ingr = convert_ingredients_to_lineitems(all_ingredients)

    instacart_ingr = format_ingredients_to_instacart(format_ingr)
    
    instacart_cart_url = get_instacart_url(instacart_ingr)
    return instacart_cart_url