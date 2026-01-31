Write-Host "Creating upload directories..."
New-Item -ItemType Directory -Force -Path "uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "backend/app/uploads" | Out-Null

Write-Host "Killing old uvicorn processes..."
Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like "*uvicorn*"} | ForEach-Object { 
    Write-Host "Killing PID $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force 
}
Start-Sleep -Seconds 2

Write-Host "Starting new backend server..."
$env:PYTHONPATH="backend"
Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -RedirectStandardOutput "backend_debug.log" -RedirectStandardError "backend_error.log" -WindowStyle Hidden
Write-Host "Backend restarted! Logs are being written to backend_debug.log"
