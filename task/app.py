import asyncio

from task.clients.anthropic.client import AnthropicAIClient
from task.clients.anthropic.custom_client import CustomAnthropicAIClient
from task.clients.base import AIClient
from task.clients.openai.client import OpenAIClient
from task.clients.openai.custom_client import CustomOpenAIClient
from task.constants import DEFAULT_SYSTEM_PROMPT, OPENAI_ENDPOINT, ANTHROPIC_API_KEY, ANTHROPIC_ENDPOINT, OPENAI_API_KEY
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role

BOT_PREFIX = "Bot: "
BOT_GOODBYE_MESSAGE = "Goodbye!"

STOP_CONVERSATION_WORDS = ["exit", "quit", "bye"]


async def start(stream: bool, client: AIClient) -> None:
    conversation = Conversation()

    print("🤖 Simple Console Chat (type 'exit' to quit)")
    print("-" * 40)

    while True:
        user_input = input("You: ")
        user_message = Message(Role.USER, user_input)
        conversation.add_message(user_message)

        if user_input.lower() in STOP_CONVERSATION_WORDS:
            print(f"{BOT_PREFIX}{BOT_GOODBYE_MESSAGE}")
            break

        if stream:
            ai_message = client.stream_completion(conversation.get_messages())
        else:
            ai_message = client.get_completion(conversation.get_messages())
        print(f"{BOT_PREFIX}{ai_message.content}")
    #TODO:
    # Main chat loop that handles user interaction with AI clients.
    # 1. Create a conversation object to maintain chat history
    # 2. Handle user input in a loop
    # 3. Add messages to conversation
    # 4. Call AI client methods (both streaming and non-streaming)
    # 5. Handle the conversation flow


#TODO:
# Create instances of AIClient:
#   - OpenAIClient
#   - CustomOpenAIClient
#   - AnthropicAIClient
#   - CustomAnthropicAIClient
# Run application:
#   Use asyncio.run() method to run the application (call `start` method in `run`)
# raise NotImplementedError
asyncio.run(start(False, OpenAIClient(OPENAI_ENDPOINT, "", DEFAULT_SYSTEM_PROMPT, OPENAI_API_KEY)))


#TODO:
# Test that your application works with different clients, additionally try to print in clients full request and
# response to to check the data that you send and get