from anthropic import Anthropic, AsyncAnthropic
from task.clients.base import AIClient
from task.constants import MAX_TOKENS, BOT_PREFIX, DEFAULT_SYSTEM_PROMPT
from task.models.message import Message
from task.models.role import Role


class AnthropicAIClient(AIClient):

    def __init__(self, endpoint: str, model_name: str, api_key: str, system_prompt: str):
        super().__init__(endpoint, model_name, api_key, system_prompt)
        self.client = Anthropic()
        self.async_client = AsyncAnthropic()

    def get_completion(self, messages: list[Message], **kwargs) -> Message:
        formatted_messages = [message.to_dict() for message in messages]
        response = self.client.messages.create(
            model=self._model_name,
            messages=formatted_messages,
            max_tokens=MAX_TOKENS,
            system=DEFAULT_SYSTEM_PROMPT
        )
        answer = response.content[0].text
        print(f"{BOT_PREFIX}{answer}")
        return Message(Role.AI, answer)

    async def stream_completion(self, messages: list[Message], **kwargs) -> Message:
        formatted_messages = [message.to_dict() for message in messages]
        async with self.async_client.messages.stream(
                model=self._model_name,
                messages=formatted_messages,
                max_tokens=MAX_TOKENS,
                system=DEFAULT_SYSTEM_PROMPT,
        ) as stream:
            answer=""
            async for event in stream:
                if event.type == "content_block_start":
                    print(BOT_PREFIX, end=" ")
                elif event.type == "content_block_delta" and event.delta.text:
                    print(event.delta.text, end="")
                    answer += event.delta.text
                elif event.type == "message_delta":
                    print()
        return Message(Role.AI, answer)
