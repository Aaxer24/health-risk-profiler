# app/ocr_parser.py
import easyocr
from PIL import Image
import io
import numpy as np
import re

# Survey keys expected in input
SURVEY_KEYS = ["age", "smoker", "exercise", "diet", "alcohol", "sleep"]

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have a GPU

def extract_fields_from_text(text: str):
    """
    Extract structured answers from raw text robustly.
    Handles multi-word values, noisy separators, and normalizes booleans/numerics.
    """
    answers = {}
    missing_fields = []

    # Preprocess text: remove extra spaces and normalize line breaks
    text = re.sub(r"\s+", " ", text).strip()

    for i, key in enumerate(SURVEY_KEYS):
        # Capture everything until the next key or end of string
        if i < len(SURVEY_KEYS) - 1:
            next_key = SURVEY_KEYS[i + 1]
            pattern = rf"{key}\s*[:=\-]?\s*(.+?)(?=\s*{next_key}\s*[:=\-]|\s*$)"
        else:
            pattern = rf"{key}\s*[:=\-]?\s*(.+)$"

        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Normalize boolean fields
            if key in ["smoker", "alcohol"]:
                answers[key] = str(value).lower() in ["yes", "true", "1"]
            # Normalize numeric fields
            elif key in ["age", "sleep"]:
                try:
                    answers[key] = int(re.findall(r"\d+", value)[0])
                except:
                    answers[key] = None
            else:
                answers[key] = value
        else:
            answers[key] = None
            missing_fields.append(key)

    confidence = round(1 - len(missing_fields)/len(SURVEY_KEYS), 2)
    return {"answers": answers, "missing_fields": missing_fields, "confidence": confidence}

def parse_text_input(text: str):
    """
    Parse direct text input into structured JSON.
    Example: "age: 42 smoker: yes exercise: rarely diet: high sugar"
    """
    return extract_fields_from_text(text)

def parse_image_input(file: bytes):
    """
    Parse image bytes into structured JSON using EasyOCR.
    """
    # Load image from bytes
    image = Image.open(io.BytesIO(file))
    image_np = np.array(image)

    # Perform OCR
    results = reader.readtext(image_np)
    # Combine OCR results into single string
    text = " ".join([res[1] for res in results])

    return extract_fields_from_text(text)
