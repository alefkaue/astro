# Entendimento e inspeção

## Objetivo da entrega

A ASTRO será uma empresa de tecnologia com duas linhas iniciais: Segurança com acompanhamento de ações e IA/Automações para uma rotina. O portal compartilha empresa, perfis, catálogo, aprovações, relatórios, atividade e suporte; cada linha tem sua própria tarefa e seus próprios estados. O terceiro módulo apenas demonstra expansão.

Esta etapa é de design e protótipo. O percurso precisa ser concluível com dados fictícios antes de escolher ferramentas, fornecedores ou implementar execução real. A promessa pública não é pentest autônomo, agente universal ou conformidade certificada.

A solicitação de manter os produtos existentes foi atendida com uma pasta nova. Não se trabalhou na cópia histórica do ZIP. Não houve alteração no scanner ou na vitrine; ambos foram registrados por hash antes da criação do projeto. Uma cópia ZIP dos dois é registrada em VERIFICACAO.md.

## Arquivos atuais inspecionados

| Origem | Evidência consultada | Situação observada | Tratamento nesta entrega |
| --- | --- | --- | --- |
| `cymag_saas/app/__init__.py` | Factory Flask e registro de blueprints | Backend real existente, com autenticação, banco e módulos próprios | Preservado; não importado nem executado |
| `cymag_saas/docs/agents/ARCHITECTURE.md` | Arquitetura e perfil defensivo documentados | Flask/SQLite, frontend HTML/CSS/JS; execução/eventos ainda descritos como não duráveis | Base para propor integração incremental depois; sem declarar produção pronta |
| `cymag_saas/docs/agents/SECURITY.md` | Controles e pendências documentados | Há controles implementados e riscos abertos. A documentação não substitui revalidação do código antes de integrar | Nenhuma certificação ou garantia inferida |
| `cymag_saas/scanner_go/main.go` | Tipos e saída JSON do scanner Go | Fonte limitada de inventário; a arquitetura documenta que o perfil atual não despacha Go | Não executado; o JSON de exemplo não é anunciado como adaptador pronto para o scanner |
| `vitrine/server.mjs` | Servidor HTTP de arquivos | Entrega estática local; sem API de negócio, sessão ou execução real | Copiado para nova pasta, com porta própria 8091 |
| `vitrine/public/model.js` | Dados, serviços e ações de exemplo | Estado frontend simulado; importação original apenas acrescentava avaliação, sem parse/prévia completa | Modelo novo na pasta nova; nenhuma edição da vitrine |
| `vitrine/public/vitrine.js` | Páginas públicas e portal | Marketing, catálogo e percursos de demonstração existentes | Composição pública reutilizada por cópia; portal refeito para o briefing |
| `vitrine/public/vitrine.css` | Layout, responsividade e controles | Base visual compatível com scanner | Cópia como `public/base.css`; complemento em `prototype.css` |
| `vitrine/public/assets/*` | CSS, script de tema e logos | Assets copiados do scanner; existem variáveis legadas de status colorido | Cópias preservadas; neutralização monocromática no CSS do novo projeto |

Não se fez auditoria integral do scanner, nem se executaram avaliações de rede, inicialização Flask ou rotinas de IA. A distinção “real” nesta tabela significa código existente, não capacidade operacional validada.

## Real, simulado, reutilizável e ausente

- **Real no protótipo:** renderização, navegação, parse/validação de arquivo local de exemplo, revisão de dados em memória, download TXT e impressão do resumo. Nenhum desses atos constitui avaliação real de segurança ou integração de negócio.
- **Simulado:** empresas, membros, contratos, autorização, sugestão de IA, conexão, tarefa no destino, execução, cancelamento, revalidação, suporte e auditoria. As telas mostram essa condição.
- **Reutilizável por cópia:** fontes, temas, logos, tokens, botões, campos, cartões, navegação, tabelas, diálogos e composição do site.
- **Ausente para produção:** autenticação, autorização no servidor, isolamento persistido, capacidades contratadas verificadas, execução durável, segredos, APIs, fila/worker, quotas atômicas, backup/restauração, fornecedores e suporte operacional.

## Hipóteses que permitiram desenhar

| Decisão aberta | Exemplo usado agora | O que falta confirmar |
| --- | --- | --- |
| Público de Segurança | Prestador de TI ou empresa com responsável técnico | Entrevistas e aceitação de cliente |
| Público de IA/Automações | Agência ou prestador que organiza pedidos | Rotina com resultado útil e volume real |
| Formato da fonte | JSON v1 próprio, fictício, por empresa/ambiente | Formato oficial e adaptador de uma origem conhecida |
| Sistemas da rotina | Caixa de pedidos e quadro de tarefas genéricos | Quais dois sistemas reais, permissões e APIs |
| Aprovação | Versão/configuração e cada pedido antes de criar tarefa | Política do cliente e atos de maior risco |
| Volume | 20 operações por sessão no cenário; cinco pedidos de teste | Limites comerciais e capacidade de operação |
| IA | Classificação pré-definida; opção de regra simples | Provedor, política de dados, custo e necessidade real |
| Motor/licença | Nenhum fornecedor incorporado | Escolha, termos e licença antes de uso comercial |
| Conector | Somente página “Em planejamento” | Necessidade de coleta interna e escopo local |
| Suporte | Solicitação em memória, sem envio; horário a combinar | Horas disponíveis do trio e substituição durante provas |

Nenhum preço, salário, participação societária, fornecedor ou regime tributário foi consolidado. O plano anterior em PDF não vira tabela comercial deste projeto.

## Componentes existentes reaproveitados

| Componente | Origem | Uso na nova pasta |
| --- | --- | --- |
| Logo claro/escuro e favicon | SVGs oficiais em `vitrine/public/assets` | Cabeçalho, site e relatório |
| Instrument Sans e JetBrains Mono | `index.html` e CSS ASTRO | Texto, identificadores e conteúdo estruturado |
| Tokens de tema | `assets/astro.css` | Superfícies, contraste, bordas, sombras e raios |
| Preferência claro/escuro/sistema | `assets/astro-theme.js` | Mesmo seletor, sem identidade nova |
| Botões/campos/cartões | `cymag.css`, `astro.css` e `base.css` | Linguagem visual preservada |
| Site público | Composição em `vitrine.js` | `site.js` copiado, com aviso de demonstração e texto alinhado |
| Sidebar/tabelas/tabs/dialog | CSS da vitrine | Organização modular com acessibilidade por teclado |
| Skip link e foco | HTML/CSS existentes | Mantidos; diálogos nativos, nomes e campos com labels |

O portal reorganiza o layout em torno da tarefa: próximo passo na visão geral, etapas do percurso, evidência e estado separados, pendência compreensível e recuperação. O assistente de documentos aparece como extensão prevista, abaixo da rotina principal.

## Estrutura da pasta nova

`server.mjs` entrega apenas arquivos públicos. `public/model.js` contém fixtures e transições simuladas; `public/app.js` contém portal, eventos e relatório; `public/site.js` contém composição pública reutilizada. `public/assets` preserva a identidade por cópia. `docs` registra design e implementação futura; `tests` contém verificações. Não há import de Python, Go, banco ou chaves do scanner.
