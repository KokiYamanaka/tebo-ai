from pydantic import BaseModel
from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    quantity: str
    store_package_quantity: str
    store_package_price: str

class IngredientSummary(BaseModel):
    Meat: Optional[List[Ingredient]] = []
    Vegetables: Optional[List[Ingredient]] = []
    Seasonings: Optional[List[Ingredient]] = []
    Oils_and_Fats: Optional[List[Ingredient]] = []
    Others: Optional[List[Ingredient]] = []
    Total_Store_Cost_CAD: str
    Total_Store_Cost_Excluding_Seasonings_CAD: str
    Num_Servings: str