import os
import gradio as gr
from utils.translate.translate_deepl import translate_by_deepl_api
from utils.translate.translate_volcengine import translate_by_volcengine_api
from utils.translate.translate_hkbu_chatgpt import translate_by_hkbu_chatgpt_api
from utils.translate.translate_openrouter import translate_by_openrouter_api
from utils.translate.translate_google import translate_by_google_api
from utils.translate.translate_baichuan import translate_by_baichuan_api
from utils.translate.translate_zhipuai import translate_by_zhipuai_api
from dotenv import load_dotenv

load_dotenv()
passcode_key = os.getenv("PASSCODE_KEY")

# Model Dictionary for Translate by HKBU ChatGPT API
model_dict_translate_by_hkbu_chatgpt_api = {
    "HKBU ChatGPT (gpt-35-turbo-16k)": "gpt-35-turbo-16k",
    "HKBU ChatGPT (gpt-4-turbo)": "gpt-4-turbo"
}

# Model Dictionary for Translate by OpenRouter API
model_dict_translate_by_openrouter_api = {
    "OpenAI (gpt-3.5-turbo-0125)": "openai/gpt-3.5-turbo-0125",
    "OpenAI (gpt-4-turbo-preview)": "openai/gpt-4-turbo-preview"
}

# Model Dictionary for Translate by Zhipu AI API
model_dict_translate_by_zhipuai_api = {
    "Zhipu AI (glm-3-turbo)": "glm-3-turbo",
    "Zhipu AI (glm-4)": "glm-4"
}


def translate_text(source_language, target_language, original_text, tone_of_voice, industry, model, passcode):
    # Check if the passcode is correct
    if passcode != passcode_key:
        return "The passcode is incorrect. Please try again."
    # Check if the source language and target language are the same
    if source_language == target_language:
        return original_text
    # Check if the original text is empty
    if original_text == "":
        return ""
    # Check if the original text is too long
    if len(original_text) > 1000:
        return "The original text is too long. Please enter a text with less than 1000 characters."

    # Generate translated text
    translated_text = ""
    if model == "DeepL":
        translated_text = translate_by_deepl_api(source_language, target_language, original_text)
    elif model == "Volcengine":
        translated_text = translate_by_volcengine_api(source_language, target_language, original_text)
    elif model in model_dict_translate_by_hkbu_chatgpt_api:
        translation_sample, translated_text = translate_by_hkbu_chatgpt_api(
            source_language, target_language, original_text, tone_of_voice, industry,
            model_dict_translate_by_hkbu_chatgpt_api[model]
        )
    elif model in model_dict_translate_by_openrouter_api:
        translation_sample, translated_text = translate_by_openrouter_api(
            source_language, target_language, original_text, tone_of_voice, industry,
            model_dict_translate_by_openrouter_api[model]
        )
    elif model == "Google Gemini (gemini-pro)":
        translation_sample, translated_text = translate_by_google_api(
            source_language, target_language, original_text, tone_of_voice, industry
        )
    elif model == "Baichuan AI (Baichuan2)":
        translation_sample, translated_text = translate_by_baichuan_api(
            source_language, target_language, original_text, tone_of_voice, industry
        )
    elif model in model_dict_translate_by_zhipuai_api:
        translation_sample, translated_text = translate_by_zhipuai_api(
            source_language, target_language, original_text, tone_of_voice, industry,
            model_dict_translate_by_zhipuai_api[model]
        )

    return translated_text


# Interface for Text Translator
text_translator = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Dropdown(
            label="Source Language",
            choices=["Chinese", "English (UK)", "English (US)", "Vietnamese", "Japanese", "Korean", "French", "German",
                     "Spanish", "Portuguese (Brazilian)", "Portuguese (European)", "Italian", "Dutch", "Polish",
                     "Russian"],
            value="Chinese"
        ),
        gr.Dropdown(
            label="Target Language",
            choices=["Chinese", "English (UK)", "English (US)", "Vietnamese", "Japanese", "Korean", "French", "German",
                     "Spanish", "Portuguese (Brazilian)", "Portuguese (European)", "Italian", "Dutch", "Polish",
                     "Russian"],
            value="Vietnamese"
        ),
        gr.Textbox(
            label="Original Text",
            placeholder="Enter the original text here",
            lines=5,
            max_lines=10
        ),
        gr.Radio(
            label="Tone of Voice",
            choices=["Standard", "Formal", "Informal"],
            value="Standard"
        ),
        gr.Dropdown(
            label="Industry Sector",
            choices=["General Fields", "Academic Papers", "Biomedicine", "Information Technology",
                     "Finance and Economics", "News and Information", "Aerospace", "Mechanical Manufacturing",
                     "Laws and Regulations", "Humanities and Social Sciences"],
            value="General Fields"
        ),
        gr.Dropdown(
            label="Model Provider (Model Name)",
            choices=["DeepL", "Volcengine", "HKBU ChatGPT (gpt-35-turbo-16k)", "HKBU ChatGPT (gpt-4-turbo)",
                     "OpenAI (gpt-3.5-turbo-0125)", "OpenAI (gpt-4-turbo-preview)", "Google Gemini (gemini-pro)",
                     "Baichuan AI (Baichuan2)", "Zhipu AI (glm-3-turbo)", "Zhipu AI (glm-4)"],
            value="OpenAI (gpt-3.5-turbo-0125)"
        ),
        gr.Textbox(
            label="Passcode",
            placeholder="Enter the passcode here",
            type="password",
            lines=1,
            max_lines=1
        )
    ],
    outputs=[
        gr.Textbox(label="Translated Text", lines=5, max_lines=20, show_copy_button=True)
    ],
    title="FloweryTranslator - Text Translator"
)
