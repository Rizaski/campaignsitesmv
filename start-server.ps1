# Start the campaign site HTTP server (port 8000)
$python = "C:\Users\Empower\AppData\Local\Programs\Python\Python313\python.exe"
if (-not (Test-Path $python)) {
    # Fallback: try python or py from PATH
    $python = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $python) { $python = (Get-Command py -ErrorAction SilentlyContinue).Source }
}
if (-not $python) { Write-Error "Python not found. Install Python or set PATH."; exit 1 }
Set-Location $PSScriptRoot
& $python server.py
