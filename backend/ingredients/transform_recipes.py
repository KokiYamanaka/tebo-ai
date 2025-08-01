"""
purpose : receives output of recommended x4 recipes from "get-recipe" endpoint 
and scrapes the recipe details from the URLs provided in the output. 
this is pass to LLM to get a summary of the ingredients + quantites + estimated cost.
"""
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

# ------------------ Recipe Scraper ------------------
class Recipe:
    def __init__(self, url: str):
        self.url = url
        self.name: str = ""
        self.servings: str = ""
        self.ingredients: List[Dict[str, str]] = []
        self._soup = None

    def fetch_html(self) -> None:
        response = requests.get(self.url)
        response.raise_for_status()
        self._soup = BeautifulSoup(response.text, "html.parser")

    def extract_name(self) -> None:
        if not self._soup:
            self.fetch_html()
        tag = self._soup.find("h1")
        if tag:
            self.name = tag.get_text(strip=True)

    def extract_servings(self) -> None:
        if not self._soup:
            self.fetch_html()
        div = self._soup.select_one("div[id^='serving_recipe_'] .mise-icon-text")
        if div and "人分" in div.get_text():
            self.servings = div.get_text(strip=True)

    def extract_ingredients(self) -> None:
        if not self._soup:
            self.fetch_html()
        items = []
        for li in self._soup.select("div.ingredient-list ol > li"):
            name_tag = li.find("span")
            qty_tag = li.find("bdi")
            name = name_tag.get_text(" ", strip=True) if name_tag else ""
            qty = qty_tag.get_text(strip=True) if qty_tag else ""
            if name and qty:
                items.append({"name": name, "quantity": qty})
        self.ingredients = items

    def scrape_all(self) -> None:
        self.fetch_html()
        self.extract_name()
        self.extract_servings()
        self.extract_ingredients()

    def as_dict(self) -> Dict:
        return {
            "name": self.name,
            "servings": self.servings,
            "url": self.url,
            "ingredients": self.ingredients
        }

# ------------------ Processor ------------------
class RecipeProcessor:
    def __init__(self, data: Dict):
        self.data = data
        """
        direct get recipe endpoint output, which looks like this:
        {
        "results": [
              {
                "id": "18925863",
                "score": 0.881210506,
                "category": "お肉のおかず",
                "title": "鶏肉の塩麹焼き",
                ... 
            } 
        """
        self.transformed_data: List[Dict] = []

    def run(self):
        for item in self.data.get("results", []):
            try:
                url = item.get("url")
                if not url:
                    continue
                recipe = Recipe(url)
                recipe.scrape_all()
                result = recipe.as_dict()
                result.update({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "title_en": item.get("title_en"),
                    "image_url": item.get("image_url"),
                    "category": item.get("category"),
                    "score": item.get("score"),
                    "url_en": item.get("url_en")
                })
                self.transformed_data.append(result)
            except Exception as e:
                print(f"Failed to process {item.get('url')}: {e}")

    def get_results(self) -> List[Dict]:
        return self.transformed_data
    
if __name__ == "__main__":
    sample_data = {
    "results": [
        {
        "id": "18925863",
        "score": 0.881210506,
        "category": "お肉のおかず",
        "title": "鶏肉の塩麹焼き",
        "url": "https://cookpad.com/jp/recipes/18925863-%E9%B6%8F%E8%82%89%E3%81%AE%E5%A1%A9%E9%BA%B9%E7%84%BC%E3%81%8D",
        "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/18925863-%E9%B6%8F%E8%82%89%E3%81%AE%E5%A1%A9%E9%BA%B9%E7%84%BC%E3%81%8D",
        "image_url": "https://img-global-jp.cpcdn.com/recipes/3410371/480x680cq50/%E9%B6%8F%E8%82%89%E3%81%AE%E5%A1%A9%E9%BA%B9%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
        "title_en": "Shio-koji grilled chicken"
        },
        {
        "id": "17917280",
        "score": 0.832703412,
        "category": "お肉のおかず",
        "title": "鶏のごま味噌焼き♪",
        "url": "https://cookpad.com/jp/recipes/17917280-%E9%B6%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%84%BC%E3%81%8D",
        "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/17917280-%E9%B6%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%84%BC%E3%81%8D",
        "image_url": "https://img-global-jp.cpcdn.com/recipes/4030490/480x680cq50/%E9%B6%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
        "title_en": "Grilled chicken with sesame miso♪"
        },
        {
        "id": "18558237",
        "score": 0.820684791,
        "category": "お肉のおかず",
        "title": "鶏胸肉のホイル焼き",
        "url": "https://cookpad.com/jp/recipes/18558237-%E9%B6%8F%E8%83%B8%E8%82%89%E3%81%AE%E3%83%9B%E3%82%A4%E3%83%AB%E7%84%BC%E3%81%8D",
        "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/18558237-%E9%B6%8F%E8%83%B8%E8%82%89%E3%81%AE%E3%83%9B%E3%82%A4%E3%83%AB%E7%84%BC%E3%81%8D",
        "image_url": "https://img-global-jp.cpcdn.com/recipes/4238875/480x680cq50/%E9%B6%8F%E8%83%B8%E8%82%89%E3%81%AE%E3%83%9B%E3%82%A4%E3%83%AB%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
        "title_en": "Chicken breast grilled in foil"
        },
        {
        "id": "18187363",
        "score": 0.87925142,
        "category": "お肉のおかず",
        "title": "鶏の照り焼き",
        "url": "https://cookpad.com/jp/recipes/18187363-%E9%B6%8F%E3%81%AE%E7%85%A7%E3%82%8A%E7%84%BC%E3%81%8D",
        "url_en": "https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://cookpad.com/jp/recipes/18187363-%E9%B6%8F%E3%81%AE%E7%85%A7%E3%82%8A%E7%84%BC%E3%81%8D",
        "image_url": "https://img-global-jp.cpcdn.com/recipes/2154458/480x680cq50/%E9%B6%8F%E3%81%AE%E7%85%A7%E3%82%8A%E7%84%BC%E3%81%8D-%E3%83%AC%E3%82%B7%E3%83%94-%E3%83%A1%E3%82%A4%E3%83%B3-%E5%86%99%E7%9C%9F.jpg",
        "title_en": "Chicken teriyaki"
        }
    ]
    }
    processor = RecipeProcessor(sample_data)
    processor.run()
    for recipe in processor.get_results():
        print(recipe)
