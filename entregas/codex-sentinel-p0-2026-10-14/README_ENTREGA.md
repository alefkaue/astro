# Entrega Codex — ASTRO Sentinel P0

Data: **14/10/2026**. Esta pasta contém código executável, testes e documentação do primeiro incremento de segurança. **Não é uma versão pronta para produção e não conclui todas as fases da especificação.**

## Por que uma pasta separada

O pacote preserva o código existente na raiz do repositório `alefkaue/astro`. Não substitui arquivos da aplicação atual. A implementação partiu da cópia local `cymag_saas`, commit `b888fb9ff818af06f79686833031ebdf42aee47f`. O repositório remoto estava em `e708177dd03f704647a7710fd4a2fc0495239ece` ao preparar esta publicação. Este pacote não afirma incorporar todas as alterações posteriores ao baseline local; a integração com a raiz deverá ser feita por revisão incremental.

## O que foi implementado

- **Isolamento por organização:** organizations/memberships, `organization_id`, filtros no SQL, checagem de posse e respostas 404 para objetos de outros tenants. Papéis da plataforma não concedem acesso global aos clientes.
- **RBAC:** permissões para escopo, avaliação, exportação e decisões; viewer não escreve e analyst não aprova escopo. Permissões e vínculos são lidos no banco, sem confiar no papel do cookie.
- **Sessões e autenticação:** bloqueio de usuários/vínculos desativados, versão de sessão rotacionada no login/logout, invalidação de cookie antigo, CSRF com rotação e verificação de Origin, rate limit persistente por email/IP.
- **Demo e configuração:** contas previsíveis e checkout simulado somente com `DEMO=true`. Inicialização de produção/staging recusada enquanto PostgreSQL e requisitos P0 estiverem pendentes. Bootstrap local interativo sem senha padrão.
- **PDF e AEGIS:** conteúdo selecionado no servidor por scan/finding autorizado; o cliente não pode substituir a evidência por payload forjado. Fallback determinístico identificado, somente sugestões e sem execução de comandos. Transferência a LLM externo desativada até consentimento e controles próprios.
- **Dados e migração:** migração SQLite idempotente e registrada, FK/index, dados órfãos/conflitantes mantidos sem associação arbitrária, backup online antes da migração legada, restore frio com preservação do estado anterior. Conexões SQLite agora são fechadas ao sair do contexto.
- **Evidências e API:** redaction conservadora de segredos em evidências/auditoria novas, validação de entrada, limite de corpo, headers de segurança e erros com request_id.
- **Frontend:** integração de CSRF/JSON, identificação persistida de scan/finding, token no PDF, rotulagem de valores e bloqueio do checkout real. Fora de demo, preços ficam sob validação comercial e perdas financeiras não são inventadas.

## Recursos temporariamente suspensos

Scan real síncrono pela web, pentest autônomo por threads, cadeia de exploração e descoberta da rede do servidor estão bloqueados. O runner também recusa novas execuções. O código técnico foi preservado para adaptação futura; esses controles não devem ser removidos para fazer a demonstração funcionar. A demo fictícia client-side permanece como alternativa local.

Worker/fila durável, agente seguro Windows/Linux, CLI, autorização por conexão e kill switch devem ser implementados na fase 3, depois do aceite P0. Nenhum alvo externo foi varrido nesta entrega.

## Testes realizados

| Validação | Resultado |
|---|---|
| Baseline anterior às correções | 49 testes Python passaram |
| Reprodução inicial de segurança | 10 falhas confirmadas em fixtures de duas organizações; corrigidas |
| Suíte Python após implementação | 100 testes passaram |
| Cliente JS: rotação CSRF, mutação sem payload e leitura | 3 testes passaram |
| Sintaxe dos dois arquivos JS | Passou |
| Compilação sintática Python | Passou |
| PDF real com dados fictícios autorizados | Passou |
| Migração, quarentena, backup, restore e integridade SQLite | Passou |
| Smoke Flask local | Index/health/CSRF 200; usuário não autenticado 401 |
| Build Go / Windows / Linux | Não executado: toolchain Go indisponível |
| Browser e2e F1–F6 / PostgreSQL | Não executado; pendente |

Há 10 warnings de depreciação do parâmetro `ln` no gerador PDF legado; não impediram a geração. Testes verdes não equivalem a auditoria independente.

