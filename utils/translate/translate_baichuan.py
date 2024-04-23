import os
import time
from langchain_community.chat_models import ChatBaichuan
from langchain.schema import HumanMessage
from dotenv import load_dotenv

from utils.prompts.translation_prompt import generate_translation_prompt
from utils.utils.other_utils import extract_json_from_response

load_dotenv()
baichuan_api_key = os.environ.get("BAICHUAN_API_KEY")
baichuan_secret_key = os.environ.get("BAICHUAN_SECRET_KEY")


def translate_by_baichuan_api(source_language, target_language, original_text, tone_of_voice, industry):
    # Prompt to provide translation
    translation_sample, translation_prompt = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)

    start_time = time.time()

    # Translate by accessing Baichuan API
    chat = ChatBaichuan(temperature=0.7, baichuan_api_key=baichuan_api_key, baichuan_secret_key=baichuan_secret_key, model='Baichuan2')
    res = chat(
        [
            HumanMessage(content=translation_prompt)
        ]
    )
    res_content = res.content

    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Time Elapsed:", time_elapsed, "seconds")
    print("Result content:", res_content)

    rationale, translated_text = extract_json_from_response(target_language, res_content)

    return translation_sample, rationale, translated_text, res_content, time_elapsed
