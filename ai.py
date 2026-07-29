from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import mimetypes
import time
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_image(image_path):
    print(f"AI received image: {image_path}")

    time.sleep(1)

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        print("Unsupported file type.")
        return

    with open(image_path, "rb") as file:
        image = file.read()

        response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            """
You are an AI file organizer.
Analyze this image and reply ONLY with valid JSON.

Format:
{
  "filename": "...",
  "folder": "..."
}

Rules:
- filename should be short.
- Do not include the file extension.
- folder can contain subfolders using "/".
- No explanations.
- No markdown.
- JSON only.
""",
            types.Part.from_bytes(
                data=image,
                mime_type=mime_type
            )
        ]
    )

    try:
        result = json.loads(response.text)
        print(result)
        return result

    except Exception:
        print("Failed to parse AI response.")
        return None
