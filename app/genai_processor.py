# app/genai_processor.py
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json
from collections import OrderedDict  

# Load environment variable
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize ChatOpenAI model
chat_model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# GPT prompt for structured health risk analysis
risk_prompt = ChatPromptTemplate.from_template(
    """
You are a health risk assistant. Analyze the following answers and provide structured JSON output.
Input: {answers}

Output JSON should include:
- risk_level: "low", "medium", or "high"
- score: numeric risk score (0-100)
- factors: list of contributing risk factors (e.g., ["smoking","poor diet"])
- rationale: list of reasons behind the risk level
- recommendations: actionable, non-diagnostic guidance
Return only valid JSON.
"""
)

def analyze_health_risk(parsed):
    """
    Analyze structured answers and return full risk assessment JSON.
    Applies guardrail if >50% fields missing.
    """
    # Ensure input is a dictionary with 'answers'
    if isinstance(parsed, list):
        parsed = {"answers": parsed}

    answers = parsed.get("answers", {})

    # Guardrail / exit condition if >50% fields missing
    total_fields = len(answers)
    missing_count = sum(1 for v in answers.values() if v is None)
    if total_fields > 0 and missing_count / total_fields >= 0.5:
        return {
            "answers": answers,  # ✅ answers always first
            "status": "incomplete_profile",
            "reason": ">50% fields missing"
        }

    # Generate risk assessment using GPT
    messages = risk_prompt.format_prompt(answers=answers).to_messages()
    response = chat_model.invoke(messages)

    # Parse GPT response safely
    try:
        risk_data = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback if GPT returns text instead of JSON
        risk_data = {
            "risk_level": "unknown",
            "score": None,
            "factors": [],
            "rationale": [],
            "recommendations": []
        }

    # Ensure 'status'
    risk_data.setdefault("status", "ok")

    ordered = OrderedDict()
    ordered["answers"] = answers
    for k, v in risk_data.items():
        if k != "answers":
            ordered[k] = v

    return ordered
