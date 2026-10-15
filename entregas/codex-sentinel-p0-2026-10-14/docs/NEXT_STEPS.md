# Checkpoint reentrante — 14/10/2026

## Estado

Especificação lida integralmente. Origem local limpa no commit `b888fb9ff818af06f79686833031ebdf42aee47f`, preservada em Desktop/scanner/cymag_saas. Workspace astro recebeu código, sem Git/venv/banco/segredos da origem. Consulte baseline_files.json antes de comparar alterações. Não recopie a origem sobre este trabalho.

Fase 0 registrada, parcial quanto ao toolchain Go/checks indisponíveis. Fase 1 implementada parcialmente com regressões de segurança; fases 2–6 não iniciadas. Executor real, exploração autônoma e LLM externo permanecem desativados; demo fictícia em navegador é a alternativa local. Nenhum trabalho continua em segundo plano após a sessão.

## Retomar pela fase 1

1. Ler IMPLEMENTATION_LOG.md e executar os checks abaixo. Conferir diff/hashes; não assumir que o destino tenha Git.
2. Completar autorização com prova, responsável, intensidade, janela, expiração e revogação; estados `draft/pending_approval/approved/revoked/expired`, testes negativos e UI correspondente. Não reativar o scanner legado.
3. Implementar delegação por tenant com prazo/justificativa/revogação e testes; MFA e recuperação segura. Completar migração/revisão de contas sem membership, auditoria append-only, retenção/criptografia e saneamento de evidências históricas.
4. Revisar RBAC de todas as rotas, incluindo billing/owner e suporte; ampliar matriz de BOLA em cada nova rota. Instalar/verificar toolchain Go em ambiente autorizado, sem declarar builds prontos.
5. Somente após aceite P0, seguir fase 2 (modelo/API v1/OpenAPI/fluxo integral simulado), 3 (fila/worker/agente/CLI), 4 (web e e2e), 5 (copiloto/relatórios/entitlements), 6 (release).

## Rodar no Windows atual (dependências locais já disponíveis)

```powershell
& C:/Users/47191173840/Desktop/scanner/cymag_saas/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
node --test --test-isolation=none tests/frontend-api.test.cjs
node --check static/cymag.js
node --check static/cymag-demo.js
python -m compileall -q app core tools tests
```

`--test-isolation=none` evita subprocesso bloqueado pelo sandbox (node --test padrão deu spawn EPERM). Pytest original com tempfile global falhava neste sandbox; testes de integração agora criam/removem bancos únicos em instance, sem alterar banco de cliente.

## Inicialização local

Sem demo, crie owner manualmente com senha sem default:

```powershell
$env:ASTRO_ENV='development'
$env:DEMO='false'
& C:/Users/47191173840/Desktop/scanner/cymag_saas/.venv/Scripts/python.exe tools/bootstrap_local.py
& C:/Users/47191173840/Desktop/scanner/cymag_saas/.venv/Scripts/python.exe run.py
```

Demo backend explícito: `DEMO=true` e **outro CYMAG_DB_PATH** reservado a fixtures. Demo visual existente é client-side; não depende do executor real. Não misturar banco demo com registros locais reais.

## Windows/Linux em ambiente com dependências provisionadas

```text
python -m pytest tests -q -p no:cacheprovider
node --test --test-isolation=none tests/frontend-api.test.cjs
python tools/bootstrap_local.py
python run.py
```

Em Linux, use `export ASTRO_ENV=development DEMO=false`. Instalação de dependências em ambiente com rede: `python -m venv .venv` e `python -m pip install -r requirements.txt` dentro do venv; requirements legado ainda não está pinado. Esses comandos de provisionamento/Linux não foram executados nesta sessão.

## Rollback SQLite (parar app/worker primeiro)

```text
python tools/restore_sqlite.py --backup instance/SEU_BANCO.db.pre-tenant-UTC.bak --database instance/SEU_BANCO.db
```

Use caminhos reais do backup gerado, nunca o placeholder literalmente. O restore conserva snapshot do estado anterior. Validar rollback com o código anterior, antes de iniciar a versão nova. Não executar contra banco real nesta sessão.

## Documentação ainda pendente

Completar PRODUCT_VISION, SERVICE_CATALOG, USER_JOURNEYS, INFORMATION_ARCHITECTURE, AGENT_CLI_SPEC, AEGIS_SPEC, DIVISAO_DESENVOLVIMENTO, CONTRATOS_ENTRE_MODULOS, ROADMAP_FUTURO e CONTRIBUTING conforme os incrementos implementados. Não preencher documentos com êxitos hipotéticos nem substituir a implementação por texto.
