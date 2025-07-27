# Discord Grok AI Bot (Python)

This project implements a simple Discord bot in Python that uses a hardcoded Grok AI prompt to generate insights and supports threaded follow-up Q&A per user. The bot listens for messages starting with `/predict` and maintains conversation context for each user.

## Features
- `/predict <your question>`: Runs the hardcoded Grok prompt combined with your question
- Context maintained per user session for follow-up questions
- Async usage with `discord.py`

---

## Project Structure
```
discord_predict_bot/
├── bot.py          # Main bot implementation
├── requirements.txt
└── .env.example    # Example environment variables
```

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/discord_predict_bot.git
   cd discord_predict_bot
   ```

2. **Create & activate a Python virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\\Scripts\\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your Discord bot token and Grok API key
   ```dotenv
   DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
   GROK_API_KEY=YOUR_GROK_API_KEY
   GROK_API_ENDPOINT=https://api.grok.ai/v1/chat/completions
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

---

## Usage
- In any channel where the bot has access, type:
  ```
  /predict Summarize the latest market trends in AI.
  ```
- The bot will reply with insights based on the hardcoded Grok prompt and your query.
- For follow-up Q&A, simply send another message starting with `/predict` and your follow-up; the bot will maintain context.
