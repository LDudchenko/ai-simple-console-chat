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
        payload = self._prepare_payload(messages, False)

        response = requests.post(self._endpoint, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        answer = data["content"][0]["text"]
        print(f"{BOT_PREFIX}{answer}")
        return Message(Role.AI, answer)


    async def stream_completion(self, messages: list[Message], **kwargs) -> Message:
        headers = self._prepare_headers()
        payload = self._prepare_payload(messages, True)

        async with aiohttp.ClientSession() as session:
            async with session.post(self._endpoint, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise Exception(f"Anthropic API error {resp.status}: {error_text}")
                answer = await self._process_stream_response(resp)

        return Message(role=Role.AI, content=answer)

    def _prepare_payload(self, messages, stream):
        formatted_messages = [message.to_dict() for message in messages]
        return {
            "model": self._model_name,
            "messages": formatted_messages,
            "max_tokens": MAX_TOKENS,
            "system": DEFAULT_SYSTEM_PROMPT,
            "stream": stream
        }

    def _prepare_headers(self):
        return {
            "X-Api-Key": self._api_key,
            "Content-Type": "application/json",
            "Anthropic-Version": "2023-06-01"
        }


    async def _process_stream_response(self, resp):
        print(BOT_PREFIX, end="")
        answer = ""
        async for line in resp.content:
            line = line.decode().strip()
            if not line:
                continue

            if line.startswith("event:"):
                event_type = line[len("event:"):].strip()
                continue

            if line.startswith("data:"):
                data_json = line[len("data:"):].strip()
                data = json.loads(data_json)

                if event_type == "content_block_delta":
                    delta = data.get("delta", {})
                    if delta.get("type") == "text_delta":
                        content = delta.get("text", "")
                        print(content, end="")
                        answer += content
                elif event_type == "message_delta":
                    if data.get("delta", {}).get("stop_reason") == "end_turn":
                        print()

        return answer