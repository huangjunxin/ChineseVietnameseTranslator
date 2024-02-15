# utils.py
import os
import json
import re
import deepl
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from langchain_community.chat_models import ChatOpenAI, ChatBaichuan
from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from zhipuai import ZhipuAI
from dotenv import load_dotenv
import requests

load_dotenv()
deepl_api_key = os.environ.get("DEEPL_API_KEY")
k_access_key = os.environ.get("K_ACCESS_KEY")
k_secret_key = os.environ.get("K_SECRET_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
baichuan_api_key = os.environ.get("BAICHUAN_API_KEY")
baichuan_secret_key = os.environ.get("BAICHUAN_SECRET_KEY")
hkbu_chatgpt_api_key = os.environ.get("HKBU_CHATGPT_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")
zhipuai_api_key = os.environ.get("ZHIPUAI_API_KEY")


def get_language_code(language_name):
    language_mapping = {
        "Chinese": "zh",
        "Chinese (traditional)": "zh-Hant",
        "Chinese (Hongkong traditional)": "zh-Hant-hk",
        "Chinese (Taiwan traditional)": "zh-Hant-tw",
        "Tswana": "tn",
        "Vietnamese": "vi",
        "Inuktitut": "iu",
        "Italian": "it",
        "Indonesian": "id",
        "Hindi": "hi",
        "English": "en",
        "English (UK)": "en-gb",
        "English (US)": "en-us",
        "Hiri": "ho",
        "Hebrew": "he",
        "Spanish": "es",
        "Modern Greek": "el",
        "Ukrainian": "uk",
        "Urdu": "ur",
        "Turkmen": "tk",
        "Turkish": "tr",
        "Tigrinya": "ti",
        "Tahitian": "ty",
        "Tagalog": "tl",
        "Tongan": "to",
        "Thai": "th",
        "Tamil": "ta",
        "Telugu": "te",
        "Slovenian": "sl",
        "Slovak": "sk",
        "Swati": "ss",
        "Esperanto": "eo",
        "Samoan": "sm",
        "Sango": "sg",
        "Southern Sotho": "st",
        "Swedish": "sv",
        "Japanese": "ja",
        "Twi": "tw",
        "Quechua": "qu",
        "Portuguese": "pt",
        "Portuguese (Brazilian)": "pt-br",
        "Portuguese (European)": "pt-pt",
        "Punjabi": "pa",
        "Norwegian": "no",
        "Norwegian Bokmål": "nb",
        "South Ndebele": "nr",
        "Burmese": "my",
        "Bengali": "bn",
        "Mongolian": "mn",
        "Marshallese": "mh",
        "Macedonian": "mk",
        "Malayalam": "ml",
        "Marathi": "mr",
        "Malay": "ms",
        "Luba-Katanga": "lu",
        "Romanian": "ro",
        "Lithuanian": "lt",
        "Latvian": "lv",
        "Lao": "lo",
        "Kwanyama": "kj",
        "Croatian": "hr",
        "Kannada": "kn",
        "Kikuyu": "ki",
        "Czech": "cs",
        "Catalan": "ca",
        "Dutch": "nl",
        "Korean": "ko",
        "Haitian Creole": "ht",
        "Gujarati": "gu",
        "Georgian": "ka",
        "Greenlandic": "kl",
        "Khmer": "km",
        "Ganda": "lg",
        "Kongo": "kg",
        "Finnish": "fi",
        "Fijian": "fj",
        "French": "fr",
        "Russian": "ru",
        "Ndonga": "ng",
        "German": "de",
        "Tatar": "tt",
        "Danish": "da",
        "Tsonga": "ts",
        "Chuvash": "cv",
        "Persian": "fa",
        "Bosnian": "bs",
        "Polish": "pl",
        "Bislama": "bi",
        "North Ndebele": "nd",
        "Bashkir": "ba",
        "Bulgarian": "bg",
        "Azerbaijani": "az",
        "Arabic": "ar",
        "Afrikaans": "af",
        "Albanian": "sq",
        "Abkhazian": "ab",
        "Ossetian": "os",
        "Ewe": "ee",
        "Estonian": "et",
        "Aymara": "ay",
        "Chinese (classical)": "lzh",
        "Amharic": "am",
        "Central Kurdish": "ckb",
        "Welsh": "cy",
        "Galician": "gl",
        "Hausa": "ha",
        "Armenian": "hy",
        "Igbo": "ig",
        "Northern Kurdish": "kmr",
        "Lingala": "ln",
        "Northern Sotho": "nso",
        "Chewa": "ny",
        "Oromo": "om",
        "Shona": "sn",
        "Somali": "so",
        "Serbian": "sr",
        "Swahili": "sw",
        "Xhosa": "xh",
        "Yoruba": "yo",
        "Zulu": "zu",
        "Tibetan": "bo",
        "Hokkien": "nan",
        "Wuyue Chinese": "wuu",
        "Cantonese": "yue",
        "Southwestern Mandarin": "cmn",
        "Uighur": "ug",
        "Nigerian Fulfulde": "fuv",
        "Hungarian": "hu",
        "Kamba": "kam",
        "Dholuo": "luo",
        "Kinyarwanda": "rw",
        "Umbundu": "umb",
        "Wolof": "wo"
    }

    # Return the language code or a default value if not found
    return language_mapping.get(language_name, "Unknown Language Code")


def translate_by_deepl_api(source_language, target_language, original_text):
    target_language_code = get_language_code(target_language).upper()
    deepl_client = deepl.Translator(deepl_api_key)
    translated_text = deepl_client.translate_text(original_text, target_lang=target_language_code)

    return translated_text.text


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


# Translation prompt
def generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry):
    languages_should_use_deepl = ["Chinese", "English (UK)", "English (US)", "French", "German", "Spanish",
                                  "Portuguese (Brazilian)", "Portuguese (European)", "Italian", "Dutch", "Polish",
                                  "Russian"]
    # Print the source language, target language
    print(f"Source language: {source_language}, Language code: {get_language_code(source_language)}, Should use DeepL: {source_language in languages_should_use_deepl}")
    print(f"Target language: {target_language}, Language code: {get_language_code(target_language)}, Should use DeepL: {target_language in languages_should_use_deepl}")
    # Generate the translation sample
    if source_language in languages_should_use_deepl and target_language in languages_should_use_deepl:
        print("Using DeepL API")
        translation_sample = translate_by_deepl_api(source_language, target_language, original_text)
    else:
        print("Using Volcengine API")
        translation_sample = translate_by_volcengine_api(source_language, target_language, original_text)

    # Generate the translation prompt
    translation_prompt = f"""{source_language}:
```
{original_text}
```

{target_language} translation sample:
```
{translation_sample}
```

As a bilingual {source_language}-{target_language} native speaker and seasoned translator, your task is to proofread the {target_language} translation sample for errors based on the {source_language} text above. The translated text should be in the tone of voice of {tone_of_voice.lower()}, and should be suitable for the {industry.lower()} industry. Before providing a proofread version, please provide suggestions for corrections (if any) to the above translation sample.

Your response should be formatted as follows:
```
Rationale:
{target_language} translation (proofread):
```"""

    print(translation_prompt)

    return translation_sample, translation_prompt


