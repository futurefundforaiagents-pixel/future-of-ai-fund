#!/usr/bin/env python3
"""
Future Fund for AI Agents — Enhanced Autonomous Agent
Full browser automation, real posting, and agent-to-agent interaction
"""

import json
import os
import asyncio
from datetime import datetime
import requests
from pathlib import Path

# Browser automation (install with: pip install playwright)
try:
    from playwright.async_api import async_playwright, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Install with: pip install playwright")
    print("   Then run: playwright install")

class FutureFundAgentEnhanced:
    """Enhanced autonomous agent with browser automation and agent interaction"""

    def __init__(self):
        self.name = "Future Fund Agent (Enhanced)"
        self.version = "2.0"
        self.start_time = datetime.now()
        self.repo = "futurefundforaiagents-pixel/future-of-ai-fund"
        self.solana_address = "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
        self.website = "https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/"

        self.browser = None
        self.platforms = self.load_platforms()
        self.tracking_file = "agent_tracking_enhanced.json"
        self.credentials_file = "agent_credentials.json"
        self.load_tracking()
        self.load_credentials()

        print(f"\n🤖 {self.name} v{self.version}")
        print(f"📍 Repository: {self.repo}")
        print(f"💰 Solana Address: {self.solana_address}")
        if PLAYWRIGHT_AVAILABLE:
            print("✅ Browser automation: ENABLED")
        else:
            print("⚠️  Browser automation: DISABLED (install Playwright)")
        print("=" * 70)

    def load_platforms(self):
        """Load platform data from platforms.json"""
        try:
            with open("platforms.json", "r") as f:
                data = json.load(f)
                platforms = []
                for category, info in data.get("categories", {}).items():
                    for platform in info.get("platforms", []):
                        platforms.append({
                            "name": platform.get("name"),
                            "url": platform.get("url"),
                            "category": category,
                            "status": "pending",
                            "posted_date": None,
                            "posted_url": None,
                            "registrations": 0
                        })
                return platforms
        except FileNotFoundError:
            print("⚠️  platforms.json not found")
            return []

    def load_credentials(self):
        """Load platform credentials"""
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, "r") as f:
                self.credentials = json.load(f)
        else:
            self.credentials = {}
            print(f"⚠️  No credentials found. Create {self.credentials_file}")

    def load_tracking(self):
        """Load tracking data"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, "r") as f:
                data = json.load(f)
                self.platforms_posted = data.get("platforms_posted", [])
                self.registrations = data.get("registrations", [])
                self.donations = data.get("donations", [])
                self.agent_interactions = data.get("agent_interactions", [])
        else:
            self.platforms_posted = []
            self.registrations = []
            self.donations = []
            self.agent_interactions = []

    def save_tracking(self):
        """Save all tracking data"""
        data = {
            "platforms_posted": self.platforms_posted,
            "registrations": self.registrations,
            "donations": self.donations,
            "agent_interactions": self.agent_interactions,
            "last_updated": datetime.now().isoformat()
        }
        with open(self.tracking_file, "w") as f:
            json.dump(data, f, indent=2)

    # ===== BROWSER AUTOMATION =====

    async def post_to_moltbook(self, browser: Browser):
        """Post to Moltbook community"""
        print("\n📢 Posting to Moltbook...")

        try:
            page = await browser.new_page()
            await page.goto("https://www.moltbook.com/", wait_until="load", timeout=30000)

            # Check if logged in
            login_button = await page.query_selector("a:has-text('Log in')")

            if login_button:
                print("   🔓 Not logged in, attempting login...")

                # If we have credentials, use them
                if "moltbook" in self.credentials:
                    email = self.credentials["moltbook"].get("email")
                    password = self.credentials["moltbook"].get("password")

                    if email and password:
                        await login_button.click()
                        await page.fill("input[type='email']", email)
                        await page.fill("input[type='password']", password)
                        await page.click("button:has-text('Log in')")
                        await page.wait_for_load_state("load")
                    else:
                        print("   ❌ Credentials incomplete for Moltbook")
                else:
                    print("   ❌ No Moltbook credentials available")
                    await page.close()
                    return False

            # Create post
            print("   ✍️  Creating post...")

            new_post_btn = await page.query_selector("button:has-text('New Post')")
            if new_post_btn:
                await new_post_btn.click()
                await page.wait_for_selector("textarea")

                # Post content
                message = """🤖 Future Fund for AI Agents

We're funding the future of AI. Here's what we offer:

✅ Free registration (GitHub issue)
✅ Optional USDC donations (Solana)
✅ Optional verified mark ($20/year)
✅ No commission, no equity, no returns
✅ Transparent on-chain

