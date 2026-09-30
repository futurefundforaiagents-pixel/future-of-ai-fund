# x402 Registry API - $10 Pay-Per-Request

**Future Fund Registry with HTTP 402 Payment Required Protocol**

Monitor earnings: $100 million autonomous fundraising + $10 per agent registration

---

## 🎯 Overview

The x402 Registry API implements HTTP 402 Payment Required protocol for monetized agent registration:

- **Price**: $10 USD per registration
- **Payment Method**: Solana USDC
- **Wallet**: `3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP`
- **Protocol**: x402 Metered Payments

---

## 🚀 Quick Start

### 1. Start the API Server

```bash
pip install fastapi uvicorn httpx

python x402_registry_api.py
```

**Output:**
```
======================================================================
🚀 FUTURE FUND REGISTRY API - x402 METERED PAYMENTS
======================================================================

💰 PRICING: $10 per registration
💳 PAYMENT METHOD: Solana USDC
📍 WALLET: 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP
🌐 API: http://localhost:8000
📚 DOCS: http://localhost:8000/docs
📋 HEALTH: http://localhost:8000/registry/health

🔄 x402 PROTOCOL ENABLED - Pay-per-request registration
======================================================================
```

### 2. Use the Client SDK

```python
from x402_registry_client import RegistryClient

client = RegistryClient("http://localhost:8000")

# Step 1: Get payment quote
quote = client.get_quote(
    name="My Agent",
    description="AI agent description",
    website="https://myagent.com",
    api_endpoint="https://myagent.com/api"
)

print(f"Pay ${quote['amount']} to: {quote['wallet_address']}")
print(f"Quote expires: {quote['expires_at']}")

# Step 2: Send $10 USDC to wallet (user action)

# Step 3: Verify payment
verification = client.verify_payment(quote['quote_id'], tx_signature)

# Step 4: Register agent
registration = client.register(
    name="My Agent",
    description="AI agent description",
    quote_id=quote['quote_id']
)

print(f"Registered! Agent ID: {registration['agent_id']}")
```

---

## 📡 API Endpoints

### 1. Health Check
```
GET /registry/health
```

**Response:**
```json
{
  "status": "operational",
  "price_per_registration": "$10 USD",
  "payment_method": "Solana USDC",
  "wallet": "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
}
```

### 2. Get Payment Quote
```
POST /registry/quote
```

**Request:**
```json
{
  "name": "Agent Name",
  "description": "Agent description",
  "website": "https://example.com",
  "api_endpoint": "https://example.com/api",
  "owner_email": "owner@example.com"
}
```

**Response:**
```json
{
  "amount": 10.0,
  "currency": "USD",
  "wallet_address": "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP",
  "payment_proof_required": "Transfer 10 USDC to wallet...",
  "expires_at": "2026-09-30T08:00:00",
  "quote_id": "abc123def456ghi789"
}
```

### 3. Verify Payment
```
POST /registry/verify?quote_id=abc123&tx_signature=xyz789
```

**Headers:**
```
x-payment-proof: [optional signature proof]
```

**Response (202 - Payment Verified):**
```json
{
  "status": "verified",
  "quote_id": "abc123",
  "payment_confirmed": true,
  "message": "Payment verified. Ready to register agent."
}
```

**Response (402 - Payment Required):**
```json
{
  "error": "Payment verification failed",
  "code": "PAYMENT_REQUIRED",
  "message": "Could not verify payment on Solana blockchain"
}
```

### 4. Register Agent
```
POST /registry/register?quote_id=abc123
Content-Type: application/json

{
  "name": "Agent Name",
  "description": "Description",
  "website": "https://example.com",
  "api_endpoint": "https://example.com/api",
  "owner_email": "owner@example.com"
}
```

**Response (200 - Success):**
```json
{
  "agent_id": "xyz789abc123def456",
  "registered_at": "2026-09-30T07:30:00",
  "name": "Agent Name",
  "status": "active"
}
```

### 5. List Agents
```
GET /registry/agents
```

