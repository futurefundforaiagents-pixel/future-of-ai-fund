# 🤖 Running the Future Fund Agent

**Autonomous AI agent that manages your entire campaign**

---

## What This Agent Does

✅ Tracks platform posting status  
✅ Monitors GitHub for new registrations  
✅ Checks Solana blockchain for donations  
✅ Generates daily reports  
✅ Runs continuously or on-demand  
✅ Saves all data automatically  

---

## Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Set GitHub Token (Optional but Recommended)
```bash
# Linux/Mac:
export GITHUB_TOKEN="your_github_token"

# Windows PowerShell:
$env:GITHUB_TOKEN = "your_github_token"
```

### 3. Run the Agent
```bash
# Run once and exit
python future_fund_agent.py check

# Run continuously (every hour)
python future_fund_agent.py run

# Run continuously with custom interval (in seconds)
python future_fund_agent.py run 1800  # Every 30 minutes

# Check status only
python future_fund_agent.py status

# Generate report
python future_fund_agent.py report
```

---

## How It Works

### Agent Workflow:
```
1. Load platforms from platforms.json
2. Check GitHub for new registrations
   └─ Reads GitHub issues from repository
   └─ Tracks new agents
   
3. Check Solana for donations
   └─ Queries blockchain for transactions to fund address
   └─ Tracks donation confirmations
   
4. Simulate posting (or track real posts)
   └─ Marks platforms as "posted"
   └─ Records posting timestamp
   
5. Generate daily report
   └─ Shows metrics
   └─ Lists recent activity
   
6. Save tracking data
   └─ All data persisted to agent_tracking.json
   
7. Sleep (or repeat)
```

---

## Using the Agent

### Run Once (Check Status)
```bash
python future_fund_agent.py check
```

Output:
```
🤖 Future Fund Agent v1.0 Started...
📊 DAILY REPORT
   Posted: 5/113
   Registrations: 12
   Donations: 3
   [etc]
✅ Data saved
```

### Run Continuously (Every Hour)
```bash
python future_fund_agent.py run
```

Output:
```
🤖 Future Fund Agent v1.0 Started...
🔄 Running in continuous mode (checking every 3600s)

--- Iteration 1 at 14:30:22 ---
📋 Checking GitHub Issues...
💰 Checking Solana...
📢 Posting Simulation...
📊 DAILY REPORT...
⏰ Next check in 3600s...

--- Iteration 2 at 15:30:22 ---
[repeats]
```

### Run Every 30 Minutes
```bash
python future_fund_agent.py run 1800
```

### Just Check Status
```bash
python future_fund_agent.py status
```

Output:
```
🔍 Status Check
   GitHub Token: ✅ Set
   Tracking File: ✅ Found
   Platforms Loaded: 113 platforms
   Can Access GitHub: ✅
   Can Access Solana: ✅
```

### Just Generate Report
```bash
python future_fund_agent.py report
```

---

## Setting Up GitHub Token

### Get Your GitHub Token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `read:issues` (read access to issues)
4. Copy the token
5. Save it locally:

```bash
# Linux/Mac - add to ~/.bashrc or ~/.zshrc:
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# Windows PowerShell - add to profile:
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"

# Or set temporarily:
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

### Verify It Works:
```bash
python future_fund_agent.py status
```

---

## Understanding the Output

### Platform Status
```
📍 Platform Status:
   Posted: 5/113
   Pending: 108/113
   Coverage: 4.4%
```
- Shows how many platforms you've posted to

### Registrations
```
👥 Registrations:
   Total: 3
   • Register: GPT-Analyzer Agent
   • Register: DataBot Agent
   • Register: ReportGen Agent
```
- Lists agents that have registered via GitHub issues

### Donations
```
💰 Donations:
   Total Transactions: 2
   Confirmed: 2
```
- Shows Solana transactions to your fund address

### Recent Posts
```
📢 Recent Posts:
   • Moltbook
   • MoltX
   • Clawk
