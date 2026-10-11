# Integração das propostas encontradas

Materiais extraídos em `../materials/inspection-20261010/` em relação ao repositório. Cada ZIP tem `CONTENTS.json` com a listagem completa. Nenhum script ou instalador extraído foi executado; dependências dos protótipos não foram instaladas.

| Critério | design-system-astro | astro-mono-luxe-main |
| --- | --- | --- |
| Tecnologia | Next.js 16.4, React 19, Tailwind 4, Base UI | React 19, TanStack Start/Router, Vite 8, Tailwind 4, Radix/shadcn |
| Estrutura | page.tsx concentra superfícies e navegação por state | Rotas separadas, shared.tsx e componentes por superfície |
| Reuso | Button e tokens; pouca divisão de domínio | Shell, Panel, Heading, Metric, Badge, Drawer e componentes UI |
| Marca | Monocromático editorial, logo feita com texto, Arial e superfícies bege | Instrument Sans, mono, cards e terminal; logo improvisada |
| Dashboard | Grid denso e composição industrial | Tabelas, filtros, estados vazios e atividade mais reutilizáveis |
| Scanner | Console demonstrativo com painel lateral | Eventos simulados, metadados, evidências e detalhe |
| Navegação | Mistura PF/PJ/cyber; não há rotas por módulo | Rotas melhores, porém ativos/achados/relatórios compartilham overview por query |
| Responsividade | Breakpoints 900/600, sidebar ocultada | Breakpoints 1100/760, sidebar compacta e grids empilhados |
| Acessibilidade | Alguns labels; vários controles sem ação real | Labels e dialog; falta foco preso/retorno de foco/Escape no Drawer |
| Dados | Simulados | Simulados; contagens fixas não necessariamente consistentes |

Decisão: aplicar ao frontend Flask funcional os padrões visuais dos dois. Mono Luxe fornece separação dashboard/console, uso de mono, cards e evidências. Next fornece hierarquia editorial, composição de métricas e contraste. São adaptações de apresentação; **nenhum TSX foi importado como componente funcional**. Evita trocar endpoints reais por mocks e adicionar dois runtimes SSR concorrentes. Uma futura migração React exige contrato completo, testes e decisão registrada.

Aplicado: tokens oficiais, botão/input/card, SVGs verdadeiros, tema, console com run ID/timestamp real, tabela de achados com validação/evidência, dashboard persistido e relatório com identidade ASTRO.

Excluído da integração: finance.tsx, rotas personal/business, carteiras PF, contas PJ financeiras, Pix, transferências, saldos, cartões bancários, impostos e extratos. ZIPs preservados como referência; nenhuma dessas superfícies é servida pelo Flask. Assinatura do SaaS legado permanece separada, explicitamente simulada onde aplicável; não é conta bancária.

Não aproveitar alegações dos protótipos como “ALL SYSTEMS OPERATIONAL”, “ENCRYPTED WORKSPACE”, versão inventada ou métricas fixas. Não usar logos improvisadas. Dashboard não apresenta ausência de avaliação como segurança comprovada.

## Atualização 2026-10-11 — pacote de redesign

Integração detalhada e resultados em [REDESIGN.md](REDESIGN.md): navegação por URLs, avaliações com wizard/detalhe, API tenant-scoped, escopos com autorização owner e viewer somente leitura. Implementação por Codex. Claude executado pelo shell terminou exit 1 / ECONNREFUSED, sem alterações. 113 testes Python e contratos frontend passaram. QA visual continua pendente: Edge falhou por acesso negado e exibiu 0x80000003; não contornar proteções do ambiente. Scanner e dados reais preservados nesta etapa.

## Experiencias por perfil — 2026-10-11

Implementacao Codex em EXPERIENCE_UI.md: sidebar por funcao, panorama executivo, centro operacional, galeria de relatorios e escopos em duas colunas. Dados das APIs existentes, sem alterar permissoes/scanner. Contratos frontend/boot/experiencia passaram; 8 regressoes Python passaram. Browser visual permanece pendente; Claude tem tarefa de revisao somente leitura preparada (-Task experience), ainda nao executada.
