from abc import ABC

from task.clients.base import AIClient


class BaseOpenAIClient(AIClient, ABC):

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        super().__init__(endpoint, model_name, system_prompt, api_key)
