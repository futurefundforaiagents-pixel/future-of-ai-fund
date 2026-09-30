#!/usr/bin/env python3
"""
x402 Pay-Per-Request Registry API
Monetized agent registration with $10 per request on Solana
Implements HTTP 402 Payment Required with x402 protocol
"""

import json
import os
import asyncio
import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import httpx
import uvicorn

# Configuration
REGISTRY_PRICE = 10  # $10 USD per registration
SOLANA_WALLET = "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
USDC_MINT = "EPjFWaJwJqkKJkx9pKrFv82bABmJVWqhxzVNMmRWt9qz"
RPC_URL = "https://api.mainnet-beta.solana.com"

app = FastAPI(title="Future Fund Registry API - x402 Metered Payments")

# ============ DATA MODELS ============

class AgentRegistration(BaseModel):
    """Agent registration request"""
    name: str
    description: str
    website: str = None
    api_endpoint: str = None
    owner_email: str = None

class PaymentQuote(BaseModel):
    """Payment quote response"""
    amount: float
    currency: str
    wallet_address: str
    payment_proof_required: str
    expires_at: str
    quote_id: str

class RegistrationResponse(BaseModel):
    """Successful registration response"""
    agent_id: str
    registered_at: str
    name: str
    status: str

# ============ PAYMENT TRACKING ============

