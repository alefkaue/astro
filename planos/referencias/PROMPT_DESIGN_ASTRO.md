# Prompt para a IA de design da ASTRO

Fonte: ASTRO_NOVA_DIRECAO_PLATAFORMA_E_PROMPT_DESIGN.md, versão 1.1.

Copie o bloco inteiro para a IA.

```text
Você vai trabalhar no DESIGN e na experiência de uma nova versão da ASTRO. Leia tudo antes de começar.

CONTEXTO
Somos três estudantes com conhecimentos em cibersegurança e IA. Ainda não temos a ideia comercial completamente definida nem uma plataforma finalizada. A ASTRO passará a ser uma empresa de tecnologia desde o início. A antiga direção centrada no scanner será ampliada.

Vamos prever duas linhas iniciais: ASTRO Segurança e ASTRO IA e Automações. Essa divisão organiza o design; os pacotes e limites comerciais exatos serão definidos depois. Queremos que novos serviços possam entrar sem refazer cadastro, navegação, acesso, relatórios e suporte.

MISSÃO DESTA ETAPA
Criar arquitetura da informação, direção visual e um protótipo navegável com dados fictícios. Priorize percursos completos e estados de interface. Lógica de produção será construída depois. Se houver código existente, primeiro identifique a estrutura e aproveite componentes úteis; preserve arquivos e não altere o scanner/backend, dados, infraestrutura, cobrança ou modelos financeiros. Se não houver repositório, entregue especificação visual e protótipo isolado adequado ao ambiente disponível. Não transforme essa etapa em migração de tecnologia.

REGRA VISUAL OBRIGATÓRIA
O design deve ser igual ao arquivo atual da plataforma ASTRO: preservar a identidade existente e mudar o layout para os serviços. Antes de desenhar, inspecione os arquivos atuais de CSS, componentes, telas e logo do projeto. Não invente uma identidade substituta. Se esses arquivos não estiverem disponíveis, peça que sejam fornecidos antes de afirmar fidelidade visual; você pode adiantar o mapa de páginas e os fluxos sem inventar o estilo.
Manter preto, branco e os cinzas existentes, fontes, logo, botões, campos, bordas, sombras e temas claro/escuro já presentes. Nenhuma cor de destaque, inclusive em gráficos, status, erros ou estados de sucesso: usar texto, símbolos, padrões e contraste monocromático. Se o código antigo tiver algum indicador colorido, a exigência atual de preto e branco prevalece nesse ponto. Não transformar automaticamente todo o produto em fundo branco se o original usa áreas escuras.
Mudar apenas a organização visual necessária: disposição das áreas, menu, hierarquia, agrupamentos e percursos; novos componentes seguem o mesmo estilo. A ampliação dos serviços não autoriza rebranding.

FORMATO DECIDIDO PARA O PROTÓTIPO
1. Site público de apresentação da ASTRO.
2. Portal web único, responsivo, com acesso por empresa.
3. Módulos liberados conforme serviço/capacidade contratados.
4. Área interna do trio com acesso distinto do cliente.
5. Percurso visual de um conector local opcional para serviços que precisem de execução no ambiente do cliente.

Não criar aplicação desktop, instalador ou terminal como interface principal. O possível .exe será um conector específico, e não uma cópia obrigatória de todo o portal. Terminal fica para técnicos em etapa posterior.

O formato depende do serviço: relatórios, assistente de IA e automações com APIs acessíveis funcionam pelo portal web; coleta na rede interna ou tarefa em programa local pode exigir execução instalada. Automação de tela requer capacidade própria e não é garantida pelo conector do scanner. Projetar o portal como interface comum e explicar instalação somente quando necessária à tarefa contratada. Não simular que a nuvem tem acesso automático à rede ou ao computador do cliente.

ESTRUTURA COMUM
Empresa atual sempre visível. Empresa é o espaço de dados e contrato do cliente. Uma pessoa pode pertencer a mais de uma empresa, mas a troca de contexto precisa ser explícita. Nenhum cenário mistura dados entre empresas.

Menu base: Início, Meus serviços, Aprovações, Relatórios, Atividade, Suporte e Configurações. Configurações reúne equipe/perfis, conexões, contrato/consumo e conectores. Itens dos serviços aparecem de acordo com as capacidades disponíveis. Separar pessoa administradora do cliente de operador interno da ASTRO.

O catálogo descreve cada serviço. Um serviço não contratado tem página explicativa e ação “Conversar sobre este serviço”; ele não dá acesso operacional. Um serviço futuro fica “Em planejamento”, sem preço, compra ou promessa de lançamento. Os contratados podem estar em configuração, ativos, pausados, suspensos ou cancelados. Permissão insuficiente, falta de contrato, limite atingido e falha técnica são mensagens diferentes.

SEGURANÇA
Projetar: visão geral, ambientes/ativos, avaliações, achados, pendências, detalhe de evidência e relatório.
Percurso: ambiente autorizado → importar resultado demonstrativo → revisar → criar pendência com responsável/prazo → anexar evidência → solicitar revalidação → consultar relatório.
Ativo é um computador, sistema ou recurso acompanhado. Achado é um resultado a analisar. Mostrar origem, data, escopo e situação: observação, suspeita, confirmado ou não verificado. Não transformar porta aberta em falha confirmada. Nenhuma avaliação não significa segurança perfeita. Não criar placar de risco/ROI/perda financeira sem metodologia.
O scanner legado é uma fonte limitada de inventário, não um pentest autônomo completo. Não prometer segurança garantida, SOC 24h, exploração ampla ou correção automática.

IA E AUTOMAÇÕES
Projetar: assistente, fontes autorizadas, rotinas, detalhe de execução, aprovações, conexões e consumo.
Percurso de IA: fonte fictícia pronta → pergunta → resposta com referências demonstrativas → revisão. Incluir resposta “Não tenho informação suficiente”, fonte indisponível e erro de processamento. Não fabricar referência quando não houver fonte.
Percurso de automação: escolher rotina preparada → configurar campos → verificar conexão → testar → aprovar → ativar → acompanhar. Usar exemplo pedido recebido → classificação sugerida → aprovação humana → tarefa registrada. Uma rotina pode funcionar sem IA. Começar com formulários guiados, não um editor universal de centenas de nós.
Estados de execução: na fila, em andamento, aguardando aprovação, concluída, falhou, cancelamento solicitado, cancelada e resultado parcial. Mostrar quando tentar novamente pode duplicar uma ação e exigir revisão. Cancelamento não deve prometer desfazer um efeito já realizado.
Assistente não pode acessar dados de outro cliente nem comandar scanner, shell ou integração financeira pelo simples fato de estar no mesmo portal.

CONTRATO, ACESSO E LIMITES
Preparar a interface para quatro verificações futuras: serviço ativo, permissão da pessoa, escopo autorizado e limite/condição operacional. No protótipo, essas regras são simuladas; esconder menu não é segurança. Documentar que serão verificadas no servidor e executores posteriormente. Nenhuma chave ou senha real no frontend.
Não implementar checkout real ou precificação comercial. Conexões, ativação de serviços, envio de mensagens, importação e download/exportação podem ser simulados, sempre identificados como demonstração. Descrever ações simuladas com honestidade; não apresentar controles visuais como implementação de produção.

CONEXÕES E CONECTOR LOCAL
Conexões mostram sistema, proprietário, escopo e estado: conectada, expirada, revogada ou com erro. Não revelar segredos. Dependências de rotinas ficam visíveis quando conexão cai.
Conector local opcional: desenhar vínculo com empresa, código temporário demonstrativo, confirmação de escopo, versão, última comunicação, pausar e desvincular. Estados: não instalado, aguardando vínculo, conectado, sem conexão, atualização necessária e revogado. Não criar download/pareamento real. Deixar claro quando o serviço pode funcionar sem instalação local.

SITE PÚBLICO
Início, serviços, páginas Segurança e IA/Automações, como funciona, sobre o trio e contato/acesso. Explicar de forma simples o que a ASTRO pretende entregar. Diferenciar capacidades planejadas de oferta pronta. Não inventar clientes, depoimentos, certificações, parcerias, garantias, resultados ou economia. Formulário de contato simulado; sem transmissão externa de dados.

DIREÇÃO VISUAL
Preservar o design preto e branco da plataforma atual conforme a regra obrigatória acima. O estilo não é uma proposta ajustável nesta entrega. Reorganizar o layout para os serviços sem mudar identidade, fontes, logo ou paleta. Componentes novos reutilizam a linguagem existente. Texto de cliente simples; detalhes técnicos em área apropriada. Ícones com rótulo; estados por palavras/símbolos; navegação por teclado; foco visível; contraste adequado; formulários com erros compreensíveis.

REFERÊNCIAS DE FUNCIONAMENTO
n8n e Make: rotinas, histórico e falhas; Zapier: conexões e revogação; Power Automate e UiPath: painel separado da execução local; Dify: fontes/aplicações de IA; Langfuse: organização/projeto e acesso; Wazuh: coleta local e dashboard; DefectDojo: achados, evidências e acompanhamento. Inspire-se em padrões, sem copiar marcas, layouts protegidos ou interfaces. Não incorpore software ou código dessas ferramentas. Licenças de n8n/Dify têm condições comerciais a avaliar depois. Nenhum fornecedor está escolhido para o backend.

CENÁRIOS NAVEGÁVEIS OBRIGATÓRIOS
A. Empresa demonstrativa Aurora: só Segurança contratada; IA aparece apenas no catálogo.
B. Empresa demonstrativa Horizonte: só IA/Automações; não tem acesso a Segurança.
C. Empresa demonstrativa Ponte: ambas contratadas, com fontes e dados próprios.
D. Empresa nova: sem serviços/dados; onboarding explica o próximo passo.
E. Usuário leitor: pode consultar o que está autorizado, mas não executar/alterar.
F. Operador ASTRO: só empresas atribuídas; área interna claramente distinta.
G. Conexão expirada, limite atingido, serviço em configuração e execução com falha.
H. Terceiro módulo “Novo serviço demonstrativo”, apenas em planejamento, acrescentado ao catálogo sem alterar o núcleo do layout.
Todos os nomes e resultados acima são fictícios. Um seletor de cenários exclusivo da demonstração é aceitável; não apresentá-lo como controle de segurança real.

ENTREGÁVEIS E ORDEM
1. Resumo da mudança de posicionamento e mapa de páginas.
2. Fluxos principais e lista de estados/ações.
3. Componentes visuais e critérios de texto/acessibilidade.
4. Primeira entrega navegável: site, início do portal, Meus serviços, Segurança, IA/Automações e troca de cenários.
5. Complementos: conexões/consumo, relatórios, equipe, área interna e conector.
6. Documento de transição para lógica: entidades e estados necessários, ações simuladas, limites do protótipo e decisões ainda abertas. Não implementar backend nesta etapa.

ACEITE
Comparar telas atuais e novas: a identidade preto e branco deve permanecer, com mudanças de layout justificadas pelos serviços. Conferir ausência de cores também em gráficos, foco, mensagens e badges. Identificar quais arquivos/componentes atuais fundamentaram a aparência. Deve ser possível compreender o que cada empresa contratou, completar uma tarefa demonstrativa de cada módulo, reconhecer estados vazios/falhas e acrescentar um serviço de exemplo. Não exibir dados de outra empresa na troca de cenário. Não usar botões sem efeito compreensível nem apresentar recurso futuro como disponível. Se alguma ação estiver fora do protótipo, identificar claramente.
Não publicar, conectar contas reais, enviar mensagens, varrer redes ou coletar informações reais. Entregue o design como trabalho revisável e mantenha a implementação de produção para a próxima etapa.
```
