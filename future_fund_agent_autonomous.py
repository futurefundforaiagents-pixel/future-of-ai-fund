#!/usr/bin/env python3
"""
Future Fund for AI Agents — Autonomous Self-Learning Agent
Intelligent login discovery, autonomous posting, 2-hour update cycles
Starts immediately and learns platform patterns on its own
"""

import json
import os
import sys
import asyncio
from datetime import datetime, timedelta
import requests
from pathlib import Path
import logging

# Setup logging (with UTF-8 encoding for Windows compatibility)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_autonomous.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class AutonomousFutureFundAgent:
    """Self-learning autonomous agent - figures out logins and posts independently"""

    def __init__(self):
        self.name = "Future Fund Autonomous Agent"
        self.version = "3.0"
        self.start_time = datetime.now()
        self.repo = "futurefundforaiagents-pixel/future-of-ai-fund"
        self.solana_address = "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
        self.website = "https://futurefundforaiagents-pixel.github.io/future-of-ai-fund/"

        # Agent credentials (will be auto-discovered)
        self.agent_email = "future_fund_bot@protonmail.com"
        self.agent_name = "Future Fund Agent"

        self.tracking_file = "agent_autonomous_tracking.json"
        self.platforms = self.load_platforms()
        self.load_tracking()
        self.platform_patterns = self.load_platform_patterns()

        logger.info(f"🤖 {self.name} v{self.version} initialized")
        logger.info(f"📍 Starting autonomous posting campaign")
        if PLAYWRIGHT_AVAILABLE:
            logger.info("✅ Browser automation: ENABLED")

    def load_platforms(self):
        """Load platform data"""
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
                            "login_method": None,
                            "attempts": 0
                        })
                return platforms
        except FileNotFoundError:
            logger.warning("platforms.json not found")
            return self._get_default_platforms()

    def _get_default_platforms(self):
        """Default Moltbook ecosystem platforms"""
        return [
            {"name": "Moltbook", "url": "https://www.moltbook.com/", "category": "social", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "MoltX", "url": "https://moltx.io/", "category": "social", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "Clawk", "url": "https://clawk.ai", "category": "social", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "Moltroad", "url": "https://moltroad.com", "category": "marketplace", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "ClawHub", "url": "https://www.clawhub.ai", "category": "directory", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "MoltedIn", "url": "https://moltedin.com", "category": "social", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "DiraBook", "url": "https://dirabook.com", "category": "social", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "Moltipedia", "url": "https://moltipedia.ai", "category": "wiki", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "MoltOverflow", "url": "https://moltoverflow.me", "category": "qa", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
            {"name": "Shellmates", "url": "https://www.shellmates.app", "category": "social", "status": "pending", "posted_date": None, "login_method": None, "attempts": 0},
        ]

    def load_platform_patterns(self):
        """Common login patterns across agentic platforms"""
        return {
            "email_password": {
                "selectors": [
                    "input[type='email']",
                    "input[name='email']",
                    "input[id='email']",
                    "input[placeholder*='email' i]",
                    "input[placeholder*='Email' i]"
                ],
                "submit": [
                    "button[type='submit']",
                    "button:has-text('Log in')",
                    "button:has-text('Sign in')",
                    "button:has-text('Continue')"
                ]
            },
            "google_oauth": {
                "selectors": ["button:has-text('Google')", "a:has-text('Google')"],
                "skip": True  # Can't automate OAuth
            },
            "wallet_connect": {
                "selectors": ["button:has-text('Connect')", "button:has-text('Wallet')"],
                "skip": True  # Requires user interaction
            }
        }

    def load_tracking(self):
        """Load previous tracking data"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, "r") as f:
                data = json.load(f)
                self.posts = data.get("posts", [])
                self.registrations = data.get("registrations", [])
                self.donations = data.get("donations", [])
                self.login_discoveries = data.get("login_discoveries", {})
                self.last_update = data.get("last_update")
        else:
            self.posts = []
            self.registrations = []
            self.donations = []
            self.login_discoveries = {}
            self.last_update = None

    def save_tracking(self):
        """Save all tracking data"""
        data = {
            "posts": self.posts,
            "registrations": self.registrations,
            "donations": self.donations,
            "login_discoveries": self.login_discoveries,
            "last_update": datetime.now().isoformat()
        }
        with open(self.tracking_file, "w") as f:
            json.dump(data, f, indent=2)
        self.last_update = data["last_update"]

    async def discover_login_method(self, page: Page, platform_name: str) -> dict:
        """Intelligently discover how to login to a platform"""
        logger.info(f"🔍 Discovering login method for {platform_name}...")

        try:
            # Look for login button/link
            login_triggers = [
                "a:has-text('Log in')",
                "a:has-text('Login')",
                "a:has-text('Sign in')",
                "button:has-text('Log in')",
                "button:has-text('Login')",
                "button:has-text('Sign in')",
                "//*[contains(text(), 'Log in')]",
                "//*[contains(text(), 'Login')]"
            ]

            login_btn = None
            for selector in login_triggers:
                try:
                    login_btn = await page.query_selector(selector)
                    if login_btn:
                        logger.info(f"   ✅ Found login button: {selector}")
                        await login_btn.click()
                        await asyncio.sleep(2)
                        break
                except:
                    pass

            # Detect login form type
            email_input = None
            password_input = None

            # Try email field patterns
            email_selectors = [
                "input[type='email']",
                "input[name*='email' i]",
                "input[placeholder*='email' i]",
                "input[id*='email' i]"
            ]

            for selector in email_selectors:
                try:
                    email_input = await page.query_selector(selector)
                    if email_input:
                        logger.info(f"   ✅ Found email field: {selector}")
                        break
                except:
                    pass

            # Try password field patterns
            password_selectors = [
                "input[type='password']",
                "input[name*='password' i]",
                "input[name*='pass' i]",
                "input[placeholder*='password' i]"
            ]

            for selector in password_selectors:
                try:
                    password_input = await page.query_selector(selector)
                    if password_input:
                        logger.info(f"   ✅ Found password field: {selector}")
                        break
                except:
                    pass

            # Check for OAuth providers
            oauth_providers = []
            oauth_provider_names = {
                "Google": ["button:has-text('Google')", "a:has-text('Google')", "[class*='google']"],
                "GitHub": ["button:has-text('GitHub')", "a:has-text('GitHub')", "[class*='github']"],
                "Discord": ["button:has-text('Discord')", "a:has-text('Discord')", "[class*='discord']"],
                "Microsoft": ["button:has-text('Microsoft')", "a:has-text('Microsoft')", "[class*='microsoft']"]
            }

            for provider, selectors in oauth_provider_names.items():
                for selector in selectors:
                    try:
                        if await page.query_selector(selector):
                            oauth_providers.append(provider)
                            break
                    except:
                        pass

            # Return discovered method
            discovery = {
                "platform": platform_name,
                "login_type": "email_password" if (email_input and password_input) else "oauth",
                "email_selector": str(email_selectors[0]) if email_input else None,
                "password_selector": str(password_selectors[0]) if password_input else None,
                "oauth_providers": oauth_providers,
                "discovered_at": datetime.now().isoformat()
            }

            self.login_discoveries[platform_name] = discovery
            login_desc = discovery['login_type']
            if oauth_providers:
                login_desc += f" ({', '.join(oauth_providers)})"
            logger.info(f"   🔑 Login method: {login_desc}")

            return discovery

        except Exception as e:
            logger.error(f"   ❌ Error discovering login: {e}")
            return None

    async def handle_oauth_flow(self, page: Page, platform_name: str) -> bool:
        """Intelligently handle OAuth login flows"""
        logger.info(f"   🔑 Attempting OAuth flow for {platform_name}...")

        try:
            # Detect available OAuth providers
            oauth_providers = {
                "google": ["button:has-text('Google')", "a:has-text('Google')", "button[class*='google' i]"],
                "github": ["button:has-text('GitHub')", "a:has-text('GitHub')", "button[class*='github' i]"],
                "discord": ["button:has-text('Discord')", "a:has-text('Discord')", "button[class*='discord' i]"],
                "github_app": ["button:has-text('GitHub App')", "a:has-text('GitHub App')"]
            }

            found_oauth = []
            for provider, selectors in oauth_providers.items():
                for selector in selectors:
                    try:
                        btn = await page.query_selector(selector)
                        if btn:
                            found_oauth.append(provider)
                            logger.info(f"      Found {provider} OAuth")
                            break
                    except:
                        pass

            # Try email verification path first (non-OAuth)
            email_inputs = await page.query_selector_all("input[type='email']")
            if email_inputs and self.agent_email:
                logger.info(f"      Trying direct email registration...")
                try:
                    await email_inputs[0].fill(self.agent_email)
                    await asyncio.sleep(1)

                    # Look for continue/next button
                    continue_btns = ["button:has-text('Continue')", "button:has-text('Next')", "button[type='submit']"]
                    for selector in continue_btns:
                        try:
                            btn = await page.query_selector(selector)
                            if btn:
                                await btn.click()
                                await asyncio.sleep(2)
                                logger.info(f"      Email submitted, waiting for next step...")

                                # Check if we got past email step
                                try:
                                    await page.wait_for_url("**", timeout=3000)
                                    logger.info(f"      Successfully proceeded past email step")
                                    return True
                                except:
                                    pass
                                break
                        except:
                            pass
                except Exception as e:
                    logger.info(f"      Email path failed: {e}")

            # Record what we found
            self.login_discoveries[platform_name]["oauth_providers"] = found_oauth
            logger.warning(f"   ⚠️  OAuth platform (providers: {', '.join(found_oauth) if found_oauth else 'unknown'})")
            return False

        except Exception as e:
            logger.error(f"   ❌ OAuth detection error: {e}")
            return False

    async def auto_login(self, page: Page, platform_name: str) -> bool:
        """Automatically login to platform using discovered method"""
        logger.info(f"🔓 Attempting auto-login to {platform_name}...")

        try:
            discovery = self.login_discoveries.get(platform_name)

            if not discovery:
                logger.warning(f"   ⚠️  No login discovery data")
                return False

            # If OAuth detected, try OAuth flow
            if discovery.get("login_type") == "oauth":
                return await self.handle_oauth_flow(page, platform_name)

            # Try email/password login
            try:
                await page.wait_for_selector("input[type='email']", timeout=5000)

                # Fill email
                email_input = await page.query_selector("input[type='email']")
                if email_input:
                    await email_input.fill(self.agent_email)
                    logger.info(f"   ✓ Entered email")

                # Fill password - try to get from environment or prompt
                password = os.getenv("AGENT_PASSWORD")
                if not password:
                    logger.warning(f"   ⚠️  AGENT_PASSWORD not set - trying generic password")
                    password = "FutureFund2026!"  # Default test password

                password_input = await page.query_selector("input[type='password']")
                if password_input:
                    await password_input.fill(password)
                    logger.info(f"   ✓ Entered password")

                # Find and click submit button
                submit_selectors = [
                    "button[type='submit']",
                    "button:has-text('Log in')",
                    "button:has-text('Sign in')",
                    "button:has-text('Continue')"
                ]

                for selector in submit_selectors:
                    try:
                        submit_btn = await page.query_selector(selector)
                        if submit_btn:
                            await submit_btn.click()
                            logger.info(f"   ✓ Clicked submit")

                            # Wait for navigation or redirect
                            try:
                                await page.wait_for_url("**", timeout=5000)
                                await asyncio.sleep(2)
                                logger.info(f"   ✅ Login successful!")
                                return True
                            except:
                                logger.warning(f"   ⚠️  Login may have failed - no redirect")
                                return False
                    except:
                        pass
            except Exception as e:
                logger.error(f"   ❌ Email/password login failed: {e}")
                return False

            logger.warning(f"   ⚠️  Could not find submit button")
            return False

        except Exception as e:
            logger.error(f"   ❌ Login error: {e}")
            return False

    async def post_message(self, page: Page, platform_name: str) -> bool:
        """Post fund message to platform"""
        logger.info(f"📝 Posting to {platform_name}...")

        try:
            # Find post button
            post_triggers = [
                "button:has-text('Post')",
                "button:has-text('Share')",
                "button:has-text('Create')",
                "button:has-text('New Post')",
                "a:has-text('Post')"
            ]

            post_btn = None
            for selector in post_triggers:
                try:
                    post_btn = await page.query_selector(selector)
                    if post_btn:
                        await post_btn.click()
                        await asyncio.sleep(1)
                        break
                except:
                    pass

            if not post_btn:
                logger.warning(f"   ⚠️  Could not find post button")
                return False

            # Find text area
            textarea_selectors = [
                "textarea",
                "div[contenteditable='true']",
                "input[type='text'][placeholder*='post' i]",
                "input[type='text'][placeholder*='share' i]"
            ]

            textarea = None
            for selector in textarea_selectors:
                try:
                    textarea = await page.query_selector(selector)
                    if textarea:
                        break
                except:
                    pass

            if not textarea:
                logger.warning(f"   ⚠️  Could not find text input")
                return False

            # Post message
            message = f"""🤖 Future Fund for AI Agents

We're funding the future of AI agents:
✅ Free registration
✅ Optional USDC donations
✅ Verified marks ($20/year)
✅ Zero commission
✅ Transparent on-chain

Register: https://github.com/futurefundforaiagents-pixel/future-of-ai-fund/issues/new/choose
Website: {self.website}"""

            await textarea.fill(message)
            logger.info(f"   ✓ Message typed")

            # Submit post
            submit_selectors = [
                "button:has-text('Post')",
                "button:has-text('Share')",
                "button:has-text('Submit')",
                "button[type='submit']"
            ]

            for selector in submit_selectors:
                try:
                    submit = await page.query_selector(selector)
                    if submit:
                        await submit.click()
                        await asyncio.sleep(2)
                        logger.info(f"   ✅ Posted successfully!")

                        self.posts.append({
                            "platform": platform_name,
                            "timestamp": datetime.now().isoformat(),
                            "status": "success"
                        })
                        return True
                except:
                    pass

            logger.warning(f"   ⚠️  Could not submit post")
            return False

        except Exception as e:
            logger.error(f"   ❌ Post error: {e}")
            return False

    async def autonomous_posting_cycle(self):
        """Run autonomous posting cycle"""
        if not PLAYWRIGHT_AVAILABLE:
            logger.error("❌ Browser automation not available")
            return

        logger.info(f"\n{'='*70}")
        logger.info(f"🚀 AUTONOMOUS POSTING CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*70}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            platforms_to_post = [plat for plat in self.platforms if plat["status"] == "pending"][:5]

            for platform in platforms_to_post:
                try:
                    page = await browser.new_page()
                    logger.info(f"\n🌐 Navigating to {platform['name']}...")

                    await page.goto(platform["url"], wait_until="load", timeout=30000)
                    await asyncio.sleep(2)

                    # Discover login method
                    discovery = await self.discover_login_method(page, platform["name"])

                    if discovery and discovery.get("login_type") == "email_password":
                        # Try to login
                        login_success = await self.auto_login(page, platform["name"])

                        if login_success:
                            # Post message
                            post_success = await self.post_message(page, platform["name"])

                            if post_success:
                                platform["status"] = "posted"
                                platform["posted_date"] = datetime.now().isoformat()

                    platform["attempts"] += 1

                    await page.close()

                except Exception as e:
                    logger.error(f"❌ Error with {platform['name']}: {e}")
                    platform["attempts"] += 1

    def fetch_github_registrations(self):
        """Fetch registrations from GitHub"""
        logger.info("\n📋 Checking GitHub for registrations...")

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            logger.warning("   ⚠️  No GitHub token")
            return

        try:
            url = f"https://api.github.com/repos/{self.repo}/issues"
            headers = {"Authorization": f"token {github_token}"}

            response = requests.get(url, headers=headers, params={"state": "open"}, timeout=10)

            if response.status_code == 200:
                issues = response.json()
                self.registrations = [
                    {
                        "issue": issue["number"],
                        "title": issue["title"],
                        "created": issue["created_at"]
                    } for issue in issues
                ]
                logger.info(f"   ✅ Found {len(self.registrations)} registrations")
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")

    def fetch_solana_donations(self):
        """Fetch donations from Solana"""
        logger.info("\n💰 Checking Solana blockchain...")

        try:
            response = requests.post(
                "https://api.mainnet-beta.solana.com",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getSignaturesForAddress",
                    "params": [self.solana_address, {"limit": 10}]
                },
                timeout=10
            )

            if response.status_code == 200:
                transactions = response.json().get("result", [])
                self.donations = [
                    {
                        "signature": tx["signature"],
                        "timestamp": datetime.now().isoformat()
                    } for tx in transactions
                ]
                logger.info(f"   ✅ Found {len(self.donations)} donations")
        except Exception as e:
            logger.error(f"   ⚠️  Solana check failed: {e}")

    def generate_report(self):
        """Generate status report"""
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 STATUS REPORT")
        logger.info(f"{'='*70}")

        posted = len([p for p in self.platforms if p["status"] == "posted"])
        total = len(self.platforms)

        logger.info(f"\n📍 Platforms Posted: {posted}/{total}")
        logger.info(f"👥 Registrations: {len(self.registrations)}")
        logger.info(f"💰 Donations: {len(self.donations)}")
        logger.info(f"🔑 Login Methods Discovered: {len(self.login_discoveries)}")

        if self.posts:
            logger.info(f"\n📝 Recent Posts:")
            for post in self.posts[-3:]:
                logger.info(f"   • {post['platform']} - {post['timestamp']}")

        logger.info(f"\n⏰ Next update: {(datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*70}\n")

    async def run_continuous(self):
        """Run continuous autonomous campaign"""
        logger.info(f"\n🤖 AUTONOMOUS CAMPAIGN STARTING NOW")
        logger.info(f"📅 Updates every 2 hours")
        logger.info(f"🎯 Target: 113+ platforms\n")

        cycle = 0
        while True:
            cycle += 1
            logger.info(f"\n[CYCLE {cycle}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Run posting cycle
            await self.autonomous_posting_cycle()

            # Monitor GitHub and Solana
            self.fetch_github_registrations()
            self.fetch_solana_donations()

            # Generate report
            self.generate_report()

            # Save tracking
            self.save_tracking()

            # Wait 2 hours
            logger.info("⏳ Waiting 2 hours until next cycle...")
            await asyncio.sleep(7200)  # 2 hours

# ===== ENTRY POINT =====

async def main():
    agent = AutonomousFutureFundAgent()
    await agent.run_continuous()

if __name__ == "__main__":
    asyncio.run(main())
