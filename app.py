from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# ここに自分の値を貼り付け！
CHANNEL_SECRET = 297e52f347a7b5346baffbacf8503f8b
CHANNEL_ACCESS_TOKEN = jGdIeEGvFXp3+kXYmXHPl0SAxe9ME8Zq6poNv3OmTtJqHzuWBZ+pFnjbgyanMT8LanOuTaXg0OogkD9eBbtwhXmiqgYb3mJcjDEWPg6axW1xIH6nOIGsYXZpMNNK7Le/QN+vQJHkVuE5o5Jbs2lqVAdB04t89/1O/w1cDnyilFU=

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーのメッセージをそのまま返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
