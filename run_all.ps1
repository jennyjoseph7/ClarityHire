$ws = Get-Location
Write-Host "Current Workspace: $ws"

Write-Host "Shutting down existing services..."
Get-CimInstance Win32_Process | Where-Object { 
    $_.CommandLine -like "*celery*" -or 
    $_.CommandLine -like "*uvicorn*" -or 
    $_.CommandLine -like "*vite*" 
} | ForEach-Object { 
    Write-Host "Stopping PID $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 2

Write-Host "Launching services in new windows..."

# Start Celery
# Note: Backticks ` before $ escape variable expansion so it happens in the new process
Start-Process -FilePath "powershell.exe" -WorkingDirectory $ws -ArgumentList "-NoExit", "-Command", "& {`$Host.UI.RawUI.WindowTitle = 'Celery Worker'; Write-Host 'Starting Celery Worker...'; `$env:PYTHONPATH='backend'; .venv\Scripts\celery -A app.worker.celery_app worker --pool=solo --loglevel=info}"

# Start Backend
Start-Process -FilePath "powershell.exe" -WorkingDirectory $ws -ArgumentList "-NoExit", "-Command", "& {`$Host.UI.RawUI.WindowTitle = 'Backend API'; Write-Host 'Starting Backend API...'; `$env:PYTHONPATH='backend'; .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload}"

# Start Frontend
Start-Process -FilePath "powershell.exe" -WorkingDirectory "$ws\frontend" -ArgumentList "-NoExit", "-Command", "& {`$Host.UI.RawUI.WindowTitle = 'Frontend'; Write-Host 'Starting Frontend...'; npm run dev}"

Write-Host "✅ System Restarted! Please check the three new PowerShell windows."
