# Contratos do incremento P0

API legada preservada. `/api/v1` e OpenAPI ainda não implementados; nenhuma alegação de conclusão da fase 2.

- `GET /api/csrf`: retorna `csrf_token`, estabelece sessão anônima. Cliente real deve enviar `X-CSRF-Token` no login e nas mutações autenticadas. Login retorna token rotacionado. Logout envia objeto JSON `{}` e invalida cookies anteriores.
- `GET /api/engagements` e `GET /api/engagements/{id}`: somente organização da membership ativa. `POST` exige `scope:write`; `/authorize` exige `scope:approve`. Aprovação é legado parcial; prova/janela/expiração/revogação ainda pendentes.
- `GET /api/scans` e `/api/scans/{id}/findings`: filtrados por tenant; findings incluem `finding_id`. IDs de outra organização retornam 404, inclusive metadados.
- `GET /api/autonomous/{id}`: progresso/eventos/report filtrados por tenant. Novas execuções reais estão suspensas.
- `POST /api/report/quick|detailed`: `{scan_id: inteiro, hosts?: lista de strings}`; exige `report:export`. O servidor escolhe alvo, score e findings persistidos. Campos de conteúdo forjados do cliente são ignorados. Detailed usa fallback sem LLM externo até consentimento implementado. Não há versões persistidas de relatórios ainda.
- `POST /api/remediation`: `{finding_id: inteiro, persona?: "exec"|"secops"}`. Seleção persistida autorizada; fallback determinístico identificado, sem comandos e sem perda financeira inventada. Payload legado `vuln` não é fonte de evidência.
- `POST /api/account/plan`: simulação somente `DEMO=true`. Fora de demo retorna 403 sem alterar entitlements. Preços e próximas cobranças de produção não são inventados; catálogo real apresenta "sob validação comercial".
- `/api/scan`, `/api/autonomous/run`, `/api/exploit_chain`, `/api/auto_discover`: retornam bloqueio explícito; não acessam redes do servidor nem iniciam threads. Alternativa atual: demo client-side fictícia. Reativação somente após controles P0 e fase 3.

Mutações exigem objeto JSON, limite de corpo 1 MiB, validação de tipos de IDs/textos/listas e origem quando presente. Erros mantêm `error` legado e acrescentam `code`, `message`, `request_id`. Headers incluem X-Request-ID, nosniff, DENY, same-origin e no-store em API.

Mudanças de frontend deste incremento: negociação/rotação CSRF, JSON em mutações sem body, token no PDF, scan_id/finding_id persistidos, bloqueio do checkout real e autorização por owner. E2E browser, catálogo final de planos, acessibilidade e interface de escopo completa continuam pendentes.
