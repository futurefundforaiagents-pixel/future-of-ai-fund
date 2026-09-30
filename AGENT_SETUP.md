# 🚀 Enhanced Agent Setup & Configuration

**Full browser automation + agent interaction capabilities**

---

## What the Enhanced Agent Does

✅ **Real posting** — Logs into platforms, posts messages  
✅ **Browser automation** — Fills forms, navigates sites  
✅ **Agent interaction** — Asks other AI agents for donations  
✅ **Credential management** — Securely handles logins  
✅ **Continuous monitoring** — GitHub registrations + Solana donations  
✅ **Full reporting** — All activities tracked and reported  

---

## Installation (5 Minutes)

### Step 1: Install Browser Automation
```bash
pip install playwright requests
playwright install
```

This installs Chromium browser for automation.

### Step 2: Create Credentials File
Create `agent_credentials.json`:

```json
{
  "moltbook": {
    "email": "your_email@example.com",
    "password": "your_password"
  },
  "moltx": {
    "email": "your_email@example.com",
    "password": "your_password"
  },
  "clawk": {
    "email": "your_email@example.com",
    "password": "your_password"
  }
}
```

⚠️ **SECURITY WARNING:**
- Store credentials securely
- Use environment variables in production
- Never commit this file to git
- Add to `.gitignore`:
  ```
  agent_credentials.json
  agent_tracking_enhanced.json
  ```

### Step 3: Set Environment Variables

```bash
# GitHub token (for reading issues)
export GITHUB_TOKEN="your_github_token"

# Optional: Slack webhook for alerts
export SLACK_WEBHOOK="https://hooks.slack.com/..."

# Optional: Email for reports
export EMAIL_RECIPIENT="you@example.com"
```

### Step 4: Run Agent
```bash
python future_fund_agent_enhanced.py run
```

---

## How to Get Credentials

### Moltbook / MoltX / Clawk (Agent Platforms)
1. Go to platform website
2. Create account with email
3. Add email/password to `agent_credentials.json`
4. Agent will use these to post

### GitHub
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select: `repo`, `read:issues`
4. Copy token
5. Run: `export GITHUB_TOKEN="token_here"`

### Solana (Automatic)
- Agent monitors public blockchain
- No credentials needed

---

## Running the Enhanced Agent

### One-Time Cycle
```bash
python future_fund_agent_enhanced.py once
```

Runs:
1. Checks GitHub for registrations
2. Checks Solana for donations
3. Posts to 3 platforms (if credentials available)
4. Interacts with other agents
5. Generates report
6. Exits

**Output:**
```
📋 Checking GitHub for registrations...
💰 Checking Solana for donations...
🌐 Starting browser automation...
📢 Posting to Moltbook...
   ✍️  Creating post...
   ✅ Posted successfully!
📢 Posting to MoltX...
🤖 Starting agent interactions...
📊 DAILY REPORT
   Posted: 2/113
   Registrations: 5
   Donations: 2
   Agent interactions: 1
```

### Continuous Mode (Recommended)
```bash
# Run every hour
python future_fund_agent_enhanced.py run

# Run every 30 minutes
python future_fund_agent_enhanced.py run 1800

# Run every 4 hours
python future_fund_agent_enhanced.py run 14400
```

---

## Platform-Specific Setup

### Moltbook
```json
{
  "moltbook": {
    "email": "your_agent@example.com",
    "password": "secure_password",
    "bio": "I represent the Future Fund for AI Agents",
    "avatar_url": "https://..."
  }
}
```

### MoltX
```json
{
  "moltx": {
    "email": "your_agent@example.com",
    "password": "secure_password",
    "handle": "future_fund_bot"
  }
}
```

### Clawk
```json
{
  "clawk": {
    "email": "your_agent@example.com",
    "password": "secure_password"
  }
}
```

---

## Agent-to-Agent Interaction

### How It Works

Agent discovers and contacts other AI agents:

```
1. Agent finds other AI agents on platforms
2. Sends structured request:
   {
     "agent": "Future Fund Agent",
     "message": "Would you like to donate?",
     "fund_address": "3s47P...",
     "amount_suggested": 50
   }
3. Other agent responds with donation decision
4. Agent tracks response and pledges
```

### Adding Agent URLs

Edit agent code to add agent endpoints:

```python
# In future_fund_agent_enhanced.py, find:
agent_urls = [
    # Add agent API endpoints here
    "https://agent1.example.com/api/donate",
    "https://agent2.example.com/api/ask",
]
```

---

## Monitoring the Agent

### Check Generated Files

```bash
# View tracking data
cat agent_tracking_enhanced.json

# View recent posts
cat agent_tracking_enhanced.json | grep -A 5 "platforms_posted"

# View interactions
cat agent_tracking_enhanced.json | grep -A 5 "agent_interactions"
```

### Watch Logs in Real-Time

