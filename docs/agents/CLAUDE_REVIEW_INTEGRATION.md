# Revisão Claude integrada por Codex — 2026-10-11

Colaboração confirmada: Claude foi executado no PowerShell normal do usuário através de CLAUDE_REVIEW_LOCAL.ps1. Primeira execução atingiu limite de ferramentas; retomada na mesma sessão retornou subtype=success, is_error=false, terminal_reason=completed. Resultado original preservado em CLAUDE_LOCAL_REVIEW_RESULT.json e log incremental em CLAUDE_LOCAL_REVIEW_STREAM.jsonl.

Claude fez revisão somente leitura; Codex verificou e implementou as correções. Nenhuma implementação ou execução de testes é atribuída ao Claude.

| Parecer | Decisão após inspeção Codex |
| --- | --- |
| F1: admin sem tenant autoriza escopo alheio | Confirmado e corrigido. login_required antes de role_required; UPDATE filtrado pelo tenant do autorizador. Regressão HTTP e DB para usuário sem tenant, tenant estrangeiro, tentativa de forjar tenant e operador sem permissão. |
| F2: helpers None removem filtro | Contrato legado de consultas internas confirmado. Separação global de helpers fica no backlog para auditar todos os chamadores; entrada vulnerável de F1 corrigida e função de autorização nunca executa escrita sem tenant. |
| F3: demo não desativa no logout | Não confirmado: logout original já define CYMAG_DEMO._active=false, limpa state e mostra login. Nenhum bypass novo necessário. |
| F4: marcador demo sobrepõe sessão real | Corrigido: boot consulta /api/me antes de usar marker/query demo; /demo permanece entrada explícita. enterApp real limpa marker. Teste VM executa o boot real. |
| F5: demo descrita como persistência real | Banner sintético explícito em histórico/relatórios/configurações/escopos; descrição de histórico distingue persistência apenas no navegador. |
| F6: resposta tardia do wizard força navegação | Callback guarda validade da rota; conclusão após sair informa o ID por toast, sem navegar. |
| F7: polling rouba foco/recria página | Refresh de metadados/status/contagens sem busy, renderRoute ou focus. Resultados atualizados são consultados nas abas; conclusão mostra aviso. |
| F8: falha de polling e metadados obsoletos | Retry incremental limitado nos eventos, 404 sem retry; conclusão consulta status/data de término. |
| F9: trecho redundante em escopos | Removido. Renderer original já tem labels, terminologia e restrição viewer. |
| F10: assets relativos em deep links | Base condicional já existe antes dos assets em index.html; suspeita principal não confirmada. Flask agora rejeita static/ sob rotas /app, evitando responder HTML para asset mal localizado. Regressão HTTP adicionada. |

Validação: 114 testes Python passaram, 13 avisos legados fpdf; contratos frontend passaram; syntax check JS passou. Regressões incrementais para assets e boot executadas separadamente depois da suite. QA visual e acessibilidade no navegador continuam pendentes. Nenhum scanner foi executado ou modificado nesta integração.

Pendências: refatoração explícita scoped/unscoped dos helpers de leitura (F2), decisão de visibilidade de revisão gerenciada, QA visual e rechecagem Claude dos fixes. O parecer é revisão estática, não validação em produção.
