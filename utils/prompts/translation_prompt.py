from utils.translate.translate_deepl import translate_by_deepl_api
from utils.translate.translate_volcengine import translate_by_volcengine_api
from utils.utils.other_utils import get_language_code


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
