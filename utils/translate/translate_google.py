import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from utils.prompts.translation_prompt import generate_translation_prompt
from utils.utils.other_utils import extract_json_from_response

load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")


def translate_by_google_api(source_language, target_language, original_text, tone_of_voice, industry):
    # Prompt to provide translation
    translation_sample, translation_prompt, translate_time = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)

    start_time = time.time()

    # Translate by accessing Google API
    chat = ChatGoogleGenerativeAI(temperature=0.7, model="gemini-pro")
    res = chat.invoke(translation_prompt)
    res_content = res.content

    end_time = time.time()
    llm_time = end_time - start_time
    print("Time Elapsed:", llm_time, "seconds")
    print("Result content:", res_content)

    rationale, translated_text = extract_json_from_response(target_language, res_content)

    return translation_sample, rationale, translated_text, res_content, translate_time, llm_time
