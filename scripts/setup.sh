#!/bin/bash
# BankSight-AI Setup Script

set -e

echo "🏦 BankSight-AI Setup Script"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your API keys!"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check for Python
echo "🐍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check for Docker
echo "🐳 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker"
    exit 1
fi
echo "✅ Docker found"
echo ""

# Check for Docker Compose
echo "🐳 Checking Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose"
    exit 1
fi
echo "✅ Docker Compose found"
echo ""

# Ask if user wants to start Docker services
read -p "📦 Do you want to start Docker services now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting Docker services..."
    docker-compose -f docker/docker-compose.yml up -d
    echo ""
    echo "✅ Services started!"
    echo ""
    echo "📊 Service URLs:"
    echo "  - API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Qdrant: http://localhost:6333/dashboard"
    echo "  - MinIO: http://localhost:9001"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3001"
    echo ""
fi

# Ask if user wants to install Python dependencies
read -p "📦 Do you want to install Python dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""

    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements-dev.txt
    echo "✅ Dependencies installed"
    echo ""

    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installed"
    echo ""
fi

echo "🎉 Setup complete!"
echo ""
echo "📚 Next steps:"
echo "  1. Edit .env and add your API keys (ANTHROPIC_API_KEY, etc.)"
echo "  2. If not done, start services: docker-compose -f docker/docker-compose.yml up -d"
echo "  3. Activate venv: source venv/bin/activate"
echo "  4. Read QUICK_START.md for more details"
echo "  5. Start coding! Check IMPLEMENTATION_ROADMAP.md for guidance"
echo ""
echo "Happy coding! 🚀"