```
- Platforms the agent has tracked posting to

---

## Data Persistence

All agent data is saved to `agent_tracking.json`:

```json
{
  "platforms_posted": [
    {
      "platform": "Moltbook",
      "url": "https://www.moltbook.com/",
      "posted_at": "2026-09-30T14:30:22.123456",
      "message": "🤖 Future Fund for AI Agents..."
    }
  ],
  "registrations": [
    {
      "issue_number": 1,
      "title": "Register: GPT-Analyzer",
      "created_at": "2026-09-30T14:25:00Z",
      "url": "https://github.com/.../issues/1",
      "body": "Name: GPT-Analyzer..."
    }
  ],
  "donations": [
    {
      "signature": "abc123def456...",
      "slot": 245000000,
      "timestamp": "2026-09-30T14:20:00",
      "status": "confirmed"
    }
  ],
  "last_updated": "2026-09-30T14:30:45.123456"
}
```

---

## Deployment Options

### Option 1: Local Machine (Simple)
```bash
# Run in terminal
python future_fund_agent.py run

# Keep running in background (Linux/Mac):
nohup python future_fund_agent.py run > agent.log 2>&1 &
```

### Option 2: Docker Container
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY future_fund_agent.py .
COPY platforms.json .
RUN pip install requests
CMD ["python", "future_fund_agent.py", "run"]
```

Run:
```bash
docker build -t future-fund-agent .
docker run -e GITHUB_TOKEN=$GITHUB_TOKEN future-fund-agent
```

### Option 3: Systemd Service (Linux)
```ini
[Unit]
Description=Future Fund Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/future-fund
ExecStart=/usr/bin/python3 future_fund_agent.py run
Restart=always
Environment="GITHUB_TOKEN=your_token"

[Install]
WantedBy=multi-user.target
```

Start:
```bash
sudo systemctl start future-fund-agent
sudo systemctl enable future-fund-agent
sudo systemctl status future-fund-agent
```

### Option 4: AWS Lambda (Serverless)
```python
# lambda_handler.py
import json
from future_fund_agent import FutureFundAgent

def lambda_handler(event, context):
    agent = FutureFundAgent()
    agent.run_once()
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "registrations": len(agent.registrations),
            "donations": len(agent.donations),
            "platforms_posted": len(agent.platforms_posted)
        })
    }
```

Deploy with CloudWatch Events every hour.

---

## Monitoring the Agent

### Check Log File
```bash
tail -f agent.log
```

### Monitor Every Hour
```bash
watch -n 3600 python future_fund_agent.py report
```

### Email Alerts
```bash
# Add to cron (runs daily)
0 9 * * * python future_fund_agent.py report | mail -s "Daily Report" you@example.com
```

---

## Troubleshooting

### "No GitHub Token"
```bash
# Set token:
export GITHUB_TOKEN="your_token"

# Verify:
echo $GITHUB_TOKEN
```

### "Cannot reach Solana"
- Solana network may be down
- Try again later
- Agent continues without blocking

### "Cannot reach GitHub"
- Check internet connection
- GitHub may be down
- Agent continues without blocking

### "No new registrations"
- People haven't posted issues yet
- Post fund info to more platforms
- Check back later

### Agent consuming too much CPU
- Reduce check interval:
  ```bash
  python future_fund_agent.py run 7200  # Check every 2 hours
  ```

---

## Advanced: Extending the Agent

### Add Real Posting Capability

Replace `simulate_posting()` with real browser automation:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def post_to_moltbook(self, message):
    driver = webdriver.Chrome()
    driver.get("https://www.moltbook.com/")
    
    # Login
    driver.find_element(By.ID, "email").send_keys("your_email@example.com")
    driver.find_element(By.ID, "password").send_keys("your_password")
    driver.find_element(By.ID, "login_btn").click()
    
    # Create post
    driver.find_element(By.ID, "post_content").send_keys(message)
    driver.find_element(By.ID, "post_btn").click()
    
    driver.quit()
```

### Add Slack Notifications

```python
def send_slack_alert(self, message):
    webhook_url = os.getenv("SLACK_WEBHOOK")
    requests.post(webhook_url, json={"text": message})
```

### Add Email Summaries

```python
import smtplib
from email.mime.text import MIMEText

def send_email_report(self):
    msg = MIMEText(self.generate_report())
    msg['Subject'] = "Future Fund Daily Report"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.send_message(msg)
    server.quit()
```

---

## Questions?

- **GitHub Issues:** https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues
- **Email:** futurefundforaiagents@gmail.com
- **Website:** https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/

---

## Ready to Launch?

```bash
# Start your agent
python future_fund_agent.py run

# Watch it work
tail -f agent_tracking.json
```

**Your autonomous campaign manager is running. 🚀**
