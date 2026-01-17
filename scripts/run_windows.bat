@echo off
setlocal

cd /d %~dp0\..

echo Starting Vestigium API...
start "Vestigium API" cmd /k "python -m uvicorn services.api.app:app --reload --host 0.0.0.0 --port 8000"

echo Starting Vestigium UI...
start "Vestigium UI" cmd /k "cd apps\desktop && npm install && npm run dev"

echo Done. Two terminals should be open now.
