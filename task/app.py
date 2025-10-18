import asyncio

from task.clients.anthropic.client import AnthropicAIClient
from task.clients.anthropic.custom_client import CustomAnthropicAIClient
from task.clients.openai.client import OpenAIClient
from task.clients.openai.custom_client import CustomOpenAIClient
from task.constants import (
    DEFAULT_SYSTEM_PROMPT, OPENAI_ENDPOINT, ANTHROPIC_ENDPOINT,
    OPENAI_API_KEY, ANTHROPIC_API_KEY,
    STOP_CONVERSATION_WORDS, BOT_PREFIX, BOT_GOODBYE_MESSAGE,
    GPT_4_MODEL, CLAUDE_MODEL
)
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


def choose_settings(openai_client, custom_openai_client,
                    anthropic_client, custom_anthropic_client,
                    current_client=None, current_stream=None):
    print("\nConfigure settings:")
    model_choice = input("Choose model [openai/anthropic/custom_openai/custom_anthropic]: ").strip().lower()

    if model_choice == "openai":
        client = openai_client
    elif model_choice == "anthropic":
        client = anthropic_client
    elif model_choice == "custom_openai":
        client = custom_openai_client
    elif model_choice == "custom_anthropic":
        client = custom_anthropic_client
    else:
        print("Invalid choice. Keeping current model.")
        client = current_client

    if current_stream is None:
        prompt = "Stream responses? [y/n]: "
    else:
        prompt = f"Stream responses? [y/n] (current: {'on' if current_stream else 'off'}): "

    stream = input(prompt).strip().lower() == "y"

    print(f"Settings: model={client.__class__.__name__}, stream={'on' if stream else 'off'}\n")
    return client, stream


async def start():
    openai_client = OpenAIClient(OPENAI_ENDPOINT, GPT_4_MODEL, DEFAULT_SYSTEM_PROMPT, OPENAI_API_KEY)
    custom_openai_client = CustomOpenAIClient(OPENAI_ENDPOINT, GPT_4_MODEL, DEFAULT_SYSTEM_PROMPT, OPENAI_API_KEY)
    anthropic_client = AnthropicAIClient(ANTHROPIC_ENDPOINT, CLAUDE_MODEL, DEFAULT_SYSTEM_PROMPT, ANTHROPIC_API_KEY)
    custom_anthropic_client = CustomAnthropicAIClient(ANTHROPIC_ENDPOINT, CLAUDE_MODEL, DEFAULT_SYSTEM_PROMPT, ANTHROPIC_API_KEY)

    current_client, stream = choose_settings(openai_client, custom_openai_client, anthropic_client, custom_anthropic_client)

    conversation = Conversation()
    print("\n🤖 Simple Console AI Chat (type 'exit' to quit, '/switch' to change settings)")
    print("-" * 45)

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in STOP_CONVERSATION_WORDS:
            print(f"{BOT_PREFIX}{BOT_GOODBYE_MESSAGE}")
            break

        if user_input.startswith("/switch"):
            current_client, stream = choose_settings(openai_client, custom_openai_client, anthropic_client,
                                                     custom_anthropic_client, current_client, stream)
            continue

        user_message = Message(Role.USER, user_input)
        conversation.add_message(user_message)

        if stream:
            ai_message = await current_client.stream_completion(conversation.get_messages())
        else:
            ai_message = current_client.get_completion(conversation.get_messages())

        conversation.add_message(ai_message)


asyncio.run(start())
