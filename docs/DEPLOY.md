# ASTRO Cyber — Deploy em Produção (Windows)

> Estado: G0 — servidor local de laboratório, antes de qualquer dado real de cliente.
> Não expor na internet sem HTTPS (G0-T04) e backup verificado (G0-T05).

---

## 1. Pré-requisitos

```
Python 3.11+       (3.14 usado no dev; 3.11+ recomendado para prod por estabilidade)
pip install -r requirements.txt   (inclui waitress, cryptography)
Nmap opcional      (scanner Go já compilado em scanner_go/)
```

---

## 2. Arquivo .env (fora do repositório)

Crie `instance/.env` (nunca commitar):

```env
CYMAG_SECRET_KEY=<string aleatória de 64+ caracteres>
CYMAG_ENV=production
CYMAG_DB_PATH=C:\caminho\absoluto\instance\cymag.db
CYMAG_SCOPE_ALLOW=192.168.1.0/24,10.0.0.0/8   # CIDRs autorizados
GROQ_API_KEY=                                   # opcional; AEGIS fica offline se vazio
```

Gerar SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 3. Iniciar servidor (G0-T03)

```powershell
# Ativa o ambiente virtual
.\.venv\Scripts\Activate.ps1

# Carrega .env
Get-Content instance\.env | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
    }
}

# Inicia com waitress (substitui Flask dev server)
.\scripts\start_prod.ps1 -Host 127.0.0.1 -Port 8080 -Threads 4
```

O servidor escuta em `http://127.0.0.1:8080`. Nunca expor diretamente na internet — usar proxy reverso com HTTPS (seção 4).

---

## 4. HTTPS com nginx (G0-T04)

### Opção A: nginx como proxy reverso (recomendada para laboratório)

Instalar nginx para Windows: https://nginx.org/en/download.html

`nginx.conf` mínimo:

```nginx
worker_processes 1;

events { worker_connections 1024; }

http {
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name _;

        # Certificado self-signed (laboratório) — substituir por Let's Encrypt em produção
        ssl_certificate     C:/caminho/para/certs/astro.crt;
        ssl_certificate_key C:/caminho/para/certs/astro.key;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass         http://127.0.0.1:8080;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
        }
    }
}
```

### Gerar certificado self-signed (laboratório)

Requer OpenSSL instalado:

```powershell
New-Item -ItemType Directory -Force instance\certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
    -keyout instance\certs\astro.key `
    -out    instance\certs\astro.crt `
    -subj "/CN=astro-cyber-lab"
```

**Atenção:** Certificado self-signed não é adequado para clientes reais — o navegador exibe aviso de segurança. Para produção com domínio real, usar Let's Encrypt (Caddy ou certbot).

### Opção B: Caddy (mais simples, com Let's Encrypt automático se tiver domínio)

```
# Caddyfile
astro.seudominio.com {
    reverse_proxy 127.0.0.1:8080
}
```

```powershell
caddy run --config Caddyfile
```

---

## 5. Backup automático (G0-T05)

### Executar manualmente

```powershell
.\scripts\backup.ps1
```

O backup usa `VACUUM INTO` (cópia consistente sem bloquear leituras) e verifica integridade com `PRAGMA integrity_check`. Últimos 30 backups são mantidos em `instance\backups\`.

### Agendar no Task Scheduler (diário)

```powershell
$action  = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NonInteractive -File C:\caminho\para\cymag_saas\scripts\backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "03:00"
Register-ScheduledTask -TaskName "ASTROCyberBackup" -Action $action -Trigger $trigger `
    -RunLevel Highest -Force
```

### Testar restore

```powershell
# Copia o backup mais recente para um banco temporário e verifica
$backup = Get-ChildItem instance\backups\cymag_*.db | Sort-Object LastWriteTime | Select-Object -Last 1
python -c "
import sqlite3, sys
conn = sqlite3.connect(sys.argv[1])
tables = conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()
print('Tabelas:', [t[0] for t in tables])
users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
print(f'Usuários: {users}')
conn.close()
" $backup.FullName
```

---

## 6. Permissões do processo (G0-T06)

O processo web **não deve ter permissões elevadas**. Nmap e o binário Go são chamados como subprocessos com timeout; não precisam de sudo/admin se o scan for em redes próprias.

**Verificar:**
- O processo Python roda como usuário padrão (não Administrador)
- O binário `scanner_go/cymag.exe` tem permissão de execução pelo usuário do serviço
- Nmap (se instalado) tem permissão de execução; no Windows pode precisar de WinPcap/Npcap para raw sockets — avaliar necessidade

**Para rodar como serviço Windows (NSSM):**

```powershell
# Instalar NSSM: https://nssm.cc
nssm install ASTROCyber powershell.exe
nssm set ASTROCyber AppParameters "-NonInteractive -File C:\...\scripts\start_prod.ps1"
nssm set ASTROCyber AppDirectory C:\...\cymag_saas
nssm set ASTROCyber ObjectName ".\astro-svc"  # usuário de serviço sem admin
nssm start ASTROCyber
```

---

## 7. Gates de segurança antes de aceitar dados reais de clientes

| Gate | Requisito | Estado |
|---|---|---|
| G0-S12 | Chave IA cifrada (Fernet) | ✅ |
| G0-S14 | Rate-limit em SQLite (multi-worker) | ✅ |
| G0-O01 | Servidor waitress (não Flask dev) | ✅ script pronto |
| G0-O02 | HTTPS (TLS) | ✅ config pronta — executar seção 4 |
| G0-O03 | Backup + restore verificado | ✅ script pronto — agendar seção 5 |
| G0-O05 | Scanner sem permissão elevada | ✅ verificar seção 6 |

Todos os gates G0 de segurança (S01–S14) estão fechados. Ao concluir os itens de operação acima, o gate G0 estará completo.
