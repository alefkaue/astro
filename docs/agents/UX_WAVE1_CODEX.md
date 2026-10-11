# UX Onda 1 — tarefa para Codex (dona do frontend)

Fonte: `../../../ANALISE_VISUAL_E_UX.md` e `../../../ANALISE-UX-ASTRO-CYMAG.md` (raiz `scanner/`). Leia os dois antes.
Regras: só frontend (`index.html`, `static/*`). Não alterar backend/scanner. Preservar identidade monocromática, temas e SVGs.
Não afirmar funcionalidades inexistentes. Rode `node tests/test_frontend_contracts.cjs` e `docs/agents/run_checks.py` ao final.
Sem commit/push. Registre o que fez em `CHANGELOG_AGENTS.md`.

## Itens (nesta ordem)
1. **UX-16** Padronizar PT-BR: `Authorized`→`Autorizado`, `Draft`→`Rascunho`, "Workspace", "Report Studio", "Security Operations"; nomes de papéis consistentes; títulos de página coerentes com o item de menu clicado (Execuções↔Avaliações etc.). Categorias internas (`smb_ad`, `iot_ot`, `remote_access`, `database`) exibidas com rótulo legível via um único mapa; manter o valor bruto no detalhe técnico.
2. **UX-04** Mobile (<=720px): linhas do histórico de avaliações e da lista de achados viram cartões com rótulo explícito por valor (`data-label` + CSS), sem depender do cabeçalho.
3. **UX-12 / UX-24** Seletor de tema sai do canto fixo e vai para o cabeçalho/topbar (ou perfil). Barra de demonstração compacta/recolhível no mobile; toasts não acumulam (máx. 1–2 visíveis, substituir o anterior).
4. **UX-13** Erros de formulário junto ao campo (texto + borda + `aria-describedby`, persistente até corrigir). Estados vazios de filtro/busca: botão "Limpar filtros", termo buscado visível.
5. **UX-05** Revisão do wizard "Nova avaliação": mostrar o alvo efetivo concreto (não "primeiro alvo do escopo") e o que acontece após iniciar. Remover texto sobre backend voltado ao usuário.
6. **UX-06** Autorizações: texto simples do que autorizar significa; rascunho nunca chamado "escopo autorizado"; para quem não pode autorizar, explicar quem pode.

Entregar: lista de arquivos tocados, o que foi feito por item, saída dos testes.
