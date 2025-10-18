import json
import aiohttp
import requests

from task.clients.base import AIClient
from task.constants import MAX_TOKENS, CLAUDE_MODEL, DEFAULT_SYSTEM_PROMPT, BOT_PREFIX
from task.models.message import Message
from task.models.role import Role


class CustomAnthropicAIClient(AIClient):

    def get_completion(self, messages: list[Message], **kwargs) -> Message:
        headers = self._prepare_headers()
        payload = self._prepare_payload(messages)

        response = requests.post(self._endpoint, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        answer = data["content"][0]["text"]
        print(f"{BOT_PREFIX}{answer}")
        return Message(Role.AI, answer)


    async def stream_completion(self, messages: list[Message], **kwargs) -> Message:
        #TODO:
        # https://docs.anthropic.com/en/docs/build-with-claude/streaming
        # - Prepare headers with api key, anthropic version and content type
        # - Add System prompt
        # - Execute post request to AI API (use `aihttp`)
        # - Handle stream with chunks
        # - Parse response
        # - Print chunks to console
        # - Return AI message
        # raise NotImplementedError
        pass

    def _prepare_payload(self, messages):
        formatted_messages = [message.to_dict() for message in messages]
        return {
            "model": CLAUDE_MODEL,
            "messages": formatted_messages,
            "max_tokens": MAX_TOKENS,
            "system": DEFAULT_SYSTEM_PROMPT,
        }

    def _prepare_headers(self):
        return {
            "X-Api-Key": self._api_key,
            "Content-Type": "application/json",
            "Anthropic-Version": "2023-06-01"
        }