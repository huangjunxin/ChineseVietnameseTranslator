---
title: FloweryTranslator
emoji: 🌸
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.8.0
app_file: main.py
pinned: false
---

# FloweryTranslator

FloweryTranslator is a state-of-the-art, multilingual translation platform designed to transcend linguistic barriers with unparalleled precision. This robust tool leverages the high-speed translation capabilities of Volcengine's AI engine, coupled with the nuanced language understanding of advanced Large Language Models (LLMs) such as OpenAI, Google, Baichuan, and Zhipu. Specially crafted to serve a wide array of languages and cater to distinct industry needs, FloweryTranslator ensues a two-tier translation process, beginning with an initial translation by Volcengine, followed by meticulous proofreading by an LLM of your choice to enhance accuracy and contextual relevance. Whether you need to translate simple text inputs or complex documents, FloweryTranslator is tailored to deliver precision and nuance in translation.

## Features

- **Diverse Language Support**: Translate text between popular languages like Chinese, English, Vietnamese, Japanese, and Korean.
- **Text and Document Translation**: Input text directly or upload `.docx` or `.pdf` files for translation.
- **Multiple Translation Models**: Choose from models provided by Volcengine, HKBU, OpenAI, Google, Baichuan, and Zhipu for tailored translations.
- **Customizable Tones**: Decide on the tone of the translated text from standard, formal, or informal to suit the context.
- **Industry-Specific Accuracy**: Select an industry sector to ensure the translation is accurate within specific fields like biomedicine, IT, finance, and more.

## How It Works

Specially crafted to serve a wide array of languages and cater to distinct industry needs, FloweryTranslator ensues a two-tier translation process, beginning with an initial translation by Volcengine, followed by meticulous proofreading by an LLM of your choice to enhance accuracy and contextual relevance. The application has two separate interfaces for translating text and documents, with options to customize the translation based on model, industry sector, and tone. It supports `.docx` and `.pdf` file formats for document translation, with a seamless workflow that includes file uploading, content extraction, and translation.

## Getting Started

### Prerequisites

Before using FloweryTranslator, you should have the following:
- Python 3.8 or higher
- Dependency management tool (either pipenv or pip)

### Installation

1. Clone the repository or download the project files.
2. Locate the project directory and open a terminal session.
3. Install the necessary dependencies with pipenv or pip:

   ```sh
   pipenv install
   ```
   or
   ```sh
   pip install -r requirements.txt
   ```

4. Ensure required third-party services' API keys are configured in a `.env` file in the project directory.

### Running FloweryTranslator

To launch the application, execute the following command in the project directory:

```sh
python main.py
```

Once initiated, you can interact with the FloweryTranslator application through your web browser at the indicated local URL.

## Contributing

Contributions to FloweryTranslator are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the *GPL-3.0 license* - see the `LICENSE` file for details.

## Acknowledgements

- Thanks to all the underlying API providers: OpenAI, Google, Volcengine, HKBU, Baichuan, and Zhipu AI.
- Appreciation to the `gradio` SDK for enabling the creation of interactive machine learning interfaces with ease.
- Gratitude to everyone contributing to the enhancement and refinement of FloweryTranslator.

Your support and feedback are highly appreciated as we work collectively to refine the art of translation in the digital era.
