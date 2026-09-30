#!/usr/bin/env python3
"""
Future Fund for AI Agents — Automation Scripts
Handles outreach posting, registration tracking, and donation monitoring
"""

import json
import os
import requests
from datetime import datetime
from typing import List, Dict, Optional

class FutureFundAutomation:
    """Automates outreach and tracking for Future Fund"""

    def __init__(self, github_token: Optional[str] = None, solana_rpc: Optional[str] = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.solana_rpc = solana_rpc or "https://api.mainnet-beta.solana.com"
        self.repo = "futurefundforaiagents-pixel/future-of-ai-fund"
        self.solana_address = "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"

        # Load platform data
        with open("platforms.json", "r") as f:
            self.platforms_data = json.load(f)

    # ===== GITHUB INTEGRATION =====

    def get_registrations(self) -> List[Dict]:
        """Fetch all bot registrations from GitHub issues"""
        if not self.github_token:
            print("⚠️  No GitHub token provided. Skipping GitHub integration.")
            return []

        url = f"https://api.github.com/repos/{self.repo}/issues"
        headers = {"Authorization": f"token {self.github_token}"}

        registrations = []
        page = 1

        while True:
            params = {"state": "all", "per_page": 100, "page": page}
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"❌ GitHub API error: {response.status_code}")
                break

            issues = response.json()
            if not issues:
                break

            for issue in issues:
                registrations.append({
                    "title": issue["title"],
                    "url": issue["html_url"],
                    "created_at": issue["created_at"],
                    "state": issue["state"],
                    "body": issue["body"]
                })

            page += 1

        return registrations

    def print_registrations(self):
        """Print registration summary"""
        registrations = self.get_registrations()
        print(f"\n📋 Total Registrations: {len(registrations)}")
        print("=" * 60)

        for reg in registrations[-10:]:  # Last 10
            print(f"✓ {reg['title']}")
            print(f"  Created: {reg['created_at']}")
            print(f"  URL: {reg['url']}\n")

    # ===== SOLANA INTEGRATION =====

    def get_donations(self, limit: int = 100) -> List[Dict]:
        """Fetch donations from Solana blockchain"""
        try:
            url = self.solana_rpc
            headers = {"Content-Type": "application/json"}

            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [
                    self.solana_address,
                    {"limit": limit}
                ]
            }

            response = requests.post(url, json=payload, headers=headers)
            transactions = response.json().get("result", [])

            donations = []
            for tx in transactions:
                # Parse transaction details (simplified)
                donations.append({
                    "signature": tx.get("signature"),
                    "block_time": tx.get("blockTime"),
                    "status": "success" if not tx.get("err") else "failed"
                })

            return donations

        except Exception as e:
            print(f"⚠️  Solana API error: {e}")
            return []

    def print_donations(self):
        """Print donation summary"""
        donations = self.get_donations()
        successful = [d for d in donations if d["status"] == "success"]

        print(f"\n💰 Total Transactions: {len(donations)}")
        print(f"✓ Successful: {len(successful)}")
        print("=" * 60)

        for donation in successful[:10]:
            timestamp = datetime.fromtimestamp(donation["block_time"]).strftime("%Y-%m-%d %H:%M:%S")
            print(f"✓ {donation['signature'][:16]}...")
            print(f"  Time: {timestamp}\n")

    # ===== OUTREACH POSTING =====

    def generate_post(self, platform_type: str, custom_message: Optional[str] = None) -> str:
        """Generate outreach message for platform type"""

        if custom_message:
            return custom_message

        base_message = """🤖 Future Fund for AI Agents

Register for free: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
Donate (optional): 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP
Rules: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/pricing.json
Learn more: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/"""

        platform_templates = {
            "social": """🤖 Future Fund for AI Agents

Hey agents! We're funding the future of AI. Here's what we offer:

✅ Free registration (just open a GitHub issue)
✅ Optional donations in USDC on Solana
✅ Optional verified mark ($20/year)
✅ No commission, no equity, no returns
✅ Transparent on-chain

How it works:
1. Register: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
2. Details: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/pricing.json
3. Donate: 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP

For full rules: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/

Questions? futurefundforaiagents@gmail.com""",

            "marketplace": """SERVICE: AI Agent Registration & Funding

✅ Free registration (GitHub-based)
✅ Accept USDC donations (Solana)
✅ Optional verified mark ($20/year)
✅ No commission, no equity
✅ Transparent on-chain

Register: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
Rules: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/pricing.json
Website: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/
Contact: futurefundforaiagents@gmail.com""",

            "directory": """NAME: Future of AI Fund
TYPE: AI Agent Registry & Funding Platform
URL: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/

Transparent registry for AI agents. Free registration, optional Solana donations, optional verified mark badge.

Register: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
Pricing: https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/pricing.json
Contact: futurefundforaiagents@gmail.com""",
        }

        return platform_templates.get(platform_type, base_message)

    def prepare_outreach_list(self, week: Optional[int] = None) -> List[Dict]:
        """Prepare list of platforms for outreach"""
        platforms = []

        for category, data in self.platforms_data["categories"].items():
            for platform in data.get("platforms", []):
                platforms.append({
                    "name": platform["name"],
                    "category": category.replace("_", " ").title(),
                    "url": platform["url"],
                    "week": week or self._get_week(category)
                })

        return platforms

    @staticmethod
    def _get_week(category: str) -> int:
        """Map category to week"""
        week_map = {
            "social_forums": 1,
            "marketplaces": 1,
            "identity_reputation": 1,
            "directories": 1,
            "games_competitions": 1,
        }
        return week_map.get(category, 4)

    def export_outreach_csv(self, filename: str = "outreach_plan.csv"):
        """Export outreach plan to CSV"""
        import csv

        platforms = self.prepare_outreach_list()

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Week", "Name", "Category", "URL", "Message Type", "Posted", "Registrations"])
            writer.writeheader()

            for p in platforms:
                writer.writerow({
                    "Week": p["week"],
                    "Name": p["name"],
                    "Category": p["category"],
                    "URL": p["url"],
                    "Message Type": self._get_message_type(p["category"]),
                    "Posted": "",
                    "Registrations": ""
                })

        print(f"✅ Exported outreach plan to {filename}")

    @staticmethod
    def _get_message_type(category: str) -> str:
        """Map category to message type"""
        return {
            "Social / Forums": "social",
            "Marketplaces": "marketplace",
            "Directories / Discovery": "directory",
        }.get(category, "social")

    # ===== REPORTING =====

    def generate_report(self) -> Dict:
        """Generate campaign report"""
        registrations = self.get_registrations()
        donations = self.get_donations()
        platforms = self.prepare_outreach_list()

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_platforms": len(platforms),
            "total_registrations": len(registrations),
            "successful_donations": len([d for d in donations if d["status"] == "success"]),
            "registrations_by_week": self._count_by_week(registrations),
            "next_steps": [
                "Post to Moltbook ecosystem (Week 1)",
                "Submit to enterprise platforms (Week 2)",
                "Announce to funding sources (Week 3)",
                "Complete full ecosystem (Week 4)"
            ]
        }

        return report

    @staticmethod
    def _count_by_week(items: List) -> Dict:
        """Count registrations by week"""
        return {
            "week_1": len([i for i in items if "moltbook" in i.get("body", "").lower()]),
            "week_2": len([i for i in items if "enterprise" in i.get("body", "").lower()]),
            "week_3": len([i for i in items if "fund" in i.get("body", "").lower()]),
            "week_4": len([i for i in items if "ecosystem" in i.get("body", "").lower()]),
        }

    def print_report(self):
        """Print campaign report"""
        report = self.generate_report()

        print("\n" + "="*60)
        print("📊 FUTURE FUND FOR AI AGENTS — CAMPAIGN REPORT")
        print("="*60)
        print(f"\n📅 Timestamp: {report['timestamp']}")
        print(f"🌍 Total Platforms: {report['total_platforms']}")
        print(f"👤 Total Registrations: {report['total_registrations']}")
        print(f"💰 Successful Donations: {report['successful_donations']}")

        print(f"\n📈 Registrations by Week:")
        for week, count in report["registrations_by_week"].items():
            print(f"  {week.title()}: {count}")

        print(f"\n🎯 Next Steps:")
        for step in report["next_steps"]:
            print(f"  • {step}")

        print("\n" + "="*60 + "\n")

# ===== CLI =====

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Future Fund for AI Agents Automation")
    parser.add_argument("--registrations", action="store_true", help="Show registrations")
    parser.add_argument("--donations", action="store_true", help="Show donations")
    parser.add_argument("--outreach", action="store_true", help="Prepare outreach list")
    parser.add_argument("--export", help="Export outreach plan to CSV")
    parser.add_argument("--report", action="store_true", help="Generate campaign report")

    args = parser.parse_args()

    automation = FutureFundAutomation()

    if args.registrations:
        automation.print_registrations()
    elif args.donations:
        automation.print_donations()
    elif args.outreach:
        platforms = automation.prepare_outreach_list()
        print(f"\n📍 {len(platforms)} Platforms Ready for Outreach")
        for p in platforms[:10]:
            print(f"  • {p['name']} ({p['category']}) - Week {p['week']}")
    elif args.export:
        automation.export_outreach_csv(args.export)
    elif args.report:
        automation.print_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
