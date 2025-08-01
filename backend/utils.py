import requests
from bs4 import BeautifulSoup
from typing import Optional
from deep_translator import GoogleTranslator

def get_translated_url(url: str) -> str:
    """
    Given a Cookpad Japan recipe URL, return the Google Translate version (JP → EN).
    """
    base = "https://translate.google.com/translate"
    return f"{base}?hl=en&sl=ja&tl=en&u={url}"


def fetch_image_url(url: str) -> Optional[str]:
    """Fetch the main image URL from a Cookpad recipe page."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1️⃣ Try <picture> with <source type="image/jpeg">
        picture = soup.find("picture")
        if picture:
            jpeg_source = picture.find("source", {"type": "image/jpeg"})
            if jpeg_source and jpeg_source.get("srcset"):
                srcset = jpeg_source["srcset"].split(",")
                high_res = srcset[-1].strip().split(" ")[0]
                return high_res

        # 2️⃣ og:image fallback
        meta_og = soup.find("meta", property="og:image")
        if meta_og and meta_og.get("content"):
            return meta_og["content"]

        # 3️⃣ alt=メイン写真
        main_img = soup.find("img", alt=lambda value: value and "メイン写真" in value)
        if main_img and main_img.get("src"):
            return main_img["src"]

        # 4️⃣ tofu_image block
        tofu_div = soup.find("div", class_="tofu_image")
        if tofu_div:
            tofu_img = tofu_div.find("img")
            if tofu_img and tofu_img.get("src"):
                return tofu_img["src"]

        # 5️⃣ Fallback: <img class="mx-auto object-contain">
        img_tag = soup.find("img", class_=lambda c: c and "mx-auto" in c and "object-contain" in c)
        if img_tag and img_tag.get("src"):
            return img_tag["src"]

    except Exception:
        pass

    return None


def translate_title_to_english(japanese_title: str) -> str:
    """
    Translate a Japanese recipe title to English using deep-translator.

    Args:
        japanese_title (str): The original title in Japanese.

    Returns:
        str: Translated title in English or original if translation fails.
    """
    try:
        return GoogleTranslator(source='ja', target='en').translate(japanese_title)
    except Exception as e:
        print(f"Translation error: {e}")
        return japanese_title  # fallback
    
def eng_to_jp(english_text: str) -> str:
    """
    Translate a Japanese recipe title to English using deep-translator.

    Args:
        japanese_title (str): The original title in Japanese.

    Returns:
        str: Translated title in English or original if translation fails.
    """
    try:
        return GoogleTranslator(source='en', target='ja').translate(english_text)
    except Exception as e:
        print(f"Translation error: {e}")
        return english_text  # fallback