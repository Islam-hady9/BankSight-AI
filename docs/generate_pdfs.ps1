# BankSight-AI PDF Generation Script (PowerShell)

Write-Host "📄 Generating PDFs from Markdown reports..." -ForegroundColor Cyan
Write-Host ""

# Check if pandoc is installed
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: pandoc is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install instructions:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://pandoc.org/installing.html"
    Write-Host "  2. Install MiKTeX (for PDF generation): https://miktex.org/download"
    Write-Host "  3. Restart PowerShell after installation"
    exit 1
}

Write-Host "✅ Pandoc found: " -NoNewline -ForegroundColor Green
pandoc --version | Select-Object -First 1
Write-Host ""

# Generate individual PDFs
Write-Host "1️⃣  Converting PRODUCTION_DEPLOYMENT.md..." -ForegroundColor Yellow
pandoc PRODUCTION_DEPLOYMENT.md `
  -o PRODUCTION_DEPLOYMENT.pdf `
  --pdf-engine=xelatex `
  --toc `
  --toc-depth=3 `
  -V geometry:margin=1in `
  -V fontsize=11pt `
  -V documentclass=article `
  --number-sections `
  --highlight-style=tango

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ PRODUCTION_DEPLOYMENT.pdf created" -ForegroundColor Green
} else {
    Write-Host "   ❌ Failed to create PRODUCTION_DEPLOYMENT.pdf" -ForegroundColor Red
}
Write-Host ""

Write-Host "2️⃣  Converting COST_ANALYSIS.md..." -ForegroundColor Yellow
pandoc COST_ANALYSIS.md `
  -o COST_ANALYSIS.pdf `
  --pdf-engine=xelatex `
  --toc `
  --toc-depth=3 `
  -V geometry:margin=1in `
  -V fontsize=11pt `
  -V documentclass=article `
  --number-sections `
  --highlight-style=tango

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ COST_ANALYSIS.pdf created" -ForegroundColor Green
} else {
    Write-Host "   ❌ Failed to create COST_ANALYSIS.pdf" -ForegroundColor Red
}
Write-Host ""

Write-Host "3️⃣  Generating combined executive report..." -ForegroundColor Yellow
pandoc PRODUCTION_DEPLOYMENT.md COST_ANALYSIS.md `
  -o BankSight_AI_Complete_Report.pdf `
  --pdf-engine=xelatex `
  --toc `
  --toc-depth=3 `
  -V geometry:margin=1in `
  -V fontsize=11pt `
  -V documentclass=report `
  --number-sections `
  --highlight-style=tango `
  -M title="BankSight-AI Production Deployment & Cost Analysis" `
  -M subtitle="Complete Report for 100-User Deployment" `
  -M author="BankSight-AI DevOps Team" `
  -M date="November 2025"

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ BankSight_AI_Complete_Report.pdf created" -ForegroundColor Green
} else {
    Write-Host "   ❌ Failed to create combined report" -ForegroundColor Red
}
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ PDF generation complete!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "📁 Generated files:" -ForegroundColor Cyan
if (Test-Path "PRODUCTION_DEPLOYMENT.pdf") {
    $size = (Get-Item "PRODUCTION_DEPLOYMENT.pdf").Length / 1KB
    Write-Host "  📄 PRODUCTION_DEPLOYMENT.pdf ($([math]::Round($size, 1)) KB)" -ForegroundColor White
}
if (Test-Path "COST_ANALYSIS.pdf") {
    $size = (Get-Item "COST_ANALYSIS.pdf").Length / 1KB
    Write-Host "  📄 COST_ANALYSIS.pdf ($([math]::Round($size, 1)) KB)" -ForegroundColor White
}
if (Test-Path "BankSight_AI_Complete_Report.pdf") {
    $size = (Get-Item "BankSight_AI_Complete_Report.pdf").Length / 1KB
    Write-Host "  📄 BankSight_AI_Complete_Report.pdf ($([math]::Round($size, 1)) KB)" -ForegroundColor White
}
Write-Host ""
Write-Host "📧 Ready to share with stakeholders!" -ForegroundColor Green
