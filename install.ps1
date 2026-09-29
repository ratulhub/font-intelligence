<#
.SYNOPSIS
    Font Intelligence - Unified Multi-Agent Installer (PowerShell)
.DESCRIPTION
    Installs the Font Intelligence skill and platform adapters for Windows.
.PARAMETER Target
    Adapter to configure: all, antigravity, claude, cursor, windsurf, cline, copilot, codex, gemini.
.PARAMETER DestDir
    Target directory to install adapters into (defaults to current directory).
.PARAMETER Global
    If set, installs to global user configuration paths where applicable.
.EXAMPLE
    .\install.ps1 -Target all
    .\install.ps1 -Target cursor -DestDir "C:\path\to\my-project"
    .\install.ps1 -Target antigravity -Global
#>

param (
    [string]$Target = "all",
    [string]$DestDir = "",
    [switch]$Global = $false
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($DestDir)) {
    $DestDir = $ScriptDir
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Installing Font Intelligence Typography Decision System" -ForegroundColor Cyan
Write-Host "Target Adapter: $Target (Global: $Global)"
Write-Host "Source Path:    $ScriptDir"
Write-Host "Destination:    $DestDir"
Write-Host "=================================================================" -ForegroundColor Cyan

function Copy-SafeItem {
    param (
        [string]$Source,
        [string]$Destination
    )
    $srcResolved = [System.IO.Path]::GetFullPath($Source)
    $destResolved = [System.IO.Path]::GetFullPath($Destination)
    if ($srcResolved -ne $destResolved) {
        $destParent = Split-Path -Parent $destResolved
        if (!(Test-Path $destParent)) { New-Item -ItemType Directory -Path $destParent -Force | Out-Null }
        Copy-Item -Path $srcResolved -Destination $destResolved -Force
    }
}

function Install-Antigravity {
    Write-Host "• Configuring Antigravity..." -ForegroundColor Yellow
    if ($Global) {
        $dest = Join-Path $env:USERPROFILE ".gemini\config\skills\font-intelligence"
    } else {
        $dest = Join-Path $DestDir ".agents\skills\font-intelligence"
    }
    if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
    $src = Join-Path $ScriptDir ".agents\skills\font-intelligence"
    if ([System.IO.Path]::GetFullPath($src) -ne [System.IO.Path]::GetFullPath($dest)) {
        Copy-Item -Path "$src\*" -Destination $dest -Recurse -Force
    }
    Write-Host "  -> Antigravity skill ready at: $dest" -ForegroundColor Green
}

function Install-Claude {
    Write-Host "• Configuring Claude Code..." -ForegroundColor Yellow
    if ($Global) {
        $dest = Join-Path $env:USERPROFILE ".claude\CLAUDE.md"
    } else {
        $dest = Join-Path $DestDir "CLAUDE.md"
    }
    Copy-SafeItem -Source "$ScriptDir\adapters\claude\CLAUDE.md" -Destination $dest
    Write-Host "  -> Claude adapter ready at: $dest" -ForegroundColor Green
}

function Install-Cursor {
    Write-Host "• Configuring Cursor..." -ForegroundColor Yellow
    $rulesDir = Join-Path $DestDir ".cursor\rules"
    Copy-SafeItem -Source "$ScriptDir\adapters\cursor\font-intelligence.mdc" -Destination "$rulesDir\font-intelligence.mdc"
    Copy-SafeItem -Source "$ScriptDir\adapters\cursor\.cursorrules" -Destination (Join-Path $DestDir ".cursorrules")
    Write-Host "  -> Cursor rules ready at: $rulesDir\font-intelligence.mdc" -ForegroundColor Green
}

function Install-Windsurf {
    Write-Host "• Configuring Windsurf..." -ForegroundColor Yellow
    Copy-SafeItem -Source "$ScriptDir\adapters\windsurf\.windsurfrules" -Destination (Join-Path $DestDir ".windsurfrules")
    Write-Host "  -> Windsurf rule ready at: $(Join-Path $DestDir '.windsurfrules')" -ForegroundColor Green
}

function Install-Cline {
    Write-Host "• Configuring Cline..." -ForegroundColor Yellow
    Copy-SafeItem -Source "$ScriptDir\adapters\cline\.clinerules" -Destination (Join-Path $DestDir ".clinerules")
    Write-Host "  -> Cline rule ready at: $(Join-Path $DestDir '.clinerules')" -ForegroundColor Green
}

function Install-Copilot {
    Write-Host "• Configuring GitHub Copilot..." -ForegroundColor Yellow
    $dest = Join-Path $DestDir ".github\copilot-instructions.md"
    Copy-SafeItem -Source "$ScriptDir\adapters\copilot\copilot-instructions.md" -Destination $dest
    Write-Host "  -> Copilot instructions ready at: $dest" -ForegroundColor Green
}

function Install-Codex {
    Write-Host "• Configuring Codex..." -ForegroundColor Yellow
    $dest = Join-Path $DestDir ".codex\instructions.md"
    Copy-SafeItem -Source "$ScriptDir\adapters\codex\instructions.md" -Destination $dest
    Write-Host "  -> Codex instructions ready at: $dest" -ForegroundColor Green
}

function Install-Gemini {
    Write-Host "• Configuring Gemini CLI..." -ForegroundColor Yellow
    Copy-SafeItem -Source "$ScriptDir\adapters\gemini\GEMINI.md" -Destination (Join-Path $DestDir "GEMINI.md")
    Write-Host "  -> Gemini CLI adapter ready at: $(Join-Path $DestDir 'GEMINI.md')" -ForegroundColor Green
}

switch ($Target.ToLower()) {
    "antigravity" { Install-Antigravity }
    "claude"      { Install-Claude }
    "cursor"      { Install-Cursor }
    "windsurf"    { Install-Windsurf }
    "cline"       { Install-Cline }
    "copilot"     { Install-Copilot }
    "codex"       { Install-Codex }
    "gemini"      { Install-Gemini }
    "all" {
        Install-Antigravity
        Install-Claude
        Install-Cursor
        Install-Windsurf
        Install-Cline
        Install-Copilot
        Install-Codex
        Install-Gemini
    }
    Default {
        Write-Error "Unknown target: $Target. Supported: all, antigravity, claude, cursor, windsurf, cline, copilot, codex, gemini"
    }
}

Write-Host ""
Write-Host "Running post-install catalog validation..." -ForegroundColor Cyan
python "$ScriptDir\scripts\validate_catalog.py"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Font Intelligence installation completed successfully!" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