Antes da publicação, os testes foram repetidos dentro desta pasta: **100 testes Python passaram em 60,44 s e 3 testes JS passaram**; checks de sintaxe JS e compileall Python passaram. Conferência do pacote: 90 arquivos, sem bancos/backups/segredos locais e sem correspondências para os padrões conhecidos de tokens GitHub/Groq/AWS ou chaves privadas pesquisados. Isso não substitui um scanner completo de segredos. Não há modificações ou exclusões dos arquivos existentes na raiz do repositório.

## Como executar

Execute os comandos **dentro desta pasta**, não na raiz do repositório. Provisionamento de dependências requer rede; o fluxo local deve funcionar sem IA externa. As dependências legadas ainda não estão pinadas.

### Windows / PowerShell

```powershell
cd entregas/codex-sentinel-p0-2026-10-14
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
$env:ASTRO_ENV='development'
$env:DEMO='false'
& ./.venv/Scripts/python.exe tools/bootstrap_local.py
& ./.venv/Scripts/python.exe run.py
```

### Linux

```bash
cd entregas/codex-sentinel-p0-2026-10-14
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export ASTRO_ENV=development DEMO=false
python tools/bootstrap_local.py
python run.py
```

Provisionamento novo e execução em Linux não foram testados nesta sessão. O servidor local padrão é `http://127.0.0.1:5000`. O bootstrap solicita senha manualmente; não passa segredos na linha de comando.

### Repetir validações

Com o Python do venv:

```text
python -m pytest tests -q -p no:cacheprovider
node --test --test-isolation=none tests/frontend-api.test.cjs
node --check static/cymag.js
node --check static/cymag-demo.js
python -m compileall -q app core tools tests
```

No PowerShell sem ativação, substitua `python` por `& ./.venv/Scripts/python.exe`. Use Node com suporte a `--test-isolation=none`; essa opção evita subprocessos bloqueados no ambiente original. Bancos fictícios dos testes são criados/removidos em `instance/`.

Para seed demo backend, use explicitamente `DEMO=true` e um `CYMAG_DB_PATH` separado, reservado a fixtures. Não misture dados demo e registros reais. `.env.example` não contém credencial válida.

## Estado das fases e pendências

| Fase | Estado |
|---|---|
| 0 — baseline | Registrado; parcial quanto a Go/checks indisponíveis |
| 1 — segurança/multitenancy | Incremento implementado/testado; fase ainda parcial |
| 2 — produto/contratos | Não iniciada, aguardando aceite P0 |
| 3 — motor/worker/agente/CLI | Não iniciada, aguardando aceite P0 |
| 4 — experiência web | Não iniciada; ajustes de compatibilidade pertencem à fase 1 |
| 5 — inteligência/relatórios/comercial | Não iniciada; barreiras de segurança pertencem à fase 1 |
| 6 — release/piloto | Não iniciada; produção recusada |

P0 restante: MFA/recuperação, delegação temporária, comprovação/janela/expiração/revogação de escopo, validação por conexão, auditoria append-only, criptografia/retention, saneamento de evidências históricas, constraints adicionais e revisão independente. Não foram feitos deploy, cobrança, compra de serviços ou anúncio de conformidade legal.

## Arquivos e evidências

- [IMPLEMENTATION_LOG.md](docs/IMPLEMENTATION_LOG.md): arquivos alterados, testes, resultados e pendências por fase.
- [BASELINE_2026.md](docs/BASELINE_2026.md): origem e comportamento anterior às alterações.
- [changed_files.json](docs/changed_files.json): 21 arquivos modificados e documentos/código adicionados em relação ao baseline local.
- [DATA_MODEL.md](docs/DATA_MODEL.md): modelo e migração/rollback.
- [API_CONTRACTS.md](docs/API_CONTRACTS.md): contratos atuais e mudanças de compatibilidade.
- [SECURITY_REQUIREMENTS.md](docs/SECURITY_REQUIREMENTS.md) e [THREAT_MODEL.md](docs/THREAT_MODEL.md): controles e riscos residuais.
- [NEXT_STEPS.md](docs/NEXT_STEPS.md): checkpoint detalhado da implementação original; contém caminhos do ambiente original.
- [README_LEGADO.md](README_LEGADO.md): documentação anterior preservada; capacidades e preços legados não representam readiness atual.
- [ESPECIFICACAO_ASTRO_SENTINEL_CODEX.md](ESPECIFICACAO_ASTRO_SENTINEL_CODEX.md): especificação integral usada.

Não foram incluídos `.env`, bancos, backups, credenciais, `instance/`, ambientes virtuais, caches ou executáveis. Arquivos demo podem conter senhas fictícias de fixture; elas não são contas de produção.
