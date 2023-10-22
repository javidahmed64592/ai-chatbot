import json
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from chatbot.chatbot import Chatbot
from helpers.general_helpers import system_msg

PERSONALITIES_FOLDER = Path("./personalities")
CHAT_HISTORY_FOLDER = Path("./history")

app = Flask(__name__)
chatbot = Chatbot(
    personality_config_filepath=PERSONALITIES_FOLDER / "piper.json",
    chat_history_directory=CHAT_HISTORY_FOLDER,
)


@app.route("/api/chat/load", methods=["GET"])
def load_chat():
    if request.method == "GET":
        chatbot.load_chat()
        return jsonify(success=True)


@app.route("/api/chat/end", methods=["GET"])
def end_chat():
    if request.method == "GET":
        chatbot.end_chat()
        return jsonify(success=True)


@app.route("/api/messages", methods=["GET"])
def messages():
    if request.method == "GET":
        return jsonify({"messages": chatbot._messages})


@app.route("/api/chat/send", methods=["POST"])
def send_message():
    if request.method == "POST":
        data = json.loads(request.data)
        message = data["message"]
        reply = chatbot.send_message(message)
        return jsonify({"reply": reply})


@app.route("/api/chat/reply", methods=["GET"])
def get_reply():
    if request.method == "GET":
        reply = chatbot.get_reply()
        return jsonify({"reply": reply})


if __name__ == "__main__":
    print(system_msg("Loading environment variables..."))
    load_dotenv()

    try:
        print(system_msg("Running app..."))
        app.run(host="0.0.0.0")
        print(system_msg("App running!..."))
    except (KeyboardInterrupt, SystemExit):
        print(system_msg("Shutting down program..."))
