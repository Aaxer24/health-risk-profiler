# app/routes.py
from fastapi import APIRouter, UploadFile, File, Form
from app.ocr_parser import parse_text_input, parse_image_input
from app.genai_processor import analyze_health_risk

router = APIRouter()

@router.post("/analyze_text")
async def analyze_text(text: str = Form(...)):
    """
    Endpoint to analyze survey answers submitted as text.

    Example input:
    "age: 42 smoker: yes exercise: rarely diet: high sugar alcohol: no sleep: 7"

    Output JSON includes:
    - answers
    - risk_level
    - factors
    - score
    - rationale
    - recommendations
    - status
    """
    # Step 1: Parse text input into structured answers
    parsed = parse_text_input(text)
    
    # Step 2: Analyze health risk and generate recommendations
    result = analyze_health_risk(parsed)
    
    return result

@router.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Endpoint to analyze survey answers submitted as an image (OCR).

    Example: Upload a scanned form or screenshot with fields like:
    "Age: 42 Smoker: yes Exercise: rarely Diet: high sugar Alcohol: no Sleep: 7"

    Output JSON includes:
    - answers
    - risk_level
    - factors
    - score
    - rationale
    - recommendations
    - status
    """
    # Read uploaded file as bytes
    contents = await file.read()
    
    # Step 1: Parse image into structured answers using OCR
    parsed = parse_image_input(contents)
    
    # Step 2: Analyze health risk and generate recommendations
    result = analyze_health_risk(parsed)
    
    return result
