# Run the CineLogic dashboard (Windows PowerShell)
# - Installs Python + frontend dependencies if missing
# - Starts backend as a background job and runs the frontend dev server

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

Write-Host "[dashboard] Installing Python requirements..."
python -m pip install -r requirements.txt

Write-Host "[dashboard] Installing frontend dependencies (if needed)..."
Push-Location (Join-Path $root 'frontend')
if (-not (Test-Path node_modules)) {
    npm install
}
Pop-Location

Write-Host "[dashboard] Starting backend as background job..."
Start-Job -ScriptBlock { param($r) & python "$r\app.py" } -ArgumentList $root | Out-Null
Start-Sleep -Seconds 2

Write-Host "[dashboard] Starting frontend (Vite) in current window..."
Push-Location (Join-Path $root 'frontend')
npm run dev
Pop-Location

Write-Host "[dashboard] Done. Frontend is running in this window; backend runs as a background job."
