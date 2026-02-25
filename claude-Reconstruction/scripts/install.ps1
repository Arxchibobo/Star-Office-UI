# Claude Reconstruction install script (Windows PowerShell)
# Usage: .\install.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         Claude Reconstruction v5.0                           ║" -ForegroundColor Green
Write-Host "║         Claude Code Engineering Config                       ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Directories
$ClaudeDir = "$env:USERPROFILE\.claude"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "Source: $ProjectDir" -ForegroundColor Yellow
Write-Host "Target: $ClaudeDir" -ForegroundColor Yellow
Write-Host ""

# Create directory structure
Write-Host "[1/5] Creating directories..." -ForegroundColor Green
$directories = @(
    $ClaudeDir,
    "$ClaudeDir\rules\core",
    "$ClaudeDir\rules\domain",
    "$ClaudeDir\rules\delegator",
    "$ClaudeDir\index",
    "$ClaudeDir\capabilities",
    "$ClaudeDir\errors",
    "$ClaudeDir\design",
    "$ClaudeDir\vibe-marketing"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Backup existing config
if (Test-Path "$ClaudeDir\CLAUDE.md") {
    $backupName = "CLAUDE.md.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "[Backup] Backing up existing CLAUDE.md..." -ForegroundColor Yellow
    Copy-Item "$ClaudeDir\CLAUDE.md" "$ClaudeDir\$backupName"
}

# Install core config
Write-Host "[2/5] Installing core config..." -ForegroundColor Green
Copy-Item "$ProjectDir\CLAUDE.md" "$ClaudeDir\CLAUDE.md" -Force
Copy-Item "$ProjectDir\CONTEXT_MANAGER.md" "$ClaudeDir\CONTEXT_MANAGER.md" -Force

# Install rules
Write-Host "[3/5] Installing rules..." -ForegroundColor Green
Copy-Item "$ProjectDir\rules\*" "$ClaudeDir\rules\" -Recurse -Force

# Install index, capabilities, errors
Write-Host "[4/5] Installing index, capabilities, errors..." -ForegroundColor Green
Copy-Item "$ProjectDir\index\*" "$ClaudeDir\index\" -Recurse -Force
Copy-Item "$ProjectDir\capabilities\*" "$ClaudeDir\capabilities\" -Recurse -Force
Copy-Item "$ProjectDir\errors\*" "$ClaudeDir\errors\" -Recurse -Force

# Install optional resources
Write-Host "[5/5] Installing design & marketing docs..." -ForegroundColor Green
if (Test-Path "$ProjectDir\design") {
    Copy-Item "$ProjectDir\design\*" "$ClaudeDir\design\" -Recurse -Force
}
if (Test-Path "$ProjectDir\vibe-marketing") {
    Copy-Item "$ProjectDir\vibe-marketing\*" "$ClaudeDir\vibe-marketing\" -Recurse -Force
}

# Verify
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "Install complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Installed:" -ForegroundColor Yellow
Write-Host "  - $ClaudeDir\CLAUDE.md (entry point)"
Write-Host "  - $ClaudeDir\CONTEXT_MANAGER.md (smart loading)"
Write-Host "  - $ClaudeDir\rules\ (rules engine)"
Write-Host "  - $ClaudeDir\index\ (navigation)"
Write-Host "  - $ClaudeDir\capabilities\ (capability docs)"
Write-Host "  - $ClaudeDir\errors\ (error library)"
Write-Host "  - $ClaudeDir\design\ (design system)"
Write-Host ""
Write-Host "Next:" -ForegroundColor Yellow
Write-Host "  1. Start Claude Code"
Write-Host "  2. Config loads automatically"
Write-Host "  3. Context usage: ~20% (down from 60%)"
Write-Host ""
