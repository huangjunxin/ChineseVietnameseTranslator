import os
import deepl
from dotenv import load_dotenv

from utils.utils.other_utils import get_language_code

load_dotenv()
deepl_api_key = os.environ.get("DEEPL_API_KEY")


def translate_by_deepl_api(source_language, target_language, original_text):
    target_language_code = get_language_code(target_language).upper()
    deepl_client = deepl.Translator(deepl_api_key)
    translated_text = deepl_client.translate_text(original_text, target_lang=target_language_code)

    return translated_text.text
