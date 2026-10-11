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
