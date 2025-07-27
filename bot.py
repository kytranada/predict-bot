import discord
from discord.ext import commands
import os
import aiohttp
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timezone

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_ENDPOINT = os.getenv("GROK_API_ENDPOINT")
SYSTEM_PROMPT_PATH = os.getenv("SYSTEM_PROMPT_PATH", "system_prompt.txt")

# --- Bot Setup ---

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

bot = commands.Bot(command_prefix="/", intents=intents)

conversation_history = {}
HISTORY_DEPTH = 10 # Max number of messages to keep per user

# --- Helper Functions ---

def load_system_prompt():
    """Loads the system prompt from the specified file."""
    try:
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: System prompt file not found at '{SYSTEM_PROMPT_PATH}'.")
        return "You are a helpful assistant." # Fallback prompt

def split_into_chunks(text, limit=1990):
    """
    Splits text into chunks of a specified limit, trying to split on
    newlines or spaces to avoid breaking words or sentences.
    """
    if len(text) <= limit:
        return [text]

    chunks = []
    while len(text) > 0:
        if len(text) <= limit:
            chunks.append(text)
            break
        
        # Find the best position to split
        # Prefer splitting at the last newline
        split_pos = text.rfind('\n', 0, limit)
        
        # If no newline found, try splitting at the last space
        if split_pos == -1:
            split_pos = text.rfind(' ', 0, limit)
            
        # If no space or newline is found, do a hard split
        if split_pos == -1:
            split_pos = limit
            
        chunks.append(text[:split_pos])
        # Move to the next part of the text, stripping leading whitespace
        text = text[split_pos:].lstrip()
        
    return chunks

def extract_predictions(full_text: str) -> str:
    """
    Extracts the 'Predictions' section from the AI's full response.
    If the section is not found, it returns the full text as a fallback.
    """
    try:
        prediction_marker = "Predictions"
        marker_index = full_text.find(prediction_marker)
        
        if marker_index != -1:
            return full_text[marker_index:]
        else:
            return full_text
    except Exception:
        return full_text
    
async def call_grok_api(user_id, user_message):
    """Calls the Grok AI API with the user's message and conversation history."""
    system_prompt = load_system_prompt()
    
    # Get or create the user's history
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    user_history = conversation_history[user_id]

    # Payload for the API
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
        "max_tokens": 3000 
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(GROK_API_ENDPOINT, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data['choices'][0]['message']['content']
                    
                    user_history.append({"role": "user", "content": user_message})
                    user_history.append({"role": "assistant", "content": ai_response})
                    
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

@bot.tree.command(name="predict", description="Get insight from the AI.")
async def predict(interaction: discord.Interaction):
    """
    Slash command to trigger the predictive insight.
    It uses a hard-coded prompt to initiate the conversation.
    """
    await interaction.response.defer() 
    
    user_id = interaction.user.id
    
    today_date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    initial_prompt = f"Web Bot: Analyze recent events for today, {today_date_str}. Initiate your scan and provide your predictive insights."
    
    full_response_text = await call_grok_api(user_id, initial_prompt)
    response_text = extract_predictions(full_response_text)
    
    if len(response_text) > 2000:
        chunks = split_into_chunks(response_text)
        await interaction.followup.send(chunks[0])
        for chunk in chunks[1:]:
            await interaction.followup.send(chunk)
    else:
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
            
            async with message.channel.typing():
                response_text = await call_grok_api(user_id, user_message)
                
                if len(response_text) > 2000:
                    chunks = split_into_chunks(response_text)
                    await message.reply(chunks[0])
                    for chunk in chunks[1:]:
                        await message.channel.send(chunk)
                else:
                    await message.reply(response_text)

    # This line is needed for future reply message-based commands.
    # await bot.process_commands(message)

# --- Main Execution ---

if __name__ == "__main__":
    if not all([DISCORD_TOKEN, GROK_API_KEY, GROK_API_ENDPOINT]):
        print("Error: Missing one or more required environment variables.")
        print("Please check your .env file.")
    else:
        bot.run(DISCORD_TOKEN)
