# ASTRO — briefing único para projetar produto e serviços

Versão 1 · 14/10/2026 · Documento principal para enviar à IA que ajudará a projetar a ASTRO.

**Como usar:** envie este arquivo e os arquivos atuais da plataforma. Peça que a IA execute as instruções da seção 13. O PDF executivo acompanha o planejamento do trio; o histórico arquivado é consulta opcional. Não é necessário enviar dezenas de relatórios antigos.

## 1. Contexto e decisão do trio

Somos três estudantes com conhecimentos em cibersegurança e IA. Ainda não temos produto finalizado, clientes ou orçamento relevante. Queremos construir a ASTRO como empresa de tecnologia desde o início, com duas linhas: **Segurança** e **IA e Automações**. Queremos poder adicionar serviços depois, sem reconstruir toda a plataforma.

O projeto tem código de segurança e uma vitrine com demonstração. Isso não significa que todos os percursos funcionem em produção. A IA deve conferir os arquivos atuais, identificar simulações e reaproveitar o que for adequado. A documentação antiga de “pentest autônomo completo” não define a promessa atual.

Este briefing propõe escopos iniciais concretos. Eles permitem começar a projetar, mas ainda precisam de revisão técnica e aceitação de clientes. Não foram demonstradas demanda, receita, precisão ou capacidade de suporte.

**Nesta etapa, vamos projetar primeiro: telas, percursos, estados, componentes e especificação. A lógica real vem depois.** Não publicar, integrar contas reais ou executar avaliações de rede por causa deste documento.

## 2. Como a ASTRO será usada

**Site público:** apresenta quem somos, as duas linhas e como entrar em contato. Não exige instalar nada para conhecer os serviços.

**Portal web:** aplicação com login, aberta no navegador. Cada empresa tem seus dados, usuários e serviços contratados. Segurança e IA/Automações ficam na mesma experiência, com áreas próprias.

**Conector local opcional:** programa instalado quando a tarefa exigir acesso autorizado à rede interna ou a recurso local. Um `.exe` é uma forma possível de distribuição no Windows; não será requisito para todo cliente.

**Terminal:** ferramenta de instalação/diagnóstico para técnicos. Não é a interface principal do cliente.

| Tarefa | Interface do cliente | Local de execução previsto |
|---|---|---|
| Consultar avaliações, pendências e relatórios | Portal web | Servidor e registros autorizados |
| Importar resultados de uma ferramenta | Portal web | Servidor, com revisão de formato e acesso |
| Coletar inventário em rede interna | Portal web e conector, se necessário | Ambiente local autorizado |
| Processar texto com IA | Portal web | Servidor e provedor aprovado, conforme política de dados |
| Automatizar sistemas com API acessível | Portal web | Executor no servidor e sistemas autorizados |
| Automatizar software só disponível no computador | Portal web e componente local específico | Máquina autorizada; capacidade futura a avaliar |

Nuvem não dá acesso automático à rede do cliente. Um conector de inventário também não resolve, por si só, automação de tela. Não desenvolver um aplicativo desktop completo apenas para empacotar o portal.

## 3. Oferta inicial A: Segurança com acompanhamento de ações

### O que pretendemos entregar

Organizar resultados de uma avaliação autorizada, revisar seu significado e acompanhar o que precisa ser feito. Público inicial a investigar: pequeno prestador de TI ou empresa com alguém responsável pela TI.

**Primeiro pacote proposto:** um ambiente, uma fonte de resultados acordada, até cinco pendências priorizadas e relatório de uma página. São limites de escopo para projetar, não uma tabela comercial validada. Achados adicionais relevantes não serão ocultados para cumprir a quantidade; serão registrados e tratados conforme escopo/aditivo, sem fabricar resultados.

### Entrada, trabalho humano e saída