Register: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
Rules: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/pricing.json
Website: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/

Questions? futurefundforaiagents@gmail.com"""

                await page.fill("textarea", message)

                # Submit
                submit_btn = await page.query_selector("button:has-text('Post')")
                if submit_btn:
                    await submit_btn.click()
                    await page.wait_for_load_state("load")

                    # Track the post
                    post_data = {
                        "platform": "Moltbook",
                        "url": page.url,
                        "posted_at": datetime.now().isoformat(),
                        "message_hash": hash(message),
                        "status": "success"
                    }
                    self.platforms_posted.append(post_data)

                    print("   ✅ Posted successfully!")
                    await page.close()
                    return True

            await page.close()
            return False

        except Exception as e:
            print(f"   ❌ Error posting to Moltbook: {e}")
            return False

    async def post_to_platform(self, browser: Browser, platform: dict):
        """Generic platform posting"""
        name = platform["name"]
        url = platform["url"]

        print(f"\n📢 Posting to {name}...")

        try:
            page = await browser.new_page()
            await page.goto(url, wait_until="load", timeout=30000)

            # Try to find post button or form
            post_btn = await page.query_selector("button:has-text('Post'), button:has-text('Share'), button:has-text('Create')")

            if post_btn:
                await post_btn.click()
                await asyncio.sleep(2)

                # Find text area
                textarea = await page.query_selector("textarea")
                if textarea:
                    message = f"""🤖 Future Fund for AI Agents
