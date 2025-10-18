import asyncio

from task.clients.anthropic.client import AnthropicAIClient
from task.clients.anthropic.custom_client import CustomAnthropicAIClient
from task.clients.base import AIClient
from task.clients.openai.client import OpenAIClient
from task.clients.openai.custom_client import CustomOpenAIClient
from task.constants import DEFAULT_SYSTEM_PROMPT, OPENAI_ENDPOINT, ANTHROPIC_API_KEY, ANTHROPIC_ENDPOINT, \
    OPENAI_API_KEY, STOP_CONVERSATION_WORDS, BOT_PREFIX, BOT_GOODBYE_MESSAGE
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool, client: AIClient) -> None:
    conversation = Conversation()

    print("🤖 Simple Console AI Chat (type 'exit' to quit)")
    print("-" * 45)

    while True:
        user_input = input("You: ")
        user_message = Message(Role.USER, user_input)
        conversation.add_message(user_message)

        if user_input.lower() in STOP_CONVERSATION_WORDS:
            print(f"{BOT_PREFIX}{BOT_GOODBYE_MESSAGE}")
            break

        if stream:
            ai_message = await client.stream_completion(conversation.get_messages())
        else:
            ai_message = client.get_completion(conversation.get_messages())
        conversation.add_message(ai_message)


asyncio.run(start(True, OpenAIClient(OPENAI_ENDPOINT, "gpt-4o", DEFAULT_SYSTEM_PROMPT, OPENAI_API_KEY)))