from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import base64
from Crypto.Cipher import AES
import hashlib

app = Flask(__name__)

CHANNEL_SECRET = '297e52f347a7b5346baffbacf8503f8b'
CHANNEL_ACCESS_TOKEN = 'jGdIeEGvFXp3+kXYmXHPl0SAxe9ME8Zq6poNv3OmTtJqHzuWBZ+pFnjbgyanMT8LanOuTaXg0OogkD9eBbtwhXmiqgYb3mJcjDEWPg6axW1xIH6nOIGsYXZpMNNK7Le/QN+vQJHkVuE5o5Jbs2lqVAdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# AES暗号化用関数（共通鍵で暗号化・Base64エンコード）
def encrypt_message(key, message):
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()
    cipher = AES.new(key_hash, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

# AES復号用関数（共通鍵で復号・Base64デコード）
def decrypt_message(key, encrypted_message):
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()
    encrypted_data = base64.b64decode(encrypted_message)
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key_hash, AES.MODE_EAX, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted.decode('utf-8')

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
    text = event.message.text

    if text.startswith('/encode '):
        try:
            parts = text.split(' ', 2)
            if len(parts) < 3:
                reply_text = '使い方: /encode キーワード メッセージ'
            else:
                key = parts[1]
                msg = parts[2]
                encrypted = encrypt_message(key, msg)
                reply_text = f'暗号文: {encrypted}'
        except Exception as e:
            reply_text = f'エラー: {str(e)}'

    elif text.startswith('/decode '):
        try:
            parts = text.split(' ', 2)
            if len(parts) < 3:
                reply_text = '使い方: /decode キーワード 暗号文'
            else:
                key = parts[1]
                encrypted_msg = parts[2]
                decrypted = decrypt_message(key, encrypted_msg)
                reply_text = f'復号文: {decrypted}'
        except Exception as e:
            reply_text = f'復号エラー: {str(e)}'

    else:
        reply_text = '「/encode キーワード メッセージ」で暗号化、「/decode キーワード 暗号文」で復号化できます'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
