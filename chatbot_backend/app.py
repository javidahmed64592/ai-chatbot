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


@app.route("/api/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        return jsonify({"messages": chatbot._messages})
    elif request.method == "POST":
        data = json.loads(request.data)
        message = data["message"]
        reply = chatbot.chat(message)
        return jsonify({"reply": reply})


if __name__ == "__main__":
    system_msg("Loading environment variables...")
    load_dotenv()

    try:
        system_msg("Running app...")
        app.run(host="0.0.0.0")
        system_msg("App running!...")
    except (KeyboardInterrupt, SystemExit):
        system_msg("Shutting down program...")
