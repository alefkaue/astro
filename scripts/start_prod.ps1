# start_prod.ps1 — Inicia o servidor ASTRO Cyber em modo produção (Windows)
# Uso: .\scripts\start_prod.ps1
# Pré-requisitos: .venv ativo, variáveis em .env configuradas (SECRET_KEY, CYMAG_ENV=production)

param(
    [string]$Host    = "0.0.0.0",
    [int]   $Port    = 8080,
    [int]   $Threads = 4
)

Set-Location $PSScriptRoot\..

# Carrega .env se existir
if (Test-Path ".env") {
    Get-Content ".env" | Where-Object { $_ -match "^\s*[^#]" -and $_ -match "=" } | ForEach-Object {
        $parts = $_ -split "=", 2
        [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim())
    }
}

# Validações mínimas antes de iniciar
if (-not $env:CYMAG_SECRET_KEY) {
    Write-Error "CYMAG_SECRET_KEY não definida. Configure em .env antes de iniciar em produção."
    exit 1
}

if ($env:CYMAG_ENV -ne "production") {
    Write-Warning "CYMAG_ENV não é 'production'. Continuando mesmo assim (ambiente: $env:CYMAG_ENV)."
}

Write-Host "Iniciando ASTRO Cyber com waitress em $Host`:$Port ($Threads threads)..."

.venv\Scripts\python.exe -c "
from waitress import serve
from app import create_app
app = create_app()
print(f'Servidor ouvindo em http://$Host`:$Port')
serve(app, host='$Host', port=$Port, threads=$Threads)
"
