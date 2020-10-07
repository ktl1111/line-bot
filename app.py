# 我們要寫一個伺服器，放在雲端上執行，來接收line轉載過來的訊息
# 這個伺服器要跟line的程式做互動
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'YzpbfkqJwhJMy6H0cc9vyLtdlROBZzeMkPQo9yvgcQvBaHBWnW8TV0o7oZh400spWRct3sIPx9WE50tSHqeR5v0gIz/GF1+ahmJ1m+R1GlE8yfsJuA7GytV4lQZhaHaGD4pAH0cbOxP18tmDSmr4LgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cb60a307dc00a676ba90f8b3cafec5c4')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂你說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg in ['hi', 'Hi', 'HI', '嗨一', '嗨']:
        r = '嗨'
    elif msg in ['你吃飯了嗎', '你吃飯了嗎?']:
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '定位' or '訂位' in msg:
        r = '你想定位，是嗎？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
