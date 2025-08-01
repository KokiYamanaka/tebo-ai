from typing import List, Dict, Union
from openai import OpenAI
from dotenv import load_dotenv
import os

from schema import RecipeList, LineItem, LineItemList, LineItemMeasurement, Filters


load_dotenv()  
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ==========================================
# SECTION: USER EATING CONSTRAINT -> A LIST OF 4 RECIPES 
# ==========================================

def get_recipe_names(user_constraint:str) -> List[str]:  
    response = client.responses.parse(
        model="gpt-4.1-nano",
        input=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that returns a list of 4 short Japanese recipe names "
                    "using fish and chicken, muscle-training friendly, calorie-conscious, "
                    "with ingredients that are commonly available in Canada. "
                    "Output in JSON as: { 'recipes': [string, string, string, string] }"
                    "Output of each recipe string is in japanese"
                ),
            },
            {
                "role": "user",
                "content": "日本の魚、鶏肉のレシピ、筋トレ、カロリー気にするレシピ4選ください。 variety。カナダでありそうな、食材",
            },
        ],
        text_format=RecipeList,
    )

    return response.output_parsed.recipes

# ==========================================
# SECTION: 4 COOKPAD RECIPE -> 4 INSTACART RECIPE OBJECT 
# ==========================================


def get_unique_aggregated_line_items(all_ingredients: List[str]) -> List[LineItem]:
    response = client.responses.parse(
        model="gpt-4.1-nano",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a JSON structuring assistant. "
                    "Given a combined list of ingredient strings gathered from multiple Japanese recipes, "
                    "your job is to identify each unique ingredient name, then aggregate the total quantity "
                    "of that ingredient across all appearances. If the same unit is used, add up the quantities. "
                    "If different units are used for the same name, choose the most common unit and estimate the quantity. "
                    "If a quantity or unit is unclear, set quantity=1 and unit='piece'.\n\n"
                    "IMPORTANT:\n"
                    "- You MUST translate all ingredient names into clear, natural English words (no Japanese).\n"
                    "- You MUST ensure that all quantity values are integers greater than or equal to 1. "
                    "No quantity may be zero or negative. If you see 0 or unclear, correct it to 1.\n"
                    "- All JSON output values MUST be fully in English, with no Japanese text at all.\n\n"
                    "Use this schema:\n\n"
                    "class LineItemMeasurement(BaseModel):\n"
                    "  quantity: int  # must be >= 1\n"
                    "  unit: str\n\n"
                    "class Filters(BaseModel):\n"
                    "  brand_filters: List[str]\n"
                    "  health_filters: List[str]\n\n"
                    "class LineItem(BaseModel):\n"
                    "  name: str  # translated to English\n"
                    "  quantity: int  # must be >= 1\n"
                    "  unit: str\n"
                    "  display_text: str  # written in English\n"
                    "  line_item_measurements: List[LineItemMeasurement]\n"
                    "  filters: Filters\n\n"
                    "Return JSON in the format: { 'line_items': [LineItem, LineItem, ...] } "
                    "with only unique ingredient names, their aggregated totals, translated to English, "
                    "and with quantities strictly greater than or equal to 1."
                )
            },
            {
                "role": "user",
                "content": (
                    f"以下の全てのingredientsリストから、ユニークにして合計量をまとめ、必ず英語に翻訳し、数量は最低でも1以上にしてください: {all_ingredients}"
                ),
            },
        ],
        text_format=LineItemList,
    )
    return response.output_parsed.line_items




def convert_ingredients_to_lineitems(
    ingredient_list: List[Union[str, LineItem]]
) -> Dict:
    line_items = []
    for ing in ingredient_list:
        if isinstance(ing, LineItem):
            # Already structured: just reuse it
            line_items.append(ing)
        else:
            # Parse raw string
            tokens = ing.split()
            name = " ".join(tokens[:-2])
            try:
                quantity = int(tokens[-2])
            except ValueError:
                quantity = 1
            unit = tokens[-1]
            display_text = f"{quantity} {unit} of {name}"
            line_items.append(
                LineItem(
                    name=name,
                    quantity=quantity,
                    unit=unit,
                    display_text=display_text,
                    line_item_measurements=[
                        LineItemMeasurement(quantity=quantity, unit=unit)
                    ],
                    filters=Filters(brand_filters=[], health_filters=[])
                )
            )
    return {"line_items": [item.dict() for item in line_items]}



