from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import mimetypes
import time
import json

load_dotenv()


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        with open("data/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        return config.get("api_key")

    except (FileNotFoundError, json.JSONDecodeError):
        return None


def analyze_image(image_path, folders):
    print(f"AI received image: {image_path}")

    api_key = get_api_key()

    if not api_key:
        print("No Gemini API key configured.")
        return None

    client = genai.Client(api_key=api_key)

    time.sleep(1)

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        print("Unsupported file type.")
        return None

    with open(image_path, "rb") as file:
        image = file.read()

    prompt = f"""
You are an AI file organizer.
Analyze this image and reply ONLY with valid JSON.

Format:
{{
    "filename": "...",
    "folder": "..."
}}

Available folders:
{folders}

Rules:
- Filename should be short and descriptive.
- Do not include the file extension.
- You MUST choose exactly one folder from Available folders.
- NEVER create a new folder name.
- Folder must exactly match one of the provided folder names.
- No explanations.
- No markdown.
- JSON only.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image,
                    mime_type=mime_type
                )
            ]
        )

    except Exception as e:
        print(f"AI error: {e}")
        return None

    try:
        result = json.loads(response.text)
        print(result)
        return result

    except Exception:
        print("Failed to parse AI response.")
        return None