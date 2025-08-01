from pydantic import BaseModel
from typing import List


# ==========================================
# SECTION: USER EATING CONSTRAINT -> A LIST OF 4 RECIPES 
# ==========================================
class RecipeList(BaseModel):
    recipes: List[str]


# ==========================================
# SECTION: 4 COOKPAD RECIPE -> 4 INSTACART RECIPE OBJECT 
# ==========================================

class LineItemMeasurement(BaseModel):
    quantity: int
    unit: str

class Filters(BaseModel):
    brand_filters: List[str]
    health_filters: List[str]

class LineItem(BaseModel):
    name: str
    quantity: int
    unit: str
    display_text: str
    line_item_measurements: List[LineItemMeasurement]
    filters: Filters

class LineItemList(BaseModel):
    line_items: List[LineItem]
 