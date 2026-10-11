# UX Onda 3 — fechamento (Codex executa TUDO até acabar)

Mesmas regras: só frontend (`index.html`, `static/*`, testes `tests/*.cjs`), identidade e temas preservados, nada de funcionalidade fingida (controle indisponível aparece como indisponível, com explicação), sem commit/push, sem iniciar servidores/navegadores, registrar item a item em `docs/agents/CHANGELOG_AGENTS.md`. Ao final rode todos os `tests/*.cjs` e `docs/agents/run_checks.py` e entregue a lista de seletores/telas para o Claude reconferir no navegador. Não pare no meio: conclua todos os grupos abaixo.

Fontes: `ANALISE_VISUAL_E_UX.md` (AV), `ANALISE-UX-ASTRO-CYMAG.md` (AU), `docs/agents/UX_WAVE2_FIXES_CODEX.md` (F11).

## Pesquisa que fundamenta
- Configurações: agrupar por ESCOPO (pessoal · organização · integrações · avançado), títulos descritivos, descrição curta no topo de cada seção, itens com URL própria; botão de salvar sempre visível (Box, GitLab, techinterview).
- Ajuda: camadas — rótulo sempre visível → tooltip curto (<80 caracteres) → popover de 1–3 frases → link para documentação; rótulo simples não precisa de tooltip; essencial visível, complementar atrás de popover; link de ajuda sempre no cabeçalho (PatternFly, LogRocket).
- Integração (IA): botão "Testar conexão" ao lado de "Salvar/Aplicar", teste real sem persistir, falha nomeia a causa específica do campo, sucesso diz o que foi alcançado; selecionar de lista em vez de pedir texto cru quando possível (Pigment, Unify, Simplechat, Truto).

## Grupo A — Resíduos da Onda 2 (rápidos)
- **R1** Modal de análise: trocar o prefixo "Somente se confirmado:" repetido 5× por UM aviso no topo da lista ("Estes passos só valem se o achado for confirmado") quando `verification_status` ≠ confirmed; remover o prefixo dos itens.
- **R2** Anel de foco: após abrir link direto/trocar rota aparecem linhas brancas verticais enquadrando o conteúdo (foco programático no container principal). Usar `:focus:not(:focus-visible){outline:none}` no container focado por script e manter anel visível para teclado real.
- **R3** Filtros no mobile: grade 2 colunas alinhada, selects com largura uniforme (100% da coluna), rótulos alinhados.
- **R4** Cartões mobile: valores que não são código (Escopo "Não registrado", status, datas) em fonte normal; monoespaçada só para IP/ID/alvo.

## Grupo B — Papéis (F11, UX-14)
- **Admin** deixa de ser cópia do Analista: página inicial/atalhos de administração (Configurações, equipe, IA) sem inventar métricas; menu com seção "Administração" destacada.
- **Equipe ASTRO**: visão multi-cliente honesta — mostrar o cliente/organização atual em destaque em avaliações, fila e detalhe ("Cliente: …" ou "Cliente não vinculado" como pendência); explicar que a troca entre organizações ainda não existe (sem seletor falso). Sem aparentar gestão de carteira completa.
- Fila de validação/laudo: coluna Cliente explícita; mover "Operação interna legada" para um item de menu próprio "Operação interna" (somente papéis que já têm acesso), com descrição do indicador de risco legado (origem e significado) e rótulo "legado" claro.

## Grupo C — Configurações e IA (UX-15, UX-20)
- Reorganizar `/app/settings` em seções com navegação lateral/âncoras e URL própria: **Organização** (conta, papéis, plano/assinatura simulada rotulada), **Equipe** (leitura; explicar capacidades indisponíveis), **Integração de IA** (admin), **Operação interna** (ver B). Cada seção com 1 frase de descrição no topo. Nomes de papel uniformes com o resto da UI.
- **IA**: sequência visível Testar → Aplicar com dois estados separados e rótulos de status ("Não testada" · "Teste OK: <o que foi alcançado>" · "Falhou: <causa>" · "Ativa" / "Offline"); "Aplicar e ativar" desabilitado até haver teste OK do valor atual (se editar o campo, volta a "Não testada"); botão primário só um por vez; avançado (endereço/endpoint) recolhido; "Restaurar padrão" com texto do que será restaurado e confirmação inline. Provedor × modelo × endereço claramente distintos. Nunca exibir a chave.

## Grupo D — Ajuda, glossário, login (UX-19, AV login)
- **Ajuda por tarefa**: página `/app/help` com blocos "Quero…" por papel (Dono: entender o painel / autorizar um alvo; Analista: iniciar avaliação / investigar um achado; Diretoria: ler a síntese), 3–5 passos curtos cada, e a distinção "Não encontrado · Não verificado · Confirmado" em linguagem simples. Manter o conteúdo atual de método/limitações numa seção "Método e limites".
- **Glossário contextual**: componente único de termo (`hosts`, `achado`, `escopo`, `cobertura`, `CVSS`, `CIDR/IP`, `não classificado`) com popover de 1–3 frases acionável por teclado (Enter/Esc, `aria-describedby`); aplicar nos termos nas telas Dono/Diretoria/Autorizações/Resumo; sem tooltip para rótulos já simples. Link "Ajuda" no cabeçalho.
- **Login**: remover texto "Conta real (backend)" (trocar por "Entrar com conta"), "Chave de acesso" → "Senha ou chave de acesso" com dica; sem prometer recuperação inexistente — mostrar "Esqueceu o acesso? Fale com o administrador da sua organização." Simplificar "inventário TCP"/"nível enterprise" na landing com exemplos simples do benefício.

## Grupo E — Apresentação (UX-21, UX-22, UX-23)
- **Datas humanas**: função única; "11 de out. de 2026, 15:03 (UTC-3 / horário local)" nas telas de Dono/Diretoria/Relatórios; UTC e ISO só no detalhe técnico/tooltip.
- **Nome do ambiente**: quando o escopo tiver nome, exibir "Nome · IP" em histórico, relatórios e detalhe; sem nome, IP + "sem nome cadastrado".
- **Relatórios**: cartões menos decorativos e mais informativos (alvo/nome, data humana, contagens por estado, status "gerado sob demanda"); diferença Relatório técnico × Relatório com IA explicada, e quando a IA está offline a opção aparece desabilitada com motivo. Na aba Relatórios do detalhe, para Dono/Diretoria mostrar resumo em vez da tabela completa de achados.

## Entrega
Por item: arquivos, o que mudou, testes novos. Liste ao final "para o Claude conferir": rota + seletor/estado para cada grupo (A–E). Atualize `docs/agents/TASKS.md` com UX-01…UX-24 como done/parcial e o que ainda depende de backend.
