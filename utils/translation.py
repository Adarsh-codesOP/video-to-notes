
from googletrans import Translator

def translate_to_kannada(text: str) -> str:
    """
    Translates the input text to Kannada using Google Translate API.
    :param text: The text to be translated.
    :return: Translated text in Kannada.
    """
    translator = Translator()

 
    translated_text = translator.translate(text, src='en', dest='kn').text

    return translated_text

if __name__ == "__main__":
    sample_text = "This is a sample text that will be translated into Kannada."
    translated = translate_to_kannada(sample_text)
    print(f"Original: {sample_text}")
    print(f"Translated: {translated}")