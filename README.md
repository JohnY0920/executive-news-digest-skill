# 📰 Executive News Digest

> **Your daily morning briefing with world-class perspectives**

An OpenClaw skill that delivers a comprehensive news digest every morning at 7:00 AM EST, featuring headlines across Economics, World News, Business, and AI Technology, plus executive commentary from Ray Dalio, Elon Musk, and Warren Buffett perspectives.

**Output:** Bilingual (English → Simplified Chinese)  
**Delivery:** Email via Gmail  
**Schedule:** Daily at 7:00 AM EST

---

## 🎯 Features

### News Coverage (20 headlines daily)
- **📊 Economics (5)** - Macro indicators, central bank decisions, trade policy
- **🌍 World News (5)** - Geopolitics, international relations, major events
- **💼 Business (5)** - Corporate earnings, M&A, market movements, industry trends
- **🤖 AI Technology (5)** - AI breakthroughs, regulations, applications, trends

### Executive Commentary
- **📈 Ray Dalio** - Macroeconomic patterns, systemic risks, historical cycles
- **🚀 Elon Musk** - Innovation implications, disruption potential, technological acceleration
- **💰 Warren Buffett** - Business fundamentals, value creation, long-term investing

### Bilingual Output
- **English** - Professional business terminology
- **简体中文** - Simplified Chinese translation

### Professional Delivery
- **HTML Email** - Beautiful, responsive design
- **Daily Schedule** - Automated cron job at 7:00 AM EST
- **Reliable** - Error handling and logging

---

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Install Python dependencies
pip install requests beautifulsoup4 feedparser

# 2. Set up Gmail via GOG CLI
brew install steipete/tap/gogcli
gog auth credentials /path/to/client_secret.json
gog auth add your@gmail.com --services gmail

# 3. Set environment variables
export GOG_ACCOUNT=your@gmail.com
export RECIPIENT_EMAIL=johnyin@aisemble.ca
export BRAVE_API_KEY=your_brave_api_key  # Optional, for live news
```

### Installation

```bash
# Clone the repo
cd /path/to/openclaw/skills/
git clone https://github.com/YourUsername/executive-news-digest-skill.git

# Test run
cd executive-news-digest-skill/scripts
python3 run_digest.py
```

### Set Up Daily Schedule

**Option A: OpenClaw Cron**
```bash
openclaw cron add \
  --name "Executive News Digest" \
  --schedule "0 7 * * *" \
  --timezone "America/Toronto" \
  --command "cd /path/to/skills/executive-news-digest && python3 scripts/run_digest.py"
```

**Option B: System Cron**
```bash
# Edit crontab
crontab -e

# Add this line (runs at 7:00 AM EST daily)
0 7 * * * cd /path/to/skills/executive-news-digest && python3 scripts/run_digest.py
```

---

## 📁 Project Structure

```
executive-news-digest/
├── README.md                      # This file
├── SKILL.md                       # OpenClaw skill documentation
├── requirements.txt               # Python dependencies
├── scripts/
│   ├── run_digest.py              # Main orchestrator
│   ├── news_fetcher.py            # Fetch news from sources
│   ├── commentary_generator.py    # Generate executive commentary
│   ├── translator.py              # Translate to Chinese
│   └── email_sender.py            # Send via email
├── references/
│   ├── news_sources.md            # News source documentation
│   └── commentary_prompts.md      # Executive commentary prompts
└── examples/
    └── sample_output.md           # Example digest output
```

---

## 🛠️ How It Works

### Daily Workflow

```
7:00 AM EST Daily:

1. Fetch News (news_fetcher.py)
   ├─ Query news sources for each category
   ├─ Extract 5 headlines per category
   └─ Save raw news data

2. Generate Commentary (commentary_generator.py)
   ├─ Analyze overall themes across all news
   ├─ Generate Ray Dalio perspective
   ├─ Generate Elon Musk perspective
   └─ Generate Warren Buffett perspective

3. Translate (translator.py)
   ├─ Translate all headlines to Simplified Chinese
   └─ Translate all commentary to Simplified Chinese

4. Format & Send (email_sender.py)
   ├─ Format as HTML email
   ├─ Include English version
   ├─ Include Chinese version
   └─ Send via Gmail (GOG CLI)
```

---

## 🎨 Customization

### Change Recipient
Edit `scripts/run_digest.py`:
```python
self.sender = EmailSender(recipient="your@email.com")
```

### Adjust News Volume
Edit `scripts/news_fetcher.py`:
```python
self.headlines_per_category = 5  # Change to desired number
```

### Modify Schedule
```bash
# 6:00 AM instead of 7:00 AM
0 6 * * * cd /path/to/skills/executive-news-digest && python3 scripts/run_digest.py

# Weekdays only (Mon-Fri)
0 7 * * 1-5 cd /path/to/skills/executive-news-digest && python3 scripts/run_digest.py
```

### Add News Sources
Edit `scripts/news_fetcher.py` and add your preferred news sources.

---

## 📊 Example Output

See `examples/sample_output.md` for a complete example of the daily digest.

**Sample Email Preview:**
- Clean, professional HTML design
- Organized by category with emoji icons
- Clickable headline links
- Executive commentary in styled boxes
- Fully bilingual (English → Chinese)

---

## 🔧 Troubleshooting

### Email Not Sending
```bash
# Check GOG authentication
gog auth list

# Test email manually
gog gmail send --to test@email.com --subject "Test" --body "Test message"
```

### No News Data
```bash
# Check Brave API key (if using live news)
echo $BRAVE_API_KEY

# Test news fetcher
cd scripts
python3 news_fetcher.py
```

### Cron Job Not Running
```bash
# Check OpenClaw cron status
openclaw cron list

# View recent runs
openclaw cron runs <job-id>

# Check system cron
crontab -l
```

### Check Logs
```bash
# View digest log
cat scripts/digest_log.txt

# View last 20 lines
tail -20 scripts/digest_log.txt
```

---

## 🚧 Development

### Testing Individual Components

```bash
cd scripts

# Test news fetcher
python3 news_fetcher.py

# Test commentary generator
python3 commentary_generator.py

# Test translator
python3 translator.py

# Test email sender (creates preview only)
python3 email_sender.py
```

### Adding LLM Integration

The skill currently uses mock data for commentary and translation. To integrate with a real LLM:

1. Add LLM API credentials to environment
2. Implement `call_llm_for_commentary()` in `run_digest.py`
3. Implement `call_llm_for_translation()` in `run_digest.py`

Example with Claude API:
```python
import anthropic

def call_llm_for_commentary(self, prompts):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    commentaries = {}
    for exec_key, prompt in prompts.items():
        response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        commentaries[exec_key] = response.content[0].text
    return commentaries
```

---

## 📝 Notes

- **Privacy:** All processing happens locally, no third-party data sharing
- **Reliability:** Includes error handling and fallback to mock data if APIs fail
- **Scalability:** Easy to add more news categories or executives
- **Extensibility:** Modular design allows easy integration with other skills

---

## 🤝 Credits

**Created for:** John Yin (johnyin@aisemble.ca)  
**Schedule:** Daily 7:00 AM EST  
**Part of:** OpenClaw Skills Ecosystem  

**Inspired by:**
- Ray Dalio's Principles
- Elon Musk's First-Principles Thinking
- Warren Buffett's Value Investing Philosophy

---

## 📄 License

MIT License - Feel free to use and modify as needed.

---

**Get world-class insights delivered to your inbox every morning.** 📬
