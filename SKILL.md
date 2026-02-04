---
name: executive-news-digest
description: Daily morning briefing with Economics, World News, Business, and AI Technology headlines plus executive commentary from Ray Dalio, Elon Musk, and Warren Buffett perspectives. Delivered via email in English and Chinese at 7 AM EST daily.
---

# 📰 Executive News Digest

> **Your daily morning briefing with world-class perspectives**

Delivers a comprehensive news digest every morning at 7:00 AM EST with:
- 📊 **5 Economics headlines**
- 🌍 **5 World News headlines**
- 💼 **5 Business headlines**
- 🤖 **5 AI Technology headlines**

Plus commentary from three executive perspectives:
- **Ray Dalio** - Macroeconomic & systemic analysis
- **Elon Musk** - Innovation & disruption focus
- **Warren Buffett** - Value investing & long-term thinking

**Output:** Bilingual (English → Simplified Chinese)  
**Delivery:** Email to johnyin@aisemble.ca  
**Schedule:** Daily at 7:00 AM EST

---

## 🎯 How It Works

### Daily Workflow

```
7:00 AM EST Daily:
1. Fetch news from multiple sources
   ├─ Economics (5 headlines)
   ├─ World News (5 headlines)
   ├─ Business (5 headlines)
   └─ AI Technology (5 headlines)
   
2. Generate executive commentary
   ├─ Ray Dalio perspective (overall themes)
   ├─ Elon Musk perspective (overall themes)
   └─ Warren Buffett perspective (overall themes)
   
3. Format digest
   ├─ English version
   └─ Chinese (Simplified) version
   
4. Send via email
   └─ To: johnyin@aisemble.ca
```

---

## 📋 News Categories

### 1. Economics (5 headlines)
- Macroeconomic indicators
- Central bank decisions
- Inflation & monetary policy
- Trade & tariffs
- Economic forecasts

### 2. World News (5 headlines)
- Geopolitical developments
- International relations
- Global conflicts
- Major policy changes
- Significant world events

### 3. Business (5 headlines)
- Corporate earnings
- M&A activity
- Market movements
- Industry trends
- Business leadership changes

### 4. AI Technology (5 headlines)
- AI breakthroughs
- Tech company developments
- Regulatory changes
- AI applications
- Industry trends

---

## 🎭 Executive Commentary

Each morning, the digest includes perspectives from three legendary executives analyzing the overall themes:

### Ray Dalio
**Focus:** Macroeconomic patterns, systemic risks, historical parallels
**Tone:** Analytical, principles-based, long-term cycles
**Expertise:** Debt cycles, geopolitical economics, systemic thinking

### Elon Musk
**Focus:** Innovation implications, disruption potential, technological acceleration
**Tone:** Bold, future-oriented, first-principles thinking
**Expertise:** Technology trends, exponential growth, market disruption

### Warren Buffett
**Focus:** Business fundamentals, value creation, long-term investment implications
**Tone:** Wisdom-based, conservative, value-oriented
**Expertise:** Capital allocation, business moats, management quality

---

## 🌐 Language Format

### English Section
```
📰 EXECUTIVE NEWS DIGEST
Date: [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ECONOMICS (5 Headlines)
• Headline 1
• Headline 2
...

🌍 WORLD NEWS (5 Headlines)
• Headline 1
• Headline 2
...

💼 BUSINESS (5 Headlines)
• Headline 1
• Headline 2
...

🤖 AI TECHNOLOGY (5 Headlines)
• Headline 1
• Headline 2
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎭 EXECUTIVE PERSPECTIVES

📈 RAY DALIO'S ANALYSIS
[Overall themes commentary]

🚀 ELON MUSK'S TAKE
[Overall themes commentary]

💰 WARREN BUFFETT'S VIEW
[Overall themes commentary]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Chinese (Simplified) Section
Same format, fully translated to Simplified Chinese

---

## 🛠️ Technical Setup

### Prerequisites
1. **News API Access**
   - Web search capability (Brave API or similar)
   - News aggregation sources
   - RSS feed access

2. **Email Configuration**
   - Gmail account setup (via GOG skill)
   - OAuth credentials
   - SMTP access

3. **AI Model Access**
   - LLM for commentary generation (Claude Sonnet/Opus recommended)
   - Translation capability

### Installation

```bash
# 1. Install dependencies
pip install requests beautifulsoup4 feedparser

