import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv

from utils.prompts.translation_prompt import generate_translation_prompt
from utils.utils.other_utils import extract_json_from_response

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
baichuan_api_key = os.environ.get("BAICHUAN_API_KEY")
baichuan_secret_key = os.environ.get("BAICHUAN_SECRET_KEY")
hkbu_chatgpt_api_key = os.environ.get("HKBU_CHATGPT_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")
zhipuai_api_key = os.environ.get("ZHIPUAI_API_KEY")


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
    rationale, translated_text = extract_json_from_response(target_language, res_content)

    return translation_sample, translated_text