all_recp_list= [{'author': 'MIHOりん♪', 'canonical_url': 'https://cookpad.com/jp/recipes/21228423', 'category': None, 'cuisine': '日本語', 'description': '加熱前に塩こうじにしばらく漬け込むと、肉魚は柔らかくなり美味しくなります♪発酵食品は最高です♪', 'host': 'cookpad.com', 'image': 'https://img-global-jp.cpcdn.com/recipes/7426640/400x400cq80/photo.jpg', 'ingredient_groups': [{'ingredients': ['生鮭 3切れ', '塩こうじ 大さじ1', 'しめじ 60g', 'ねぎ 1/2本'], 'purpose': None}], 'ingredients': ['生鮭 3切れ', '塩こうじ 大さじ1', 'しめじ 60g', 'ねぎ 1/2本'], 'instructions': '生鮭の表面に塩こうじをまんべんなく塗り15〜20分おく。\nしめじは石づきを取り、ねぎは斜めに切る。\nフライパンにオーブンシートを敷き、鮭、しめじ、ねぎをのせる。\n蓋をして火にかけ、熱くなったら弱火にして5分焼く。\n鮭をひっくり返し蓋をして、更に弱火で5分焼き火を切る。\n器に盛って出来上がり。', 'instructions_list': ['生鮭の表面に塩こうじをまんべんなく塗り15〜20分おく。', 'しめじは石づきを取り、ねぎは斜めに切る。', 'フライパンにオーブンシートを敷き、鮭、しめじ、ねぎをのせる。', '蓋をして火にかけ、熱くなったら弱火にして5分焼く。', '鮭をひっくり返し蓋をして、更に弱火で5分焼き火を切る。', '器に盛って出来上がり。'], 'keywords': ['生鮭', '塩こうじ', 'しめじ', 'ねぎ'], 'language': 'ja', 'nutrients': {}, 'site_name': 'Cookpad', 'title': 'カンタン！ヘルシー！鮭の塩こうじ焼き', 'yields': '3 servings'}, {'author': 'Senchan08', 'canonical_url': 'https://cookpad.com/jp/recipes/18997429', 'category': None, 'cuisine': '日本語', 'description': '酒蒸しにするので鶏むね肉がしっとり仕上がります♪ピリリとゆずこしょうが効いた大人の味です', 'host': 'cookpad.com', 'image': 'https://img-global-jp.cpcdn.com/recipes/3424580/400x400cq80/photo.jpg', 'ingredient_groups': [{'ingredients': ['鶏むね肉 200g', '片栗粉 適量', '酒 大さじ1', '麺つゆ 大さじ1', '醤油 小さじ1', 'ゆずこしょう お好みで'], 'purpose': None}], 'ingredients': ['鶏むね肉 200g', '片栗粉 適量', '酒 大さじ1', '麺つゆ 大さじ1', '醤油 小さじ1', 'ゆずこしょう お好みで'], 'instructions': '鶏むね肉を一口大にそぎ切りにし、片栗粉をまぶす\nフライパンにサラダ油を熱し、むね肉を焼く。焼き色がついたらひっくり返し、酒を加える。フタをして5分ほど蒸し焼きにする\n火が通ったら麺つゆ、醤油、ゆずこしょうで味付け', 'instructions_list': ['鶏むね肉を一口大にそぎ切りにし、片栗粉をまぶす', 'フライパンにサラダ油を熱し、むね肉を焼く。焼き色がついたらひっくり返し、酒を加える。フタをして5分ほど蒸し焼きにする', '火が通ったら麺つゆ、醤油、ゆずこしょうで味付け'], 'keywords': ['鶏むね肉', '片栗粉', '酒', '麺つゆ', '醤油', 'ゆずこしょう'], 'language': 'ja', 'nutrients': {}, 'site_name': 'Cookpad', 'title': 'しっとり鶏むね肉のゆずこしょうソテー', 'yields': '2 servings'}, {'author': '暇人の料理', 'canonical_url': 'https://cookpad.com/jp/recipes/24834680', 'category': None, 'cuisine': '日本語', 'description': 'このレシピの生い立ち 炊飯器1つで鯖の味噌煮缶を使った炊き込みご飯を作りたくて', 'host': 'cookpad.com', 'image': 'https://img-global-jp.cpcdn.com/recipes/642a784600de7901/400x400cq80/photo.jpg', 'ingredient_groups': [{'ingredients': ['米 2合分', '鯖の味噌煮缶 1缶', '大葉かネギ 適量', 'オイスターソース 大さじ1', '醤油 大さじ1', '料理酒 大さじ1', 'みりん 大さじ1', '生姜チューブ 3cm'], 'purpose': None}], 'ingredients': ['米 2合分', '鯖の味噌煮缶 1缶', '大葉かネギ 適量', 'オイスターソース 大さじ1', '醤油 大さじ1', '料理酒 大さじ1', 'みりん 大さじ1', '生姜チューブ 3cm'], 'instructions': '米2合を研いで、ザルに上げて30分乾燥させる\n炊飯釜に研いだ白米、鯖の味噌煮の汁、調味料の材料を全て入れて、白米炊飯のメモリの9割まで水を入れてよく混ぜる\n鯖の味噌煮を上に乗せて白米炊飯でスイッチオンして炊飯する\n皿によそって、ネギか大葉を乗せて完成', 'instructions_list': ['米2合を研いで、ザルに上げて30分乾燥させる', '炊飯釜に研いだ白米、鯖の味噌煮の汁、調味料の材料を全て入れて、白米炊飯のメモリの9割まで水を入れてよく混ぜる', '鯖の味噌煮を上に乗せて白米炊飯でスイッチオンして炊飯する', '皿によそって、ネギか大葉を乗せて完成'], 'keywords': ['米', '鯖の味噌煮缶', '大葉かネギ', 'オイスターソース', '醤油', '料理酒', 'みりん', '生姜チューブ'], 'language': 'ja', 'nutrients': {}, 'site_name': 'Cookpad', 'title': '炊飯器で！鯖の味噌煮炊き込みご飯'}, {'author': 'まさひ', 'canonical_url': 'https://cookpad.com/jp/recipes/21786154', 'category': None, 'cuisine': '日本語', 'description': '高たんぱく質でヘルシーな「鶏ささみ」を使った、簡単作り置きレシピです♪にんにくが良いアクセントになり、食べやすいですよ☆', 'host': 'cookpad.com', 'image': 'https://img-global-jp.cpcdn.com/recipes/6747916/400x400cq80/photo.jpg', 'ingredient_groups': [{'ingredients': ['鶏ささみ 4本', 'ブロッコリー 100ｇ', 'A ごま油 大さじ1', 'A 鶏がらスープの素（顆粒） 小さじ1～小さじ1.5', 'A すりおろしにんにく 小さじ1', '白ごま ひとつまみ'], 'purpose': None}], 'ingredients': ['鶏ささみ 4本', 'ブロッコリー 100ｇ', 'A ごま油 大さじ1', 'A 鶏がらスープの素（顆粒） 小さじ1～小さじ1.5', 'A すりおろしにんにく 小さじ1', '白ごま ひとつまみ'], 'instructions': '鍋に水500ｍｌと酒大さじ1（分量外）を入れ、沸騰するまで火にかける。\n１に鶏ささみを入れて、再沸騰して30秒茹でたら火を止めて蓋をする。そのまま10分放置して火を通す。\n２の粗熱が取れたら、鶏ささみの筋を取って裂く\nブロッコリーを小分けにして、耐熱ボウルに入れる。ふんわりラップをかけ、600Wで4分加熱する。\nキッチンペーパーで４の水気を取る。そこに３とAを入れてよく和え、仕上げに白ごまを散らす。\n完成♪', 'instructions_list': ['鍋に水500ｍｌと酒大さじ1（分量外）を入れ、沸騰するまで火にかける。', '１に鶏ささみを入れて、再沸騰して30秒茹でたら火を止めて蓋をする。そのまま10分放置して火を通す。', '２の粗熱が取れたら、鶏ささみの筋を取って裂く', 'ブロッコリーを小分けにして、耐熱ボウルに入れる。ふんわりラップをかけ、600Wで4分加熱する。', 'キッチンペーパーで４の水気を取る。そこに３とAを入れてよく和え、仕上げに白ごまを散らす。', '完成♪'], 'keywords': ['鶏ささみ', 'ブロッコリー', 'A ごま油', 'A 鶏がらスープの素（顆粒）', 'A すりおろしにんにく', '白ごま'], 'language': 'ja', 'nutrients': {}, 'site_name': 'Cookpad', 'title': '作り置き♪鶏ささみとブロッコリーの和え物', 'yields': '2 servings'}]
res = get_unique_aggregated_line_items(all_recp_list) 
format_ing = convert_ingredients_to_lineitems(res)
print(format_ing) 