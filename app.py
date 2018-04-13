from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('fWY8cZFQEVDLhpi2YTn0x5v1lW8kf2P2gWNRsOU+Y/Ftsx2I6kFfhSR3ej5TIGg7xl6CS4RROpSGR0jE98cg3m10CUPpELENt7NRELxXxxj1AEZVAAdmaAykMtmnrocj2Bx0qCTluKm5B/lHncoveQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b284cb989441ebcfb2a69c157d445ba')

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
