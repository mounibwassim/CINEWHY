@echo off
:: Run the CineLogic dashboard (Windows CMD)
:: - Installs Python + frontend dependencies if missing
:: - Starts backend in a new console and runs the frontend dev server

:: Ensure script runs from repository root
pushd %~dp0

echo [dashboard] Installing Python requirements...
python -m pip install -r requirements.txt

if not exist frontend\node_modules (
  echo [dashboard] Installing frontend dependencies...
  pushd frontend
  npm install
  popd
)

:: Start backend in new window so we can keep frontend logs here
start "CineLogic Backend" cmd /k "cd /d %~dp0 && python app.py"

:: Wait for backend health endpoint to become available (improves UX when backend cold-starts)
powershell -NoProfile -Command " $health='http://localhost:5000/api/init'; $max=15; for ($i=1;$i -le $max;$i++) { try { $r=Invoke-WebRequest -Uri $health -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop; Write-Host '[dashboard] Backend is up.'; exit 0 } catch { Start-Sleep -Seconds 2; Write-Host '[dashboard] Backend not ready, attempt $i/$max...' } }; Write-Host '[dashboard] Warning: Backend did not respond after multiple attempts.'; exit 1 "

:: Run frontend in this window
pushd frontend
npm run dev
popd

popd

echo [dashboard] Exited frontend; backend should still be running in its window.