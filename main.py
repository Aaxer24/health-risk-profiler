# main.py
import warnings
warnings.filterwarnings("ignore", message=".*pin_memory.*")

from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Health Risk Profiler API",
    description="API to analyze lifestyle survey responses (text or scanned forms) and generate structured health risk profiles.",
    version="1.0.0"
)

# Include the router with endpoints
app.include_router(router)

@app.get("/")
def home():
    """
    Health Risk Profiler API root endpoint.
    """
    return {"message": "Health Risk Profiler API is running"}
