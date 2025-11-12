# BankSight-AI Production Deployment Guide

**Target:** 100 Concurrent Users | **Platform:** Alibaba Cloud | **Version:** 1.0.0

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Infrastructure Requirements](#infrastructure-requirements)
4. [Deployment Configuration](#deployment-configuration)
5. [Scaling Strategy](#scaling-strategy)
6. [Security & Compliance](#security--compliance)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Disaster Recovery](#disaster-recovery)

---

## 1. Executive Summary

### Project Overview

BankSight-AI is an AI-powered banking assistant using **open-source LLMs** deployed on **Alibaba Cloud** infrastructure. This deployment supports **100 concurrent users** with high availability and horizontal scaling capabilities.

### Key Specifications

| Component | Specification |
|-----------|--------------|
| **Target Users** | 100 concurrent (500+ registered) |
| **LLM Model** | Mistral-7B-Instruct-v0.3 (Open Source) |
| **Embedding Model** | all-MiniLM-L6-v2 |
| **Vector Database** | ChromaDB (Persistent) |
| **Backend** | FastAPI (Python 3.10+) |
| **Frontend** | Streamlit |
| **Infrastructure** | Alibaba Cloud ECS + GPU Instances |

### Expected Performance

- **Response Time:** 3-5 seconds per query (with GPU)
- **Throughput:** 20-30 queries/second (with load balancing)
- **Uptime SLA:** 99.5% (43.8 hours downtime/year)
- **Concurrent Users:** 100 simultaneous connections

---

## 2. Architecture Overview

### High-Level Architecture

```
                                    ┌─────────────────┐
                                    │   Alibaba SLB   │
                                    │ (Load Balancer) │
                                    └────────┬────────┘
                                             │
                          ┌──────────────────┼──────────────────┐
                          │                  │                  │
                    ┌─────▼─────┐      ┌────▼─────┐     ┌─────▼─────┐
                    │  ECS-GPU  │      │ ECS-GPU  │     │ ECS-GPU   │
                    │ Instance 1│      │Instance 2│     │ Instance 3│
                    │           │      │          │     │           │
                    │ Backend + │      │ Backend +│     │ Backend + │
                    │    LLM    │      │   LLM    │     │   LLM     │
                    └─────┬─────┘      └────┬─────┘     └─────┬─────┘
                          │                  │                  │
                          └──────────────────┼──────────────────┘
                                             │
                                    ┌────────▼────────┐
                                    │   ECS Standard  │
                                    │                 │
                                    │  ChromaDB +     │
                                    │  Shared Storage │
                                    └─────────────────┘
                                             │
                                    ┌────────▼────────┐
                                    │   OSS Storage   │
                                    │ (Model Cache +  │
                                    │  Documents)     │
                                    └─────────────────┘
```

### Component Breakdown

#### Frontend Tier
- **Deployment:** Alibaba Cloud CDN + OSS for static assets
- **Technology:** Streamlit (compiled to static assets) or Nginx reverse proxy
- **Scaling:** CDN handles unlimited users for static content

#### Application Tier
- **Deployment:** 3x GPU-enabled ECS instances (gn6v-c8g1.2xlarge)
- **Load Balancing:** Alibaba SLB (Server Load Balancer)
- **Technology:** FastAPI with Gunicorn/Uvicorn workers
- **Auto-scaling:** Based on CPU/GPU utilization (60-80% threshold)

#### AI/ML Tier
- **Model Hosting:** Co-located with application tier
- **GPU:** NVIDIA T4 (16GB VRAM) per instance
- **Model Loading:** Shared model cache via NFS/OSS
- **Caching:** Redis for response caching

#### Data Tier
- **Vector Database:** ChromaDB on dedicated ECS instance
- **Persistent Storage:** Alibaba Cloud Disk (SSD)
- **Backup:** Daily snapshots to OSS

---

## 3. Infrastructure Requirements

### Recommended Configuration (100 Concurrent Users)

#### Option 1: GPU Instances (Recommended for Performance)

| Component | Instance Type | Specs | Quantity | Purpose |
|-----------|--------------|-------|----------|---------|
| **Application + LLM** | ecs.gn6v-c8g1.2xlarge | 8 vCPU, 32GB RAM, 1x T4 GPU (16GB) | 3 | Backend API + Model inference |
| **Vector DB** | ecs.g6.xlarge | 4 vCPU, 16GB RAM, 100GB SSD | 1 | ChromaDB persistent storage |
| **Load Balancer** | Alibaba SLB | Standard Edition | 1 | Traffic distribution |
| **Object Storage** | OSS | Standard | 500GB | Models, documents, backups |
| **CDN** | Alibaba CDN | Standard | 1TB/month | Frontend assets |

**Total Infrastructure:**
- 3x GPU instances for horizontal scaling
- 1x Standard instance for vector database
- Load balancer for distribution
- Shared storage for models and data

#### Option 2: CPU-Only Instances (Budget Option)

| Component | Instance Type | Specs | Quantity | Purpose |
|-----------|--------------|-------|----------|---------|
| **Application + LLM** | ecs.g6.4xlarge | 16 vCPU, 64GB RAM | 6 | Backend API + Model inference (slower) |
| **Vector DB** | ecs.g6.xlarge | 4 vCPU, 16GB RAM | 1 | ChromaDB |
| **Load Balancer** | SLB Standard | - | 1 | Traffic distribution |
| **Object Storage** | OSS Standard | 500GB | 1 | Storage |

**Note:** CPU-only option requires 2x more instances due to slower inference (15-30s vs 3-5s per query).

### Network Configuration

- **Bandwidth:** 100 Mbps per instance (burstable to 200 Mbps)
- **VPC:** Private network for backend instances
- **Security Groups:** Strict firewall rules (allow only necessary ports)
- **Public IPs:** Only for SLB, backend instances in private subnet

### Storage Requirements

| Type | Size | Purpose |
|------|------|---------|
| **Model Cache** | 50GB | Pre-downloaded LLM models (Mistral-7B: ~14GB) |
| **Vector DB** | 100GB | Document embeddings (grows with documents) |
| **Application Logs** | 50GB | Rotating logs (7-day retention) |
| **Backups** | 200GB | Daily snapshots |
| **Total** | **400GB** | Initial deployment |

---

## 4. Deployment Configuration

### Docker Deployment (Recommended)

#### Docker Compose Configuration

```yaml
version: '3.8'

services:
  backend:
    image: banksight-ai/backend:latest
    deploy:
      replicas: 3
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.3
      - DEVICE=cuda
      - WORKERS=4
      - VECTOR_DB_HOST=vectordb
    volumes:
      - /mnt/oss/models:/app/models:ro
      - /mnt/oss/documents:/app/data/documents:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - banksight-network

  vectordb:
    image: banksight-ai/chromadb:latest
    volumes:
      - chromadb-data:/chroma/data
    networks:
      - banksight-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend
    networks:
      - banksight-network

volumes:
  chromadb-data:

networks:
  banksight-network:
    driver: bridge
```

### Environment Configuration

```bash
# Production Environment Variables
export LLM_MODEL="mistralai/Mistral-7B-Instruct-v0.3"
export DEVICE="cuda"
export MAX_WORKERS=4
export VECTOR_DB_HOST="chromadb.internal"
export CACHE_DIR="/mnt/oss/models"
export LOG_LEVEL="INFO"
export ENABLE_METRICS=true
export PROMETHEUS_PORT=9090
```

### Nginx Load Balancing

```nginx
upstream backend_servers {
    least_conn;  # Use least connections algorithm

    server backend-1.internal:8000 max_fails=3 fail_timeout=30s;
    server backend-2.internal:8000 max_fails=3 fail_timeout=30s;
    server backend-3.internal:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name banksight.example.com;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Timeouts for LLM responses
        proxy_connect_timeout 60s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    location /health {
        access_log off;
        proxy_pass http://backend_servers/health;
    }
}
```

---

## 5. Scaling Strategy

### Horizontal Scaling

#### Auto-Scaling Rules

```yaml
# Alibaba Cloud ESS (Elastic Scaling Service)
scaling_group:
  min_instances: 2
  max_instances: 10
  desired_instances: 3

  scaling_rules:
    - name: "Scale Up on High GPU Usage"
      metric: gpu_utilization
      threshold: 75%
      duration: 5 minutes
      action: add_1_instance

    - name: "Scale Up on High Request Rate"
      metric: request_count
      threshold: 500 req/min
      duration: 3 minutes
      action: add_2_instances

    - name: "Scale Down on Low Usage"
      metric: gpu_utilization
      threshold: 30%
      duration: 15 minutes
      action: remove_1_instance
```

### Vertical Scaling

| Users | Instance Type | GPU | vCPU | RAM | Cost Impact |
|-------|--------------|-----|------|-----|-------------|
| 0-50 | gn6v-c8g1.xlarge | 1x T4 (16GB) | 4 | 16GB | Baseline |
| 50-100 | gn6v-c8g1.2xlarge | 1x T4 (16GB) | 8 | 32GB | +50% |
| 100-200 | gn6v-c10g1.4xlarge | 1x V100 (32GB) | 16 | 64GB | +200% |

### Caching Strategy

```python
# Redis caching for frequent queries
from functools import lru_cache
import redis

redis_client = redis.Redis(host='redis.internal', port=6379)

@lru_cache(maxsize=1000)
def get_cached_response(query_hash: str):
    """Cache responses for 1 hour"""
    cached = redis_client.get(f"response:{query_hash}")
    if cached:
        return cached
    return None

def cache_response(query_hash: str, response: str, ttl=3600):
    """Store response in cache"""
    redis_client.setex(f"response:{query_hash}", ttl, response)
```

**Cache Hit Rate Target:** 30-40% (reduces GPU load by 30-40%)

---

## 6. Security & Compliance

### Security Measures

#### 1. Network Security

- **VPC Isolation:** Backend instances in private subnet
- **Security Groups:** Whitelist only necessary ports
  - Port 443: HTTPS (public)
  - Port 8000: Backend API (internal only)
  - Port 6379: Redis (internal only)
- **DDoS Protection:** Alibaba Anti-DDoS Basic (included)

#### 2. Data Encryption

- **In Transit:** TLS 1.3 for all HTTPS connections
- **At Rest:** Alibaba Cloud Disk encryption enabled
- **Secrets Management:** Alibaba KMS for API keys

#### 3. Access Control

```yaml
# IAM Policies
Policies:
  - Name: "BankSight-Backend-Policy"
    Permissions:
      - oss:GetObject  # Read models from OSS
      - oss:PutObject  # Upload documents
      - ecs:DescribeInstances  # Auto-scaling
      - slb:DescribeLoadBalancers  # Health checks
```

#### 4. Compliance Considerations

For banking applications, ensure compliance with:
- **PCI-DSS:** If handling payment data
- **GDPR/CCPA:** For user data protection
- **SOC 2:** For security audits
- **ISO 27001:** Information security

**Note:** This demo uses dummy data. For production, implement:
- Data anonymization
- Audit logging
- User consent management
- Right to be forgotten (GDPR)

### Monitoring & Logging

```yaml
# Prometheus Metrics
metrics:
  - llm_inference_duration_seconds
  - gpu_utilization_percent
  - vector_db_query_duration_seconds
  - http_requests_total
  - http_request_duration_seconds

# Log Aggregation (Alibaba SLS)
log_sources:
  - application_logs (JSON format)
  - nginx_access_logs
  - nginx_error_logs
  - gpu_metrics

# Alerting Rules
alerts:
  - name: "High GPU Temperature"
    condition: gpu_temp > 80°C
    action: notify_ops_team

  - name: "Response Time Degradation"
    condition: p95_latency > 10s
    action: auto_scale_up
```

---

## 7. Monitoring & Maintenance

### Health Checks

```python
# Backend Health Check Endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "checks": {
            "llm_loaded": llm_client.is_loaded(),
            "gpu_available": torch.cuda.is_available(),
            "gpu_memory_free": f"{torch.cuda.mem_get_info()[0] / 1024**3:.1f} GB",
            "vector_db_count": vector_store.get_count(),
            "uptime_seconds": time.time() - start_time
        }
    }
```

### Maintenance Schedule

| Task | Frequency | Downtime | Description |
|------|-----------|----------|-------------|
| **Model Updates** | Monthly | 5 min | Deploy new model versions |
| **Security Patches** | Weekly | 2 min | OS and dependency updates |
| **Database Backup** | Daily | 0 min | Automated snapshots |
| **Log Rotation** | Daily | 0 min | Compress and archive logs |
| **Performance Tuning** | Quarterly | 10 min | Optimize configurations |

### Backup Strategy

```bash
# Daily Backup Script
#!/bin/bash
BACKUP_DIR="/mnt/oss/backups/$(date +%Y%m%d)"

# Backup Vector Database
tar -czf $BACKUP_DIR/vectordb.tar.gz /data/vector_db/

# Backup Application Configs
tar -czf $BACKUP_DIR/configs.tar.gz /app/config.yaml

# Upload to OSS
aliyun oss cp $BACKUP_DIR oss://banksight-backups/$(date +%Y%m%d)/ --recursive

# Retain 30 days of backups
find /mnt/oss/backups/ -type d -mtime +30 -exec rm -rf {} \;
```

---

## 8. Disaster Recovery

### Recovery Time Objective (RTO) & Recovery Point Objective (RPO)

| Scenario | RTO | RPO | Recovery Procedure |
|----------|-----|-----|-------------------|
| **Single Instance Failure** | 2 min | 0 min | Auto-scaling replaces instance |
| **Database Corruption** | 30 min | 24 hours | Restore from daily backup |
| **Region Outage** | 4 hours | 24 hours | Failover to secondary region |
| **Complete Data Loss** | 8 hours | 24 hours | Rebuild from OSS backups |

### Disaster Recovery Procedures

#### 1. Instance Failure

```bash
# Automated by Alibaba ESS
# - Health check fails → Instance terminated
# - New instance launched automatically
# - Rejoins load balancer pool
```

#### 2. Database Recovery

```bash
# Restore ChromaDB from backup
1. Stop vector database service
2. Download latest backup from OSS
3. Extract to /data/vector_db/
4. Restart service
5. Verify data integrity
```

#### 3. Multi-Region Failover

```
Primary Region (Shanghai): Main production
Secondary Region (Beijing): Hot standby
   - Replication lag: 5 minutes
   - Automatic DNS failover via Alibaba Cloud DNS
```

---

## 📝 Deployment Checklist

### Pre-Deployment

- [ ] Provision all Alibaba Cloud resources
- [ ] Configure VPC and security groups
- [ ] Set up OSS buckets for models and backups
- [ ] Deploy ChromaDB and verify persistence
- [ ] Download and cache LLM models to OSS
- [ ] Configure SSL certificates (Let's Encrypt)
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure log aggregation (Alibaba SLS)

### Deployment

- [ ] Build and push Docker images to Alibaba ACR
- [ ] Deploy backend services (3 instances)
- [ ] Configure load balancer health checks
- [ ] Deploy Nginx reverse proxy
- [ ] Verify GPU detection on all instances
- [ ] Load test with 100 concurrent users
- [ ] Verify auto-scaling triggers

### Post-Deployment

- [ ] Monitor logs for errors (first 24 hours)
- [ ] Verify backup jobs running successfully
- [ ] Test disaster recovery procedures
- [ ] Document incident response procedures
- [ ] Train operations team
- [ ] Set up on-call rotation

---

## 📞 Support & Escalation

### Operational Contacts

| Role | Responsibility | Contact |
|------|---------------|---------|
| **DevOps Lead** | Infrastructure, deployment | devops@example.com |
| **Backend Engineer** | API, model serving | backend@example.com |
| **DBA** | Vector database, backups | dba@example.com |
| **Security Engineer** | Access control, compliance | security@example.com |

### Escalation Path

1. **Level 1 (Monitoring Alert)** → On-call engineer investigates
2. **Level 2 (Service Degradation)** → Escalate to team lead
3. **Level 3 (Service Outage)** → Page senior engineering + management

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-11
**Next Review:** 2025-12-11
**Owner:** DevOps Team
