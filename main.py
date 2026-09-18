import os
from fastapi import FastAPI, Request
from google import genai

app = FastAPI()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
VERIFY_TOKEN = os.environ.get("CLUSTER_VERIFY_TOKEN")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.post("/navi")
async def cluster_external(request: Request):
    try:
        data = await request.json()
        user_query = data.get("request", "")
        
        # ★修正: プロンプトを英語に変更し、AIに英語で答えさせる
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=f"You are Navi, a terminal AI. Answer strictly in English, under 30 characters: {user_query}"
        )
        answer = response.text.strip()
    except Exception as e:
        # ★修正: エラーメッセージも英語に
        answer = "Connection error."

    return {
        "verify": VERIFY_TOKEN,
        "response": answer
    }

@app.get("/")
def health_check():
    return {"status": "ok"}
