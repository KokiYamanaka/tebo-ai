from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from reci import get_recipe
from ingredients import aggr2 
from typing import List

# from ingr.aggr import some_aggregator_function
 
app = FastAPI()

# CORS setup (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow only your domain later
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/")
def read_root():
    return {"msg": "API is running"}


class RecipeRequest(BaseModel):
    text: str
    
@app.post("/get-recipe")
def generate_list(request: RecipeRequest):
    user_input = request.text
    return get_recipe(user_input=user_input)


"""
##  Recipe Item and Payload Models
##  summarze ingredients endpoint 
"""

# input data structure
class RecipeItem(BaseModel):
    id: str
    score: float
    category: str
    title: str
    url: HttpUrl
    url_en: HttpUrl
    image_url: HttpUrl
    title_en: str


class RecipePayload(BaseModel):
    results: List[RecipeItem]


@app.post("/summarize-ingredients")
def summarize(payload: RecipePayload):
    # convert pydantic model to python dict
    get_recipe_endpoint_data = payload.model_dump()

    # You can access payload.results[i].url, etc.
    result = aggr2.get_ingredient_summary(get_recipe_endpoint_data) 

    return result 