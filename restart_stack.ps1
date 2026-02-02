Write-Host "Shutting down existing services..."
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*celery*" -or $_.CommandLine -like "*uvicorn*" } | ForEach-Object { 
    Write-Host "Stopping PID $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 2

Write-Host "Launching services in new windows..."

# Start Celery
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "& {HOST_NAME; Write-Host 'Starting Celery Worker...'; $env:PYTHONPATH='backend'; .venv\Scripts\celery -A app.worker.celery_app worker --pool=solo --loglevel=info}"

# Start Backend
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "& {HOST_NAME; Write-Host 'Starting Backend API...'; $env:PYTHONPATH='backend'; .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload}"

Write-Host "✅ System Restarted! Please check the two new PowerShell windows."
