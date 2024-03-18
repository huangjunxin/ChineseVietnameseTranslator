import os
import json
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from dotenv import load_dotenv

from utils.utils.other_utils import get_language_code

load_dotenv()
k_access_key = os.environ.get("K_ACCESS_KEY")
k_secret_key = os.environ.get("K_SECRET_KEY")


def translate_by_volcengine_api(source_language, target_language, original_text):
    source_language_code = get_language_code(source_language)
    target_language_code = get_language_code(target_language)

    k_service_info = ServiceInfo(
        'translate.volcengineapi.com',
        {'Content-Type': 'application/json'},
        Credentials(k_access_key, k_secret_key, 'translate', 'cn-north-1'),
        5,
        5
    )
    k_query = {
        'Action': 'TranslateText',
        'Version': '2020-06-01'
    }
    k_api_info = {
        'translate': ApiInfo('POST', '/', k_query, {}, {})
    }
    service = Service(k_service_info, k_api_info)
    body = {
        'TargetLanguage': target_language_code,
        'TextList': [original_text],
    }
    res = service.json('translate', {}, json.dumps(body))
    print(res)
    translated_dict = json.loads(res)
    translated_text = translated_dict["TranslationList"][0]["Translation"]

    return translated_text
