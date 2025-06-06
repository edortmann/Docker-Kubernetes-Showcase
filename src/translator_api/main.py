from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.translator_core.model import translate

app = FastAPI(title="Translator-API")

class Payload(BaseModel):
    text: str

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}

@app.post("/translate", tags=["inference"])
def translate_endpoint(payload: Payload):
    if not payload.text.strip():
        raise HTTPException(status_code=422, detail="Empty text")
    return {"translation": translate(payload.text)}