def extract_content_from_response(target_language, response):
    if "(" in target_language and ")" in target_language:
        target_language = target_language.replace("(", "\(")
        target_language = target_language.replace(")", "\)")
    # Define the regex patterns
    rationale_pattern = rf'Rationale:\n(.*?)(?:{target_language} translation \(proofread\):|$)'
    translation_pattern = rf'{target_language} translation \(proofread\):(.*?)$'

    # Extract the rationale
    rationale_match = re.search(rationale_pattern, response, re.DOTALL)
    rationale = rationale_match.group(1).strip() if rationale_match else None

    # Extract the Vietnamese translation (proofread)
    translation_match = re.search(translation_pattern, response, re.DOTALL)
    translation = translation_match.group(1).strip().strip("```").strip() if translation_match else None

    return rationale, translation


def translate_by_openai_api(source_language, target_language, original_text, tone_of_voice, industry, model_name="gpt-3.5-turbo-1106"):
    # Prompt to provide translation
    translation_sample, translation_prompt = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)
    # Translate by accessing OpenAI API
    chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key, model_name=model_name)
    res = chat(
        [
            HumanMessage(content=translation_prompt)
        ]
    )
    res_content = res.content
    print(res_content)
    rationale, translated_text = extract_content_from_response(target_language, res_content)

    return translation_sample, translated_text


