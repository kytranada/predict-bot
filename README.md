# Discord Grok AI Bot (Python)

This project implements a simple Discord bot in Python that uses a Grok AI prompt to generate insights and supports threaded follow-up Q&A per user. The bot listens for messages starting with `/predict` and maintains conversation context for each user.

## Features
- `/predict <your question>`: Runs the hardcoded Grok prompt combined with your question
- Context maintained per user session for follow-up questions
- Async usage with `discord.py`

---

## Use Case: Geo-Political/Financial Data Prediction

This bot is specifically designed to scrape information from X (formerly Twitter) to identify language patterns that may indicate future geo-political or financial events. The system uses predictive linguistics techniques to analyze real-time social media discussions for early signals of upcoming events.

### Data Sources
- Verified news accounts (NYTimes, BBC, CNN, Reuters, etc.)
- Real-time user comments and reactions to breaking news
- Recent posts (within last 24-72 hours) with high engagement

### Analysis Approach
- Detection of anomalies and emotional archetypes
- Identification of temporal markers implying futurity
- Aggregation of findings by time windows and thematic clusters
- Generation of predictions based on pattern recognition in language

### System Prompt
The bot uses a local system prompt (`system_prompt.txt`) 

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
