import openai
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.crud import update_translation_task
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Set OpenAI API key
openai.api_key = API_KEY

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}

    for lang in languages:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use a valid model name
                messages=[
                    {'role': "system", "content": f"You are a helpful assistant that translates text into {lang}."},
                    {'role': "user", "content": text}
                ],
                max_tokens=1000
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            translations[lang] = translated_text
            print(f"Translation for {lang}: {translated_text}")
        except Exception as e:
            error_message = f"Error translating to {lang}: {str(e)}"
            print(error_message)
            translations[lang] = error_message

    # Update the database with translations
    try:
        update_translation_task(db, task_id, translations)
        print(f"Updated task {task_id} in database with translations.")
    except Exception as e:
        print(f"Error updating database: {str(e)}")