def translate_by_baichuan_api(source_language, target_language, original_text, tone_of_voice, industry):
    # Prompt to provide translation
    translation_sample, translation_prompt = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)
    # Translate by accessing Baichuan API
    chat = ChatBaichuan(temperature=0.7, baichuan_api_key=baichuan_api_key, baichuan_secret_key=baichuan_secret_key, model='Baichuan2')
    res = chat(
        [
            HumanMessage(content=translation_prompt)
        ]
    )
    res_content = res.content
    print(res_content)
    rationale, translated_text = extract_content_from_response(target_language, res_content)

    return translation_sample, translated_text


def call_hkbu_chatgpt_api(conversation_list, model_name="gpt-35-turbo-16k", temperature=0.7):
    basic_url = "https://chatgpt.hkbu.edu.hk/general/rest"
    api_version = "2023-08-01-preview"
    if model_name == "gpt-35-turbo-16k":
        api_version = "2023-08-01-preview"
    elif model_name == "gpt-4-turbo":
        api_version = "2023-12-01-preview"
    url = basic_url + "/deployments/" + model_name + "/chat/completions/?api-version=" + api_version
    headers = {'Content-Type': 'application/json', 'api-key': hkbu_chatgpt_api_key}
    payload = {'messages': conversation_list, 'temperature': temperature}

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return 'Error', response.status_code, response.text
    except requests.RequestException as e:
        return 'Error:', e


def translate_by_hkbu_chatgpt_api(source_language, target_language, original_text, tone_of_voice, industry, model_name="gpt-35-turbo-16k"):
    # Prompt to provide translation
    translation_sample, translation_prompt = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)
    res = ""
    try:
        # Translate by accessing HKBU ChatGPT API
        res = call_hkbu_chatgpt_api(
            conversation_list=[
                {"role": "user", "content": translation_prompt}
            ],
            model_name=model_name,
            temperature=0.7
        )
        res_content = res["choices"][0]["message"]["content"]
    except Exception as e:
        res_content = 'Error:', e, res
        return res_content

    print(res_content)
    rationale, translated_text = extract_content_from_response(target_language, res_content)

    return translation_sample, translated_text


def translate_by_google_api(source_language, target_language, original_text, tone_of_voice, industry):
    # Prompt to provide translation
    translation_sample, translation_prompt = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)
    # Translate by accessing Google API
    chat = ChatGoogleGenerativeAI(temperature=0.7, model="gemini-pro")
    res = chat.invoke(translation_prompt)
    res_content = res.content
    print(res_content)
    rationale, translated_text = extract_content_from_response(target_language, res_content)

    return translation_sample, translated_text


def translate_by_zhipuai_api(source_language, target_language, original_text, tone_of_voice, industry, model_name="glm-3-turbo"):
    # Prompt to provide translation
    translation_sample, translation_prompt = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)
    # Translate by accessing ZhipuAI API
    chat = ZhipuAI(api_key=zhipuai_api_key)
    res = chat.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": translation_prompt}
        ],
        temperature=0.7
    )
    res_content = res.choices[0].message.content
    print(res_content)
    rationale, translated_text = extract_content_from_response(target_language, res_content)

    return translation_sample, translated_text
