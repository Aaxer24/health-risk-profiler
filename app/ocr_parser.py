# app/ocr_parser.py
import easyocr
from PIL import Image
import io
import numpy as np
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Survey keys expected in input
SURVEY_KEYS = ["age", "smoker", "exercise", "diet", "alcohol", "sleep"]

# Initialize EasyOCR reader (only once)
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if GPU is available

# Initialize GPT model
chat_model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# GPT prompt template for field extraction
prompt_template = ChatPromptTemplate.from_template(
    """
You are a health survey parser. Extract the following fields from the given text: {fields}.
Return only valid JSON with these keys: {fields}.

Rules:
- Booleans: true if the person mentions smoking or drinking alcohol at all, even socially or occasionally. False only if explicitly mentioned as not smoking/drinking. Null if no info.
- Numbers: integers only.
- Text fields: summarize in one sentence.
- Only fill fields based on the text. If not mentioned, set as null.
- Return strictly valid JSON.

Text: {text}
"""
)


def extract_fields_with_gpt(text: str):
    """
    Extract structured survey fields from text using GPT.
    """
    messages = prompt_template.format_prompt(
        text=text,
        fields=", ".join(SURVEY_KEYS)
    ).to_messages()

    response = chat_model.invoke(messages)

    # Convert GPT response to dictionary safely
    try:
        data = json.loads(response.content)
    except json.JSONDecodeError:
        data = {key: None for key in SURVEY_KEYS}

    # Compute confidence as proportion of non-null fields
    non_null = sum(1 for v in data.values() if v is not None)
    confidence = round(non_null / len(SURVEY_KEYS), 2)

    return {
        "answers": data,
        "missing_fields": [k for k, v in data.items() if v is None],
        "confidence": confidence
    }

def parse_text_input(text: str):
    """
    Parse direct text input into structured JSON using GPT.
    """
    return extract_fields_with_gpt(text)

def parse_image_input(file: bytes):
    """
    Parse image bytes into structured JSON using OCR + GPT.
    """
    # Load image from bytes
    image = Image.open(io.BytesIO(file))
    image_np = np.array(image)

    # Perform OCR
    results = reader.readtext(image_np)

    # Combine OCR results into single string
    text = " ".join([res[1] for res in results])

    return extract_fields_with_gpt(text)
