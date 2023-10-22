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
        self._num_messages_at_start = 1

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
        self.personality = self.personality_config["personality"]
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
            del self._messages[self._num_messages_at_start : self._num_messages_at_start + 2]

        self._messages.append({"role": role, "content": msg})

    def _msg_system(self, msg):
        self._add_msg("system", msg)

    def _msg_assistant(self, msg):
        self._add_msg("assistant", msg)

    def _msg_user(self, msg):
        self._add_msg("user", msg)

    def _generate_response(self):
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

    def load_chat(self):
        try:
            if not os.path.exists(self._chat_history_filename):
                raise FileNotFoundError("Chat history does not exist.")

            self._messages = eval(read_txt_file(self._chat_history_filename))
        except (FileNotFoundError, SyntaxError):
            self._msg_system(
                f"Your name is {self.name}. {self.personality}. You follow these rules: \n{Chatbot.create_numbered_list(self.rules)}"
            )

        self._num_messages_at_start = len(self._messages)

    def summarise_chat(self, num_messages):
        self._msg_user(f"Can you summarise the last {num_messages} messages? Keep your response concise.")
        summary = self._generate_response()
        del self._messages[self._num_messages_at_start :]
        self._msg_system(f"Summary of last conversation: {summary}")

    def end_chat(self):
        num_messages = len(self._messages) - self._num_messages_at_start

        if num_messages > 0:
            self.summarise_chat(num_messages)
            write_to_txt_file(self._chat_history_filename, str(self._messages))

    def send_message(self, msg):
        if len(msg) == 0:
            return "Can't send empty message!"

        self._msg_user(msg)
        return "Message sent!"

    def get_reply(self):
        return self._generate_response()
