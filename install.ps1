# Claude Essential Mode Installer for Windows PowerShell

$ErrorActionPreference = "Stop"

$ClaudeDir = Join-Path $HOME ".claude"
$StylesDir = Join-Path $ClaudeDir "output-styles"
$SettingsFile = Join-Path $ClaudeDir "settings.json"
$TargetFile = Join-Path $StylesDir "essential.md"
$SourceUrl = "https://raw.githubusercontent.com/Iliesseu28/claude-essential-mode/main/styles/essential.md"

Write-Host "Installing Essential Mode for Claude Code on Windows..." -ForegroundColor Cyan

if (-not (Test-Path $StylesDir)) {
    New-Item -ItemType Directory -Path $StylesDir -Force | Out-Null
}

Invoke-WebRequest -Uri $SourceUrl -OutFile $TargetFile -UseBasicParsing

if (Test-Path $SettingsFile) {
    try {
        $content = Get-Content $SettingsFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $content | Add-Member -NotePropertyName "outputStyle" -NotePropertyValue "Essential" -Force
        $content | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile -Encoding UTF8
        Write-Host "Updated settings.json with outputStyle: 'Essential'" -ForegroundColor Green
    } catch {
        Write-Warning "Could not update settings.json automatically: $_"
    }
}

Write-Host "Successfully installed Essential Mode!" -ForegroundColor Green
Write-Host "Claude Code will now respond in Essential Mode by default."
Write-Host "To switch manually anytime in a session: /output-style essential" -ForegroundColor Yellow
