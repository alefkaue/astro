# ASTRO Cyber — design system

Implementação atual: `static/astro.css`, carregado depois do CSS legado, sem outro frontend. `static/astro-theme.js` aplica tema antes da pintura e persiste apenas a preferência visual. Identificadores internos CYMAG e rotas mantidos para compatibilidade.

| Token | Claro | Escuro |
| --- | --- | --- |
| Fundo | #F2F2F2 | #0A0A0A |
| Superfície | #FFFFFF | #141414 |
| Secundária | #F2F2F2 | #242424 |
| Texto | #0A0A0A | #F2F2F2 |
| Primário / texto | #0A0A0A / branco | branco / #0A0A0A |
| Borda | #E2E2E2 | #3A3A3A |
| Texto secundário | #6B6B6B | #8C8C8C |

Instrument Sans na aplicação, JetBrains Mono para identificadores, evidências e console. Fontes carregadas do Google Fonts; self-host e revisão de licença/disponibilidade offline pendentes. PDF usa SVG oficial e fontes padrão do gerador; embutir Instrument Sans no PDF está pendente.

Botões 14px, inputs 16px, cards 20px. Sem azul, roxo ou verde de marca. Verde #1F9D55 para sucesso, âmbar #B7791F para atenção e vermelho #D93025 para risco/erro. Cinzas para informação e observações.

SVGs oficiais copiados sem redesenho para `static/brand/`; duas variantes conforme tema e branco sobre a landing escura. PDF renderiza o SVG branco como vetor. Console sempre escuro, eventos reais via polling, timestamps UTC e run ID. Não há progresso artificial ou cancelamento de fachada.

Foco visível, skip link, aria-live nos eventos/toasts, evidências em details/summary nativo e reduced-motion. Layout responsivo existente preservado. Revisão de contraste semântico, teclado de todos os modais e QA visual em 320/375/768/1024/1440/1920px continuam pendentes; não afirmar conformidade WCAG.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.

## Experiencias por perfil — 2026-10-11

Implementacao Codex em EXPERIENCE_UI.md: sidebar por funcao, panorama executivo, centro operacional, galeria de relatorios e escopos em duas colunas. Dados das APIs existentes, sem alterar permissoes/scanner. Contratos frontend/boot/experiencia passaram; 8 regressoes Python passaram. Browser visual permanece pendente; Claude tem tarefa de revisao somente leitura preparada (-Task experience), ainda nao executada.

Auditoria parcial de contraste: verde/branco 3.49, ambar/branco 3.64, vermelho/#141414 3.86; insuficientes para texto normal 4.5:1. Texto de status/erro alterado para monocromatico, cores semanticas em indicadores. Microtexto ampliado. Ver COMMERCIAL_READINESS.md; nao comprova conformidade AA.