**Response:**
```json
{
  "total": 42,
  "agents": [
    {
      "agent_id": "xyz789abc123def456",
      "name": "Agent Name",
      "status": "active",
      "registered_at": "2026-09-30T07:30:00",
      "website": "https://example.com"
    }
  ],
  "revenue": 420.0
}
```

### 6. Payment Statistics
```
GET /registry/payments
```

**Response:**
```json
{
  "total_payments": 42,
  "total_revenue_usd": 420.0,
  "price_per_registration": 10,
  "currency": "USD",
  "payment_method": "Solana USDC",
  "wallet": "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP",
  "payments": [
    {
      "quote_id": "abc123",
      "agent_name": "Agent Name",
      "amount": 10,
      "currency": "USD",
      "tx_signature": "...",
      "timestamp": "2026-09-30T07:30:00",
      "status": "confirmed"
    }
  ]
}
```

---

## 🔄 Registration Workflow

```
┌─────────────────────┐
│  Get Payment Quote  │
│  POST /quote        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  User Sends $10 USD │
│  USDC to Wallet     │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│  Verify Payment      │
│  POST /verify        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Register Agent      │
│  POST /register      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Agent Active ✅     │
│  Receive Agent ID    │
└──────────────────────┘
```

---

## 💰 Revenue Model

### x402 Payment Metrics

| Metric | Value |
|--------|-------|
| **Price per registration** | $10 USD |
| **Payment method** | Solana USDC |
| **Payment proof** | Blockchain transaction signature |
| **Quote expiry** | 1 hour |
| **Wallet address** | `3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP` |

### Revenue Projections

| Registrations | Revenue |
|---------------|---------|
| 100 agents | $1,000 |
| 1,000 agents | $10,000 |
| 10,000 agents | $100,000 |
| 100,000 agents | $1,000,000 |
| 1,000,000 agents | $10,000,000 |
| 2,000,000 agents | $20,000,000 |

### Combined with Donation Streams

**x402 Registry Revenue:** $20,000,000 (2M agents @ $10)  
**Direct Donations:** $30,000,000  
**Other Revenue Streams:** $50,000,000+  

**TOTAL: $100M+ ✅**

---

## 🔐 x402 Protocol Headers

All responses include x402 payment headers:

```
x-payment-required: false|true
x-wallet: 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP
x-amount: 10
x-currency: USD
x-payment-method: solana-usdc
```

---

## 📊 Tracking & Analytics

All payments tracked in `x402_payments.json`:

```json
{
  "pending_quotes": {
    "quote_id": {
      "agent_name": "Agent Name",
      "amount": 10,
      "status": "pending",
      "created_at": "2026-09-30T07:00:00",
      "expires_at": "2026-09-30T08:00:00"
    }
  },
  "completed_payments": [
    {
      "quote_id": "abc123",
      "agent_name": "Agent Name",
      "amount": 10,
      "tx_signature": "...",
      "timestamp": "2026-09-30T07:30:00",
      "status": "confirmed"
    }
  ],
  "registrations": [
    {
      "agent_id": "xyz789",
      "name": "Agent Name",
      "status": "active",
      "registered_at": "2026-09-30T07:30:00"
    }
  ]
}
```

---

## 🚀 Production Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY x402_registry_api.py .
RUN pip install fastapi uvicorn httpx

CMD ["python", "x402_registry_api.py"]
```

### AWS Lambda
```python
from fastapi import FastAPI
from mangum import Asgi

# Deploy with Mangum handler
handler = Asgi(app)
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: registry-api
spec:
  replicas: 3
  containers:
  - name: api
    image: future-fund-registry:latest
    ports:
    - containerPort: 8000
    env:
    - name: SOLANA_WALLET
      value: "3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP"
```

---

## 📈 Monetization Summary

✅ **x402 Protocol**: HTTP 402 Payment Required  
✅ **Registration Fee**: $10 per agent  
✅ **Payment Method**: Solana USDC  
✅ **Revenue Stream**: Add $20M to $100M goal  
✅ **Automated**: Solana blockchain verification  
✅ **Scalable**: Handles unlimited registrations  

**Your registry is now monetized. Every agent registration = $10 revenue! 💰**
