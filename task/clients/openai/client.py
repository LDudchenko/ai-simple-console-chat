from openai import OpenAI

from task.clients.openai.base import BaseOpenAIClient
from task.constants import DEFAULT_SYSTEM_PROMPT, BOT_PREFIX
from task.models.message import Message
from task.models.role import Role


class OpenAIClient(BaseOpenAIClient):

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        super().__init__(endpoint, model_name, system_prompt, api_key)
        self.client = OpenAI()


    def get_completion(self, messages: list[Message], **kwargs) -> Message:
        messages = self._prepare_message_history(messages)
        completion = self.client.chat.completions.create(
            model=self._model_name,
            messages=messages,
        )
        answer = completion.choices[0].message.content
        print(f"{BOT_PREFIX}{answer}")
        return Message(Role.AI, answer)

    async def stream_completion(self, messages: list[Message], **kwargs) -> Message:
        messages = self._prepare_message_history(messages)
        stream = self.client.chat.completions.create(
            model=self._model_name,
            messages=messages,
            stream=True
        )

        answer = BOT_PREFIX
        for event in stream:
            delta = event.choices[0].delta.content
            if delta is None:
                break

            print(delta, end="", flush=True)
            answer += delta
        print()
        return Message(Role.AI, answer)


    @staticmethod
    def _prepare_message_history(messages):
        system_message = Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT)
        messages_with_system_prompt = [system_message] + messages
        return [message.to_dict() for message in messages_with_system_prompt]