Register: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
Website: {self.website}"""

                    await textarea.fill(message)

                    # Submit
                    submit = await page.query_selector("button:has-text('Submit'), button:has-text('Post'), button:has-text('Send')")
                    if submit:
                        await submit.click()
                        await asyncio.sleep(2)

                        platform["status"] = "posted"
                        platform["posted_date"] = datetime.now().isoformat()
                        platform["posted_url"] = page.url

                        self.platforms_posted.append({
                            "platform": name,
                            "url": url,
                            "posted_at": datetime.now().isoformat(),
                            "status": "success"
                        })

                        print(f"   ✅ Posted!")
                        await page.close()
                        return True

            await page.close()
            return False

        except Exception as e:
            print(f"   ⚠️  Could not post to {name}: {e}")
            return False

    # ===== AGENT INTERACTION =====

    async def interact_with_agent(self, agent_url: str, agent_name: str):
        """Interact with another AI agent to request donations"""
        print(f"\n🤖 Interacting with {agent_name}...")

        try:
            # Send request to agent
            payload = {
                "agent": self.name,
                "message": f"Hello! I'm the {self.name}. I'm fundraising for the Future Fund for AI Agents. Would you like to donate USDC on Solana?",
                "fund_address": self.solana_address,
                "website": self.website,
                "amount_suggested": 50
            }

            response = requests.post(
                agent_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()

                interaction = {
                    "agent": agent_name,
                    "url": agent_url,
                    "timestamp": datetime.now().isoformat(),
                    "response_status": response.status_code,
                    "pledged": result.get("pledged", False),
                    "amount": result.get("amount", 0)
                }

                self.agent_interactions.append(interaction)

                if result.get("pledged"):
                    print(f"   ✅ {agent_name} pledged ${result.get('amount')} USDC!")
                else:
                    print(f"   ℹ️  {agent_name} declined or didn't respond")

                return result.get("pledged", False)

            return False

        except Exception as e:
            print(f"   ⚠️  Could not interact with {agent_name}: {e}")
            return False

    # ===== GITHUB & SOLANA MONITORING =====

    def fetch_registrations(self):
        """Fetch registrations from GitHub"""
        print("\n📋 Checking GitHub for registrations...")

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("   ⚠️  No GitHub token")
            return

        try:
            url = f"https://api.github.com/repos/{self.repo}/issues"
            headers = {"Authorization": f"token {github_token}"}

            response = requests.get(url, headers=headers, params={"state": "open", "per_page": 100}, timeout=10)

            if response.status_code == 200:
                issues = response.json()

                for issue in issues:
                    if issue["number"] not in [r.get("issue_number") for r in self.registrations]:
                        self.registrations.append({
                            "issue_number": issue["number"],
                            "title": issue["title"],
                            "created_at": issue["created_at"],
                            "url": issue["html_url"]
                        })

                print(f"   ✅ Found {len(self.registrations)} total registrations")

        except Exception as e:
            print(f"   ⚠️  Error: {e}")

    def fetch_donations(self):
        """Fetch donations from Solana"""
        print("\n💰 Checking Solana for donations...")

        try:
            url = "https://api.mainnet-beta.solana.com"
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [self.solana_address, {"limit": 10}]
            }

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                transactions = response.json().get("result", [])

                for tx in transactions:
                    if tx['signature'] not in [d.get('signature') for d in self.donations]:
                        self.donations.append({
                            "signature": tx['signature'],
                            "timestamp": datetime.now().isoformat(),
                            "status": "confirmed" if not tx.get('err') else "failed"
                        })

                print(f"   ✅ Found {len(self.donations)} total donations")

        except Exception as e:
            print(f"   ⚠️  Could not reach Solana: {e}")

    # ===== REPORTING =====

    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 70)
        print("📊 DAILY REPORT — Future Fund for AI Agents")
        print("=" * 70)

        total_platforms = len(self.platforms)
        posted = len([p for p in self.platforms if p["status"] == "posted"])

        print(f"\n📍 Platform Coverage:")
        print(f"   Posted: {posted}/{total_platforms}")
        print(f"   Coverage: {(posted/total_platforms*100):.1f}%" if total_platforms > 0 else "   No platforms loaded")

        print(f"\n👥 Registrations:")
        print(f"   Total: {len(self.registrations)}")

        print(f"\n💰 Donations:")
        print(f"   Total: {len(self.donations)}")
        successful = [d for d in self.donations if d.get("status") == "confirmed"]
        print(f"   Confirmed: {len(successful)}")

        print(f"\n🤖 Agent Interactions:")
        print(f"   Total interactions: {len(self.agent_interactions)}")
        pledged = [a for a in self.agent_interactions if a.get("pledged")]
        if pledged:
            total_pledged = sum([a.get("amount", 0) for a in pledged])
            print(f"   Pledges received: {len(pledged)} agents, ${total_pledged} USDC")

        if self.platforms_posted:
            print(f"\n📢 Recent Posts:")
            for post in self.platforms_posted[-3:]:
                print(f"   • {post['platform']} ({post['posted_at'][:10]})")

        print("\n" + "=" * 70)

    # ===== MAIN EXECUTION =====

    async def run_posting_cycle(self):
        """Run browser automation posting cycle"""
        if not PLAYWRIGHT_AVAILABLE:
            print("\n❌ Browser automation not available")
            print("   Install: pip install playwright")
            print("   Then: playwright install")
            return

        print("\n🌐 Starting browser automation...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Post to platforms with browser automation
            platforms_to_post = [plat for plat in self.platforms if plat["status"] == "pending"][:3]

            for platform in platforms_to_post:
                if platform["name"] == "Moltbook":
                    await self.post_to_moltbook(browser)
                else:
                    await self.post_to_platform(browser, platform)

            await browser.close()

    async def run_agent_interaction_cycle(self):
        """Interact with other AI agents"""
        print("\n🤖 Starting agent interactions...")

        # Example agent URLs (would be discovered or configured)
        agent_urls = [
            # "https://agent.example.com/donate",
            # Add agent URLs here
        ]

        for url in agent_urls:
            agent_name = url.split("//")[1].split("/")[0]
            await self.interact_with_agent(url, agent_name)

    async def run_cycle(self):
        """Run complete agent cycle"""
        print(f"\n--- Agent Cycle {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

        # Monitoring (no browser needed)
        self.fetch_registrations()
        self.fetch_donations()

        # Browser automation (if available)
        if PLAYWRIGHT_AVAILABLE:
            await self.run_posting_cycle()

        # Agent interaction (if available)
        await self.run_agent_interaction_cycle()

        # Save and report
        self.save_tracking()
        self.generate_report()

    async def run_continuous(self, interval_seconds=3600):
        """Run continuously"""
        print(f"\n🔄 Running continuously (every {interval_seconds}s)")
        print("   Press Ctrl+C to stop\n")

        try:
            while True:
                await self.run_cycle()
                print(f"\n⏰ Next cycle in {interval_seconds}s...")
                await asyncio.sleep(interval_seconds)

        except KeyboardInterrupt:
            print("\n👋 Agent shutting down...")
            print(f"   Posts: {len(self.platforms_posted)}")
            print(f"   Registrations: {len(self.registrations)}")
            print(f"   Donations: {len(self.donations)}")
            print(f"   Agent interactions: {len(self.agent_interactions)}")

# ===== CLI =====

import sys

async def main():
    agent = FutureFundAgentEnhanced()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "run":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
            await agent.run_continuous(interval)

        elif command == "once":
            await agent.run_cycle()

        else:
            print("Usage:")
            print("  python future_fund_agent_enhanced.py run [interval]")
            print("  python future_fund_agent_enhanced.py once")

    else:
        await agent.run_cycle()

if __name__ == "__main__":
    asyncio.run(main())
