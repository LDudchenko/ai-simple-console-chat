from abc import ABC

from task.clients.base import AIClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.message import Message
from task.models.role import Role


class BaseOpenAIClient(AIClient, ABC):

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        super().__init__(endpoint, model_name, api_key, system_prompt)

    @staticmethod
    def _prepare_message_history(messages):
        system_message = Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT)
        messages_with_system_prompt = [system_message] + messages
        return [message.to_dict() for message in messages_with_system_prompt]