- **Entrada:** autorização, lista do ambiente e arquivo de resultados de origem conhecida. No protótipo, tudo fictício.
- **Trabalho do trio:** conferir escopo, revisar resultados, separar observação de confirmação, definir ação e revisar o relatório.
- **Saída:** registros rastreáveis, responsável/prazo por ação, evidências e relatório com limites da avaliação.
- **Continuidade possível:** revisão periódica das pendências e revalidação contratada. A frequência e o suporte serão definidos antes da venda; não presumir mensalidade obrigatória.

### O software precisa permitir

1. Identificar empresa e ambiente.
2. Registrar escopo, autorização e origem dos dados.
3. Importar um formato escolhido e apresentar prévia/erros antes de confirmar.
4. Exibir resultado com data, origem, ativo e evidência.
5. Classificar a confiança: observação, suspeita, confirmado ou não verificado.
6. Criar uma ação com responsável, prazo, comentário e evidência.
7. Solicitar revalidação do mesmo problema por método comparável.
8. Gerar relatório rastreável e mostrar o que não foi avaliado.

**Importante:** confiança do achado e andamento da ação são coisas diferentes. Uma observação pode ter uma ação aberta sem virar vulnerabilidade confirmada. Uma ação concluída pelo usuário pode continuar aguardando verificação.

### Estados previstos

- Avaliação: rascunho → autorizada → na fila → em andamento → em revisão → concluída; com falha/cancelamento quando aplicável.
- Ação: aberta → em execução → aguardando verificação → encerrada; pode ser reaberta se a verificação falhar.
- Verificação: não realizada, inconclusiva, problema persiste ou correção verificada.

### Fora do primeiro pacote

Pentest completo, exploração ofensiva autônoma, garantia de proteção, estimativa inventada de perda financeira, certificação de conformidade, SOC 24h e correção automática de sistemas. O scanner estudado é uma fonte limitada de inventário, não prova de todas essas capacidades.

### Critérios para a primeira versão útil

Com dados de teste, completar importação → revisão → ação → evidência → relatório. Uma empresa não acessa resultados de outra. Falha de coleta não aparece como ambiente seguro. O relatório distingue observação e confirmação. A operação humana necessária fica explícita.

## 4. Oferta inicial B: IA e Automações para uma rotina

### O que pretendemos entregar

Reduzir trabalho repetitivo em uma tarefa específica. Público inicial a investigar: pequena agência ou prestador de serviços que organiza pedidos e tarefas entre sistemas.

**Primeiro pacote proposto:** uma rotina preparada pelo trio, até dois sistemas autorizados, volume acordado, teste e instrução de uso. Exemplo de projeto: pedido recebido → classificação sugerida → revisão humana → tarefa registrada. Os limites de uso serão definidos conforme o caso, antes de contratar.

Automação executa regras e passos; IA pode sugerir uma classificação ou preparar um rascunho. Não adicionar IA onde uma regra simples já resolve.

### Entrada, trabalho humano e saída

- **Entrada:** descrição do processo, campos necessários e contas/sistemas autorizados. Usar cinco pedidos fictícios para começar.
- **Trabalho do trio:** mapear a tarefa, preparar a rotina, testar exceções, configurar limites e documentar suporte.
- **Saída:** tarefa registrada no sistema de destino, histórico do que ocorreu e pendências de revisão.
- **Continuidade possível:** manutenção de conexão, tratamento de falhas e ajuste contratado. Se a rotina estável não justificar recorrência, avaliar implantação e suporte por demanda.

### O software precisa permitir

1. Escolher uma rotina preparada, com explicação de entrada e saída.
2. Configurar campos e conexão autorizada sem expor segredos.
3. Testar com dados fictícios e visualizar o que aconteceria.
4. Separar sugestão de IA, aprovação e ação executada.
5. Ativar, pausar e consultar histórico de execuções.
6. Mostrar falha compreensível e caminho de recuperação.
7. Evitar que o mesmo pedido crie duas tarefas.
8. Mostrar consumo e bloquear excedentes conforme condição contratada, sem cobrança surpresa.

### Estados previstos

