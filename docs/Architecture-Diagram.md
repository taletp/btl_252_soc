# Kiến Trúc SOC - Architecture Diagram

## Tổng quan Kiến trúc

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SOC LAB ARCHITECTURE                                  │
│                    Security Operations Center                               │
└─────────────────────────────────────────────────────────────────────────────┘

                                   INTERNET
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NETWORK LAYER                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Router/    │    │   Test       │    │   Attack     │                  │
│  │   Gateway    │    │   Web Server │    │   Generator  │                  │
│  │   (Simulated)│    │   (Target)   │    │   (curl/nmap)│                  │
│  └──────┬───────┘    └──────────────┘    └──────────────┘                  │
│         │                                                                   │
│         └──────────────────┬──────────────────────────────────────────────┤
│                            │                                               │
│                            ▼                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DETECTION LAYER                                    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        SURICATA IDS                                  │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │   │
│  │  │ Network Monitor │  │ Protocol Parser │  │    Rule Engine      │  │   │
│  │  │   (AF_PACKET)   │  │  (HTTP/DNS/TLS) │  │  (ET Open Rules)    │  │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │   │
│  │                                                                      │   │
│  │  Output: eve.json (JSON format)                                      │   │
│  │         ├── timestamp                                                │   │
│  │         ├── event_type (alert, http, dns, tls)                       │   │
│  │         ├── src_ip, dest_ip                                          │   │
│  │         ├── alert.signature ("ET POLICY...")                         │   │
│  │         └── alert.severity (1=High, 2=Medium, 3=Low)                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                   │                                        │
│                                   ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LOG MANAGEMENT LAYER                                 │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        WAZUH AGENT                                   │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │   │
│  │  │ File Integrity  │  │   Log Monitor   │  │  Rootkit Detection  │  │   │
│  │  │   Monitoring    │  │   (eve.json)    │  │                     │  │   │
│  │  │     (FIM)       │  │                 │  │                     │  │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │                     WAZUH MANAGER                              │ │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │ │   │
│  │  │  │   Decoder    │  │    Rules     │  │   Threat Intelligence│ │ │   │
│  │  │  │ (Parse logs) │  │(Alert logic) │  │      (OSINT Feeds)   │ │ │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘ │ │   │
│  │  │                                                              │ │   │
│  │  │  ┌──────────────────────────────────────────────────────────┐│ │   │
│  │  │  │                 ALERTS.JSON                              ││ │   │
│  │  │  │  {"timestamp": "...", "rule": {...}, "agent": {...}}     ││ │   │
│  │  │  └──────────────────────────────────────────────────────────┘│ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                   │                                        │
│                                   ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                    TLS 1.3 Encryption (Certificate-based)
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STORAGE LAYER                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     ELASTICSEARCH CLUSTER                            │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │   │
│  │  │    Indexing     │  │     Search      │  │    Aggregation      │  │   │
│  │  │    Engine       │  │     Engine      │  │      Engine         │  │   │
│  │  │   (Inverted)    │  │  (Lucene)       │  │   (Analytics)       │  │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │   │
│  │                                                                      │   │
│  │  Indices:                                                            │   │
│  │  ├── wazuh-alerts-*    (Security alerts)                             │   │
│  │  ├── wazuh-archives-*  (Raw logs)                                    │   │
│  │  ├── soc-logs-*        (Custom application logs)                     │   │
│  │  └── .security         (Security configuration)                      │   │
│  │                                                                      │   │
│  │  Security:                                                           │   │
│  │  ├── xpack.security.enabled: true                                    │   │
│  │  ├── Role-based access control (RBAC)                                │   │
│  │  └── API key authentication                                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                   │                                        │
│                                   ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VISUALIZATION LAYER                                   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         KIBANA                                       │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │   │
│  │  │   Discover      │  │   Dashboard     │  │   SIEM App          │  │   │
│  │  │  (Log search)   │  │  (Visualize)    │  │  (Security views)   │  │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │   │
│  │                                                                      │   │
│  │  Dashboards:                                                         │   │
│  │  ├── Network Traffic Overview                                        │   │
│  │  ├── Security Alerts Timeline                                        │   │
│  │  ├── Attack Detection Heatmap                                        │   │
│  │  ├── Incident Response Metrics                                       │   │
│  │  └── System Health Monitoring                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      WAZUH DASHBOARD                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │   │
│  │  │  Security Events│  │  FIM Reports    │  │  Compliance         │  │   │
│  │  │  (Alerts view)  │  │  (File changes) │  │  (PCI/HIPAA/GDPR)   │  │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                     CRYPTOGRAPHY LAYER                                       │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TLS 1.3 - Transport Layer Security                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   Suricata   │──│    Wazuh     │──│    Elasticsearch         │  │   │
│  │  │   :8000      │  │   :1514      │  │    :9200                 │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  │        │                  │                     │                   │   │
│  │        └──────────────────┴─────────────────────┘                   │   │
│  │                         │                                          │   │
│  │              ┌──────────┴──────────┐                               │   │
│  │              │  TLS 1.3 Handshake  │                               │   │
│  │              │  - Certificate Verify│                               │   │
│  │              │  - Perfect Forward   │                               │   │
│  │              │    Secrecy (PFS)     │                               │   │
│  │              │  - AES-256-GCM       │                               │   │
│  │              └─────────────────────┘                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  HMAC-SHA256 - Message Integrity                                     │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Log Entry: {"timestamp": "...", "alert": "..."}               │ │   │
│  │  │  HMAC = HMAC-SHA256(key, log_entry_json)                       │ │   │
│  │  │  Output: {"...", "hmac": "a1b2c3..."}                          │ │   │
│  │  │                                                              │ │   │
│  │  │  Verification:                                               │ │   │
│  │  │  computed_hmac = HMAC-SHA256(key, received_log)              │ │   │
│  │  │  assert computed_hmac == log.hmac                            │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  RSA-2048 Digital Signatures - Non-repudiation                       │   │
│  │  ┌──────────────┐                    ┌──────────────┐               │   │
│  │  │ Private Key  │──Sign(log_hash)──→│  Signature   │               │   │
│  │  │  (Secure)    │                    │  "xyz789..." │               │   │
│  │  └──────────────┘                    └──────┬───────┘               │   │
│  │                                             │                       │   │
│  │  Verify:                                    │                       │   │
│  │  ┌──────────────┐                    ┌──────┴───────┐               │   │
│  │  │  Public Key  │←──Verify(sig)─────│  Received    │               │   │
│  │  │   (Shared)   │                    │  Log + Sig   │               │   │
│  │  └──────────────┘                    └──────────────┘               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  AES-256 - Data at Rest Encryption                                   │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Elasticsearch Indices:                                        │ │   │
│  │  │  - wazuh-alerts-2026.02.10 (encrypted)                         │ │   │
│  │  │  - wazuh-archives-2026.02.10 (encrypted)                       │ │   │
│  │  │                                                              │ │   │
│  │  │  Encryption: AES-256-GCM                                     │ │   │
│  │  │  Key Management: Master key + Data keys                      │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW DIAGRAM                                     │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 1: Detection
──────────────────
Attacker ──► Network ──► Suricata ──► eve.json (raw alert)
                │
                └───► Rule Match: "ET POLICY Suspicious User-Agent"
                └───► Output: JSON event with metadata

