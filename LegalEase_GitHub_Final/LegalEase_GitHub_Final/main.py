from fastapi import FastAPI
from routes import router

app = FastAPI(title="LegalEase API")

@app.get("/")
def root():
    return {"status": "LegalEase backend running"}

app.include_router(router)
