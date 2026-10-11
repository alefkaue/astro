# INTEGRATION — contratos e fronteiras entre agentes

## Divisão de arquivos (evitar edição simultânea)
| Área | Dono | Arquivos |
|------|------|----------|
| Dados, auth, escopo, rotas, isolamento | 🔵 Claude | `app/db.py`, `app/config.py`, `app/scope.py`, `app/auth/**`, `app/*/routes.py`, `app/reports/**`, `tests/test_tenant_isolation.py` |
| Honestidade de detecção/negócio + fixtures | 🟢 Codex | `core/business.py`, `core/checks/**`, `tests/test_business.py`, novos `tests/test_checks_*.py` |

## Contrato compartilhado: `account_id`
SEC-002 adiciona `engagements.account_id` e `scans.account_id`. Codex **não**
depende dessas colunas (trabalha em `core/`), então as tarefas são paralelas sem
conflito. Se Codex precisar do schema, consultar `app/db.py` após SEC-002 estar `done`.

## Mudanças incompatíveis previstas
- `resolve_authorized_target(engagement_id, target)` ganha parâmetro `account_id`
  (assinatura nova). Chamadores atualizados no mesmo PR (scans + autonomous).
- `POST /api/report/*` passará a exigir `scan_id` (quebra o front demo atual;
  compat temporária documentada quando SEC-006 for feito).

## Revisão cruzada
Claude revisa o diff de Codex em `core/business.py` antes de integrar; Codex (via
`codex exec review`) pode revisar o diff de isolamento. Nada é dado como testado
sem saída de `pytest`.

## Contratos da sessão ASTRO

- `GET /api/dashboard` → `{source, generated_at, counts, severity, recent, coverage, limitations}`. Sem login 401, usuário inativo/deletado 401, sem organização 403. Tenant vem de current_user; query params não selecionam outra organização. Counts: assessments/running/completed/failed/observed_hosts/confirmed/pending_validation/observations/unclassified.
- Demo implementa o mesmo contrato em `__demoApi`, source synthetic_demo, sem fetch a ativos. Backend normal source persisted_assessments. Dados demo continuam claramente identificados na barra e no relatório.
- Achado mantém chaves existentes e exibe verification_status e confidence; evidência é escapada. Desconhecido/legado → sem classificação, nunca confirmado por inferência.
- `POST /api/scan` e `/api/autonomous/run`: operator/cymag/admin ativos com organização, escopo autorizado e plano/quota. Owner/viewer recebem 403 mesmo enviando request diretamente.
- Polling autônomo já retorna scan_id; frontend agora preserva esse ID para PDF, pois report sozinho não o continha. Análise de achado no histórico usa a lista carregada, não state.lastScan.
- PDF continua montado do backend por scan_id, agora com SVG ASTRO vetorial. Não altera IDs, schema ou dados existentes.

### Reprodução de Claude (quando conectividade estiver disponível)

Na raiz do repo, em PowerShell:

```powershell
$astroTask = Get-Content -Raw docs/agents/CLAUDE_SEC007_TASK.txt
& "$env:USERPROFILE/.local/bin/claude.exe" -p $astroTask --safe-mode --strict-mcp-config --permission-mode manual --permission-prompts none --tools 'Read,Glob,Grep,Edit,Write,Bash' --allowedTools 'Read,Glob,Grep,Edit(app/auth/decorators.py),Write(tests/test_auth_hardening.py),Bash(.venv/Scripts/python.exe -m pytest tests/test_auth_hardening.py)' --output-format json
$LASTEXITCODE
```

Tarefa já concluída por Codex: antes de repetir, mudar o prompt para **revisão somente leitura** dessas correções para evitar duplicação. Resultado original em CLAUDE_SEC007_RESULT.json. A função shell claude perdeu stdin na primeira tentativa; chamada direta ao executável com prompt como argumento funcionou e chegou à tentativa de API. Não houve permission bypass, alteração de autenticação, commits ou pushes.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.

Nova tentativa por stdin e PTY e diagnóstico de rede documentados em [CLAUDE_RETRY.md](CLAUDE_RETRY.md). Revisão reproduzível no terminal do usuário: CLAUDE_REVIEW_LOCAL.ps1. Nenhuma contribuição Claude recebida nesta tentativa.

## Experiencias por perfil — 2026-10-11

Implementacao Codex em EXPERIENCE_UI.md: sidebar por funcao, panorama executivo, centro operacional, galeria de relatorios e escopos em duas colunas. Dados das APIs existentes, sem alterar permissoes/scanner. Contratos frontend/boot/experiencia passaram; 8 regressoes Python passaram. Browser visual permanece pendente; Claude tem tarefa de revisao somente leitura preparada (-Task experience), ainda nao executada.
