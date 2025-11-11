<#
run_demo.ps1
Helper script to activate the repository virtual environment (if present)
and run the Flask demo app from the `Demo` folder.

Usage (PowerShell):
  .\run_demo.ps1

This script is non-destructive and only attempts to activate `../.venv` if it exists.
#>

Write-Host "Starting TribalLink demo..."

$repoRoot = Split-Path -Parent $PSScriptRoot
$venvActivate = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment at $venvActivate"
    & $venvActivate
} else {
    Write-Warning "No .venv found at $venvActivate. Make sure dependencies are installed in your active environment."
}

Set-Location $PSScriptRoot

Write-Host "Installing (missing) dependencies from requirements.txt if present..."
if (Test-Path "requirements.txt") {
    python -m pip install -r requirements.txt
}

Write-Host "Running app.py (Flask dev server). Press Ctrl+C to stop."
python app.py
