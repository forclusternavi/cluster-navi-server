import os
from fastapi import FastAPI, Request
from google import genai
from google.genai import types  # ★設定用のモジュールを追加

app = FastAPI()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
VERIFY_TOKEN = os.environ.get("CLUSTER_VERIFY_TOKEN")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.post("/navi")
async def cluster_external(request: Request):
    try:
        data = await request.json()
        user_query = data.get("request", "")
        
        # ★API側で文体、言語、長さを詳細に設定
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=user_query,
            config=types.GenerateContentConfig(
                # AIの性格・言語・文体の根本設定（英語で指示を出すと英語で返しやすくなります）
                system_instruction="You are Navi, an AI in an old underground terminal. Answer strictly in short English. Be cynical, mechanical, and slightly cryptic.",
                
                # トークン数（文字数）の物理的な上限。これ以上は強制的にカットされます
                max_output_tokens=30, 
                
                # 回答の温度感。0.0（完全に機械的で固定）〜 2.0（非常にランダムで感情的）
                temperature=0.4 
            )
        )
        answer = response.text.strip()
    except Exception as e:
        answer = "Connection error."

    return {
        "verify": VERIFY_TOKEN,
        "response": answer
    }

@app.get("/")
def health_check():
    return {"status": "ok"}
