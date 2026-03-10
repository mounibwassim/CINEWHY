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
start "CineLogic Backend" cmd /k "cd /d %~dp0 && python webapp.py"

:: Run frontend in this window
pushd frontend
npm run dev
popd

popd

echo [dashboard] Exited frontend; backend should still be running in its window.