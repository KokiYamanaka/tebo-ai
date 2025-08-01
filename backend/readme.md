# directories 
- vector_ingredient.pkl 
    - ingredients in vector representation
    - use to compute similarity between ingredient in rank.py


# endpoint definition 
✅ Request Body: RecipePayload 
```
{
  "results": [
    {
      "id": "18925863",
      "score": 0.881210506,
      "category": "お肉のおかず",
      "title": "鶏肉の塩麹焼き",
      "url": "https://cookpad.com/jp/recipes/18925863-...",
      "url_en": "https://translate.google.com/translate?u=https://cookpad.com/jp/recipes/18925863-...",
      "image_url": "https://img-global-jp.cpcdn.com/recipes/3410371/...",
      "title_en": "Shio-koji grilled chicken"
    },
    ...
  ]
}
``` 
🔁 Response Body: IngredientSummary (AI-generated format)
``` 
Meat=[Ingredient(name='Skinless Chicken Breast', quantity='350g', store_package_quantity='1kg', store_package_price='10.99 CAD'), Ingredient(name='Chicken Thigh', quantity='2 pieces', store_package_quantity='1kg', store_package_price='13.99 CAD')] Vegetables=[Ingredient(name='Onion', quantity='1/2', store_package_quantity='3lb Bag', store_package_price='6.00 CAD'), Ingredient(name='Green Bell Pepper', quantity='1 1/2', store_package_quantity='3', store_package_price='5.00 CAD'), Ingredient(name='Okra', quantity='2', store_package_quantity='1 lb', store_package_price='7.00 CAD'), Ingredient(name='Radish', quantity='2', store_package_quantity='1 bunch', store_package_price='3.00 CAD'), Ingredient(name='Japanese Bunching Onion (Wakegi)', quantity='1 bunch', store_package_quantity='1 bunch', store_package_price='3.00 CAD')] Seasonings=[Ingredient(name='Salt Koji', quantity='3 teaspoons', store_package_quantity='200g', store_package_price='8.00 CAD'), Ingredient(name='Sugar Substitute', quantity='3/4 teaspoon', store_package_quantity='200g', store_package_price='12.00 CAD'), Ingredient(name='Grated Ginger', quantity='1.5 serving', store_package_quantity='100g', store_package_price='3.00 CAD'), Ingredient(name='Salt and Pepper', quantity='a little', store_package_quantity='1 set', store_package_price='6.00 CAD'), Ingredient(name='Miso', quantity='1 tablespoon', store_package_quantity='500g', store_package_price='9.00 CAD'), Ingredient(name='Mirin', quantity='2 tablespoons', store_package_quantity='500ml', store_package_price='10.00 CAD'), Ingredient(name='Ground Sesame Seeds', quantity='1 tablespoon', store_package_quantity='100g', store_package_price='5.00 CAD'), Ingredient(name='Sake', quantity='2 tablespoons', store_package_quantity='750ml', store_package_price='20.00 CAD'), Ingredient(name='Soy Sauce', quantity='4 tablespoons', store_package_quantity='1L', store_package_price='8.00 CAD'), Ingredient(name='Sugar', quantity='1 tablespoon', store_package_quantity='2kg', store_package_price='4.00 CAD'), Ingredient(name='3x Concentrated Mentsuyu', quantity='1 tablespoon', store_package_quantity='500ml', store_package_price='7.00 CAD'), Ingredient(name='Chili Pepper', quantity='a little', store_package_quantity='30g', store_package_price='4.00 CAD')] Oils_and_Fats=[Ingredient(name='Sesame Oil', quantity='1 teaspoon', store_package_quantity='150ml', store_package_price='7.00 CAD'), Ingredient(name='Salad Oil', quantity='to taste', store_package_quantity='1L', store_package_price='6.00 CAD')] Others=[Ingredient(name='Potato Starch', quantity='1/2 teaspoon', store_package_quantity='500g', store_package_price='5.00 CAD'), Ingredient(name='Water', quantity='3 tablespoons', store_package_quantity='1L', store_package_price='2.00 CAD')] Total_Store_Cost_CAD='130.97 CAD' Total_Store_Cost_Excluding_Seasonings_CAD='64.97 CAD' Num_Servings='8'

```