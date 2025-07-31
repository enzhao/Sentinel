import json
from pathlib import Path
from typing import Dict, Any

class MessageManager:
    _instance = None
    _messages: Dict[str, str] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageManager, cls).__new__(cls)
            cls._instance.load_messages()
        return cls._instance

    def load_messages(self):
        """Loads message templates from the JSON file."""
        config_path = Path(__file__).parent.parent / "config" / "messages.json"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._messages = json.load(f)
            print("Successfully loaded message templates.")
        except FileNotFoundError:
            print(f"Warning: Message file not found at {config_path}. Messages will not be available.")
            self._messages = {}
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {config_path}. Messages will not be available.")
            self._messages = {}

    def get_message(self, key: str, **kwargs: Any) -> str:
        """
        Formats a message string with the given key and arguments.

        Args:
            key: The message key (e.g., "P_I_1001").
            **kwargs: The arguments to format the string with.

        Returns:
            The formatted message string.
        """
        template = self._messages.get(key, f"Missing message for key: {key}")
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"Warning: Missing placeholder {e} for message key {key}")
            return f"Missing placeholder {e} for message key: {key}"

# Singleton instance
message_manager = MessageManager()

def get_message(key: str, **kwargs: Any) -> str:
    """
    A convenience function to access the MessageManager singleton.
    """
    return message_manager.get_message(key, **kwargs)