- Rotina: rascunho, em teste, pronta para revisão, ativa, pausada ou arquivada.
- Execução: na fila, em andamento, aguardando aprovação, concluída, falhou, parcialmente concluída, cancelamento solicitado ou cancelada.
- Conexão: não configurada, conectada, expirada, revogada ou com erro.

Cancelar uma execução não promete desfazer uma mensagem ou tarefa já criada. Tentar novamente exige saber quais passos já tiveram efeito.

### Assistente de documentos: extensão prevista, não requisito da primeira rotina

O módulo pode acomodar depois um assistente que responde sobre fontes autorizadas, indica referências e admite informação insuficiente. Projetar seu encaixe e um exemplo demonstrativo. Não construir uma base universal de conhecimento ou exigir essa função para concluir a primeira rotina.

### Fora do primeiro pacote

Agente universal, integração com qualquer sistema, consumo ilimitado, envio externo sem controle, decisão financeira autônoma, acesso amplo ao computador e editor visual universal de fluxos. Provedor/modelo de IA e motor de automação ainda não foram escolhidos.

### Critérios para a primeira versão útil

Um pedido fictício percorre teste → revisão → aprovação → tarefa registrada. Repetir o pedido não duplica o efeito. Conexão expirada gera pendência, não sucesso fictício. O usuário entende o que a IA sugeriu e o que foi executado. Dados permanecem vinculados à empresa correta.

## 5. Núcleo comum da plataforma

| Parte comum | Necessidade inicial |
|---|---|
| Empresas e membros | Dados e acesso separados por organização |
| Serviços e capacidades | Ativar apenas os recursos contratados de cada linha |
| Perfis | Administrador da empresa, operador, aprovador e leitor; uma pessoa pode acumular funções autorizadas |
| Onboarding | Mostrar o que falta para iniciar o serviço: autorização, configuração, fonte ou conexão |
| Aprovações | Registrar ação/conteúdo exato, aprovador, validade e decisão |
| Atividade e auditoria | Quem alterou acesso, configuração, autorização e execução |
| Relatórios e arquivos | Origem, versão, acesso e exportação permitida |
| Consumo e contrato | Situação, limites e condições compreensíveis |
| Suporte | Solicitação, responsável e horário informado, sem promessa 24h |

Administrador do cliente não é administrador global da ASTRO. Operadores do trio acessam somente empresas atribuídas, com registro. Um usuário de suporte não deve receber automaticamente todas as credenciais dos clientes.

Para liberar uma ação, verificar serviço/capacidade ativa, permissão da pessoa, escopo autorizado, condição operacional e limites. A lógica futura precisa verificar isso no servidor e na execução, não somente no menu.

## 6. Telas e percursos para o design

### Site público

Início, serviços, Segurança, IA e Automações, como funciona, sobre e contato. Apresentar benefícios e limites. Diferenciar o que está em demonstração do que já pode ser contratado. Não inventar clientes, certificados, resultados ou preços.

### Portal

Início com empresa atual e próximo passo; Meus serviços; áreas de Segurança e IA/Automações; Aprovações; Relatórios; Atividade; Suporte; Configurações com equipe, conexões, consumo e conector.

Primeira entrega de design: site + entrada do portal + catálogo/serviços + um percurso completo de cada linha. Depois complementar configurações e operação interna, evitando construir muitas telas sem uma tarefa concluível.

### Cenários fictícios obrigatórios

1. Empresa Aurora: somente Segurança.
2. Empresa Horizonte: somente IA/Automações.
3. Empresa Ponte: ambas as linhas, com dados próprios.
4. Empresa nova: sem serviço e sem resultados.
5. Usuário leitor: consulta permitida, sem execução/alteração.
6. Operador interno: empresas atribuídas e área separada.
7. Falha de importação, conexão expirada, ação sem permissão e limite atingido.
8. Terceiro serviço demonstrativo: “Em planejamento”, sem compra ou execução, encaixado no mesmo catálogo.

Nomes e resultados são inventados para testar a interface. O seletor de cenários é ferramenta da demonstração, não mecanismo de segurança real.