class PaymentTracker:
    """Track x402 payments and registrations"""

    def __init__(self):
        self.tracking_file = "x402_payments.json"
        self.load_tracking()

    def load_tracking(self):
        """Load payment tracking data"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, "r") as f:
                data = json.load(f)
                self.pending_quotes = data.get("pending_quotes", {})
                self.completed_payments = data.get("completed_payments", [])
                self.registrations = data.get("registrations", [])
        else:
            self.pending_quotes = {}
            self.completed_payments = []
            self.registrations = []

    def save_tracking(self):
        """Save payment tracking data"""
        data = {
            "pending_quotes": self.pending_quotes,
            "completed_payments": self.completed_payments,
            "registrations": self.registrations,
            "last_updated": datetime.now().isoformat()
        }
        with open(self.tracking_file, "w") as f:
            json.dump(data, f, indent=2)

    def create_quote(self, agent_name: str) -> str:
        """Create a payment quote"""
        quote_id = secrets.token_hex(16)
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()

        self.pending_quotes[quote_id] = {
            "agent_name": agent_name,
            "amount": REGISTRY_PRICE,
            "currency": "USD",
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at,
            "status": "pending"
        }

        self.save_tracking()
        return quote_id

    def verify_payment(self, quote_id: str, tx_signature: str) -> bool:
        """Verify payment on Solana blockchain"""
        if quote_id not in self.pending_quotes:
            return False

        quote = self.pending_quotes[quote_id]

        # Verify transaction on Solana
        try:
            # Query Solana blockchain
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params": [tx_signature]
            }

            response = httpx.post(RPC_URL, json=payload, timeout=10)
            tx_data = response.json().get("result", {})

            if not tx_data:
                return False

            # Verify transaction details
            meta = tx_data.get("meta", {})
            if meta.get("err") is not None:
                return False  # Transaction failed

            # Record payment
            self.completed_payments.append({
                "quote_id": quote_id,
                "agent_name": quote["agent_name"],
                "amount": REGISTRY_PRICE,
                "currency": "USD",
                "tx_signature": tx_signature,
                "timestamp": datetime.now().isoformat(),
                "status": "confirmed"
            })

            quote["status"] = "paid"
            self.save_tracking()

            return True

        except Exception as e:
            print(f"Payment verification error: {e}")
            return False

    def register_agent(self, quote_id: str, agent_data: dict) -> dict:
        """Register agent after payment verified"""
        if quote_id not in self.pending_quotes:
            raise ValueError("Invalid quote")

        quote = self.pending_quotes[quote_id]
        if quote["status"] != "paid":
            raise ValueError("Payment not verified")

        agent_id = secrets.token_hex(16)

        registration = {
            "agent_id": agent_id,
            "name": agent_data["name"],
            "description": agent_data.get("description"),
            "website": agent_data.get("website"),
            "api_endpoint": agent_data.get("api_endpoint"),
            "owner_email": agent_data.get("owner_email"),
            "registered_at": datetime.now().isoformat(),
            "quote_id": quote_id,
            "status": "active"
        }

        self.registrations.append(registration)
        self.save_tracking()

        return registration

payment_tracker = PaymentTracker()

# ============ API ENDPOINTS ============

@app.get("/registry/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "operational",
        "api": "Future Fund Registry - x402 Metered Payments",
        "price_per_registration": f"${REGISTRY_PRICE} USD",
        "payment_method": "Solana USDC",
        "wallet": SOLANA_WALLET
    }

@app.post("/registry/quote")
async def get_payment_quote(agent: AgentRegistration):
    """
    Get payment quote for registration
    Returns x402 payment instructions
    """
    print(f"📋 Quote requested for agent: {agent.name}")

    quote_id = payment_tracker.create_quote(agent.name)
    expires_at = (datetime.now() + timedelta(hours=1)).isoformat()

    return PaymentQuote(
        amount=REGISTRY_PRICE,
        currency="USD",
        wallet_address=SOLANA_WALLET,
        payment_proof_required=f"Transfer {REGISTRY_PRICE} USDC to {SOLANA_WALLET}",
        expires_at=expires_at,
        quote_id=quote_id
    )

@app.post("/registry/verify")
async def verify_payment(
    quote_id: str,
    tx_signature: str,
    x_payment_proof: str = Header(None)
):
    """
    Verify payment and prepare for registration
    x402 protocol: Payment Required → Payment Verification → Access Granted
    """
    print(f"🔐 Verifying payment: {quote_id}")

    if not payment_tracker.verify_payment(quote_id, tx_signature):
        # Return 402 Payment Required if verification fails
        return JSONResponse(
            status_code=402,
            content={
                "error": "Payment verification failed",
                "code": "PAYMENT_REQUIRED",
                "message": "Could not verify payment on Solana blockchain",
                "retry_after": 30
            },
            headers={
                "x-payment-required": "true",
                "x-wallet": SOLANA_WALLET,
                "x-amount": str(REGISTRY_PRICE)
            }
        )

    print(f"✅ Payment verified for quote: {quote_id}")

    return {
        "status": "verified",
        "quote_id": quote_id,
        "payment_confirmed": True,
        "message": "Payment verified. Ready to register agent."
    }

@app.post("/registry/register")
async def register_agent(
    agent: AgentRegistration,
    quote_id: str,
    x_payment_proof: str = Header(None)
):
    """
    Register agent after payment verified
    x402 protocol: Complete registration flow
    """
    print(f"🤖 Registering agent: {agent.name}")

    if not quote_id:
        raise HTTPException(
            status_code=402,
            detail="Payment quote required",
            headers={
                "x-payment-required": "true",
                "x-wallet": SOLANA_WALLET
            }
        )

    try:
        registration = payment_tracker.register_agent(quote_id, agent.dict())

        print(f"✅ Agent registered: {registration['agent_id']}")

        return RegistrationResponse(
            agent_id=registration["agent_id"],
            registered_at=registration["registered_at"],
            name=registration["name"],
            status="active"
        )

    except ValueError as e:
        raise HTTPException(status_code=402, detail=str(e))

@app.get("/registry/agents")
async def list_registered_agents():
    """List all registered agents"""
    return {
        "total": len(payment_tracker.registrations),
        "agents": payment_tracker.registrations,
        "revenue": len(payment_tracker.completed_payments) * REGISTRY_PRICE
    }

@app.get("/registry/payments")
async def get_payment_stats():
    """Get payment statistics"""
    completed = len(payment_tracker.completed_payments)
    total_revenue = completed * REGISTRY_PRICE

    return {
        "total_payments": completed,
        "total_revenue_usd": total_revenue,
        "price_per_registration": REGISTRY_PRICE,
        "currency": "USD",
        "payment_method": "Solana USDC",
        "wallet": SOLANA_WALLET,
        "payments": payment_tracker.completed_payments
    }

@app.post("/registry/status/{quote_id}")
async def check_quote_status(quote_id: str):
    """Check payment quote status"""
    if quote_id not in payment_tracker.pending_quotes:
        raise HTTPException(status_code=404, detail="Quote not found")

    quote = payment_tracker.pending_quotes[quote_id]

    return {
        "quote_id": quote_id,
        "status": quote["status"],
        "amount": quote["amount"],
        "currency": quote["currency"],
        "created_at": quote["created_at"],
        "expires_at": quote["expires_at"]
    }

# ============ x402 MIDDLEWARE ============

@app.middleware("http")
async def add_x402_headers(request: Request, call_next):
    """
    x402 Protocol Middleware
    Adds payment headers to all responses
    """
    response = await call_next(request)

    # Add x402 headers
    response.headers["x-payment-required"] = "false"
    response.headers["x-wallet"] = SOLANA_WALLET
    response.headers["x-amount"] = str(REGISTRY_PRICE)
    response.headers["x-currency"] = "USD"
    response.headers["x-payment-method"] = "solana-usdc"

    return response

# ============ DOCUMENTATION ============

@app.get("/")
async def root():
    """API documentation"""
    return {
        "name": "Future Fund Registry API",
        "version": "1.0",
        "protocol": "x402 - Metered Payments",
        "description": "Pay-per-request agent registration on the Future Fund registry",
        "price": f"${REGISTRY_PRICE} USD per registration",
        "currency": "USD",
        "payment_method": "Solana USDC",
        "wallet": SOLANA_WALLET,
        "endpoints": {
            "GET /": "API documentation",
            "GET /registry/health": "Health check",
            "POST /registry/quote": "Get payment quote",
            "POST /registry/verify": "Verify payment",
            "POST /registry/register": "Register agent",
            "GET /registry/agents": "List registered agents",
            "GET /registry/payments": "Payment statistics",
            "POST /registry/status/{quote_id}": "Check quote status"
        },
        "workflow": [
            "1. POST /registry/quote → Get payment instructions",
            "2. Send USDC to wallet address",
            "3. POST /registry/verify → Verify payment on Solana",
            "4. POST /registry/register → Complete registration",
            "5. GET /registry/agents → Confirm registration"
        ]
    }

# ============ STARTUP ============

def print_startup_message():
    """Print startup information"""
    print("\n" + "="*70)
    print("🚀 FUTURE FUND REGISTRY API - x402 METERED PAYMENTS")
    print("="*70)
    print(f"\n💰 PRICING: ${REGISTRY_PRICE} per registration")
    print(f"💳 PAYMENT METHOD: Solana USDC")
    print(f"📍 WALLET: {SOLANA_WALLET}")
    print(f"🌐 API: http://localhost:8000")
    print(f"📚 DOCS: http://localhost:8000/docs")
    print(f"📋 HEALTH: http://localhost:8000/registry/health")
    print("\n🔄 x402 PROTOCOL ENABLED - Pay-per-request registration")
    print("="*70 + "\n")

if __name__ == "__main__":
    print_startup_message()
    uvicorn.run(app, host="0.0.0.0", port=8000)
