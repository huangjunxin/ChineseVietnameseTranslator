import os
import time
import json
import requests
from dotenv import load_dotenv

from utils.prompts.translation_prompt import generate_translation_prompt
from utils.utils.other_utils import extract_json_from_response

load_dotenv()
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")


def call_openrouter_api(conversation_list, model_name="openai/gpt-3.5-turbo-0125", temperature=0.7):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
                "HTTP-Referer": f"https://bit.ly/FloweryTranslator",  # Optional, for including your app on openrouter.ai rankings.
                "X-Title": f"FloweryTranslator",  # Optional. Shows in rankings on openrouter.ai.
            },
            data=json.dumps({
                "model": model_name,
                "messages": conversation_list,
                "temperature": temperature
            })
        )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return 'Error', response.status_code, response.text
    except requests.RequestException as e:
        return 'Error:', e


def translate_by_openrouter_api(source_language, target_language, original_text, tone_of_voice, industry, model_name="openai/gpt-3.5-turbo-0125"):
    print("Use OpenRouter API")

    # Prompt to provide translation
    translation_sample, translation_prompt, translate_time = generate_translation_prompt(source_language, target_language, original_text, tone_of_voice, industry)

    start_time = time.time()

    res = ""
    try:
        # Generate response by accessing OpenRouter API
        res = call_openrouter_api(
            conversation_list=[
                {"role": "user", "content": translation_prompt}
            ],
            model_name=model_name,
            temperature=0.7
        )
        if isinstance(res, tuple) and res[0] == 'Error':
            res_content = res
        else:
            res_content = res["choices"][0]["message"]["content"]
    except Exception as e:
        res_content = 'Error:', e, res

    end_time = time.time()
    llm_time = end_time - start_time
    print("Time Elapsed:", llm_time, "seconds")
    print("Result content:", res_content)

    rationale, translated_text = extract_json_from_response(target_language, res_content)

    return translation_sample, rationale, translated_text, res_content, translate_time, llm_time