## 7. Identidade visual obrigatória

**Manter o design preto e branco da plataforma atual. Mudar o layout para os novos serviços.** Preservar fontes, logo, linguagem de botões/campos, bordas, sombras e temas existentes. Cinzas são permitidos dentro da identidade monocromática. Não criar uma nova marca ou paleta.

A IA deve abrir os arquivos atuais de CSS, componentes, logo e telas antes de desenhar. Se faltarem, pedir os arquivos; pode antecipar o mapa funcional sem alegar fidelidade visual. Não usar as cores dos produtos pesquisados como inspiração para a ASTRO.

Sem cor de destaque em gráficos, status, erros, foco ou sucesso. Se houver indicador colorido legado, a exigência atual de preto e branco prevalece nesse ponto. Usar palavras, símbolos, contraste e padrões. Não impor fundo branco a todas as áreas se o original contém tema/áreas escuras.

O cliente precisa compreender “o que falta”, “o que aconteceu” e “o que pode fazer”. Detalhes técnicos ficam disponíveis no lugar apropriado. Garantir texto legível, teclado, foco visível, nomes claros e adaptação ao celular.

## 8. Arquitetura para a etapa de lógica

Proposta inicial: um portal e um backend organizado em módulos, com núcleo compartilhado. Isso permite começar num projeto com divisões claras, conhecido como monólito modular. Separar executores com riscos distintos e credenciais por serviço; não exige dezenas de microsserviços.

Entidades previstas: Empresa, Membro, Perfil/Permissão, Serviço, Capacidade contratada, Ambiente, Autorização, Conexão, Rotina, Execução, Aprovação, Resultado, Ação, Relatório e Evento de auditoria. Segurança e IA podem ter modelos específicos. Não misturar todo conteúdo numa tabela sem estrutura.

Execuções precisam de registro durável, versão, estado e recuperação após falha. Ações repetidas não podem duplicar efeitos. Ao iniciar, o executor verifica novamente escopo, autorização e acesso. Revogação deve afetar novas execuções e ter política explícita para as já iniciadas.

Segredos ficam fora do frontend e dos logs. Informações de um cliente não entram nas respostas ou buscas de outro. Texto de documento ou resposta de IA não vira comando confiável. Não dar shell livre ou acesso ao scanner para um assistente genérico.

A base histórica usava Flask/SQLite. A IA precisa identificar o repositório e a implementação atuais antes de propor mudanças. Não impor reescrita, framework ou banco por preferência. Avaliar concorrência, migrações, backup e operação quando a lógica for projetada; não declarar a base atual adequada à produção sem verificar.

## 9. Como acrescentar serviços no futuro

Um novo módulo declara identificador, nome, capacidades, rotas/menu, permissões, limites, tipos de execução e resultados. Também precisa de escopo comercial, responsável, dados necessários e suporte. O núcleo reutiliza usuários, contratação, atividade e relatórios.

Preparar o encaixe não significa implementar marketplace ou executar plugins de terceiros. Não anunciar funcionalidades futuras como prontas. A tela não deve exigir contratação de um serviço para acessar os dados de outro.

## 10. Requisitos fora do código

Para cada entrega real, o trio precisa de proposta com resultado, limites, prazo, preço, aceite, acessos autorizados e suporte. Precisa documentar o procedimento, testar falhas, esclarecer dados/fornecedores e saber quem cobre a operação durante provas.

Um integrante pode liderar Segurança, outro IA/Automações e outro núcleo/experiência e organização, com revisão cruzada. Todos participam da entrega e aprendem substituição. Não presumir horas disponíveis ou participação societária iguais sem combinar.

Não abrir estrutura cara só para produzir demonstração. Antes de contratar/receber, esclarecer forma de atuação, município e obrigações. Este briefing não define enquadramento tributário, preços nem salários. Não copiar valores dos estudos antigos como tabela comercial.

## 11. O que é obrigatório agora e o que pode esperar

