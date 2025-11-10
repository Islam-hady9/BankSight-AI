# BankSight-AI Quick Start Guide

Get your BankSight-AI development environment up and running in minutes!

## Prerequisites

### Required
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** ([Download](https://git-scm.com/downloads))

### API Keys
- **Anthropic API Key** (Required) - Get from [Anthropic Console](https://console.anthropic.com/)
- **OpenAI API Key** (Optional, for embeddings) - Get from [OpenAI Platform](https://platform.openai.com/)
- **Pinecone API Key** (Optional, alternative to Qdrant) - Get from [Pinecone](https://www.pinecone.io/)

---

## Option 1: Docker Setup (Recommended)

This is the fastest way to get started with all services.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/BankSight-AI.git
cd BankSight-AI
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required changes in `.env`:**
```bash
ANTHROPIC_API_KEY=your-anthropic-api-key-here
SECRET_KEY=your-random-secret-key-here
JWT_SECRET_KEY=your-random-jwt-secret-here
```

**Generate random keys:**
```bash
# On Linux/Mac:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# On Windows PowerShell:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Start All Services

```bash
# Start all services in detached mode
docker-compose -f docker/docker-compose.yml up -d

# For development with live reload:
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d
```

### Step 4: Verify Services

```bash
# Check if all containers are running
docker-compose -f docker/docker-compose.yml ps

# Check API health
curl http://localhost:8000/health
```

**Services will be available at:**
- API Server: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard
- MinIO Console: http://localhost:9001 (credentials: minioadmin/minioadmin)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (credentials: admin/admin)
- PgAdmin (dev): http://localhost:5050 (admin@banksight.local/admin)
- Mongo Express (dev): http://localhost:8081

### Step 5: Test the API

```bash
# Interactive API documentation
open http://localhost:8000/docs

# Or test with curl
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, BankSight!"}'
```

---

## Option 2: Local Python Setup

For development without Docker.

### Step 1: Clone and Setup Environment

```bash
git clone https://github.com/yourusername/BankSight-AI.git
cd BankSight-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Step 2: Install External Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr ffmpeg postgresql redis-server
```

#### On macOS:
```bash
brew install tesseract ffmpeg postgresql redis
```

#### On Windows:
- Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Install [FFmpeg](https://ffmpeg.org/download.html)
- Install [PostgreSQL](https://www.postgresql.org/download/windows/)
- Install [Redis](https://redis.io/docs/install/install-redis/install-redis-on-windows/)

### Step 3: Setup Databases

#### PostgreSQL:
```bash
# Create database and user
psql postgres
CREATE DATABASE banksight_db;
CREATE USER banksight WITH PASSWORD 'changeme';
GRANT ALL PRIVILEGES ON DATABASE banksight_db TO banksight;
\q
```

#### Qdrant (Vector Database):
```bash
# Run Qdrant in Docker
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

### Step 4: Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 5: Run Database Migrations

```bash
# Run migrations (once implemented)
alembic upgrade head
```

### Step 6: Start the API Server

```bash
# Development mode with auto-reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Or use the run script
python -m src.api.main
```

---

## Initial Setup Tasks

### 1. Create Vector Collection

```bash
# Using the API
curl -X POST http://localhost:8000/api/v1/admin/init-vector-store
```

### 2. Upload Sample Documents

```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@/path/to/your/document.pdf" \
  -F "metadata={\"type\": \"policy\", \"category\": \"banking\"}"
```

### 3. Test RAG System

```bash
# Ask a question
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the account opening requirements?",
    "session_id": "test-session-1"
  }'
```

### 4. Test MCP Actions (Mock Mode)

```bash
# Check account balance
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my account balance?",
    "session_id": "test-session-1"
  }'
```

---

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_rag.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with black
black src tests

# Sort imports
isort src tests

# Run linter
flake8 src tests

# Type checking
mypy src
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

---

## Common Commands

### Docker

```bash
# View logs
docker-compose -f docker/docker-compose.yml logs -f api

# Restart a service
docker-compose -f docker/docker-compose.yml restart api

# Stop all services
docker-compose -f docker/docker-compose.yml down

# Stop and remove volumes (clean slate)
docker-compose -f docker/docker-compose.yml down -v

# Rebuild containers
docker-compose -f docker/docker-compose.yml up -d --build
```

### Database

```bash
# Connect to PostgreSQL
docker exec -it banksight-postgres psql -U banksight -d banksight_db

# Connect to MongoDB
docker exec -it banksight-mongodb mongosh -u banksight -p changeme

# Connect to Redis
docker exec -it banksight-redis redis-cli
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process
kill -9 <PID>  # On Mac/Linux
taskkill /PID <PID> /F  # On Windows
```

### Docker Issues

```bash
# Clean up Docker
docker system prune -a

# Remove all stopped containers
docker container prune

# Remove all unused volumes
docker volume prune
```

### Database Connection Issues

1. Verify services are running: `docker-compose ps`
2. Check logs: `docker-compose logs <service-name>`
3. Verify credentials in `.env` file
4. Try restarting the service: `docker-compose restart <service-name>`

### API Key Issues

1. Verify API key is set in `.env`
2. Check API key is valid on provider's console
3. Restart the API service after changing `.env`

---

## Next Steps

Now that you have BankSight-AI running:

1. **Explore the API** - Visit http://localhost:8000/docs for interactive documentation
2. **Read the Architecture** - Check [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system
3. **Follow the Roadmap** - See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for implementation phases
4. **Start Development** - Pick a feature from Phase 1 and start coding!

---

## Learning Resources

### RAG Systems
- [LangChain Documentation](https://python.langchain.com/)
- [Anthropic Claude Guide](https://docs.anthropic.com/)
- [Vector Database Comparison](https://www.pinecone.io/learn/vector-database/)

### MCP (Model Context Protocol)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Building MCP Servers](https://modelcontextprotocol.io/docs/concepts/servers)

### Banking APIs
- [Plaid Documentation](https://plaid.com/docs/)
- [Open Banking Standards](https://www.openbanking.org.uk/)

---

## Getting Help

- **Documentation:** Check the `docs/` folder
- **Issues:** Create an issue on GitHub
- **Discussions:** Join project discussions

---

## Quick Reference Card

```bash
# Start everything
docker-compose -f docker/docker-compose.yml up -d

# View API logs
docker-compose -f docker/docker-compose.yml logs -f api

# Run tests
pytest

# Format code
black src tests && isort src tests

# Stop everything
docker-compose -f docker/docker-compose.yml down
```

Happy coding! 🚀
