<#
Push helper for Windows PowerShell

Usage (after installing Git and generating a new PAT):
1. Open PowerShell and run as your user (not elevated required)
2. Run: `.	ools\push_to_github.ps1` from the repo root or run this file directly

Notes:
- This script will NOT store or echo your personal access token. When Git prompts for credentials, paste your PAT as the password.
- Make sure you've revoked the old exposed token and created a new one with `repo` + `workflow` scopes.
#>

# Ensure script is run from repository root. Adjust path if needed.
Set-Location -Path "$PSScriptRoot\.."

Write-Host "Checking Git availability..."
git --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Git is not installed or not on PATH. Please install Git: https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

Write-Host "Repository status:"
git status --porcelain -b

Write-Host "Staging all changes..."
git add .

Write-Host "Creating commit (if any staged changes)..."
try {
    git commit -m "Apply documentation cleanup and backup" | Out-String | Write-Host
} catch {
    Write-Host "No changes to commit or commit failed. If nothing changed this is fine." -ForegroundColor Yellow
}

Write-Host "Checking remote 'origin'..."
$remote = git remote -v 2>$null
if (-not $remote) {
    Write-Host "No remote 'origin' configured. Adding your GitHub repo URL..."
    Write-Host "Replace the URL below with your repository URL if different." -ForegroundColor Yellow
    $repoUrl = 'https://github.com/Chloe-Tu2/boba-chain.git'
    git remote add origin $repoUrl
}

Write-Host "Ensuring main branch name..."
git branch -M main 2>$null

Write-Host "Configuring credential helper (manager-core) to make pushes easier..."
git config --global credential.helper manager-core

Write-Host "About to push to origin/main. When prompted, enter your GitHub username and your NEW PAT as the password."
git push -u origin main

Write-Host "Push completed (review output above). If the push failed due to authentication, make sure you pasted the correct PAT and that it has 'repo' scope." -ForegroundColor Green
