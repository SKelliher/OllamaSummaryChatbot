import llamabot
from llamabot import SimpleBot

systemPrompt = 'Hello'

bot = SimpleBot(systemPrompt, temperature=0.5, json_mode=False, model_name='ollama/sapphire')

print(bot('What is your name'))