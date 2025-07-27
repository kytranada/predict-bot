import discord
from discord.ext import commands
import os
import aiohttp
from dotenv import load_dotenv
import asyncio

# --- Configuration ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_ENDPOINT = os.getenv("GROK_API_ENDPOINT")
SYSTEM_PROMPT_PATH = os.getenv("SYSTEM_PROMPT_PATH", "system_prompt.txt")

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True 

# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix="/", intents=intents)

# --- In-memory Conversation History ---
# Store conversation history for each user.
# The key is the user's ID, and the value is a list of messages.
conversation_history = {}
HISTORY_DEPTH = 10 


def load_system_prompt():
    """Loads the system prompt from the specified file."""
    try:
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: System prompt file not found at '{SYSTEM_PROMPT_PATH}'.")
        return "You are a helpful assistant." 

async def call_grok_api(user_id, user_message):
    """Calls the Grok AI API with the user's message and conversation history."""
    system_prompt = load_system_prompt()
    
    # Get or create the user's history
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    user_history = conversation_history[user_id]

    # Construct the messages payload for the API
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(user_history)
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-3-mini", 
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(GROK_API_ENDPOINT, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data['choices'][0]['message']['content']
                    
                   
                    user_history.append({"role": "user", "content": user_message})
                    user_history.append({"role": "assistant", "content": ai_response})
                    
                    # Keep the conversation history within the defined depth
                    conversation_history[user_id] = user_history[-HISTORY_DEPTH*2:] # *2 for user/assistant pairs
                    
                    return ai_response
                else:
                    error_text = await response.text()
                    print(f"Error from Grok API: {response.status} - {error_text}")
                    return f"Sorry, I encountered an error with the AI service (HTTP {response.status})."
        except Exception as e:
            print(f"An exception occurred while calling Grok API: {e}")
            return "Sorry, I couldn't connect to the AI service."

# --- Bot Events ---

@bot.event
async def on_ready():
    """Event handler for when the bot has connected to Discord."""
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# --- Slash Commands ---

@bot.tree.command(name="predict", description="Get a predictive insight from the AI.")
async def predict(interaction: discord.Interaction):
    """
    Slash command to trigger the predictive insight.
    It uses a hard-coded prompt to initiate the conversation.
    """
    await interaction.response.defer() # Defer the response to show a loading state
    
    user_id = interaction.user.id
    # The hard-coded initial prompt for the /predict command
    initial_prompt = "Give me the latest predictive insight based on your instructions."
    
    # Call the Grok API
    response_text = await call_grok_api(user_id, initial_prompt)
    
    # Send the response
    await interaction.followup.send(response_text)

@bot.event
async def on_message(message):
    """
    Event handler for messages. Used for follow-up questions.
    """
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is a reply to the bot
    if message.reference and message.reference.resolved:
        replied_to_message = message.reference.resolved
        if replied_to_message.author == bot.user:
            user_id = message.author.id
            user_message = message.content
            
            # Show typing indicator
            async with message.channel.typing():
                response_text = await call_grok_api(user_id, user_message)
                await message.reply(response_text)

# --- Main Execution ---

if __name__ == "__main__":
    if not all([DISCORD_TOKEN, GROK_API_KEY, GROK_API_ENDPOINT]):
        print("Error: Missing one or more required environment variables.")
        print("Please check your .env file.")
    else:
        bot.run(DISCORD_TOKEN)
