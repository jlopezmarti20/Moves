from google import genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini model to use
MODEL_NAME = "gemini-3.6-flash"

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_user_request(user_request):
    """
    Analyze a user's natural language request and return
    a structured Python dictionary.
    """

    prompt = f"""
    You are part of the Moves recommendation engine.

    The user says:

    "{user_request}"

    Your job is to classify the user's request.

    The mood MUST be exactly one of these:

    - shopping
    - coffee
    - party
    - food
    - workout
    - adventurous
    - artsy
    - education

    Return ONLY raw JSON.

    Rules:
    - Do NOT use markdown.
    - Do NOT wrap the response in ```json.
    - Do NOT include explanations.
    - The "mood" field must be one of the allowed moods.
    - The "place_types" field must contain only valid Google Place Types.
    - The "keywords" field should contain descriptive search terms.

    Return exactly this structure:

    {{
        "mood": "",
        "place_types": [],
        "keywords": []
    }}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

    except Exception as e:

        # Gemini free-tier rate limit
        if "429" in str(e):
            raise RuntimeError(
                "Gemini rate limit exceeded. Please wait about a minute and try again."
            )

        raise RuntimeError(f"Gemini request failed:\n{e}")

    text = response.text.strip()

    # Remove markdown if Gemini accidentally returns it
    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        raise ValueError(
            f"Gemini returned invalid JSON:\n\n{text}"
        )


    