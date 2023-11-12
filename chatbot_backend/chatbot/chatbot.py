import os

import openai
from openai.error import RateLimitError

from helpers.general_helpers import load_json, read_txt_file, update_json_file, write_to_txt_file


class Chatbot:
    def __init__(self, personality_config_filepath, chat_history_directory):
        self._api_key = os.getenv("API_KEY")
        openai.api_key = self._api_key

        self._personality_config_filepath = personality_config_filepath
        self._personality_config = None
        self.set_personality()

        self._chat_history_directory = chat_history_directory
        self._chat_history_filename = self._chat_history_directory / f"{self.name}.txt"
        self._messages = []
        self._chat_summaries = []

    @property
    def personality_config(self):
        if not self._personality_config:
            self._personality_config = load_json(self._personality_config_filepath)

        return self._personality_config

    @personality_config.setter
    def personality_config(self, new_config):
        self._personality_config = new_config
        update_json_file(self._personality_config_filepath, new_config)
        self.set_personality()

    def set_personality(self):
        self.name = self.personality_config["name"]
        self.rules = self.personality_config["rules"]

        self.model = self.personality_config["model"]
        self.temperature = self.personality_config["temperature"]
        self.max_tokens = self.personality_config["max_tokens"]
        self.n = self.personality_config["n"]
        self.stop = self.personality_config["stop"]
        self.max_messages = self.personality_config["max_messages"]

    @staticmethod
    def create_numbered_list(lst):
        numbered_list = [f"{i}) {item}" for i, item in enumerate(lst, start=1)]
        numbered_string = "\n".join(numbered_list)
        return numbered_string

    def _add_msg(self, role, msg):
        if len(self._messages) >= self.max_messages:
            del self._messages[1:3]

        self._messages.append({"role": role, "content": msg})

    def _msg_system(self, msg):
        self._add_msg("system", msg)

    def _msg_assistant(self, msg):
        self._add_msg("assistant", msg)

    def _msg_user(self, msg):
        self._add_msg("user", msg)

    def _create_context_msg(self):
        context_msg = (
            f"Your name is {self.name}. You follow these rules: \n\n{Chatbot.create_numbered_list(self.rules)}"
        )

        if self._chat_summaries:
            context_msg += f"\n\nIn previous conversations, we have discussed: \n\n{Chatbot.create_numbered_list(self._chat_summaries)}"

        return context_msg

    def generate_response(self):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self._messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                n=self.n,
                stop=self.stop,
            )

            reply = response.choices[0]["message"]["content"]
            self._msg_assistant(reply)

        except RateLimitError:
            reply = "Too many requests! Please try again shortly..."
            del self._messages[-1]
        except Exception as err:
            reply = f"Something has gone wrong: {err}"
            del self._messages[-1]
        finally:
            return reply

    def reset_chat(self):
        self._messages = []
        self._msg_system(self._create_context_msg())

    def load_chat(self):
        reply = "Starting new chat..."

        if os.path.exists(self._chat_history_filename):
            self._chat_summaries = eval(read_txt_file(self._chat_history_filename))
            reply = "Chat summaries loaded successfully."

        self.reset_chat()
        return reply

    def summarise_chat(self):
        self._msg_user(f"Can you summarise all these messages? Ignore the first message. Keep your response concise.")
        summary = self.generate_response()
        self._chat_summaries.append(summary)

    def end_chat(self):
        reply = "Ending chat without summarising..."
        num_messages = len(self._messages)

        if num_messages > 4:
            self.summarise_chat()
            write_to_txt_file(self._chat_history_filename, str(self._chat_summaries))
            self.reset_chat()
            reply = "Last conversation successfully summarised. Ending chat..."

        return reply

    def send_message(self, msg):
        if len(msg) == 0:
            return "Can't send empty message!"

        self._msg_user(msg)
        return "Message sent!"
