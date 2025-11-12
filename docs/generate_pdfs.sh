#!/bin/bash

echo "📄 Generating PDFs from Markdown reports..."
echo ""

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Error: pandoc is not installed"
    echo ""
    echo "Install instructions:"
    echo "  Mac:     brew install pandoc && brew install --cask basictex"
    echo "  Ubuntu:  sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended"
    echo "  Windows: Download from https://pandoc.org/installing.html"
    exit 1
fi

echo "✅ Pandoc found: $(pandoc --version | head -1)"
echo ""

# Generate individual PDFs
echo "1️⃣  Converting PRODUCTION_DEPLOYMENT.md..."
pandoc PRODUCTION_DEPLOYMENT.md \
  -o PRODUCTION_DEPLOYMENT.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article \
  --number-sections \
  --highlight-style=tango

if [ $? -eq 0 ]; then
    echo "   ✅ PRODUCTION_DEPLOYMENT.pdf created"
else
    echo "   ❌ Failed to create PRODUCTION_DEPLOYMENT.pdf"
fi
echo ""

echo "2️⃣  Converting COST_ANALYSIS.md..."
pandoc COST_ANALYSIS.md \
  -o COST_ANALYSIS.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article \
  --number-sections \
  --highlight-style=tango

if [ $? -eq 0 ]; then
    echo "   ✅ COST_ANALYSIS.pdf created"
else
    echo "   ❌ Failed to create COST_ANALYSIS.pdf"
fi
echo ""

echo "3️⃣  Generating combined executive report..."
pandoc PRODUCTION_DEPLOYMENT.md COST_ANALYSIS.md \
  -o BankSight_AI_Complete_Report.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=report \
  --number-sections \
  --highlight-style=tango \
  -M title="BankSight-AI Production Deployment & Cost Analysis" \
  -M subtitle="Complete Report for 100-User Deployment" \
  -M author="BankSight-AI DevOps Team" \
  -M date="November 2025"

if [ $? -eq 0 ]; then
    echo "   ✅ BankSight_AI_Complete_Report.pdf created"
else
    echo "   ❌ Failed to create combined report"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ PDF generation complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Generated files:"
echo "  📄 PRODUCTION_DEPLOYMENT.pdf ($(du -h PRODUCTION_DEPLOYMENT.pdf 2>/dev/null | cut -f1 || echo '?'))"
echo "  📄 COST_ANALYSIS.pdf ($(du -h COST_ANALYSIS.pdf 2>/dev/null | cut -f1 || echo '?'))"
echo "  📄 BankSight_AI_Complete_Report.pdf ($(du -h BankSight_AI_Complete_Report.pdf 2>/dev/null | cut -f1 || echo '?'))"
echo ""
echo "📧 Ready to share with stakeholders!"
