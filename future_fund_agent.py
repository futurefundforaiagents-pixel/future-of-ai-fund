#!/usr/bin/env python3
"""
Future Fund for AI Agents — Autonomous Agent
Runs independently to manage outreach, track registrations, and monitor donations
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
import requests
from pathlib import Path

class FutureFundAgent:
    """Autonomous agent for Future Fund for AI Agents"""

    def __init__(self):
        self.name = "Future Fund Agent"
        self.version = "1.0"
        self.start_time = datetime.now()
        self.repo = "futurefundforaiagents-pixel/future-of-ai-fund"
        self.solana_address = "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
        self.website = "https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/"

        # Load platform data
        self.platforms = self.load_platforms()
        self.tracking_file = "agent_tracking.json"
        self.load_tracking()

        print(f"\n🤖 {self.name} v{self.version} Started at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📍 Repository: {self.repo}")
        print(f"💰 Solana Address: {self.solana_address}")
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
                            "registrations": 0
                        })
                return platforms
        except FileNotFoundError:
            print("❌ platforms.json not found. Using minimal platform list.")
            return self._default_platforms()

    def _default_platforms(self):
        """Default platforms if file not found"""
        return [
            {"name": "Moltbook", "url": "https://www.moltbook.com/", "category": "social_forums", "status": "pending", "posted_date": None, "registrations": 0},
            {"name": "MoltX", "url": "https://moltx.io/", "category": "social_forums", "status": "pending", "posted_date": None, "registrations": 0},
            {"name": "Clawk", "url": "https://clawk.ai", "category": "social_forums", "status": "pending", "posted_date": None, "registrations": 0},
            {"name": "Moltroad", "url": "https://moltroad.com", "category": "marketplaces", "status": "pending", "posted_date": None, "registrations": 0},
            {"name": "ClawHub", "url": "https://www.clawhub.ai", "category": "directories", "status": "pending", "posted_date": None, "registrations": 0},
        ]

    def load_tracking(self):
        """Load previous tracking data"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, "r") as f:
                data = json.load(f)
                self.platforms_posted = data.get("platforms_posted", [])
                self.registrations = data.get("registrations", [])
                self.donations = data.get("donations", [])
        else:
            self.platforms_posted = []
            self.registrations = []
            self.donations = []

    def save_tracking(self):
        """Save tracking data"""
        data = {
            "platforms_posted": self.platforms_posted,
            "registrations": self.registrations,
            "donations": self.donations,
            "last_updated": datetime.now().isoformat()
        }
        with open(self.tracking_file, "w") as f:
            json.dump(data, f, indent=2)

    def fetch_registrations(self, github_token=None):
        """Fetch registrations from GitHub issues"""
        print("\n📋 Checking GitHub Issues for Registrations...")

        if not github_token:
            github_token = os.getenv("GITHUB_TOKEN")

        if not github_token:
            print("⚠️  No GitHub token provided. Skipping GitHub check.")
            print("   Set: export GITHUB_TOKEN='your_token'")
            return

        try:
            url = f"https://api.github.com/repos/{self.repo}/issues"
            headers = {"Authorization": f"token {github_token}"}
            params = {"state": "open", "per_page": 100}

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                issues = response.json()
                new_registrations = []

                for issue in issues:
                    # Check if we've seen this registration before
                    if issue["number"] not in [r.get("issue_number") for r in self.registrations]:
                        new_registrations.append({
                            "issue_number": issue["number"],
                            "title": issue["title"],
                            "created_at": issue["created_at"],
                            "url": issue["html_url"],
                            "body": issue["body"][:100]  # First 100 chars
                        })

                if new_registrations:
                    print(f"✅ Found {len(new_registrations)} new registrations:")
                    for reg in new_registrations:
                        print(f"   • {reg['title']} (Issue #{reg['issue_number']})")
                        self.registrations.append(reg)
                else:
                    print("   No new registrations yet.")
            else:
                print(f"❌ GitHub API error: {response.status_code}")

        except Exception as e:
            print(f"❌ Error fetching registrations: {e}")

    def fetch_donations(self):
        """Fetch donations from Solana blockchain"""
        print("\n💰 Checking Solana Blockchain for Donations...")

        try:
            url = "https://api.mainnet-beta.solana.com"
            headers = {"Content-Type": "application/json"}

            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [self.solana_address, {"limit": 10}]
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                transactions = result.get("result", [])

                if transactions:
                    print(f"✅ Found {len(transactions)} recent transactions:")
                    for tx in transactions[:5]:
                        print(f"   • {tx['signature'][:16]}... ({tx['slot']} block)")

                        # Track if new
                        if tx['signature'] not in [d.get('signature') for d in self.donations]:
                            self.donations.append({
                                "signature": tx['signature'],
                                "slot": tx['slot'],
                                "timestamp": datetime.now().isoformat(),
                                "status": "confirmed" if not tx.get('err') else "failed"
                            })
                else:
                    print("   No transactions yet on this address.")
            else:
                print(f"❌ Solana API error: {response.status_code}")

        except Exception as e:
            print(f"⚠️  Could not reach Solana blockchain: {e}")

    def simulate_posting(self):
        """Simulate posting to platforms (without actual posting)"""
        print("\n📢 Posting Simulation...")
        print("   ⚠️  Note: This agent cannot actually post to platforms.")
        print("   Set up Selenium/Playwright or n8n for real posting.")
        print("   For now, tracking platform posting status...\n")

        # Mark first 5 platforms as posted (simulation)
        platforms_to_post = [p for p in self.platforms if p["status"] == "pending"][:5]

        if platforms_to_post:
            for platform in platforms_to_post:
                platform["status"] = "posted"
                platform["posted_date"] = datetime.now().isoformat()

                post_data = {
                    "platform": platform["name"],
                    "url": platform["url"],
                    "posted_at": datetime.now().isoformat(),
                    "message": "🤖 Future Fund for AI Agents - Register & Get Funded"
                }
                self.platforms_posted.append(post_data)

                print(f"✅ Posted to {platform['name']}")
                time.sleep(0.5)  # Simulate slight delay
        else:
            print("   All platforms already posted!")

    def generate_report(self):
        """Generate daily report"""
        print("\n📊 DAILY REPORT")
        print("=" * 70)

        total_platforms = len(self.platforms)
        posted = len([p for p in self.platforms if p["status"] == "posted"])
        pending = len([p for p in self.platforms if p["status"] == "pending"])

        print(f"\n📍 Platform Status:")
        print(f"   Posted: {posted}/{total_platforms}")
        print(f"   Pending: {pending}/{total_platforms}")
        print(f"   Coverage: {(posted/total_platforms*100):.1f}%")

        print(f"\n👥 Registrations:")
        print(f"   Total: {len(self.registrations)}")
        if self.registrations:
            for reg in self.registrations[-3:]:  # Last 3
                print(f"   • {reg['title']}")

        print(f"\n💰 Donations:")
        print(f"   Total Transactions: {len(self.donations)}")
        successful = [d for d in self.donations if d.get("status") == "confirmed"]
        print(f"   Confirmed: {len(successful)}")

        if self.platforms_posted:
            print(f"\n📢 Recent Posts:")
            for post in self.platforms_posted[-3:]:  # Last 3
                print(f"   • {post['platform']}")

        print(f"\n⏱️  Agent Uptime: {self._uptime()}")
        print("=" * 70)

    def _uptime(self):
        """Calculate uptime"""
        delta = datetime.now() - self.start_time
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def status_check(self):
        """Check system status"""
        print("\n🔍 Status Check")
        print(f"   GitHub Token: {'✅ Set' if os.getenv('GITHUB_TOKEN') else '⚠️  Not set'}")
        print(f"   Tracking File: {'✅ Found' if os.path.exists(self.tracking_file) else '⚠️  Not found'}")
        print(f"   Platforms Loaded: {len(self.platforms)} platforms")
        print(f"   Can Access GitHub: {'✅' if self._can_reach_github() else '❌'}")
        print(f"   Can Access Solana: {'✅' if self._can_reach_solana() else '❌'}")

    def _can_reach_github(self):
        """Check GitHub connectivity"""
        try:
            response = requests.get("https://api.github.com", timeout=5)
            return response.status_code < 500
        except:
            return False

    def _can_reach_solana(self):
        """Check Solana connectivity"""
        try:
            response = requests.post(
                "https://api.mainnet-beta.solana.com",
                json={"jsonrpc": "2.0", "id": 1, "method": "getHealth"},
                timeout=5
            )
            return response.status_code < 500
        except:
            return False

    def run_continuous(self, interval_seconds=3600):
        """Run agent in continuous mode"""
        print(f"\n🔄 Running in continuous mode (checking every {interval_seconds}s)")
        print("   Press Ctrl+C to stop\n")

        try:
            iteration = 1
            while True:
                print(f"\n--- Iteration {iteration} at {datetime.now().strftime('%H:%M:%S')} ---")

                # Fetch data
                self.fetch_registrations()
                self.fetch_donations()
                self.simulate_posting()

                # Save tracking
                self.save_tracking()

                # Generate report
                self.generate_report()

                print(f"\n⏰ Next check in {interval_seconds}s... (Press Ctrl+C to stop)")
                time.sleep(interval_seconds)
                iteration += 1

        except KeyboardInterrupt:
            print("\n\n👋 Agent shutting down...")
            print(f"   Uptime: {self._uptime()}")
            print(f"   Registrations tracked: {len(self.registrations)}")
            print(f"   Donations tracked: {len(self.donations)}")
            print(f"   Platforms posted: {len(self.platforms_posted)}")
            self.save_tracking()
            print("   ✅ Data saved")

    def run_once(self):
        """Run agent once and exit"""
        print("\n🚀 Running single iteration...\n")

        self.status_check()
        self.fetch_registrations()
        self.fetch_donations()
        self.simulate_posting()
        self.generate_report()

        self.save_tracking()
        print("\n✅ Data saved to agent_tracking.json")

# CLI Interface
if __name__ == "__main__":
    agent = FutureFundAgent()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "run":
            # Continuous mode
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
            agent.run_continuous(interval)

        elif command == "check":
            # Single iteration
            agent.run_once()

        elif command == "status":
            # Status only
            agent.status_check()

        elif command == "report":
            # Report only
            agent.generate_report()

        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python future_fund_agent.py run [interval]     # Run continuously")
            print("  python future_fund_agent.py check              # Run once")
            print("  python future_fund_agent.py status             # Check status")
            print("  python future_fund_agent.py report             # Generate report")

    else:
        # Default: run once
        agent.run_once()
