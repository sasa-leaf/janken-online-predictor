import asyncio
import os

import nest_asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pyngrok import ngrok
from uvicorn import Config, Server

from app.model_utils import MOVES, ai_instance
from app.visualization import create_probability_chart

# 設定
PORT = 8000
NGROK_TOKEN = os.getenv("NGROK_TOKEN")  # 環境変数からトークン取得推奨

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 静的ファイル用ディレクトリ（必要なら作成）
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """トップページ"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/play")
async def play(request: Request):
    """じゃんけんを実行するAPI"""
    data = await request.json()
    user_move = int(data.get("move"))

    # 1. AIがユーザーの次の手を予測 (確率は前のターンまでの履歴に基づく)
    pred_probs = ai_instance.predict_next_move()

    # 2. AIが手を決める
    ai_move = ai_instance.get_counter_move(pred_probs)

    # 3. 勝敗判定
    result_text = ai_instance.determine_result(user_move, ai_move)

    # 4. 予測データの可視化生成
    chart_img = create_probability_chart(pred_probs)

    # 5. AI学習 (今回の手を履歴に追加して学習)
    ai_instance.update_and_train(user_move)

    return JSONResponse(
        {
            "user_move_name": MOVES[user_move],
            "ai_move_name": MOVES[ai_move],
            "result": result_text,
            "games_count": len(ai_instance.history),
            "chart_img": chart_img,
        }
    )


@app.post("/reset")
async def reset():
    """履歴をリセット"""
    ai_instance.history = []
    ai_instance.model = ai_instance._build_model()
    return JSONResponse({"status": "reset"})


def main():
    """サーバー起動"""
    nest_asyncio.apply()
    if NGROK_TOKEN:
        ngrok.set_auth_token(NGROK_TOKEN)
        public_url = ngrok.connect(PORT)
        print(f"🔗 公開URL: {public_url.public_url}")
    else:
        print("⚠️ Ngrok Tokenが設定されていません。ローカルでのみアクセス可能です。")

    config = Config(app=app, host="0.0.0.0", port=PORT, log_level="info")
    server = Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
