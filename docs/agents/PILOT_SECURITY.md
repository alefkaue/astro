# Controles do piloto — 2026-10-11

Codex implementou app/features.py e os bloqueios do AEGIS. Claude forneceu a revisão comercial anterior; a nova chamada pelo shell de Codex não produziu resposta e foi interrompida (exit 1). Não houve alteração de proxies, permissões, autenticação ou execução de avaliações externas.

## Comportamento implementado

- IA e execução autônoma desabilitadas por padrão fora de development/test/demo. CYMAG_ENABLE_AI e CYMAG_ENABLE_AUTONOMOUS podem habilitar explicitamente cada recurso; isso não substitui consentimento do cliente, autorização ou habilitação por plano.
- CYMAG_ENABLE_SELF_BILLING e CYMAG_ENABLE_AUTO_DISCOVER só operam em ambientes locais. Nenhum override libera upgrades simulados ou descoberta da rede do servidor em produção/staging.
- Geração de cadeia de ataque indisponível em todos os ambientes, fora da proposta defensiva.
- AEGIS.call e test_key respeitam o bloqueio antes de qualquer chamada externa, inclusive com cliente previamente configurado.
- A UI ainda precisa consumir capacidades de implantação para ocultar controles desabilitados; atualmente a API rejeita a operação com mensagem explícita.

## Divisão com Claude

Tarefa pilot-security no script CLAUDE_REVIEW_LOCAL.ps1: Claude prepara patch e testes de contenção em core/scope.py, app/scope.py e novo tests/test_scope_safety.py. Retorno em diff somente leitura evita alterações concorrentes e permite revisão antes da aplicação. Codex mantém features, factory, AEGIS e integração. Executar no terminal autenticado do usuário, como nas revisões anteriores.

## Ainda não resolvido

Bloqueios de alvos do próprio serviço e redes especiais; política allowlist hospedada; max_ips; cobertura e truncamento; autenticação/CSRF; persistência e reconciliação de jobs; segredos do provedor; consentimento por organização; retenção e backups. Não liberar piloto hospedado apenas com estes gates. Reiniciar o processo local para carregar mudanças Python.
