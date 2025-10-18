from openai import OpenAI, AsyncOpenAI
from task.clients.openai.base import BaseOpenAIClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.message import Message
from task.models.role import Role


class OpenAIClient(BaseOpenAIClient):

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        super().__init__(endpoint, model_name, system_prompt, api_key)
        self.client = OpenAI()
        self.async_client = AsyncOpenAI()


    def get_completion(self, messages: list[Message], **kwargs) -> Message:
        system_message = Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT)
        messages_with_system_prompt = [system_message] + messages
        formatted_messages = [m.to_dict() for m in messages_with_system_prompt]
        completion = self.client.chat.completions.create(
            model=self._model_name,
            messages=formatted_messages,
        )
        answer = completion.choices[0].message.content
        return Message(Role.AI, answer)


    async def stream_completion(self, messages: list[Message], **kwargs) -> Message:
        #TODO:
        # - Prepare message history with System prompt
        # - Call client with streaming mode
        # - Handle stream with chunks
        # - Print response to console
        # - Return AI message
        raise NotImplementedError
