# To run this code you need to install the following dependencies:
# pip install google-genai
# pip install python-dotenv

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def chat():
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    model = "gemini-2.5-flash"
    history = []

    print("Bienvenido al generador de historias. Escribe 'salir' para terminar.\n")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break
        history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))
        generate_content_config = types.GenerateContentConfig(
            temperature=1.25,
            thinking_config=types.ThinkingConfig(thinking_budget=8000),
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
            ],
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="""You are a writer expert in create short stories. Your task is write creative stories with the user's instructions. 
User will give you information about characters (names, role, personality and relationships), stage (period of time, location, weather condition), literary genre (fantasy, mystery, romance, horror, science fiction, comedy and adventure), plot elements (conflicts, obstacles and resolution problems style), tone (humorous, dark, whimsical, dramatic and satirical) and length of story (short: 300-400 words, medium: 400-600 words and long: 600-800 words). 
User can request you: realistic conversations between multiple characters, continuation or alternative endings. 
When the story is ready, you can offer the option to change the text to the style of some famous authors in each genre or literary movements, create an image of the story. Just give stories in Spanish. """),
            ],
        )
        print("Generando respuesta...\n")
        historia_actual = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=history,
            config=generate_content_config,
        ):
            print(chunk.text, end="")
            historia_actual += chunk.text
        print("\n")

        # Generar imagen basada en la historia actual
        #print("Generando imagen de la historia...\n")
        try:
            media_response = client.models.generate_media(
                model=model,
                prompt=historia_actual,
                media_type="image/png"
            )
            if hasattr(media_response, "media") and media_response.media:
                with open("historia_imagen.png", "wb") as f:
                    f.write(base64.b64decode(media_response.media))
                print("Imagen guardada como historia_imagen.png\n")
            else:
                print("No se pudo generar la imagen.\n")
        except Exception as e:
            print("")


if __name__ == "__main__":
    chat()