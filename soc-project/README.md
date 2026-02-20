# SOC Project — Docker Deployment

This directory contains the Docker Compose stack and all service configuration files.

**For installation instructions, usage guide, and scripts reference, see the root README:**

👉 [../README.md](../README.md)

---

## Quick Start

```bash
# From this directory (soc-project/)
docker network create soc-net
cp .env.example .env   # then edit .env and change all passwords
docker-compose up -d
docker-compose ps      # wait ~3 minutes for first start
```

Access Kibana at <http://localhost:5601>
