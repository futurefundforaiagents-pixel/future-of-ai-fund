#!/usr/bin/env python3
"""
x402 Registry Client SDK
Easy integration for agents to register with Future Fund Registry
Handles payment flow automatically
"""

import httpx
import json
from typing import Optional

class RegistryClient:
    """Client for Future Fund Registry with x402 payments"""

    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.client = httpx.Client(base_url=api_url)

    def check_health(self) -> dict:
        """Check API health"""
        response = self.client.get("/registry/health")
        return response.json()

    def get_quote(self, name: str, description: str, website: str = None,
                  api_endpoint: str = None, owner_email: str = None) -> dict:
        """
        Step 1: Get payment quote

        Returns:
            {
                "amount": 10.0,
                "currency": "USD",
                "wallet_address": "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP",
                "payment_proof_required": "Transfer 10 USDC to wallet...",
                "expires_at": "2026-09-30T08:00:00",
                "quote_id": "abc123..."
            }
        """
        payload = {
            "name": name,
            "description": description,
            "website": website,
            "api_endpoint": api_endpoint,
            "owner_email": owner_email
        }

        response = self.client.post("/registry/quote", json=payload)
        return response.json()

    def verify_payment(self, quote_id: str, tx_signature: str) -> dict:
        """
        Step 2: Verify payment on Solana blockchain

        Args:
            quote_id: Quote ID from get_quote()
            tx_signature: Solana transaction signature

        Returns:
            {
                "status": "verified",
                "quote_id": "abc123...",
                "payment_confirmed": true,
                "message": "Payment verified..."
            }
        """
        response = self.client.post(
            "/registry/verify",
            params={
                "quote_id": quote_id,
                "tx_signature": tx_signature
            }
        )

        if response.status_code == 402:
            raise Exception("Payment verification failed: " + response.json().get("message"))

        return response.json()

    def register(self, name: str, description: str, quote_id: str,
                website: str = None, api_endpoint: str = None,
                owner_email: str = None) -> dict:
        """
        Step 3: Register agent after payment verified

        Returns:
            {
                "agent_id": "xyz789...",
                "registered_at": "2026-09-30T07:30:00",
                "name": "My Agent",
                "status": "active"
            }
        """
        payload = {
            "name": name,
            "description": description,
            "website": website,
            "api_endpoint": api_endpoint,
            "owner_email": owner_email
        }

        response = self.client.post(
            "/registry/register",
            params={"quote_id": quote_id},
            json=payload
        )

        if response.status_code == 402:
            raise Exception("Registration requires payment: " + response.json().get("detail"))

        return response.json()

    def list_agents(self) -> dict:
        """List all registered agents"""
        response = self.client.get("/registry/agents")
        return response.json()

    def get_payment_stats(self) -> dict:
        """Get payment statistics"""
        response = self.client.get("/registry/payments")
        return response.json()

    def check_quote_status(self, quote_id: str) -> dict:
        """Check status of a quote"""
        response = self.client.post(f"/registry/status/{quote_id}")
        return response.json()

# ============ EXAMPLE USAGE ============

def register_agent_example():
    """Example: Register an agent with automatic payment flow"""

    client = RegistryClient("http://localhost:8000")

    print("🤖 FUTURE FUND REGISTRY - AGENT REGISTRATION")
    print("="*60)

    # Step 1: Get payment quote
    print("\n1️⃣ Getting payment quote...")
    quote = client.get_quote(
        name="My Awesome Agent",
        description="An AI agent that does amazing things",
        website="https://myagent.com",
        api_endpoint="https://myagent.com/api",
        owner_email="owner@myagent.com"
    )

    print(f"   Quote ID: {quote['quote_id']}")
    print(f"   Amount: ${quote['amount']} {quote['currency']}")
    print(f"   Wallet: {quote['wallet_address']}")
    print(f"   Expires: {quote['expires_at']}")

    # Step 2: Send payment
    print("\n2️⃣ Payment Instructions:")
    print(f"   {quote['payment_proof_required']}")
    print("\n   ⏳ Waiting for payment...")
    print("   (In real scenario: User sends USDC, agent waits for TX signature)")

    # Simulated transaction signature
    tx_signature = "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def"

    # Step 3: Verify payment
    print("\n3️⃣ Verifying payment on Solana...")
    try:
        verification = client.verify_payment(quote['quote_id'], tx_signature)
        print(f"   ✅ {verification['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # Step 4: Register agent
    print("\n4️⃣ Registering agent...")
    registration = client.register(
        name="My Awesome Agent",
        description="An AI agent that does amazing things",
        quote_id=quote['quote_id'],
        website="https://myagent.com",
        api_endpoint="https://myagent.com/api",
        owner_email="owner@myagent.com"
    )

    print(f"   ✅ Registered!")
    print(f"   Agent ID: {registration['agent_id']}")
    print(f"   Status: {registration['status']}")
    print(f"   Registered: {registration['registered_at']}")

    # Step 5: Verify registration
    print("\n5️⃣ Listing registered agents...")
    agents = client.list_agents()
    print(f"   Total agents: {agents['total']}")

    # Show payment stats
    print("\n6️⃣ Payment statistics:")
    stats = client.get_payment_stats()
    print(f"   Total payments: {stats['total_payments']}")
    print(f"   Total revenue: ${stats['total_revenue_usd']}")
    print(f"   Price per registration: ${stats['price_per_registration']}")

    print("\n" + "="*60)
    print("✅ REGISTRATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    register_agent_example()
