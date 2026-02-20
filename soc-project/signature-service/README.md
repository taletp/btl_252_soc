# Log Signature Service

## Overview
Flask-based microservice for HMAC-SHA256 and RSA-2048 digital signature of log entries.

## Features
- RSA-2048 key pair generation and management
- HMAC-SHA256 for message authentication
- RSA-PSS-SHA256 digital signatures
- Suricata EVE event specific signing
- Public key retrieval for external verification

## API Endpoints

### Health Check
```
GET /health
```

### Sign Log Entry
```
POST /sign
Content-Type: application/json

{
  "event_type": "alert",
  "src_ip": "192.168.1.1",
  "dest_ip": "10.0.0.1"
}
```

### Verify Log Entry
```
POST /verify
Content-Type: application/json

{
  "log_entry": {...},
  "signatures": {
    "hmac_sha256": "...",
    "rsa_signature": "..."
  }
}
```

### Get Public Key
```
GET /public-key
```

### Sign Suricata Event
```
POST /sign/suricata
Content-Type: application/json
```

## Environment Variables
- `HMAC_SECRET`: Secret key for HMAC generation
- `KEYS_DIR`: Directory to store RSA keys

## Docker Integration
Service runs on port 5000 within the soc-net network.
