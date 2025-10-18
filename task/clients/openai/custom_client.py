import json
import aiohttp
import requests

from task.clients.openai.base import BaseOpenAIClient
from task.constants import DEFAULT_SYSTEM_PROMPT, BOT_PREFIX, MAX_TOKENS
from task.models.message import Message
from task.models.role import Role


class CustomOpenAIClient(BaseOpenAIClient):

    def get_completion(self, messages: list[Message], **kwargs) -> Message:
        messages = self._prepare_message_history(messages)
        headers = self._prepare_headers()
        payload = self._prepare_payload(messages, False)

        response = requests.post(self._endpoint, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        print(f"{BOT_PREFIX}{answer}")
        return Message(Role.AI, answer)

    async def stream_completion(self, messages: list[Message], **kwargs) -> Message:
        messages = self._prepare_message_history(messages)
        headers = self._prepare_headers()
        payload = self._prepare_payload(messages, True)

        async with aiohttp.ClientSession() as session:
            async with session.post(self._endpoint, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise Exception(f"OpenAI API error {resp.status}: {error_text}")
                answer = await self._process_stream_response(resp)

        return Message(role=Role.AI, content=answer)

    def _prepare_payload(self, messages, stream):
        return {
            "model": self._model_name,
            "messages": messages,
            "stream": stream,
            "max_tokens": MAX_TOKENS,
        }

    def _prepare_headers(self):
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def _process_stream_response(self, resp):
        print(BOT_PREFIX, end="")
        answer = ""
        async for line in resp.content:
            if not line:
                continue

            decoded_line = line.decode("utf-8").strip()

            if not decoded_line.startswith("data:"):
                continue

            if decoded_line == "data: [DONE]":
                print()
                break

            try:
                data = json.loads(decoded_line[len("data: "):])
                content = data["choices"][0]["delta"].get("content", "")
                if content:
                    print(content, end="")
                    answer += content
            except Exception:
                continue
        return answer
