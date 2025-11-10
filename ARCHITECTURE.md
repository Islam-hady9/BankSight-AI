# BankSight-AI System Architecture

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Technology Decisions](#technology-decisions)
6. [Scalability & Performance](#scalability--performance)
7. [Security Architecture](#security-architecture)

---

## System Overview

BankSight-AI is a microservices-based intelligent banking assistant that combines:
- **RAG (Retrieval-Augmented Generation)** for knowledge retrieval from documents
- **MCP (Model Context Protocol)** for executing banking actions
- **LLM Orchestration** for intelligent conversation and decision-making

### Architecture Principles
- **Modularity:** Loosely coupled components
- **Scalability:** Horizontal scaling capabilities
- **Security-First:** Defense in depth
- **Observability:** Comprehensive monitoring and logging
- **Resilience:** Fault tolerance and graceful degradation

---

## Architecture Diagram

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATIONS                          │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Web App    │  │  Mobile App  │  │  API Client  │             │
│  │  (React)     │  │ (React       │  │              │             │
│  │              │  │  Native)     │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                  │                  │                     │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         API GATEWAY                                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  - Rate Limiting                                            │   │
│  │  - Authentication/Authorization                             │   │
│  │  - Request Routing                                          │   │
│  │  - SSL/TLS Termination                                      │   │
│  │  - API Versioning                                           │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Chat       │  │   Document       │  │   Action         │
│   Service    │  │   Service        │  │   Service        │
│              │  │                  │  │                  │
│  FastAPI     │  │  FastAPI         │  │  FastAPI         │
└──────────────┘  └──────────────────┘  └──────────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      AI AGENT ORCHESTRATOR                           │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     Query Router                              │  │
│  │                                                               │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                │  │
│  │  │ Intent Classifier│  │ Entity Extractor │                │  │
│  │  └──────────────────┘  └──────────────────┘                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                             │                                       │
│          ┌──────────────────┼──────────────────┐                   │
│          │                  │                  │                   │
│    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐             │
│    │   RAG     │     │    MCP    │     │Conversation│             │
│    │  Handler  │     │  Handler  │     │  Handler   │             │
│    └───────────┘     └───────────┘     └────────────┘             │
│          │                  │                  │                   │
└──────────┼──────────────────┼──────────────────┼───────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   RAG SYSTEM     │  │   MCP ENGINE     │  │  LLM SERVICE     │
│                  │  │                  │  │                  │
│ ┌──────────────┐ │  │ ┌──────────────┐ │  │ ┌──────────────┐ │
│ │  Document    │ │  │ │ Tool Registry│ │  │ │Claude API    │ │
│ │  Ingestion   │ │  │ │              │ │  │ │Integration   │ │
│ └──────────────┘ │  │ └──────────────┘ │  │ └──────────────┘ │
│ ┌──────────────┐ │  │ ┌──────────────┐ │  │ ┌──────────────┐ │
│ │  Chunking    │ │  │ │ Action       │ │  │ │Context       │ │
│ │  & Embedding │ │  │ │ Executor     │ │  │ │Manager       │ │
│ └──────────────┘ │  │ └──────────────┘ │  │ └──────────────┘ │
│ ┌──────────────┐ │  │ ┌──────────────┐ │  │                  │
│ │  Vector      │ │  │ │ Validator    │ │  │                  │
│ │  Search      │ │  │ │              │ │  │                  │
│ └──────────────┘ │  │ └──────────────┘ │  │                  │
│ ┌──────────────┐ │  │                  │  │                  │
│ │  Re-ranker   │ │  │                  │  │                  │
│ └──────────────┘ │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         │                      │
         ▼                      ▼
┌──────────────────┐  ┌──────────────────┐
│   VECTOR DB      │  │  BANKING BACKEND │
│                  │  │                  │
│  - Pinecone      │  │  ┌────────────┐  │
│  - Qdrant        │  │  │ Account    │  │
│  - Weaviate      │  │  │ Service    │  │
│                  │  │  └────────────┘  │
└──────────────────┘  │  ┌────────────┐  │
                      │  │Transaction │  │
┌──────────────────┐  │  │ Service    │  │
│  DOCUMENT STORE  │  │  └────────────┘  │
│                  │  │  ┌────────────┐  │
│  - MongoDB       │  │  │ Payment    │  │
│  - S3/MinIO      │  │  │ Service    │  │
│                  │  │  └────────────┘  │
└──────────────────┘  └──────────────────┘
         │                      │
         ▼                      ▼
┌──────────────────┐  ┌──────────────────┐
│  POSTGRESQL      │  │  EXTERNAL APIs   │
│                  │  │                  │
│  - Users         │  │  - Plaid         │
│  - Sessions      │  │  - Stripe        │
│  - Audit Logs    │  │  - Credit Bureau │
│  - Metadata      │  │  - KYC Services  │
└──────────────────┘  └──────────────────┘
```

---

## Component Details

### 1. API Gateway

**Purpose:** Single entry point for all client requests

**Responsibilities:**
- Request authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- SSL/TLS termination
- API versioning
- Request routing to appropriate services
- CORS handling

**Technology Options:**
- Kong
- AWS API Gateway
- NGINX with custom middleware
- Traefik

### 2. Chat Service

**Purpose:** Handle conversational interactions

**Responsibilities:**
- WebSocket/HTTP endpoints for chat
- Session management
- Conversation history tracking
- Real-time response streaming
- User preference management

**API Endpoints:**
- `POST /api/v1/chat` - Send message
- `GET /api/v1/chat/history` - Get conversation history
- `DELETE /api/v1/chat/session` - Clear session
- `WS /api/v1/chat/stream` - WebSocket for streaming

### 3. Document Service

**Purpose:** Handle document upload and management

**Responsibilities:**
- File upload handling
- File type validation
- Virus scanning
- Document metadata storage
- Trigger ingestion pipeline
- Document retrieval

**API Endpoints:**
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/documents/{id}/reindex` - Trigger re-indexing

### 4. Action Service

**Purpose:** Execute banking actions

**Responsibilities:**
- Action request validation
- Action authorization
- Action execution via MCP
- Action confirmation workflow
- Action history tracking

**API Endpoints:**
- `POST /api/v1/actions/execute` - Execute action
- `GET /api/v1/actions/history` - Get action history
- `POST /api/v1/actions/confirm` - Confirm pending action
- `POST /api/v1/actions/cancel` - Cancel pending action

### 5. AI Agent Orchestrator

**Purpose:** Central intelligence coordinator

**Components:**

#### Query Router
- Analyzes incoming queries
- Routes to appropriate handler (RAG/MCP/Conversational)
- Manages complex multi-step queries

#### Intent Classifier
- Classifies user intent using LLM or classifier model
- Categories: information_retrieval, action_execution, clarification, greeting, etc.

#### Entity Extractor
- Extracts entities: dates, amounts, account numbers, etc.
- Uses NER models or LLM-based extraction

#### RAG Handler
- Coordinates RAG pipeline
- Retrieves relevant documents
- Constructs context for LLM
- Generates response with citations

#### MCP Handler
- Selects appropriate tools
- Validates parameters
- Executes actions
- Handles confirmations

#### Conversation Handler
- Handles chitchat
- Provides clarifications
- Manages multi-turn conversations

### 6. RAG System

**Purpose:** Retrieve and generate responses from documents

**Architecture:**

```
Document Upload
      │
      ▼
┌──────────────────┐
│  File Parser     │
│  - PDF           │
│  - DOCX          │
│  - XLSX          │
│  - Images (OCR)  │
│  - Audio/Video   │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Preprocessing   │
│  - Clean text    │
│  - Extract       │
│    metadata      │
│  - Detect        │
│    language      │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Chunking        │
│  - Semantic      │
│  - Hierarchical  │
│  - Overlap       │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Embedding       │
│  - Generate      │
│    vectors       │
│  - Batch process │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Vector Store    │
│  - Index vectors │
│  - Store         │
│    metadata      │
└──────────────────┘

Query Processing
      │
      ▼
┌──────────────────┐
│  Query           │
│  Enhancement     │
│  - Expansion     │
│  - Rewriting     │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Hybrid Search   │
│  - Dense         │
│    (semantic)    │
│  - Sparse        │
│    (keyword)     │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Re-ranking      │
│  - Cross-encoder │
│  - MMR           │
│  - Diversity     │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  Context         │
│  Assembly        │
│  - Top-k docs    │
│  - Metadata      │
│  - Citations     │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│  LLM Generation  │
│  - Claude API    │
│  - With context  │
│  - Citations     │
└──────────────────┘
```

### 7. MCP Engine

**Purpose:** Execute banking actions through structured tools

**Architecture:**

```
┌──────────────────────────────────────┐
│         MCP Server                   │
│                                      │
│  ┌────────────────────────────────┐ │
│  │      Tool Registry             │ │
│  │                                │ │
│  │  - Account Tools               │ │
│  │  - Transaction Tools           │ │
│  │  - Payment Tools               │ │
│  │  - Card Tools                  │ │
│  │  - Analytics Tools             │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │      Tool Executor             │ │
│  │                                │ │
│  │  1. Parameter Validation       │ │
│  │  2. Authorization Check        │ │
│  │  3. Execute Action             │ │
│  │  4. Result Formatting          │ │
│  │  5. Error Handling             │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │   Confirmation Manager         │ │
│  │                                │ │
│  │  - High-risk action detection  │ │
│  │  - Confirmation workflow       │ │
│  │  - Rollback mechanism          │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Tool Structure:**

```python
class BankingTool:
    name: str
    description: str
    parameters: List[Parameter]
    requires_confirmation: bool
    risk_level: RiskLevel  # LOW, MEDIUM, HIGH

    async def execute(self, params: Dict) -> ToolResult:
        # Implementation
        pass

    async def validate(self, params: Dict) -> bool:
        # Validation logic
        pass
```

### 8. Security Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Security Layers                         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Layer 1: Network Security                         │ │
│  │  - WAF (Web Application Firewall)                  │ │
│  │  - DDoS Protection                                 │ │
│  │  - VPC/Network Isolation                           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Layer 2: API Security                             │ │
│  │  - JWT Authentication                              │ │
│  │  - OAuth 2.0                                       │ │
│  │  - Rate Limiting                                   │ │
│  │  - Input Validation                                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Layer 3: Application Security                     │ │
│  │  - RBAC (Role-Based Access Control)               │ │
│  │  - PII Detection & Masking                         │ │
│  │  - SQL Injection Prevention                        │ │
│  │  - XSS Protection                                  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Layer 4: Data Security                            │ │
│  │  - Encryption at Rest (AES-256)                    │ │
│  │  - Encryption in Transit (TLS 1.3)                 │ │
│  │  - Key Management (KMS)                            │ │
│  │  - Data Anonymization                              │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Layer 5: Monitoring & Audit                       │ │
│  │  - Immutable Audit Logs                            │ │
│  │  - Anomaly Detection                               │ │
│  │  - Security Alerts                                 │ │
│  │  - Compliance Reporting                            │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Document Upload & Ingestion Flow

```
User uploads document
         │
         ▼
┌────────────────────┐
│  API Gateway       │ ─── Authentication
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Document Service  │ ─── Virus scan, validation
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  S3/MinIO Storage  │ ─── Store raw file
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Message Queue     │ ─── Async processing
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  RAG Ingestion     │
│  - Parse           │
│  - Chunk           │
│  - Embed           │
└─────────┬──────────┘
          │
          ├──────────────────┐
          │                  │
          ▼                  ▼
┌────────────────────┐  ┌────────────────────┐
│  Vector Database   │  │  Document Store    │
│  (embeddings)      │  │  (metadata)        │
└────────────────────┘  └────────────────────┘
          │
          ▼
┌────────────────────┐
│  Notification      │ ─── User notified
└────────────────────┘
```

### 2. Query Processing Flow

```
User asks question
         │
         ▼
┌────────────────────┐
│  Chat Service      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  AI Agent          │
│  Orchestrator      │
└─────────┬──────────┘
          │
          ├─── Intent Classification
          │
          ├──────────┬──────────┬──────────┐
          │          │          │          │
     [RAG]      [ACTION]   [CHAT]    [COMPLEX]
          │          │          │          │
          ▼          ▼          ▼          ▼
┌─────────────┐ ┌─────────┐ ┌──────┐ ┌──────────┐
│ RAG Handler │ │MCP      │ │Direct│ │Multi-step│
│             │ │Handler  │ │LLM   │ │Workflow  │
└──────┬──────┘ └────┬────┘ └───┬──┘ └────┬─────┘
       │             │          │         │
       ▼             ▼          │         │
┌─────────────┐ ┌─────────┐    │         │
│Vector Search│ │Banking  │    │         │
│+ Re-rank    │ │Backend  │    │         │
└──────┬──────┘ └────┬────┘    │         │
       │             │          │         │
       └─────────────┴──────────┴─────────┘
                     │
                     ▼
              ┌─────────────┐
              │  LLM        │
              │  (Claude)   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  Response   │
              │  Formatting │
              └──────┬──────┘
                     │
                     ▼
                   User
```

### 3. Action Execution Flow

```
User: "Transfer $500 to savings"
         │
         ▼
┌────────────────────┐
│  Intent: ACTION    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Entity Extraction │
│  - Amount: 500     │
│  - Destination:    │
│    savings         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  MCP Tool          │
│  Selection         │
│  -> transfer_funds │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Parameter         │
│  Validation        │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Risk Assessment   │
│  HIGH → Confirm    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Confirmation      │
│  Request to User   │
└─────────┬──────────┘
          │
    User confirms
          │
          ▼
┌────────────────────┐
│  Authorization     │
│  Check             │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Execute via       │
│  Banking Backend   │
└─────────┬──────────┘
          │
          ├──── Success ────┐
          │                 │
          ▼                 ▼
┌────────────────────┐  ┌────────────────────┐
│  Audit Log         │  │  Notification      │
└────────────────────┘  └────────────────────┘
          │                 │
          └────────┬────────┘
                   │
                   ▼
            Response to User
```

---

## Technology Decisions

### Backend Framework: FastAPI

**Reasons:**
- High performance (async/await)
- Automatic API documentation (OpenAPI)
- Type hints for better code quality
- Built-in validation (Pydantic)
- WebSocket support
- Modern Python (3.11+)

**Alternatives Considered:**
- Flask: More mature but lacks async support
- Django: Too heavyweight for microservices
- Node.js/Express: Different language stack

### LLM: Anthropic Claude

**Reasons:**
- Long context window (200K tokens)
- Strong reasoning capabilities
- Better at following instructions
- Built-in safety features
- Function calling support
- Streaming responses

**Alternatives:**
- OpenAI GPT-4: Comparable but shorter context
- Google Gemini: Newer, less proven
- Open-source LLMs: Less capable for complex tasks

### Vector Database: Pinecone (Primary) / Qdrant (Alternative)

**Pinecone:**
- Fully managed
- High performance
- Easy to scale
- Good documentation
- Higher cost

**Qdrant:**
- Self-hosted option
- Open source
- Good performance
- Lower cost
- More control

**Why not others:**
- Milvus: Complex setup
- Weaviate: Less mature
- Chroma: Better for development only

### Document Processing

**PDF:** pdfplumber
- Better table extraction than PyPDF2
- Good text formatting preservation

**OCR:** Tesseract (pytesseract)
- Open source
- Multi-language support
- Good accuracy

**Audio Transcription:** Whisper
- State-of-the-art accuracy
- Multiple language support
- OpenAI or self-hosted

### Database: PostgreSQL

**Reasons:**
- ACID compliance
- JSON support
- Full-text search
- Mature and stable
- Excellent performance
- Rich ecosystem

**Document Store:** MongoDB
- Flexible schema
- Document-oriented
- Good for metadata storage
- Aggregation framework

**Cache:** Redis
- In-memory performance
- Pub/sub support
- Session storage
- Rate limiting

---

## Scalability & Performance

### Horizontal Scaling Strategy

```
                    ┌──────────────┐
                    │ Load Balancer│
                    └───────┬──────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  API Server  │    │  API Server  │    │  API Server  │
│  Instance 1  │    │  Instance 2  │    │  Instance 3  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Caching Strategy

**Layer 1: Browser Cache**
- Static assets
- CDN for global distribution

**Layer 2: Redis Cache**
- Session data
- Frequently accessed data
- Rate limiting counters
- LRU eviction policy

**Layer 3: Application Cache**
- In-memory caching for embeddings
- Query result caching
- TTL-based invalidation

**Layer 4: Database Query Cache**
- PostgreSQL query cache
- Vector DB cache

### Performance Optimization

**Database:**
- Connection pooling
- Index optimization
- Query optimization
- Read replicas

**Vector Search:**
- Approximate nearest neighbor (ANN)
- Batch embedding generation
- Index optimization (HNSW)

**API:**
- Response compression (gzip)
- Request batching
- Async processing
- Streaming responses

**Background Processing:**
- Message queue (RabbitMQ/Kafka)
- Worker pools
- Job prioritization
- Retry mechanisms

### Monitoring & Observability

```
┌─────────────────────────────────────────────┐
│           Monitoring Stack                  │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Metrics (Prometheus)               │   │
│  │  - Request rate                     │   │
│  │  - Error rate                       │   │
│  │  - Response time (p50, p95, p99)    │   │
│  │  - Resource utilization             │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Logs (ELK Stack)                   │   │
│  │  - Application logs                 │   │
│  │  - Access logs                      │   │
│  │  - Error logs                       │   │
│  │  - Audit logs                       │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Traces (Jaeger)                    │   │
│  │  - Distributed tracing              │   │
│  │  - Request flow                     │   │
│  │  - Performance bottlenecks          │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Visualization (Grafana)            │   │
│  │  - Real-time dashboards             │   │
│  │  - Alert management                 │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## Security Architecture

### Authentication Flow

```
1. User Login
   │
   ├─── Username/Password
   │    ├─── Bcrypt hash verification
   │    └─── Password policy enforcement
   │
   ├─── MFA (Optional)
   │    ├─── TOTP (Time-based OTP)
   │    └─── SMS/Email OTP
   │
   └─── Biometric (Mobile)
        ├─── FaceID
        └─── Fingerprint

2. Token Generation
   │
   ├─── JWT Access Token (15 min)
   ├─── JWT Refresh Token (7 days)
   └─── Store in secure cookie

3. Token Validation
   │
   ├─── Signature verification
   ├─── Expiration check
   ├─── Token blacklist check
   └─── Permissions check
```

### Data Protection

**PII Detection:**
```python
class PIIDetector:
    patterns = {
        'SSN': r'\d{3}-\d{2}-\d{4}',
        'Credit Card': r'\d{4}-\d{4}-\d{4}-\d{4}',
        'Account Number': r'[0-9]{8,16}',
        'Email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    }

    def mask(self, text: str) -> str:
        # Mask PII in text
        pass
```

**Encryption:**
- **At Rest:** AES-256-GCM
- **In Transit:** TLS 1.3
- **Database:** Transparent Data Encryption (TDE)
- **Backups:** Encrypted with separate keys

### Audit Logging

```python
class AuditLog:
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    details: dict
    ip_address: str
    user_agent: str
    result: str  # SUCCESS / FAILURE
    risk_score: float
```

**Log Retention:**
- Audit logs: 7 years
- Application logs: 90 days
- Access logs: 1 year

---

## Deployment Architecture

### Development Environment

```
Docker Compose:
  - API Server
  - PostgreSQL
  - MongoDB
  - Redis
  - Qdrant (Vector DB)
  - MinIO (S3-compatible)
```

### Production Environment

```
Kubernetes Cluster:
  - Multiple availability zones
  - Auto-scaling (HPA)
  - Rolling updates
  - Health checks
  - Resource limits

External Services:
  - Managed PostgreSQL (RDS)
  - Managed Redis (ElastiCache)
  - Pinecone (Vector DB)
  - S3 (Document storage)
  - CloudFront (CDN)
```

---

## Disaster Recovery

### Backup Strategy

**Databases:**
- Automated daily backups
- Point-in-time recovery
- Cross-region replication
- Backup testing (monthly)

**Documents:**
- S3 versioning enabled
- Cross-region replication
- Glacier for archives

**Vector Database:**
- Snapshot backups
- Metadata backup in PostgreSQL

### Recovery Objectives

- **RTO (Recovery Time Objective):** 1 hour
- **RPO (Recovery Point Objective):** 15 minutes

---

**Last Updated:** 2025-11-10