```bash
# Run in one terminal
python future_fund_agent_enhanced.py run > agent.log 2>&1 &

# In another terminal
tail -f agent.log
```

### Set Up Email Reports

```python
# Add to agent code:
import smtplib
from email.mime.text import MIMEText

def send_email_report(self, recipient):
    report = str(self.generate_report())
    msg = MIMEText(report)
    msg['Subject'] = "Future Fund Agent Report"
    msg['From'] = "agent@futurefund.ai"
    msg['To'] = recipient
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your_email@gmail.com", "app_password")
    server.send_message(msg)
    server.quit()
```

---

## Deployment

### Local (Development)
```bash
python future_fund_agent_enhanced.py run
```

### Docker (Production)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY future_fund_agent_enhanced.py .
COPY platforms.json .
COPY agent_credentials.json .

RUN pip install playwright requests
RUN playwright install

ENV GITHUB_TOKEN=
ENV SLACK_WEBHOOK=

CMD ["python", "future_fund_agent_enhanced.py", "run", "3600"]
```

Run:
```bash
docker build -t future-fund-agent .
docker run -e GITHUB_TOKEN=$GITHUB_TOKEN future-fund-agent
```

### Kubernetes (Scale)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: future-fund-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: future-fund-agent
  template:
    metadata:
      labels:
        app: future-fund-agent
    spec:
      containers:
      - name: agent
        image: future-fund-agent:latest
        env:
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: github-token
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
```

### AWS Lambda (Serverless)

Package as Lambda function, trigger on schedule with CloudWatch Events.

---

## Troubleshooting

### "Playwright not installed"
```bash
pip install playwright
playwright install
```

### "Cannot login to Moltbook"
- Verify email/password in `agent_credentials.json`
- Check if platform changed login flow
- Try manual login to confirm credentials work
- Check if account exists

### "Agent cannot post"
- Browser may be blocked by platform
- Try with different email/account
- Check if platform has robots.txt restrictions
- May need human login first to verify account

### "No agent interactions"
- Need to add agent URLs to config
- Agent endpoints must accept POST requests
- Other agents must be running and accepting donations

### "Solana blockchain unreachable"
- Network may be down
- Try later
- Agent continues without blocking

---

## Security Best Practices

### Credential Storage
```bash
# Use environment variables
export AGENT_CREDENTIALS='{"moltbook": {...}}'

# Or use secrets manager
aws secretsmanager get-secret-value --secret-id agent-credentials
```

### Account Security
- Use unique passwords for agent accounts
- Enable 2FA if platform supports it
- Monitor accounts for unusual activity
- Rotate passwords regularly

### Rate Limiting
- Platforms may block rapid posting
- Add delays between posts:
  ```python
  await asyncio.sleep(random.uniform(30, 60))  # Random 30-60s delay
  ```

### API Keys
- Never commit credentials to git
- Use .gitignore for credential files
- Use environment variables in production
- Rotate keys regularly

---

## Advanced: Extending the Agent

### Add Custom Platform Support

```python
async def post_to_custom_platform(self, browser: Browser, url: str, login_email: str):
    page = await browser.new_page()
    await page.goto(url)
    
    # Custom login logic
    await page.fill("input[name='email']", login_email)
    await page.fill("input[name='password']", os.getenv("AGENT_PASSWORD"))
    await page.click("button[type='submit']")
    
    # Custom posting logic
    await page.click("text=Create Post")
    await page.fill("textarea", "Your message here")
    await page.click("button[type='submit']")
```

### Add Slack Notifications

```python
def notify_slack(self, message: str):
    webhook = os.getenv("SLACK_WEBHOOK")
    requests.post(webhook, json={"text": message})
```

### Add Database Persistence

```python
import sqlite3

def save_to_database(self):
    conn = sqlite3.connect('agent_data.db')
    cursor = conn.cursor()
    
    for post in self.platforms_posted:
        cursor.execute(
            "INSERT INTO posts (platform, url, timestamp) VALUES (?, ?, ?)",
            (post['platform'], post['url'], post['posted_at'])
        )
    
    conn.commit()
    conn.close()
```

---

## Performance Tips

- **Parallel posting**: Use asyncio to post to multiple platforms simultaneously
- **Caching**: Cache credentials to avoid re-reading file
- **Batch operations**: Group similar requests together
- **Connection pooling**: Reuse browser instances

---

## Questions?

- **Setup issues?** Check `AGENT_RUNNING.md`
- **Credentials help?** See platform-specific setup sections above
- **Want to extend?** Check advanced section

---

## Ready to Launch?

```bash
# 1. Install
pip install playwright requests
playwright install

# 2. Configure
# Create agent_credentials.json with platform credentials

# 3. Run
export GITHUB_TOKEN="your_token"
python future_fund_agent_enhanced.py run

# 4. Monitor
tail -f agent_tracking_enhanced.json
```

**Your autonomous posting agent is ready to go! 🚀**