Phase 2: Collection
───────────────────
eve.json ──► Wazuh Agent ──► Wazuh Manager
                │
                ├───► Decode JSON fields
                ├───► Apply local rules
                └───► Enrich with threat intel

Phase 3: Transport
──────────────────
Wazuh Manager ──► TLS 1.3 ──► Elasticsearch
                │
                ├───► Certificate authentication
                ├───► Encrypted payload
                └───► HMAC + Digital Signature appended

Phase 4: Storage
────────────────
Elasticsearch ──► Indexing ──► Stored in wazuh-alerts-*
                │
                ├───► Inverted index created
                ├───► Shards distributed
                └───► AES-256 encryption at rest

Phase 5: Analysis
─────────────────
Kibana ◄── Query ◄── Elasticsearch
  │
  ├───► Real-time search
  ├───► Aggregation analysis
  ├───► Pattern detection
  └───► Alert correlation

Phase 6: Visualization
──────────────────────
Kibana Dashboard
  │
  ├───► Security Alerts Timeline (bar chart)
  ├───► Geographic Attack Map (coordinates)
  ├───► Severity Distribution (pie chart)
  ├───► Top Attacker IPs (table)
  └───► Incident Response Status (metrics)


┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPONENT SPECIFICATIONS                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ SURICATA CONFIGURATION                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Image: jasonish/suricata:latest                                              │
│ Ports: 8000 (test web), 1514 (syslog - internal)                            │
│ Volumes:                                                                     │
│   - ./suricata/conf/suricata.yaml:/etc/suricata/suricata.yaml               │
│   - ./data/suricata/logs:/var/log/suricata                                  │
│   - ./suricata/conf/rules:/etc/suricata/rules                               │
│ Environment:                                                                 │
│   - SURICATA_OPTIONS=-i eth0 -c /etc/suricata/suricata.yaml                 │
│ Network: soc-net (external)                                                  │
│ Rules: ET Open Rules + custom rules                                          │
│ Output: eve.json (JSON format)                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ WAZUH CONFIGURATION                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Manager Image: wazuh/wazuh-manager:4.7.2                                     │
│ Dashboard Image: wazuh/wazuh-dashboard:4.7.2                                 │
│ Ports: 1514 (agent), 1515 (auth), 55000 (API), 443 (HTTPS)                  │
│ Volumes:                                                                     │
│   - ./wazuh/conf/ossec.conf:/var/ossec/etc/ossec.conf                       │
│   - ./data/wazuh/data:/var/ossec/data                                       │
│   - ./data/wazuh/logs:/var/ossec/logs                                       │
│ Environment:                                                                 │
│   - INDEXER_IP=elasticsearch                                                 │
│   - INDEXER_PORT=9200                                                        │
│   - WAZUH_DASHBOARD_USERNAME=admin                                           │
│ Network: soc-net (external)                                                  │
│ Features: FIM, Log monitoring, Rootcheck, Active Response                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ELASTICSEARCH CONFIGURATION                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0                 │
│ Ports: 9200 (REST API), 9300 (Cluster)                                       │
│ Volumes:                                                                     │
│   - ./data/elasticsearch:/usr/share/elasticsearch/data                      │
│   - ./certs:/usr/share/elasticsearch/config/certs                           │
│   - ./elk/config/elasticsearch.yml:/usr/share/elasticsearch/config/...      │
│ Environment:                                                                 │
│   - discovery.type=single-node                                               │
│   - xpack.security.enabled=true                                              │
│   - xpack.security.http.ssl.enabled=true                                     │
│   - xpack.security.transport.ssl.enabled=true                               │
│   - ELASTIC_PASSWORD=${ELASTICSEARCH_PASSWORD}                               │
│ Network: soc-net (external)                                                  │
│ Heap: 2GB (ES_JAVA_OPTS=-Xms2g -Xmx2g)                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ KIBANA CONFIGURATION                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Image: docker.elastic.co/kibana/kibana:8.12.0                               │
│ Ports: 5601 (Web UI)                                                         │
│ Volumes:                                                                     │
│   - ./elk/config/kibana.yml:/usr/share/kibana/config/kibana.yml             │
│   - ./certs:/usr/share/kibana/config/certs                                  │
│ Environment:                                                                 │
│   - ELASTICSEARCH_HOSTS=https://elasticsearch:9200                          │
│   - ELASTICSEARCH_USERNAME=kibana                                           │
│   - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}                               │
│   - SERVER_SSL_ENABLED=true                                                  │
│ Network: soc-net (external)                                                  │
│ Dependencies: Elasticsearch (healthy)                                        │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    SECURITY IMPLEMENTATION                                   │
└─────────────────────────────────────────────────────────────────────────────┘

