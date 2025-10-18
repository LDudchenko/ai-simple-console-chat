import os

DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."

OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

ANTHROPIC_API_KEY=os.getenv('ANTHROPIC_API_KEY', '')
ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages"

BOT_PREFIX = "Bot: "
BOT_GOODBYE_MESSAGE = "Goodbye!"
STOP_CONVERSATION_WORDS = ["exit", "quit", "bye"]

MAX_TOKENS = 1024
GPT_4_MODEL="gpt-4o"
CLAUDE_MODEL="claude-sonnet-4-5-20250929"