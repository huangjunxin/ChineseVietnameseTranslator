import gradio as gr
from app.routes.text_translator import text_translator
from app.routes.document_translator import document_translator

# Combine both interfaces into tabs
demo = gr.TabbedInterface(
    title="FloweryTranslator",
    interface_list=[text_translator, document_translator],
    tab_names=["Text", "Document"]
)

if __name__ == "__main__":
    demo.launch(show_api=False)
