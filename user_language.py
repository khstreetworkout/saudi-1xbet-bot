import json
import os

LANGUAGE_FILE = os.path.join("/app/data" if os.path.exists("/app/data") else ".", "user_languages.json")

def load_languages():
    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_languages(languages):
    with open(LANGUAGE_FILE, 'w') as f:
        json.dump(languages, f, indent=2)

def get_user_language(user_id):
    languages = load_languages()
    return languages.get(str(user_id), "en")

def set_user_language(user_id, lang):
    languages = load_languages()
    languages[str(user_id)] = lang
    save_languages(languages)
