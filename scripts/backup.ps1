# backup.ps1 — Faz cópia datada do banco SQLite e verifica integridade (G0-T05)
# Uso: .\scripts\backup.ps1 [-DbPath <caminho>] [-BackupDir <pasta>] [-Verify]
# Agendar no Task Scheduler para rodar diariamente.

param(
    [string]$DbPath    = "$PSScriptRoot\..\instance\cymag.db",
    [string]$BackupDir = "$PSScriptRoot\..\instance\backups",
    [switch]$Verify    = $true
)

$ErrorActionPreference = "Stop"

# ─── Cria pasta de backup se não existir ──────────────────────────────────────
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

# ─── Resolve caminhos absolutos ───────────────────────────────────────────────
$DbPath    = (Resolve-Path $DbPath    -ErrorAction SilentlyContinue)?.Path
$BackupDir = (Resolve-Path $BackupDir)?.Path

if (-not $DbPath -or -not (Test-Path $DbPath)) {
    Write-Error "Banco não encontrado: $DbPath"
    exit 1
}

# ─── Nome do arquivo de backup ────────────────────────────────────────────────
$timestamp  = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupFile = Join-Path $BackupDir "cymag_$timestamp.db"

# ─── Cópia usando SQLite VACUUM INTO (cópia consistente online) ───────────────
Write-Host "[backup] Copiando $DbPath → $backupFile"

$pythonExe = "$PSScriptRoot\..\\.venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

& $pythonExe -c "
import sqlite3, sys
src = sys.argv[1]; dst = sys.argv[2]
conn = sqlite3.connect(src)
conn.execute(f'VACUUM INTO \"{dst}\"')
conn.close()
print(f'[backup] Cópia criada: {dst}')
" $DbPath $backupFile

if ($LASTEXITCODE -ne 0) {
    Write-Error "[backup] VACUUM INTO falhou (código $LASTEXITCODE)."
    exit 1
}

# ─── Verificação de integridade ────────────────────────────────────────────────
if ($Verify) {
    Write-Host "[backup] Verificando integridade de $backupFile..."
    $result = & $pythonExe -c "
import sqlite3, sys
conn = sqlite3.connect(sys.argv[1])
r = conn.execute('PRAGMA integrity_check').fetchone()
print(r[0])
conn.close()
" $backupFile

    if ($result -ne "ok") {
        Write-Error "[backup] FALHA na verificação de integridade: $result"
        Remove-Item $backupFile -Force
        exit 1
    }
    Write-Host "[backup] Integridade OK."
}

# ─── Retém apenas os últimos 30 backups ───────────────────────────────────────
$files = Get-ChildItem -Path $BackupDir -Filter "cymag_*.db" | Sort-Object LastWriteTime -Descending
if ($files.Count -gt 30) {
    $files | Select-Object -Skip 30 | ForEach-Object {
        Write-Host "[backup] Removendo backup antigo: $($_.Name)"
        Remove-Item $_.FullName -Force
    }
}

Write-Host "[backup] Concluído: $backupFile"
