# Health Risk Profiler API

## Overview
The **Health Risk Profiler** is an AI-powered service that analyzes lifestyle survey responses (typed or scanned forms) and generates a structured health risk profile with actionable, non-diagnostic recommendations. The system handles noisy inputs, missing answers, and provides guardrails for incomplete data.

---

## Features
- Accepts **text input** and **image input** (via OCR)
- Extracts structured answers from survey forms
- Converts answers into **risk factors**
- Computes **risk level** and **score**
- Generates **actionable recommendations**
- Implements **guardrails** for incomplete or missing fields
- Outputs **structured JSON** for easy integration

---

## Project Structure
```

health-risk-profiler/
│
├── app/
│   ├── **init**.py            
│   ├── config.py              
│   ├── genai_processor.py     
│   ├── ocr_parser.py          
│   ├── routes.py              
│   └── schemas.py            
│
├── main.py                    
├── requirements.txt        
├── .gitignore
└── README.md

````

---

## Setup Instructions

1. **Clone the repository**
```cmd
git clone https://github.com/Aaxer24/health-risk-profiler.git
cd health-risk-profiler
````

2. **Create and activate a virtual environment**

```cmd
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```cmd
pip install -r requirements.txt
```

4. **Add `.env` file**
   Create a file `.env` in the project root with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the FastAPI server**

```cmd
uvicorn main:app --reload
```

6. **Optional:** Expose locally with ngrok for sharing/demo

```cmd
ngrok http 8000
```

---

## API Endpoints

### 1. Analyze Text

**POST** `/analyze_text`

**Form Data Example:**

```
text=age: 42 smoker: yes exercise: rarely diet: high sugar alcohol: no sleep: 7
```

**Sample Command Prompt `curl` request:**

```cmd
curl -X POST "http://127.0.0.1:8000/analyze_text" -F "text=age: 42 smoker: yes exercise: rarely diet: high sugar alcohol: no sleep: 7"
```

**Sample Response:**

```json
{
  "answers": {
    "age": 42,
    "smoker": true,
    "exercise": "rarely",
    "diet": "high sugar",
    "alcohol": false,
    "sleep": 7
  },
  "risk_level": "high",
  "score": 78,
  "factors": ["smoking","poor diet","low exercise"],
  "rationale": ["smoking","high sugar diet","low activity"],
  "recommendations": ["Quit smoking","Reduce sugar","Walk 30 mins daily"],
  "status": "ok"
}
```

---

### 2. Analyze Image (OCR)

**POST** `/analyze_image`

**Form Data:**

* Upload an image file containing survey answers (scanned form, screenshot, etc.)

**Sample Command Prompt `curl` request:**

```cmd
curl -X POST "http://127.0.0.1:8000/analyze_image" -F "file=@D:/Plum/health-risk-profiler/data/handwritten_image.png"
```

**Sample Response:** Same JSON structure as above.

---

## Architecture

* **FastAPI:** Backend API framework
* **EasyOCR:** Extracts text from scanned forms
* **LangChain + OpenAI GPT:** AI analysis for risk factors and recommendations
* **Modular design:**

  * `ocr_parser.py` → Parse text/image input
  * `genai_processor.py` → Generate risk assessment using AI
  * `routes.py` → API endpoints
  * `schemas.py` → Pydantic models for validation
  * `config.py` → Environment variable management

---

## Guardrails & Validation

* If **>50% fields are missing**, the API returns:

```json
{
  "status": "incomplete_profile",
  "reason": ">50% fields missing",
  "answers": {...}
}
```

* Ensures **robust handling of noisy inputs**
* AI outputs are **validated and returned as structured JSON**

---

## Testing the API

You can test endpoints using:

* **Postman**: Send POST requests with text or file input.
* **curl**: Examples provided above.
* **Python scripts**: Use `requests` library to send POST requests programmatically.

---

## Notes

* The API is **non-diagnostic** and for educational/experimental purposes.
* Fully extensible to include **additional survey fields** and **risk factors**.
* Modular code allows **easy integration with web or mobile frontends**.

---

## References

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [EasyOCR](https://www.jaided.ai/easyocr/)
* [LangChain](https://www.langchain.com/)
* [OpenAI API](https://platform.openai.com/docs/)

```

If you want, I can also **write a few more sample curl commands with different text/image inputs** ready for your submission. Do you want me to do that?
```


