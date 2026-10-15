# Baseline — 14/10/2026

Especificação lida integralmente (UTF-8, seções 0–13). O workspace inicialmente continha somente a especificação e não era um checkout Git.

Origem local encontrada: `C:/Users/47191173840/Desktop/scanner/cymag_saas`, commit `b888fb9ff818af06f79686833031ebdf42aee47f`, status Git limpo; remote `https://github.com/alefkaue/cymag_saas.git`. Código copiado para o workspace sem alterar a origem. Excluídos `.git`, `.venv`, caches, `instance`, `.env`, bancos e executáveis. A especificação original foi preservada. Não há histórico Git no destino; não foram criados commits.

Arquitetura: monólito Flask, sqlite3 direto, contas e papéis legados, frontend JS/CSS e index.html; scanner Python e Go. Scan manual bloqueia a requisição; modo autônomo usa threads daemon e progresso em memória. Não há worker durável, protocolo de agente, API v1 ou migrações reversíveis. Tabelas: accounts, users, engagements, scans, findings, audit_log, budget_decisions. Documentação README/INSTALL inspecionada; PLATAFORMA.md ausente.

Ambiente: Windows/PowerShell, Python global 3.14.2 sem pytest; Python do venv de origem reutilizado somente como interpretador/dependências. Go não encontrado no PATH nem em Program Files/Go. Node disponível. GitHub inacessível via proxy local; nenhuma execução externa ou deploy.

## Testes anteriores às alterações

`python -m pytest tests -q -p no:cacheprovider`: 42 passaram, 7 erros ao abrir banco temporário neste sandbox. Com Config.DB_PATH direcionado a `instance/baseline-test.db`, mesma suíte: **49 passaram em 2,16 s**. Banco de teste fictício, não copiado do cliente. Comando usado:

```powershell
& C:/Users/47191173840/Desktop/scanner/cymag_saas/.venv/Scripts/python.exe -c "from app.config import config; config.DB_PATH='instance/baseline-test.db'; import pytest; raise SystemExit(pytest.main(['tests','-q','-p','no:cacheprovider']))"
```

Build Go: não executável por ausência de toolchain. Testes existentes cobrem billing simulado, business, plans, sanitize, scope e severity; não cobrem BOLA nem sessões. Rotas inventariadas em `docs/baseline_routes.txt`; hashes dos arquivos de origem em `docs/baseline_files.json`.

## Backlog inicial

| Prioridade | Evidência inicial | Ação |
|---|---|---|
| P0 | app/db.py:354,370,438,444; app/scans/routes.py:230 | Reproduzir e bloquear consultas de objetos/listas entre organizações |
| P0 | app/autonomous/routes.py:90; runner.py:64 | Autorizar polling por organização, inclusive metadados/eventos |
| P0 | app/auth/decorators.py:79 | Remover bypass global de admin e consultar identidade ativa no banco |
| P0 | app/db.py:175; app/config.py:53 | Seed apenas DEMO explícito, guarda de inicialização de produção |
| P0 | app/billing/routes.py:70 | Troca fictícia apenas demo; nenhuma concessão de produção |
| P0 | app/scans/routes.py:34; core/checks/; app/autonomous/ | Suspender execução real pela web até worker/agente seguro; sem probes invasivos |
| P0 | app/reports/routes.py:33,62; app/scans/routes.py:106 | Export e IA baseados em dados persistidos autorizados, CSRF |
| P1 | app/db.py; app/scope.py | Memberships, delegação expiráveis, aprovação/expiração/revogação de escopo |
| P1 | app/; static/ | API v1, contratos, fluxo integral de laboratório |
| P2 | requirements.txt; scanner_go/ | Lock, CI, toolchain Go, builds Windows/Linux, release independente |

Falhas de segurança só são confirmadas após testes isolados; este inventário sozinho não é prova de exploração.