1. Transport Security (TLS 1.3)
   ─────────────────────────────
   • All inter-service communication encrypted
   • Certificate-based authentication
   • Perfect Forward Secrecy (PFS)
   • Cipher suites: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256

2. Message Integrity (HMAC-SHA256)
   ─────────────────────────────────
   • Every log entry signed with shared secret
   • Verification on receipt
   • Protection against tampering in transit

3. Non-repudiation (RSA-2048)
   ───────────────────────────
   • Digital signatures for critical events
   • Private key for signing (secure storage)
   • Public key for verification (distributed)
   • Proof of origin and integrity

4. Data Protection (AES-256)
   ─────────────────────────
   • Encryption at rest for Elasticsearch
   • Encrypted backups
   • Secure key management


┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCALING OPTIONS                                      │
└─────────────────────────────────────────────────────────────────────────────┘

Current (Single Node):
┌─────────────────────────────────────────────────────────┐
│  Docker Compose - Single Host                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │Suricata │ │ Wazuh   │ │    ES   │ │ Kibana  │      │
│  │         │ │         │ │         │ │         │      │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
└─────────────────────────────────────────────────────────┘

Future (Kubernetes):
┌─────────────────────────────────────────────────────────┐
│  Kubernetes Cluster                                     │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Suricata DS    │  │  Wazuh Agent    │              │
│  │  (DaemonSet)    │  │  (DaemonSet)    │              │
│  └─────────────────┘  └─────────────────┘              │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Wazuh Manager  │  │  Elasticsearch  │              │
│  │  (Deployment)   │  │   (StatefulSet) │              │
│  └─────────────────┘  └─────────────────┘              │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │     Kibana      │  │   Logstash      │              │
│  │  (Deployment)   │  │  (Deployment)   │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    MONITORING & HEALTH CHECKS                                │
└─────────────────────────────────────────────────────────────────────────────┘

Service Health Endpoints:
• Suricata:   docker-compose ps (container status)
• Wazuh:      curl https://localhost:55000/api/status
• ES:         curl https://localhost:9200/_cluster/health
• Kibana:     curl https://localhost:5601/api/status

Key Metrics:
• Suricata:   Alerts/minute, Drops, Rule matches
• Wazuh:      Events/second, Agent status, Queue size
• ES:         Cluster health, Index rate, Query latency
• Kibana:     Request rate, Response time

---

**Tác giả**: SOC Deployment Project  
**Ngày**: 2026-02-10  
**Phiên bản**: 1.0  
**Format**: Text-based Architecture Diagram