# 2. Set up email credentials (GOG)
gog auth credentials /path/to/client_secret.json
gog auth add your@gmail.com --services gmail

# 3. Configure environment
export GOG_ACCOUNT=your@gmail.com
export RECIPIENT_EMAIL=johnyin@aisemble.ca
```

### Cron Job Setup

```bash
# Run daily at 7:00 AM EST
0 7 * * * cd /Users/Phoestia/clawd/skills/executive-news-digest && python3 scripts/run_digest.py
```

Or use OpenClaw cron:
```bash
# Create cron job via OpenClaw
openclaw cron add \
  --name "Executive News Digest" \
  --schedule "0 7 * * *" \
  --timezone "America/Toronto" \
  --command "cd /Users/Phoestia/clawd/skills/executive-news-digest && python3 scripts/run_digest.py"
```

---

## 📁 File Structure

```
executive-news-digest/
├── SKILL.md                          # This file
├── README.md                         # GitHub README
├── scripts/
│   ├── run_digest.py                 # Main orchestrator
│   ├── news_fetcher.py               # Fetch news from sources
│   ├── commentary_generator.py       # Generate executive commentary
│   ├── translator.py                 # Translate to Chinese
│   └── email_sender.py               # Send via email
├── references/
│   ├── news_sources.md               # News source documentation
│   ├── commentary_prompts.md         # Executive commentary prompts
│   └── email_template.html           # HTML email template
└── examples/
    └── sample_output.md              # Example digest output
```

---

## 🚀 Usage

### Manual Trigger
```bash
cd /Users/Phoestia/clawd/skills/executive-news-digest
python3 scripts/run_digest.py
```

### Via OpenClaw
```
"Generate today's executive news digest"
"Send morning briefing"
"Run news digest"
```

### Check Status
```bash
# View cron job status
openclaw cron list

# View recent runs
openclaw cron runs <job-id>
```

---

## 🎨 Customization

### Change Schedule
Edit the cron schedule:
- 7:00 AM EST: `0 7 * * *`
- 6:00 AM EST: `0 6 * * *`
- Weekdays only: `0 7 * * 1-5`

### Adjust News Volume
Edit `scripts/news_fetcher.py`:
```python
NEWS_CONFIG = {
    "economics": 5,     # Change count here
    "world_news": 5,
    "business": 5,
    "ai_technology": 5
}
```

### Add News Sources
Edit `references/news_sources.md` and update `scripts/news_fetcher.py`

### Modify Commentary Style
Edit prompts in `references/commentary_prompts.md`

---

## 📊 Example Output

See `examples/sample_output.md` for a complete example of the daily digest format.

---

## 🔧 Troubleshooting

### Email Not Sending
```bash
# Check GOG auth
gog auth list

# Test email manually
gog gmail send --to johnyin@aisemble.ca --subject "Test" --body "Test"
```

### News Fetching Issues
```bash
# Check Brave API key
echo $BRAVE_API_KEY

# Test news fetcher
python3 scripts/news_fetcher.py --test
```

### Cron Job Not Running
```bash
# Check cron status
openclaw cron status

# View logs
openclaw cron runs <job-id> --logs
```

---

## 📝 Notes

- **News Quality:** Uses multiple sources to ensure comprehensive coverage
- **Commentary Authenticity:** AI-generated based on public knowledge of each executive's thinking patterns
- **Delivery Reliability:** Email delivery tracked and logged
- **Translation Quality:** Simplified Chinese translation optimized for business terminology
- **Privacy:** All processing happens locally, no data sharing with third parties

---

## 🤝 Credits

**Created for:** John Yin (johnyin@aisemble.ca)  
**Schedule:** Daily 7:00 AM EST  
**Part of:** OpenClaw Skills Ecosystem

---

*Get world-class insights delivered to your inbox every morning.* 📬
