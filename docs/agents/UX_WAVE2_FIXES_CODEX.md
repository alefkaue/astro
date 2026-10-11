# UX Onda 2 — correções após inspeção real no navegador (Claude, 2026-10-11)

Servidor de conferência do Claude: `http://127.0.0.1:5077` (demo). Mesmas regras: só frontend, sem commit/push, testes ao final, registrar no `docs/agents/CHANGELOG_AGENTS.md` (oficial). Você não consegue abrir navegador; trabalhe por CSS/DOM e testes, e descreva o que mudou para eu reconferir.

Fontes: `ANALISE_VISUAL_E_UX.md` (AV) e `ANALISE-UX-ASTRO-CYMAG.md` (AU), mais pesquisa (Au Fait UX/TechTarget: uma pergunta por tela, divulgação progressiva; SAP/setproduct: tabela com cabeçalho sticky e filtros fora da tabela; IANS/Bugcrowd: métrica só se leva a decisão).

## O que está certo (não mexer)
Panorama do Dono (17 em destaque + "zero confirmados"), síntese da Diretoria com "sem dados suficientes", filtros/chips/densidade, Escape fecha modal e devolve foco, rótulos nos cartões móveis, barra de demo compacta, decomposição "12 = 0+0+12+0" no Resumo.

## Defeitos a corrigir (prioridade)

**F1 (P1) Mobile: topbar ocupa ~172px de 700px (25% da tela).** Em 390px o seletor "Tema" fica numa linha própria dentro do topo fixo. (AV "Celular", UX-12/24.) Corrigir: topbar de UMA linha (menu + título + toggle de tema compacto/ícone), ≤56px; breadcrumb escondido no mobile; sem sticky se passar de 64px.

**F2 (P1) Mobile: cartões altos demais.** Cada cartão de avaliação/achado empilha um valor por linha (~400px por cartão) e há borda dentro de borda. (AV UX-04, UX-10.) Corrigir: cartão sem moldura aninhada; cabeçalho do cartão = título + severidade/status; demais campos em grade 2 colunas rótulo/valor; meta ≤ ~180px por cartão.

**F3 (P1) Achados desktop: rolagem aninhada.** `.findings-scroll` tem `max-height ≈ 582px` com scrollbar interna dentro da página, e só ~1,5 linha fica visível sem rolar a página (filtros + metadados ocupam o resto). (AV UX-09/10; SAP: sticky header para rolagem longa.) Corrigir: remover a rolagem interna; a página rola e o `thead` fica `position: sticky` abaixo do topbar; OU deixar a barra de filtros sticky e a tabela ocupar `calc(100vh - alturas fixas)`. Escolha uma e garanta ≥6 linhas visíveis em 900px de altura.

**F4 (P2) Campo de busca de achados trunca o placeholder** ("Título, descrição ou evidê…") em desktop e mobile. Corrigir: `flex: 1 1 280px; min-width` adequado ou placeholder "Buscar achado". (UX-09.)

**F5 (P1) Modal "Ver orientação de análise": numeração duplicada** ("1. 1. Confirmar…", "2. 2. Isolar…"): lista `<ol>` mais prefixo numérico no texto. Corrigir: remover prefixo do texto ou usar `<ul>`/`list-style:none`. (UX-03.)

**F6 (P1) Modal: honestidade e público.** Para achado "Sem classificação", o modal diz "Orientação não confirma o achado" mas os passos mandam "Isolar o ativo afetado da rede produtiva imediatamente" e mostram `iptables -I INPUT … DROP` e `nmap -A`, "Cadeia de ataque", MITRE, "Próximo recon" — inclusive ao Dono/Diretoria. (AV: "distinguir evidência, resultado e sugestão"; princípio honestidade do produto.) Corrigir: (a) passos de remediação prefixados por "Somente se confirmado:" quando `verification_status` ≠ confirmed; (b) comandos, cadeia de ataque, MITRE e recon dentro de `<details>` "Detalhes técnicos para a TI", fechado por padrão e ausente para os papéis owner/viewer; (c) manter "Copiar orientação".

**F7 (P2) Resumo da avaliação: cartões mostram só 12/0/0** (Registrados, Confirmados, Suspeitas) e os 12 não classificados só aparecem numa linha pequena. (AV UX-02: contadores sem contradição aparente.) Corrigir: cartões Registrados · Confirmados · Suspeitas · **Não classificados** (destacado quando >0) · Observações; a linha de decomposição vira legenda, não substituta.

**F8 (P3) Panorama do Dono: "Zero não significa risco zero" aparece duas vezes** no mesmo cartão (coluna esquerda e direita) e o cartão "Resultados classificados · 0" disputa atenção com o 17. Corrigir: manter a frase uma vez (à esquerda); reduzir o cartão da direita a secundário (tamanho/peso menores). (UX-01, uma pergunta principal por tela.)

**F9 (P2) Síntese da Diretoria é um bloco de 5 parágrafos iguais.** Corrigir: lista rotulada (Situação · Pendências · Limites · Tendência · Impacto) com rótulo em destaque e valor ao lado, e remover o que repete o hero (confirmados/pendências). (UX-08; IANS: cada item deve levar a decisão.)

**F10 (P2) Link direto/recarga cai no login.** `/app/assessments/1001` aberto direto mostra a tela de login (e título da aba genérico); depois de "Explorar demonstração" ele volta para a rota certa (bom), mas recarregar a página perde a sessão demo. (AU item 7.) Corrigir sem backend: guardar flag de sessão demo + papel em `sessionStorage` e restaurar a rota ao recarregar; título da aba do login coerente.

**F11 (registrar, não implementar agora):** Admin e Equipe ASTRO continuam com navegação e telas idênticas (mesmo menu, "Configurações"), e Equipe é indistinguível do Analista. (AU itens 3 e Equipe; AV UX-14/15.) Fica para a Onda 3 — só confirme no changelog que está pendente.

## Entrega
Arquivos tocados, o que mudou por item (F1–F10), saída dos testes (`node tests/*.cjs`, `run_checks.py`), e quais seletores/alturas você usou para F1/F3 (preciso reconferir no navegador).
