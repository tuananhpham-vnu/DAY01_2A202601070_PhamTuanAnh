$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$env:PYTHONIOENCODING = "utf-8"

function Get-FreePort {
    param(
        [int[]]$Candidates = @(8000, 8001, 8002, 8003, 8004, 8005)
    )

    foreach ($port in $Candidates) {
        $listener = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if (-not $listener) {
            return $port
        }
    }

    throw "No free port found in the candidate range."
}

if (-not $env:PORT -or [string]::IsNullOrWhiteSpace($env:PORT)) {
    $env:PORT = (Get-FreePort).ToString()
}

Write-Host "[run_web_app] Using port $env:PORT"
Write-Host "[run_web_app] Logs will also be written to web_app.log"
Write-Host "[run_web_app] Open http://127.0.0.1:$env:PORT"
Write-Host "[run_web_app] Press Ctrl+C to stop"

& .\.venv\Scripts\python.exe .\web_app.py 2>&1 | Tee-Object -FilePath .\web_app.log -Append
