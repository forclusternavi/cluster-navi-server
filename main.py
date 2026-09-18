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
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=f"あなたはターミナル常駐AIのNaviです。30文字以内で簡潔に回答してください: {user_query}"
        )
        answer = response.text.strip()
    except Exception as e:
        answer = "通信エラーが発生しました。"

    return {
        "verify": VERIFY_TOKEN,
        "response": answer
    }

@app.get("/")
def health_check():
    return {"status": "ok"}
