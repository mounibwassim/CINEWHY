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

# Wait for backend health endpoint to become available (improves UX when backend cold-starts)
$healthUrl = "http://localhost:5000/api/init"
$maxAttempts = 15
$attempt = 0
Write-Host "[dashboard] Waiting for backend to become healthy at $healthUrl..."
while ($attempt -lt $maxAttempts) {
    try {
        $r = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($r.StatusCode -eq 200) {
            Write-Host "[dashboard] Backend is up."
            break
        }
    } catch {
        Start-Sleep -Seconds 2
        $attempt++
        Write-Host "[dashboard] Backend not ready, attempt $($attempt)/$maxAttempts..."
    }
}
if ($attempt -ge $maxAttempts) {
    Write-Host "[dashboard] Warning: Backend did not respond after $maxAttempts attempts. Frontend will start but may show 'Backend Offline'." -ForegroundColor Yellow
}

Write-Host "[dashboard] Starting frontend (Vite) in current window..."
Push-Location (Join-Path $root 'frontend')
npm run dev
Pop-Location

Write-Host "[dashboard] Done. Frontend is running in this window; backend runs as a background job."
