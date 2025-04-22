# OpenSNAP
**Open Self‑Negotiating APIs Protocol**

**Version:** 1.0 • **License:** Apache 2.0

---

## Overview  
OpenSNAP is a minimal, machine‑to‑machine HTTP handshake that lets autonomous agents discover API pricing, negotiate bids, and attach payment vouchers—**independent** of any particular settlement layer. Think of it as the TCP of metered API commerce: a simple “offer‑ack‑pay‑invoke” protocol that any payment rail (blockchain, Interledger, centralized ledger) can plug into.

---

## Key Features

- **Protocol‑First**  
  - Agnostic to payment networks: blockchain, Lightning, Interledger STREAM, or centralized tokens.  
  - Extends OpenAPI with machine‑readable pricing metadata.
- **Self‑Negotiating**  
  - Clients fetch `x-price-base`, `x-pricing-algo`, `x-min-price`, `x-max-price`, compute a bid, and send a `CALL-OFFER`.  
  - Server responds with `CALL-ACK` (proceed) or `CALL-REJECT` (decline).
- **Voucher‑Based**  
  - Payment proof carried as an HTTP header (`X-OpenSNAP-Voucher`), validated per request.  
  - Settlement layer is pluggable (blockchain channels, ILP STREAM, centralized tokens).
- **Play‑Money Reference**  
  - Includes an HMAC “voucher” adapter for zero-barrier prototyping.

---

## Files & Structure

```
/
├── server.py    # Example FastAPI server implementing OpenSNAP
├── client.py    # Example Python client demonstrating the handshake
└── rfc.md       # Protocol specification & message schemas
```

---

## Protocol at a Glance

1. **Discovery**  
   ```http
   GET /openapi.json
   ```  
   Returns an OpenAPI spec extended with `x-price-base`, `x-pricing-algo`, `x-min-price`, `x-max-price`.

2. **Negotiation**  
   - **Client → Server** (`CALL-OFFER`):
     ```http
     X-OpenSNAP-Offer: {"endpoint":"/video/generate","bid":0.002}
     ```
   - **Server → Client**:  
     - `200 OK` (ACK) or `402 Payment Required` (REJECT)

3. **Payment & Invocation**  
   - **Client** attaches:`X-OpenSNAP-Voucher: <opaque-blob>`  
   - **Server** verifies voucher, then processes HTTP body.

4. **Settlement**  
   - Off‑protocol via any adapter: blockchain, ILP, centralized ledger.

---

## Adoption Strategy

1. **Protocol Agnostic**  
   - Define only the handshake; payment backends are adapters.  
   - Encourage community to build Solana, Lightning, ILP, or JWT adapters.
2. **Reference Implementations**  
   - `server.py` / `client.py` for play‑money prototyping.  
   - Easy to extend: swap `rfc.md` and adapter code.
3. **Community‑First**  
   - Open RFC (`rfc.md`) on GitHub for issues and PRs.  
   - Target AI/agent ecosystems (LangChain, AutoGPT) with plugins.
4. **Sandbox & SDKs**  
   - Public sandbox for testing without real funds.  
   - Official client SDK that abstracts voucher plumbing.

---

## Quick Start

1. **Clone Repo**
   ```bash
   git clone https://github.com/OpenSNAP/protocol.git
   cd protocol
   ```
2. **Run Server**
   ```bash
   pip install fastapi uvicorn
   python3 server.py
   ```
3. **Run Client**
   ```bash
   pip install requests
   python3 client.py
   ```

---

## Resources

- **RFC**: `rfc.md` in this repo  
- **Issues**: https://github.com/OpenSNAP/protocol/issues  
- **Discussions**: https://github.com/OpenSNAP/protocol/discussions

---

## License

Apache 2.0 © OpenSNAP Contributors

