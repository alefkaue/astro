# Integração do pacote de redesign — 2026-10-11

## Materiais e decisão

ASTRO_CYBER_REDESIGN_PACOTE.zip foi listado e extraído sem sobrescrita em `../materials/redesign-20261011/`. Contém ASTRO_CYBER_REDESIGN_LAYOUT.md e ASTRO_CYBER_PROTOTIPO_LAYOUT.html; CONTENTS.json registra os membros. O Markdown foi lido integralmente e o HTML inspecionado como referência, sem executar scripts extraídos. É uma proposta estrutural de navegação, não um novo framework. Aproveitados: sidebar agrupada, hierarquia dos módulos, avaliações como unidade de trabalho, filtros, wizard de quatro etapas, detalhe com abas e inspector lateral. Adaptado ao frontend Flask/JS existente, mantendo tokens monocromáticos, temas e SVGs oficiais da integração anterior.

Não integrar dados sintéticos do protótipo à API real. Não criar inventário global, gestão de achados e correções sem modelos persistidos. Nenhuma funcionalidade bancária foi introduzida. Assinatura comercial fica em Configurações, identificada como simulada. Scanner não foi modificado nesta etapa.

## Implementação Codex

| Rota | Fonte / comportamento |
| --- | --- |
| /app/overview | /api/dashboard, métricas persistidas e histórico real |
| /app/assessments | /api/scans, filtros status e busca na URL |
| /app/assessments/new | Escopo autorizado → modo → limites → revisão; APIs existentes |
| /app/assessments/:id | /api/assessments/:id, resumo/console/hosts/achados/cobertura/relatórios |
| /app/scopes | Cadastro e autorização reais; owner/admin autoriza, viewer somente consulta |
| /app/reports | Avaliações concluídas e PDF sob demanda |
| /app/settings | Organização/equipe/plano; configurações de IA só admin |
| /app/help | Método e limitações explícitos |
| /login e /demo | Entradas; demonstração sintética separada da sessão real |

History API oferece links diretos e navegação voltar/avançar. Flask serve o mesmo index nessas rotas; /api desconhecida continua 404. Base de assets é corrigida somente nas URLs reservadas. Todas as funções antigas continuam disponíveis para integração interna, sem dois frontends concorrentes.

Detalhe backend usa tenant da sessão; account_id fornecido por URL é ignorado. Outra organização recebe 404. Estado running sem achados continua vazio. Modo histórico e cobertura não mensurados são identificados como desconhecidos. Hosts são derivados apenas dos achados daquela avaliação.

Execução automatizada acompanha eventos via polling sequencial, guarda associação scan/run na sessão do navegador, cancela acompanhamento ao navegar e explica indisponibilidade de eventos após reinício. Não implementa cancelamento de execução nem persistência de eventos. Demonstração persiste apenas resultados sintéticos em localStorage, inclusive novas avaliações, sem fazer conexões aos ativos.

Escopos agora mostram autorização também ao owner, conforme permissão já existente no backend. POST de criação nega viewer. Carregamento de escopos com falha mostra erro em vez de lista vazia. Labels associados aos inputs; modal e menu mobile têm foco/Escape, sem afirmar conformidade completa de acessibilidade.

## Claude Code: execução confirmada, sem implementação

Claude 2.1.296 autenticado e modo -p disponível. Tarefa delimitada enviada pelo shell: rotas frontend e endpoint read-only tenant-scoped; prompt em CLAUDE_REDESIGN_TASK.txt. Invocação usou safe-mode, permissões manuais, ferramentas/arquivos restritos e sem MCP externo. Processo terminou exit 1, ECONNREFUSED, zero tokens, nenhuma edição. Resultado bruto: CLAUDE_REDESIGN_RESULT.json. Após término, Codex assumiu os arquivos do backend. Não é correto atribuir implementação nova ao Claude. Não houve controle do outro terminal, alteração de credenciais ou bypass de rede/permissões.

Para retomar colaboração, usar o prompt como referência e convertê-lo em revisão somente leitura do diff atual, pois a implementação já existe. Executar claude -p no terminal autenticado e registrar saída/código antes de integrar qualquer contribuição.

## Validação

- `.venv/Scripts/python.exe docs/agents/run_checks.py`: **113 passed**, 13 avisos de depreciação fpdf; runner agora restringe coleta padrão a tests.
- `node tests/test_frontend_contracts.cjs`: passou. Rotas, IDs inexistentes, persistência demo, transição running/done, contagens coerentes, origem sintética, ausência de fetch e temas.
- node --check em cymag.js, cymag-demo.js e astro-workspace.js: passou.
- git diff --check: passou, apenas avisos de conversão LF/CRLF.
- HTTP local em /app/assessments: 200 após encerrar a instância antiga.
- **Browser/QA visual não concluído**. Edge headless falhou por acesso negado nos processos Mojo/crashpad e exibiu 0x80000003 ao usuário. Teste CDP falhou por ECONNREFUSED; não há screenshots validados desta etapa. Não repetir nem desabilitar sandbox para contornar. tests/browser_redesign.cjs fica como teste reproduzível quando houver navegador de testes funcional; exige CDP local previamente disponível.

## Próximas tarefas

1. QA visual e teclado no navegador normal em 320/375/768/1024/1440/1920px, temas claro/escuro e todos os perfis.
2. Revisão independente Claude quando acesso à API funcionar.
3. Persistir modo, perfil, limites, cobertura e eventos por avaliação; fila durável e cancelamento seguro.
4. AEGIS contextual via IDs autorizados e fatos persistidos; remover dependência de payload livre para explicações.
5. Modelos persistidos para ativos/achados, atribuição, histórico de correção e revalidação antes de criar módulos globais.

Nenhum scan real, commit, push ou migração destrutiva foi executado nesta etapa. Banco existente preservado; testes utilizam bancos isolados.
