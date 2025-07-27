# Discord Grok AI Bot (Python)

This project implements a Discord bot in Python that uses the Grok AI API to generate geopolitical and economic insights. The bot supports slash commands for different types of analysis and maintains conversation history for follow-up questions.

## Features
- `/geopolitical`: Generates geopolitical analysis based on a specialized prompt.
- `/economic`: Generates economic analysis based on a specialized prompt.
- **Follow-up Questions**: Users can reply to the bot's messages to ask follow-up questions within the same context.
- **Modular Design**: The code is structured to be easily maintainable and extensible.

---

## Use Case: Geo-Political/Financial Data Analysis

This bot is specifically designed to scrape information from X (formerly Twitter) to identify language patterns that may indicate geo-political or financial events. The system uses predictive linguistics techniques to analyze real-time social media discussions for early signals of upcoming events.

### Data Sources
- Verified news accounts (NYTimes, BBC, CNN, Reuters, etc.)
- Real-time user comments and reactions to breaking news
- Recent posts (within last 24-72 hours) with high engagement

### Analysis Approach
- Detection of anomalies and emotional archetypes
- Identification of temporal markers implying futurity
- Aggregation of findings by time windows and thematic clusters
- Generation of analysis reports based on pattern recognition in language

### System Prompts
The bot uses local prompt files for different commands:
- `predict_prompt.txt`: Used for the `/predict` command to generate geopolitical analysis.
- `economic_prompt.txt`: Used for the `/economic` command to generate economic analysis.

---

## Project Structure
```
discord_predict_bot/
├── bot.py              # Main bot logic
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (ignored by git)
├── predict_prompt.txt  # Prompt for geopolitical analysis
└── economic_prompt.txt # Prompt for economic analysis
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
   GROK_API_ENDPOINT=https://api.groq.com/openai/v1/chat/completions
   SYSTEM_PROMPT_PATH=predict_prompt.txt
   ECONOMIC_PROMPT_PATH=economic_prompt.txt
   ```
   *Note: The `SYSTEM_PROMPT_PATH` and `ECONOMIC_PROMPT_PATH` variables are optional and will default to `predict_prompt.txt` and `economic_prompt.txt` respectively.*

5. **Run the bot**
   ```bash
   python bot.py
   ```

---

## Usage
- **Geopolitical Analysis**:
  ```
  /predict
  ```
- **Economic Analysis**:
  ```
  /economic
  ```
- **Follow-up Questions**:
  To ask a follow-up question, simply reply to one of the bot's messages with your query. The bot will use the conversation history to provide a contextual answer.
