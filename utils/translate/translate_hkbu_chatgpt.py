import os
import time
from dotenv import load_dotenv
import requests

from utils.prompts.translation_prompt import generate_translation_prompt
from utils.utils.other_utils import extract_json_from_response

load_dotenv()
hkbu_chatgpt_api_key = os.environ.get("HKBU_CHATGPT_API_KEY")


def call_hkbu_chatgpt_api(conversation_list, model_name="gpt-35-turbo", temperature=0.7):
    basic_url = "https://chatgpt.hkbu.edu.hk/general/rest"
    api_version = "2024-02-15-preview"
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

    start_time = time.time()

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

    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Time Elapsed:", time_elapsed, "seconds")
    print("Result content:", res_content)

    rationale, translated_text = extract_json_from_response(target_language, res_content)

    return translation_sample, rationale, translated_text, res_content, time_elapsed
