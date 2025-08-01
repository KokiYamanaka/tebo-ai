from typing import List, Dict
from utils import get_translated_url, fetch_image_url, translate_title_to_english 



class RecipeEnricher:
    def __init__(self, recipes: List[Dict]):
        self.recipes = recipes
    
    def enrich(self) -> List[Dict]:
        for recipe in self.recipes:
            recipe['url_en'] = get_translated_url(recipe['url'])
            recipe['image_url'] = fetch_image_url(recipe['url'])
            recipe['title_en'] = translate_title_to_english(recipe['title'])
        return self.recipes
    
# if __name__ == "__main__":
#     # Example usage 
#     orderd_recipes = ['ご飯が進む(´▽｀)/\u3000チキン照り焼き', '白菜とゴボウと鶏むね肉の味噌煮～中華煮～', '簡単＊節約にも！鶏むね肉の中華風☆醤油煮', 'ご飯にかけたい♡鶏ごぼうの絶品親子煮', '鶏むね肉と筍 もやしの胡麻油香る中華煮', '☼超簡単♪空芯菜と鶏もも肉の中華炒め', '鶏ささみのポテト衣焼き～カレー風味～', '☆鶏もも肉の塩麹味噌焼き☆', '照り焼きチキン〜おろしソースがけ〜', 'チキンとブローコリーのインド風カレー']
#     orderd_recipes = orderd_recipes[:3]

#     metadata_instance = RecipeMetadata(orderd_recipes)
#     res = metadata_instance.add_metadata()
#     print(res)