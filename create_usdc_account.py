#!/usr/bin/env python3
"""
Create USDC Token Account for Future Fund
Interactive script to set up USDC receiving on Solana mainnet
"""

import subprocess
import sys
import os
import json
from pathlib import Path

WALLET_ADDRESS = "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
USDC_MINT = "EPjFWaJwJqkKJkx9pKrFv82bABmJVWqhxzVNMmRWt9qz"
NETWORK = "mainnet-beta"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_solana_cli():
    """Check if Solana CLI is installed"""
    print("🔍 Checking for Solana CLI...")

    try:
        result = subprocess.run(["solana", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass

    print("❌ Solana CLI not found")
    print("\n📥 INSTALL SOLANA CLI:")
    print("   1. Download: https://docs.solana.com/cli/install-solana-cli-tools")
    print("   2. Run installer")
    print("   3. Restart terminal")
    print("   4. Verify: solana --version")
    return False

def check_keypair():
    """Find or prompt for keypair file"""
    print("\n🔑 Checking for keypair file...")

    # Common keypair locations
    possible_paths = [
        Path.home() / ".config" / "solana" / "id.json",
        Path.home() / "solana-wallet.json",
        Path("id.json"),
    ]

    # Check if any exist
    for path in possible_paths:
        if path.exists():
            print(f"✅ Found keypair: {path}")
            return str(path)

    print("❌ No keypair file found in default locations:")
    for path in possible_paths:
        print(f"   • {path}")

    # Prompt user
    print("\n📝 Enter your keypair file path:")
    custom_path = input("  > ").strip()

    if Path(custom_path).exists():
        print(f"✅ Found keypair: {custom_path}")
        return custom_path
    else:
        print(f"❌ File not found: {custom_path}")
        print("\n💡 Create a new keypair with:")
        print("   $ solana-keygen new -o ~/solana-wallet.json")
        return None

def set_network():
    """Set Solana network to mainnet-beta"""
    print("\n🌐 Setting network to mainnet-beta...")

    try:
        result = subprocess.run(
            ["solana", "config", "set", "--url", NETWORK],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Network set to mainnet-beta")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")

    return False

def show_config():
    """Show Solana config"""
    print("\n📋 Current Solana configuration:")

    try:
        result = subprocess.run(
            ["solana", "config", "get"],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split("\n"):
            if line.strip():
                print(f"   {line}")
    except Exception as e:
        print(f"⚠️  Could not show config: {e}")

def create_token_account(keypair_path):
    """Create USDC token account"""
    print_header("CREATING USDC TOKEN ACCOUNT")

    print("This will:")
    print(f"  1. Create token account on Solana {NETWORK}")
    print(f"  2. Cost: ~0.002 SOL (you have sufficient balance)")
    print(f"  3. Link to wallet: {WALLET_ADDRESS}")
    print(f"  4. Accept USDC donations")
    print()

    print("Command:")
    print(f"  spl-token create-account {USDC_MINT} \\")
    print(f"    --owner {WALLET_ADDRESS} \\")
    print(f"    --fee-payer {keypair_path}")
    print()

    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Cancelled")
        return False

    print("\n⏳ Creating account...")

    try:
        result = subprocess.run([
            "spl-token", "create-account", USDC_MINT,
            "--owner", WALLET_ADDRESS,
            "--fee-payer", keypair_path
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ Account created successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Error creating account:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_account():
    """Verify token account was created"""
    print("\n✓ Verifying token accounts...")

    try:
        result = subprocess.run([
            "spl-token", "accounts",
            "--owner", WALLET_ADDRESS
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("⚠️  Could not verify")
            return False
    except Exception as e:
        print(f"⚠️  Verification failed: {e}")
        return False

def show_success():
    """Show success message"""
    print_header("SUCCESS! READY TO RECEIVE USDC")

    print("✅ Your USDC token account is created!")
    print()
    print("📍 Wallet Address:")
    print(f"   {WALLET_ADDRESS}")
    print()
    print("💰 How to receive donations:")
    print("   1. Share address with agents")
    print("   2. They send USDC to your address")
    print("   3. Deposits appear instantly")
    print()
    print("🔍 View on Solscan:")
    print(f"   https://solscan.io/account/{WALLET_ADDRESS}")
    print()
    print("📊 Monitor with agent:")
    print("   MEGA Agent watches 24/7 for donations")
    print()
    print("💸 Withdraw when ready:")
    print("   Use: spl-token transfer [amount] [recipient]")
    print()

def main():
    print_header("FUTURE FUND - CREATE USDC TOKEN ACCOUNT")

    # Step 1: Check Solana CLI
    if not check_solana_cli():
        return 1

    # Step 2: Set network
    if not set_network():
        print("❌ Failed to set network")
        return 1

    # Step 3: Show config
    show_config()

    # Step 4: Find keypair
    keypair = check_keypair()
    if not keypair:
        return 1

    # Step 5: Create account
    if not create_token_account(keypair):
        return 1

    # Step 6: Verify
    verify_account()

    # Step 7: Success
    show_success()

    return 0

if __name__ == "__main__":
    sys.exit(main())
