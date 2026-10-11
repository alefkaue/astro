# UX Onda 3 — correções após inspeção real (Claude, 2026-10-11)

Mesmas regras (só frontend, sem funcionalidade fingida, sem commit/push, sem servidor/navegador, changelog oficial, testes). Conclua G1–G8 e entregue lista para reconferência.

Conferido OK: Admin com menu "Administração" próprio; Equipe com bloco de contexto e datas humanas; Ajuda por tarefa; glossário presente (7 termos); fluxo IA com "Aplicar e ativar" desabilitado até teste; sem overflow horizontal em 390px; TASKS/CHANGELOG atualizados.

**G1 (P1) Configurações: navegação lateral coberta pelo cartão "Status do AEGIS".** Medido no navegador: `.settings-nav` (left 404, top 160, h 207) fica sob o bloco de status (top 167, largura total 1376), escondendo os botões "Organização" e "Equipe" (só "Integração de IA" e "Operação interna" aparecem). Corrigir o grid/posicionamento: nav em coluna própria (≈200px) e status/conteúdo na coluna ao lado, sem sobreposição; em ≤720px nav vira abas roláveis no topo. Teste: assertion de que nav e status estão em células de grid distintas.

**G2 (P2) Redundância.** Para Admin, a sidebar já lista Configurações · Equipe · Integração de IA e a página repete a mesma navegação interna; e o cartão de IA tem dois parágrafos com a mesma instrução ("Teste a conexão sem salvar…" e "Cole a chave…"). Corrigir: manter uma só navegação (a da página ou a da sidebar, não ambas) e UM parágrafo de instrução. Mostrar "Não testada/Teste OK/Falhou/Ativa" como selo (badge) visível junto dos botões, não texto solto.

**G3 (P1, honestidade) "Cliente: ASTRO (equipe)" está semanticamente errado** na visão da Equipe: é o nome da própria organização, não de um cliente. Corrigir para dois campos: "Organização atual: ASTRO (equipe)" e "Cliente: não vinculado a esta avaliação" (pendência) até existir vínculo real; ajustar espaçamento entre esse bloco e o título/eyebrow da página (hoje colados). Manter o aviso "troca entre organizações ainda não está disponível".

**G4 (P3) "· sem nome cadastrado" repetido em toda linha**, em monoespaçada. Usar texto normal, cor secundária e mais curto ("sem nome"), ou omitir na lista e mostrar só no detalhe.

**G5 (P2) Home do Admin quase vazia** (um cartão + vazio) e a sidebar tem 4 itens de administração que se sobrepõem. Transformar os botões Organização/Equipe/Integração de IA em cartões com 1 linha de estado REAL (ex.: "IA: offline", "Plano: <plano simulado>", "N pessoas na equipe — somente leitura") usando dados já disponíveis; sem números inventados. Reduzir a sidebar a: Administração · Equipe · Integração de IA (Configurações = Organização).

**G6 (P2) Mobile (390px): topbar apertada** — título trunca ("Panorama de segura…") com "Sistema ▾" e "Ajuda" ao lado. Corrigir: Ajuda vira item do menu hambúrguer em ≤480px; tema só ícone; título pode ocupar 2 linhas ou usar título curto.

**G7 (P2) Glossário: indicador de termo quase invisível** (sublinhado pontilhado fraco e descolado). Usar `text-decoration: underline dotted; text-underline-offset: 3px`, contraste ≥3:1 contra o fundo nos dois temas, cursor `help`, e foco visível por teclado. Adicionar teste de contraste do token usado.

**G8 (P3) Seção restrita sem saída.** Ao abrir `/app/settings?tab=ai` como Dono aparece "Esta seção exige um papel autorizado" e nada mais (título da página ainda "Organização e equipe"). Corrigir: dizer quem acessa ("Administradores da organização"), e oferecer link "Voltar para Organização" e "Ajuda".

Entrega: arquivos tocados, mudança por item, testes, e rota+estado de cada G para eu reconferir (G1 e G3 primeiro).