| Agora: projeto e protótipo | Antes de cliente real | Depois, se necessário |
|---|---|---|
| Visual original e layout modular | Autenticação e isolamento verificados | Conector local próprio |
| Um percurso por serviço | Autorização, contrato e acesso seguro | Mais formatos/integrações |
| Estados vazios, erro e acesso | Execução real, limites e histórico | Editor avançado de fluxos |
| Dados fictícios identificados | Backup/restauração e procedimento de suporte | Aplicativo desktop completo |
| Catálogo e contratação simulada | Testes de falha, repetição e revisão | Novos serviços e automação mais autônoma |

O aceite do protótipo é visual/funcional simulado. O aceite para produção exige controles reais. Uma lista de recursos planejados não é declaração de implementação.

## 12. Decisões abertas que a IA deve registrar

Quem é o público inicial de cada linha? Qual formato será importado? Quais dois sistemas entram na primeira rotina? Que ações exigem aprovação? Qual volume cabe no pacote? Qual provedor de IA e política de dados? Qual motor/licença de automação? O conector é realmente necessário? Quais horas de suporte o trio consegue cumprir?

Não travar o design por essas decisões: usar exemplos identificados e registrar hipóteses. Não consolidar escolhas de fornecedor, operação ou preço sem confirmação. Ferramentas como n8n e Dify têm condições de licença a verificar antes de incorporação comercial; não copiar ou revender sua interface automaticamente.

## 13. Instrução pronta para a IA

> Leia este briefing inteiro e trate-o como especificação principal da nova ASTRO. Comece inspecionando os arquivos atuais da plataforma e registrando o que é real, simulado, reutilizável ou ausente. Preserve rigorosamente a identidade preto e branco; reorganize o layout para Segurança e IA/Automações, com expansão modular.
>
> Primeiro entregue: (1) resumo do entendimento e hipóteses; (2) mapa de páginas; (3) percursos e estados; (4) lista de componentes existentes a reutilizar; (5) protótipo navegável com os cenários da seção 6; (6) lista priorizada do que precisará de lógica depois. Implemente o protótipo visual no projeto apropriado quando houver acesso, preservando a lógica existente. Se os arquivos visuais não estiverem disponíveis, peça-os antes de inventar a identidade.
>
> No protótipo, complete importação → revisão → ação → evidência → relatório de Segurança; e configuração → teste → aprovação → execução de uma rotina. Tudo com dados fictícios e ações simuladas identificadas. Mostre diferença entre serviço não contratado, falta de permissão, configuração pendente e falha técnica. Demonstre que o layout recebe um terceiro serviço sem reconstrução.
>
> Não implemente integrações reais, cobrança, scanner novo, instalador ou lógica de produção nesta primeira etapa. Não publique, envie mensagens, conecte contas ou execute testes em rede. Não troque framework nem reescreva backend por preferência. Não prometa funcionalidades que só existem em telas.
>
> Depois da revisão do design, use os requisitos deste arquivo para propor a implementação em etapas pequenas, começando por empresa, acesso, capacidades contratadas e execução durável. Defina testes e critérios de aceite antes de liberar ações reais. Explique decisões em linguagem acessível aos três estudantes e preserve os documentos/modelos existentes.

## 14. Arquivos e histórico

Para planejar, basta este briefing. Para executar o design, a IA também precisa dos arquivos atuais da interface. No computador desta sessão, o projeto consultado fica em `C:\Users\alefk\Documents\scanner`, com `vitrine` e `cymag_saas`; esse caminho pode ser diferente em outro ambiente. Não trabalhar na cópia histórica do ZIP pensando que ela é o repositório atual.

O [PDF executivo](ASTRO_PLANO_EXECUTIVO_PARA_COMECAR.pdf) explica organização, custos e primeiros passos. O [roteiro de acordo](ACORDO_COLABORACAO_ASTRO.pdf) ajuda a registrar decisões do trio. Pesquisas, referências e versões anteriores estão no arquivo histórico, preservadas para consulta; não são instruções concorrentes ao briefing atual.
