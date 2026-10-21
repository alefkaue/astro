
Data de referência: 21 de outubro de 2026. Preços propostos, horas de trabalho, metas e projeções da ASTRO são hipóteses de planejamento, não resultados comerciais observados.

———

## 01 — Diagnóstico da ASTRO

Conclusão: a documentação pública revela uma distância entre a ambição original e a capacidade que ela própria declara como ativa. A maturidade técnica atual permanece indeterminada; a maturidade comercial precisa ser demonstrada por entregas e pagamentos.

### O que foi possível verificar

A página pública apresenta uma main com diretórios como app, core, scanner_go, tests, docs e planos. O README contém uma advertência datada de 10/10/2026: scanner restrito ao inventário TCP defensivo, exploração e planejamento de ataque desativados, sem declaração de prontidão para produção. Abaixo dela, permanece a apresentação legada de pentesting autônomo, AEGIS e tradução de vulnerabilidades em valores financeiros. A documentação também descreve demonstração com backend simulado e checkout simulado. Essas são declarações documentais; a implementação não foi inspecionada. Repositório público (https://github.com/alefkaue/astro).

Isso permite identificar um problema documental relevante: visitantes podem interpretar capacidades históricas ou demonstrativas como capacidades comerciais atuais.

### Inventário de acesso e limitações

| Elemento solicitado | Resultado desta investigação | Consequência |
|---|---|---|
| Branches locais | Não acessíveis | Não foi possível identificar trabalho ainda não publicado |
| Referências remotas | Não atualizadas | Não foi executado fetch |
| Relação completa de branches remotas | Consulta pública falhou | Não há inventário confiável de branches |
| main | Página pública acessível, sem fixação de SHA | Visão documental possivelmente defasada |
| Commits, ancestralidade e diferenças | Não acessíveis | Nenhuma conclusão sobre qual branch está mais avançada |
| docs/strategy | Conteúdo não acessível | Planejamentos internos não foram lidos |
| Arquitetura, segurança e roadmap internos | Links identificados, leitura indisponível | Não constituem evidência analisada |
| Vitrine institucional | Branch e implementação não verificadas | Não é possível classificá-la |
| Central de gestão e CRM | Existência informada por vocês | Implementação e cobertura não verificadas |

Portanto, não afirmo que a main representa o desenvolvimento mais recente.

### Classificação honesta das capacidades

| Capacidade | Situação documental acessível | Estado do código |
|---|---|---|
| Inventário TCP defensivo | Declarado como perfil ativo | Não verificado |
| Pentesting autônomo | Descrito no legado; execução ofensiva declarada desativada | Não verificado |
| AEGIS | Descrito como copiloto | Não verificado |
| Visão executiva e decisões sobre correção | Descritas | Não verificadas |
| Demonstração no navegador | Declaradamente simulada | Não executada |
| Cobrança | Checkout descrito como simulado | Integração financeira não comprovada |
| Autorização de escopo e permissões | Descritas | Eficácia não verificada |
| Testes automatizados | Mencionados | Não executados |

Não existe fundamento suficiente para classificar funcionalidades como plenamente implementadas, seguras ou comercialmente operáveis.

### Diagnóstico de maturidade

Técnica: indeterminada. É necessário verificar o comportamento do sistema, seus controles e seus limites antes de usá-lo com dados reais.

Documental: precisa de uma separação clara entre funcionamento atual, demonstração, legado e planejamento.

Comercial: não foram fornecidas evidências de contratos, faturamento, retenção ou disposição de pagamento. Isso não prova ausência de clientes; significa que essas evidências não estão disponíveis para este estudo.

Operacional: três estudantes podem construir uma operação pequena e competente, desde que o escopo seja menor que o portfólio de uma consultoria estabelecida.

### Possíveis esforços duplicados

Não identifiquei duplicações concretas entre branches, porque não consegui compará-las. Existem, porém, riscos que precisam ser investigados:

- CRM e plataforma criando cadastros paralelos de clientes, responsáveis e tarefas.
- Relatórios comerciais e técnicos mantendo informações divergentes.
- Vitrine prometendo capacidades que o produto ainda não entrega.
- Scanner próprio consumindo esforço que poderia ser atendido por ferramentas existentes.
- Desenvolvimento simultâneo de vendas, cobrança, gestão de projetos, IA e motor de segurança antes da validação comercial.

Recomendação: definir uma fonte principal para cada informação. O CRM deve cuidar do relacionamento comercial; o processo de entrega deve manter escopo, evidências, responsáveis e acompanhamento. Uma nova plataforma só se justifica quando resolver limitações observadas nessa operação.

### O que falta para concluir a auditoria

Em um ambiente com acesso comum autorizado, ainda será necessário:

1. Inventariar branches locais e remotas, com seus respectivos SHAs.
2. Atualizar referências remotas, quando permitido.
3. Comparar ancestralidade, commits exclusivos e diferenças.
4. Ler integralmente estratégia, arquitetura, segurança e planejamento.
5. Rastrear funcionalidades da interface até persistência e execução.
6. Separar dados reais, fixtures, mocks e demonstrações.
7. Verificar isolamento entre clientes, autenticação, autorização e escopo.
8. Examinar testes, dependências, tratamento de segredos e operação.
9. Relacionar cada promessa comercial a uma capacidade comprovada.

Decisão provisória: preservar o trabalho existente e interromper a expansão comercialmente especulativa. Não recomendo apagar código nem escolher uma branch definitiva sem essa auditoria.

———

## 02 — Pesquisa de Mercado

Conclusão: há um mercado brasileiro relevante e problemas reais nas empresas menores. Entretanto, os dados disponíveis não demonstram automaticamente que pequenas empresas do ABC comprarão um scanner ou contratarão a ASTRO.

### Dimensão e crescimento: o que os números significam

| Fonte e período | Informação | Interpretação correta |
|---|---|---|
| Brasscom, relatório setorial divulgado em 2026 | Projeção de R$ 126,9 bilhões em segurança da informação entre 2026 e 2029; crescimento anual composto de 14% no quadro apresentado | Investimento acumulado nacional projetado, com escopo amplo |
| Mordor Intelligence, atualização de agosto/2026 | Estima US$ 3,68 bilhões em 2025 e US$ 4,05 bilhões em 2026 para cibersegurança no Brasil | Estimativa comercial de mercado |
| Grand View Research, página consultada em outubro/2026 | Estima US$ 5,87 bilhões em 2025 | Outra estimativa comercial, com resultado significativamente diferente |

Fontes: Brasscom, página 32 do PDF (https://brasscom.org.br/wp-content/uploads/2026/05/BRI2-2026-001-Relatorio-Setorial-2025-versao-resumida-v5-SITE-2.pdf), Mordor Intelligence (https://www.mordorintelligence.com/industry-reports/brazil-cybersecurity-market), Grand View Research (https://www.grandviewresearch.com/horizon/outlook/cyber-security-market/brazil).

Não é adequado tirar uma média desses números. Os recortes, métodos e categorias não foram harmonizados. Também não é correto transformar o investimento nacional acumulado em um mercado imediatamente acessível à ASTRO.

A Brasscom publicou um relatório específico de cibersegurança em 15/10/2026. Sua página foi localizada, mas o PDF apresentou falha de carregamento. Por isso, não atribuo a ele informações que não consegui ler. Publicação identificada (https://brasscom.org.br/pdfs/relatorio-de-ciberseguranca/).

### Evidência brasileira sobre empresas menores

Na TIC Empresas 2025:

- 53% das empresas com Internet declararam possuir política de segurança digital.
- Entre empresas de 10 a 49 pessoas ocupadas, foram 49%.
- Entre aquelas com 250 pessoas ou mais, foram 88%.

A população pesquisada e os setores abrangidos precisam ser respeitados. Esses resultados não representam indistintamente MEIs, negócios com menos de dez pessoas ou todas as clínicas brasileiras. Cetic.br/NIC.br, indicador D11, referência 2025 (https://cetic.br/es/tics/pesquisa/2025/empresas/D11/).

No indicador de práticas de segurança, 26% das empresas de 10 a 49 pessoas declararam promover treinamento sobre gestão de risco digital, contra 57% das grandes. Isso aponta diferença de adoção, não demonstra intenção de contratar treinamento externo. Cetic.br/NIC.br, D16, referência 2025 (https://cetic.br/es/tics/pesquisa/2025/empresas/D16/).

Há espaço para melhorar controles e rotinas. A questão comercial é descobrir quem reconhece essa necessidade, em qual circunstância e com qual orçamento.

### Problemas e compradores

| Problema | Consequência que o comprador reconhece | Comprador provável | Obstáculo à contratação |
|---|---|---|---|
| Conta de e-mail comprometida | Fraude, perda de acesso e exposição de informações | Sócio, gestor administrativo, TI | Acreditar que a licença já resolve tudo |
| Solicitação fraudulenta de pagamento | Desvio financeiro | Financeiro e proprietário | Tratar o problema apenas como treinamento |
| Acessos de ex-funcionários | Uso indevido e dependência de pessoas | Administração, RH, TI | Falta de processo de desligamento |
| Backup sem recuperação verificada | Paralisação e perda de dados | Proprietário e TI | Confundir cópia existente com recuperação possível |
| Serviço exposto ou desatualizado | Acesso indevido e indisponibilidade | TI e gestor responsável | Falta de responsável pela correção |
| Exigência de segurança de um cliente maior | Risco de perder contrato | Sócio ou comercial | Necessidade urgente, mas pontual |
| Incidente sem plano de reação | Atraso e decisões desordenadas | Diretoria | Baixa percepção de urgência antes do incidente |

Esses compradores são hipóteses para entrevistas, não resultados de uma pesquisa feita com clientes da ASTRO.

### Fraudes exigem controles de processo

O CERT.br recomenda verificar destinatários e dados de pagamentos, entre outras medidas contra golpes. Para uma empresa, isso pode se traduzir em:

- Confirmar mudanças bancárias por um canal previamente conhecido.
- Separar solicitação e aprovação.
- Exigir conferência adicional para operações definidas.
- Estabelecer um canal de comunicação de suspeitas.
- Treinar funcionários a interromper uma solicitação duvidosa.

São intervenções que um scanner de rede não entrega. CERT.br, fascículo “Golpes: evite fraudes”, 2026 (https://cartilha.cert.br/fasciculos/golpes-evite-fraudes/fasciculo-golpes-evite-fraudes.pdf).

As estatísticas do CERT.br também exigem cuidado: parte delas decorre de notificações voluntárias. Variações não equivalem diretamente a mudanças na incidência nacional. Nota metodológica do CERT.br (https://stats.cert.br/sobre/).

### O que aprender com dados internacionais

O DBIR 2026 reúne mais de 22 mil violações confirmadas em 145 países. Na base apresentada, exploração de vulnerabilidades passou a representar 31% dos vetores de acesso inicial, enquanto abuso de credenciais correspondeu a 13%.

Isso sustenta a relevância de atualização, exposição externa e identidades. Não significa que 31% das PMEs brasileiras serão invadidas dessa forma. Verizon, DBIR 2026, resumo executivo (https://www.verizon.com/business/resources/executivebriefs/2026-dbir-executive-summary.pdf).

O uso correto desses relatórios é orientar hipóteses e prioridades técnicas; a demanda comercial brasileira precisa de evidência própria.

### Serviços mais contratados: uma lacuna da pesquisa

Não encontrei uma base pública recente e representativa que permita ordenar, com segurança, os serviços de cibersegurança mais contratados pelas pequenas empresas do ABC.

A TIC Empresas mostra terceirização de funções de TIC, mas suporte técnico, infraestrutura e desenvolvimento não podem ser convertidos automaticamente em contratação de segurança. Cetic.br, indicador F4, referência 2025 (https://cetic.br/pt/tics/pesquisa/2025/empresas/F4/).

Portanto, não apresento um ranking artificial de pentest, conscientização, MDR e consultoria.

### São Paulo e ABC

O mercado local oferece acesso presencial, redes de relacionamento e possibilidade de conhecer processos de perto. Também possui fornecedores estabelecidos, inclusive empresas que atendem contabilidades, clínicas e escritórios com serviços recorrentes.

O IBGE disponibiliza dados empresariais por atividade e território no CEMPRE/Sidra. Essa é uma base adequada para um dimensionamento futuro por município, CNAE e porte. Não extraí uma contagem validada do público ideal; consequentemente, não há TAM ou SAM local numérico confiável nesta entrega. IBGE, CEMPRE 2024 (https://www.ibge.gov.br/estatisticas/economicas/industria/9016-estatisticas-do-cadastro-central-de-empresas.html).

O mercado inicialmente alcançável deve ser dimensionado pela capacidade de venda e atendimento: quantas empresas qualificadas vocês conseguem conhecer, converter e atender com qualidade.

### Tendências e implicações

Serviços recorrentes: são atraentes quando existe trabalho recorrente real — revisão de acessos, mudanças, recuperação, pendências e evidências. Repetir o mesmo relatório mensalmente não constitui valor recorrente suficiente.

Automação: reduz tarefas repetitivas, mas acrescenta manutenção, integração, revisão de erros e responsabilidade.

IA: já aparece nas ofertas de diversos concorrentes. Isso reduz seu poder como argumento exclusivo de posicionamento.

Consolidação de ferramentas: plataformas existentes já integram segurança de identidade, endpoints, e-mail, exposição e relatórios. Uma empresa pequena precisa escolher onde acrescentará trabalho especializado.

Internacionalização: oferece mercado maior, mas amplia exigências de idioma, contratação, suporte e concorrência. Não deve ser a primeira hipótese operacional dos três fundadores.

### Lacunas plausíveis e ideias já amplamente oferecidas

| Hipótese | Avaliação |
|---|---|
| “Falta scanner acessível” | Diferenciação fraca: existem alternativas gratuitas e comerciais |
| “Falta relatório em linguagem empresarial” | Oferta já existente; execução pode variar |
| “Falta alguém acompanhar a correção” | Problema plausível; disposição de pagamento ainda precisa ser testada |
| “Falta proteção para pequenas empresas” | Afirmação ampla demais para orientar vendas |
| “Falta implementar corretamente o que já foi comprado” | Hipótese forte para investigar |
| “Falta ligar procedimentos financeiros a controles de identidade” | Hipótese promissora, dependente do segmento |
| “Falta IA em segurança” | Refutada pela oferta concorrente observada |

A oportunidade provável está na qualidade e continuidade da execução em um contexto específico, não na ausência de tecnologia.

———

## 03 — Concorrentes e Startups

Conclusão: quase todas as categorias consideradas pela ASTRO já possuem oferta. Isso não inviabiliza uma empresa pequena, mas exige um recorte comercial claro.

Os recursos abaixo foram verificados em páginas dos próprios fornecedores. Servem para documentar oferta e posicionamento; não comprovam eficácia, satisfação geral, lucratividade ou superioridade técnica.

### Concorrentes e substitutos relevantes

| Empresa | Modelo, público e oferta | Preço público verificado | Aprendizado e limite da comparação |
|---|---|---|---|
| GOIT — ABC | Gestão recorrente de TI para PMEs; Microsoft 365, backup, firewall, monitoramento e apoio à segurança | Página informa dimensionamento sem preços públicos | Já ocupa a combinação proximidade + continuidade + segurança. ASTRO precisaria demonstrar especialização complementar. Fonte (https://goit.com.br/) |
| Computer Consulting — ABC | Suporte, servidores, redes, backup, firewall e continuidade para PMEs | Não localizado na página consultada | O prestador de TI atual é um concorrente e também um possível parceiro. Relação existente pode pesar mais que uma nova ferramenta. Fonte (https://www.computerconsulting.com.br/consultoria-em-ti-abc/) |
| Canny Security | Consultoria com pentest, engenharia social, defesa, conscientização e AppSec | Diagnóstico gratuito anunciado; preço profissional não localizado | Gratuidade e amplitude já são usadas comercialmente. Não representam diferenciação suficiente. Fonte (https://www.cannysecurity.com.br/) |
| Tempest | Consultoria especializada; pentest e entregáveis técnicos e gerenciais, com acesso por plataforma | Sob proposta na oferta consultada | Relatório executivo, plataforma e validação de correções já integram serviços maduros. A ASTRO não deve prometer equivalência de profundidade. Fonte (https://www.tempest.com.br/consultoria/pentest-digital) |
| Redbelt Security | Consultoria e SOC/MDR, com integração de operação humana, automação e Google SecOps | Valor não publicado na página consultada | Operação de detecção e resposta exige pessoas, processos e cobertura. Não pode ser reproduzida apenas instalando um SIEM. Fonte (https://www.redbelt.com.br/soc-mdr/) |
| Conviso | Serviços e plataforma de AppSec; consolidação de achados, priorização, integração com desenvolvimento e gestão | Valor numérico não identificado na página consultada | Gestão de correções e integração com ferramentas já são categorias maduras. Seu foco em software diferencia o público do pequeno escritório local. Fonte (https://www.convisoappsec.com/conviso-platform) |
| Perallis / Hacker Rangers | Plataforma de conscientização com gamificação e conteúdo; licenciamento por usuário | Valor depende de proposta; trial divulgado | Uma palestra inicial da ASTRO pode ser viável; construir biblioteca e plataforma equivalentes criaria outra empresa. Oferta (https://www.perallis.com/solucoes/planos-empresarias-para-capacitacao-em-ciberseguranca), licenciamento (https://www.perallis.com/terms-of-use-clients) |
| Axur | Plataforma de ameaças externas, proteção de marca, credenciais expostas, takedown e EASM | Não localizado na página consultada | Exposição externa e prevenção de fraude digital já contam com fornecedores especializados. Coleta e resposta em escala têm custos próprios. Fonte (https://www.axur.com/pt-br/) |
| Intruder | Gestão de vulnerabilidades e exposição, voltada também a equipes pequenas; integra motores existentes | Free com limites; pentest anunciado a partir de US$ 3.500/teste. Preços pagos do scanner não foram extraídos do calculador | Integração e experiência de uso podem gerar produto sem reinventar todos os motores. Os preços são internacionais e não validam preços brasileiros. Fonte (https://www.intruder.io/pricing) |
| Tenable / Nessus | Ferramentas de avaliação de vulnerabilidades; linha profissional para consultores e pentesters | Essentials gratuito, atualmente limitado a uso não comercial; linha comercial separada | Scanner gratuito para estudo não implica licença para atender clientes. A amplitude de checks existentes torna difícil competir pelo motor. Fonte (https://www.tenable.com/products/nessus/nessus-essentials) |
| Cobalt | Pentest como serviço, especialistas, plataforma, integrações e modelo de créditos | Standard, Premium e Enterprise sob cotação | Há espaço para padronizar contratação e acompanhamento, mas a capacidade técnica continua necessária. Fonte (https://www.cobalt.io/platform/pricing) |
| Cynomi | Plataforma para MSPs, MSSPs e consultorias; avaliações, riscos, continuidade e gestão de programas | Cotação não obtida | Um “painel de risco com IA” enfrenta concorrência direta. A ASTRO pode inicialmente ser usuária ou integradora de ferramentas dessa categoria. Fonte (https://cynomi.com/) |
| Guardz | Plataforma para MSPs, com controles de identidade, e-mail, endpoints e MDR integrado | Precificação por usuário, informada diretamente ao MSP | “Tudo em um para pequenas empresas” já é uma proposta existente. Avaliar parceria exige custos, contratos e cobertura reais. Fonte (https://guardz.com/pricing/) |
| Huntress | Serviços gerenciados de EDR, identidade, treinamento e outros controles, apoiados por SOC | Exemplo público para 100 endpoints: US$ 7,99/endpoint/mês para Managed EDR | Ferramenta com operação humana pode ser comprada em vez de reconstruída. O exemplo não é uma cotação para a ASTRO nem para o Brasil. Fonte (https://www.huntress.com/pricing) |

Não foram encontradas evidências suficientes para atribuir falhas de qualidade a esses fornecedores. As limitações apontadas são de adequação ao público e comparabilidade com a ASTRO.

### Casos documentados de serviços evoluindo para produto

Conviso: ferramenta interna antes de produto. A empresa relata que a plataforma nasceu para organizar e padronizar suas entregas. Há divergência histórica entre textos da própria empresa: um situa uma primeira versão em 2008; outro descreve criação em 2010. A origem em uma necessidade operacional é consistente; a data exata não deve ser tratada como definitivamente resolvida. História da plataforma (https://blog.convisoappsec.com/a-trajetoria-do-appsec-flow-conheca-a-historia-do-nosso-produto/), relato anterior (https://blog.convisoappsec.com/como-funciona-a-gestao-de-vulnerabilidades-na-conviso-platform/).

Aplicação à ASTRO: automatizar problemas repetidos das entregas pode ser uma trajetória coerente. Isso não prova que qualquer ferramenta interna encontrará compradores externos.

Bishop Fox: experiência acumulada apoiando plataforma. A empresa documenta o lançamento do Cosmos em 2020 para ampliar a capacidade dos especialistas e apoiar serviços de avaliação contínua. Relato da empresa (https://bishopfox.com/blog/principles-for-the-new-platform), uso como plataforma de apoio aos serviços (https://bishopfox.com/news/bishop-fox-expands-cosmos-with-jira-support).

Aplicação: combinar automação e especialistas é uma trajetória documentada. Não é evidência de que três iniciantes devam começar com uma plataforma ofensiva autônoma.

Tempest e El Pescador: aquisição também é estratégia. A KnowBe4 documenta que a Tempest comprou El Pescador em 2015 e a vendeu em 2019. Portanto, não seria correto apresentar esse caso como prova de que a Tempest necessariamente construiu esse produto internamente a partir da consultoria. Anúncio da KnowBe4, 25/02/2019 (https://www.knowbe4.com/press/knowbe4-expands-into-brazil-with-the-acquisition-of-el-pescador).

Aplicação: integrar, licenciar, adquirir ou estabelecer parceria pode ser melhor que desenvolver.

### Um caso de dificuldade financeira

A IronNet informou à SEC que interrompeu atividades em setembro de 2023 por falta de liquidez. Documentos posteriores registram pedido de reorganização sob Chapter 11 em outubro. Isso impede simplificar a história como encerramento definitivo naquela data ou atribuir o resultado a uma única causa técnica. Comunicado de setembro (https://www.sec.gov/Archives/edgar/data/1777946/000119312523246581/d331760d8k.htm), documentação posterior (https://www.sec.gov/Archives/edgar/data/1777946/000095017024009153/irnt-20230731.htm).

Aplicação: mesmo empresas com tecnologia e estrutura podem enfrentar falta de caixa. Para a ASTRO, receita contratada, prazo de recebimento e custo de atendimento precisam orientar expansão.

### O espaço competitivo plausível

O posicionamento inicial não deveria ser “fazemos cibersegurança completa com IA”.

Uma hipótese mais defensável seria:

> Ajudamos pequenos escritórios contábeis a organizar a proteção de contas, os procedimentos contra fraudes e o acompanhamento das correções, trabalhando com o TI existente e comprovando o que foi verificado.

Ainda existe concorrência. O diferencial precisaria aparecer na entrega:

- Escopo compreensível.
- Evidências verificáveis.
- Responsável por cada ação.
- Mudanças realizadas com controle.
- Reavaliação das pendências.
- Conhecimento dos processos do segmento.
- Preço compatível com o esforço.

———

## 04 — Estratégia de Serviços

Conclusão: começar por diagnóstico de controles e procedimentos, acompanhado de orientação prática. Implantação de identidade e e-mail pode gerar mais valor, mas exige competência demonstrada e revisão experiente. Pentest amplo, SOC e resposta emergencial não são boas ofertas iniciais.

### Como interpretar “demanda comprovada”

Há três evidências diferentes:

1. O problema existe: padrões técnicos, incidentes e pesquisas sustentam sua relevância.
2. Há contratação da categoria: fornecedores oferecem e clientes contratam serviços semelhantes.
3. O público escolhido comprará da ASTRO pelo preço necessário: ainda não comprovado.

Confundir essas etapas é um risco central deste projeto.

### Matriz de oportunidades: comprador e resultado

| ID | Serviço | Problema e comprador provável | Situação da demanda para a ASTRO | Prioridade |
|---|---|---|---|---|
| S1 | Diagnóstico delimitado de controles | Sócio e TI precisam saber prioridades, responsabilidades e próximos passos | Necessidade plausível; compra ainda não validada | Iniciar |
| S2 | Identidade, contas e e-mail | Sócio, administração e TI querem reduzir perda de acesso e uso indevido | Categoria consolidada; depende do ambiente e do fornecedor atual | Preparar e entregar com revisão |
| S3 | Procedimentos contra fraude | Financeiro e proprietário precisam conferir solicitações e pagamentos | Problema documentado; valor da intervenção precisa ser testado | Iniciar com escopo pequeno |
| S4 | Conscientização aplicada | Administração precisa melhorar identificação e comunicação de suspeitas | Oferta estabelecida; palestra genérica tem diferenciação limitada | Complemento |
| S5 | Exposição e vulnerabilidades | TI precisa identificar exposição e corrigir falhas verificadas | Categoria consolidada; risco de virar simples revenda de scan | Preparar |
| S6 | Infraestrutura e nuvem | TI precisa revisar configurações, acessos e atualização | Demanda ampla, execução muito variável | Depois, em uma stack conhecida |
| S7 | Entrada, mudança e saída de acessos | Administração e TI precisam controlar ciclo de vida das contas | Dor operacional plausível e padronizável | Incorporar ao S1/S2 |
| S8 | Preparação para incidentes e continuidade | Proprietário precisa saber contatos, dependências e recuperação | Relevância técnica forte; orçamento pode ser reativo | Iniciar pela preparação |
| S9 | Pentest | TI, segurança ou cliente contratante exige avaliação especializada | Categoria comprovada; capacidade da ASTRO não demonstrada | Parceiro ou etapa posterior |
| S10 | Acompanhamento recorrente de controles | Sócio e TI precisam manter ações e revisões funcionando | Boa hipótese após projeto inicial pago | Priorizar após validar entrega |
| S11 | Preparação de evidências para exigências B2B | Sócio ou comercial precisa responder questionário de cliente maior | Gatilho comercial plausível; pesquisar frequência no segmento | Testar seletivamente |
| S12 | SOC, MDR e resposta emergencial própria | Gestão espera detecção e resposta com cobertura operacional | Oferta estabelecida; incompatível com a estrutura inicial | Não operar inicialmente |

A seleção se apoia na orientação de começar por controles essenciais, adequada ao perfil de recursos, e em planejamento formal de avaliações. Isso não substitui a validação de compra. NIST, guias CSF 2.0 para pequenas empresas (https://www.nist.gov/cyberframework/quick-start-guides), CIS, grupos de implementação (https://www.cisecurity.org/controls/implementation-groups), NIST SP 800-115 (https://csrc.nist.gov/pubs/sp/800/115/final).

### Esforço, conhecimentos e responsabilidades

As horas abaixo são estimativas iniciais por entrega pequena, incluindo análise e relatório. Devem ser substituídas por horas medidas. Complexidade, quantidade de sistemas e qualidade das informações podem alterar muito o esforço.

| Serviço | Esforço inicial estimado | Conhecimento e ferramentas | Principal responsabilidade |
|---|---:|---|---|
| S1 | 12–18 h | Entrevistas, inventário, evidências, priorização; checklist e planilha podem bastar | Não apresentar uma avaliação limitada como cobertura completa |
| S2 | 16–28 h | Administração da suíte escolhida, recuperação, MFA, permissões e fluxo de e-mail | Evitar bloqueio de usuários, perda de acesso ou interrupção de envio |
| S3 | 6–10 h | Mapeamento financeiro, aprovações e comunicação; trabalho majoritariamente manual | Não prometer eliminação de fraude |
| S4 | 6–10 h na primeira preparação | Educação de adultos, exemplos do setor, métricas e conteúdo autorizado | Evitar constrangimento, coleta desnecessária e conclusões frágeis |
| S5 | 10–18 h | Escopo, DNS, HTTP, rede, scanners e validação de achados | Falso positivo, impacto de testes e ativos fora do escopo |
| S6 | 12–24 h ou mais | Uma plataforma específica, configuração segura e reversão | Interrupção de serviços ou alteração inadequada |
| S7 | 8–14 h | Papéis, inventário de contas e fluxo de admissão/desligamento | Contas esquecidas e privilégios excessivos |
| S8 | 12–20 h | Dependências, contatos, objetivos de recuperação e exercício de mesa | Confundir plano escrito com recuperação comprovada |
| S9 | 40–100 h ou mais | Metodologia, exploração, lógica de negócio, evidência, relatório e reteste | Danos operacionais, exposição de dados e cobertura insuficiente |
| S10 | 3–5 h/cliente/mês | Organização, reavaliação, evidências e relacionamento com TI | Vender cobertura maior que a efetivamente prestada |
| S11 | 10–24 h | Interpretação de requisitos, evidências e processos | Atestar controles inexistentes ou fornecer parecer indevido |
| S12 | Não estimar como operação simples | Equipe, cobertura, telemetria, escalonamento, resposta e contratos | Incapacidade de atender quando necessário |

A capacidade de rodar um scanner não cobre as competências de S5 ou S9. É preciso reconhecer erros, compreender o sistema, documentar limitações e indicar correções adequadas.

Para aplicações web, o WSTG oferece metodologia mais ampla que a execução de ferramentas; a página consultada identifica a versão 4.2 como release publicada e a 5.0 em desenvolvimento. OWASP WSTG (https://owasp.org/projects/web-security-testing-guide).

### Potencial de padronização

| Serviço | Pode começar manualmente? | Padronização | Recorrência legítima | Automação futura | Adequação inicial |
|---|---|---|---|---|---|
| S1 | Sim | Alta em um nicho | Revisão periódica, sem repetir trabalho inútil | Coleta, evidências e relatório | Alta |
| S2 | Sim | Alta por suíte e configuração | Revisão de acessos e alterações | Conectores e detecção de desvios | Média, com revisão |
| S3 | Sim | Média/alta | Revisão de processos e novos funcionários | Aprovações e registros | Alta |
| S4 | Sim | Alta por segmento | Integração de novos funcionários e reforços | Distribuição e acompanhamento | Alta como complemento |
| S5 | Sim | Média | Novos ativos, mudanças e reavaliação | Alta na coleta; revisão continua necessária | Média |
| S6 | Sim | Média por stack | Possível | Verificação de configuração | Baixa sem especialização |
| S7 | Sim | Alta | Alta | Fluxos e integrações | Alta |
| S8 | Sim | Média | Exercícios e revisão de dependências | Lembretes e evidências | Média |
| S9 | Parcialmente | Parcial | Por mudança ou exigência, não necessariamente mensal | Apoio à execução e gestão | Baixa sem supervisão |
| S10 | Sim | Alta | É o próprio serviço | Alta nas tarefas repetitivas | Alta após experiência |
| S11 | Sim | Média | Revisões e renovações contratuais | Reutilização controlada de evidências | Média |
| S12 | Não como operação improvisada | Exige processo maduro | Alta | Alta, com operação humana | Inadequada inicialmente |

### Oferta inicial recomendada

Oferta 1 — Diagnóstico de contas e rotinas essenciais

Público: empresa pequena, uma suíte corporativa conhecida, um responsável executivo e um responsável técnico.

Escopo de teste comercial:

- Uma organização e um ambiente de colaboração.
- Até 20 usuários.
- Até dois domínios.
- Revisão de contas privilegiadas e recuperação.
- Levantamento de entrada e saída de acessos.
- Revisão de procedimentos contra solicitações fraudulentas.
- Verificação documental das rotinas de backup.
- Plano de ações com responsáveis.
- Reunião de apresentação.

Entregáveis:

1. Resumo executivo curto.
2. Evidências das verificações realizadas.
3. Itens não avaliados e informações ausentes.
4. Até dez ações priorizadas.
5. Responsável e dependência por ação.
6. Proposta separada de implantação ou acompanhamento, quando fizer sentido.

Esse limite é uma hipótese de desenho. Se o trabalho consumir 30 horas, será necessário reduzir escopo ou aumentar preço.

Oferta 2 — Implantação assistida de melhorias

Contratação separada, com mudanças específicas e reversão planejada. Nos primeiros projetos, deve ser executada ou revisada por alguém que demonstre experiência na suíte.

Começar somente com uma stack. Microsoft 365 e Google Workspace não devem ser tratados como produtos idênticos.

Há controles que o cliente já pode possuir. A Microsoft informa que Security Defaults está disponível via Entra ID Free; regras de Conditional Access dependem de licenciamento apropriado. O serviço deve verificar o estado real e implementar melhorias adequadas, sem vender como novidade algo já ativo. Documentação Microsoft (https://learn.microsoft.com/en-us/microsoft-365/business-premium/m365bp-conditional-access?tabs=secdefaults&view=o365-worldwide).

Oferta 3 — Acompanhamento mensal

Somente depois de conhecer o ambiente e o esforço:

- Reunião de revisão.
- Acompanhamento das ações.
- Revisão de acessos e mudanças selecionadas.
- Verificação de evidências combinadas.
- Encaminhamento de demandas ao TI.
- Reavaliação periódica.

Definir quantidade de usuários, ambientes, reuniões, verificações e horas. Projetos novos, atendimento emergencial e operação de SOC exigem contratação e capacidade próprias.

### Precificação inicial

Faixas para experimentar, não preços de mercado comprovados:

| Oferta | Hipótese inicial |
|---|---:|
| Avaliação reduzida, aproximadamente 6 h | R$ 1.500–1.800 |
| Diagnóstico delimitado, aproximadamente 12–18 h | R$ 2.400–3.200 |
| Implantação | Orçamento por mudanças e esforço |
| Acompanhamento limitado | R$ 900–1.800/mês |
| Pentest especializado | Orçamento com parceiro; não anunciar preço genérico |

O limite inferior não deve ser usado automaticamente. A viabilidade depende das horas e dos custos apresentados no documento 06.

### Pilotos gratuitos e portfólio

Recomendação: combinar poucos pilotos gratuitos com ofertas pagas desde o início.

| Atividade | Finalidade | Limite proposto |
|---|---|---|
| Reunião de descoberta | Entender problema e processo de compra | 30–45 minutos, sem teste |
| Avaliação educativa | Explicar controles e coletar autopercepção | Sem conclusão técnica de segurança |
| Piloto autorizado | Aprender a entregar um escopo específico | Até dois participantes, até 6 h de equipe por piloto |
| Serviço profissional | Resolver um problema contratado | Escopo, preço, responsabilidades e aceite definidos |

Um piloto gratuito não deve ser um pentest completo disfarçado.

Selecionar participantes que:

- Se aproximem do público desejado.
- Tenham um decisor disponível.
- Possuam responsável técnico ou fornecedor de TI.
- Aceitem discutir o resultado e o processo.
- Possam considerar uma contratação posterior.
- Não estejam buscando resposta emergencial.

Condições do piloto:

- Documento de escopo e autorização.
- Alvos e métodos expressamente delimitados.
- Regras de interrupção.
- Canal de comunicação.
- Tratamento, retenção e descarte das informações.
- Nenhuma obrigação de depoimento positivo.
- Nenhuma autorização implícita de uso de marca.

A abordagem é coerente com distinguir interesse declarado de comportamento de compra. Pagamento e contratação produzem evidência comercial mais forte que elogios. Strategyzer, testes de ideias e força da evidência (https://www.strategyzer.com/library/testing-business-ideas-book-summary).

Conversão: apresentar a próxima etapa e seu preço desde o início do piloto. Ao terminar, separar as opções de corrigir com a ASTRO, com o TI existente ou com outro fornecedor.

Feedback útil:

- Qual decisão o trabalho permitiu tomar?
- O que estava incompreensível?
- Qual ação será executada?
- Quem aprovaria a contratação seguinte?
- Qual motivo impediria o pagamento?

Encerrar a gratuidade: depois de dois pilotos ou 45 dias de programa, o que ocorrer primeiro. Essa é uma regra proposta de gestão de esforço, não uma conclusão estatística.

Se ambos gostarem do trabalho, isso continua sendo uma amostra pequena demais para estimar conversão de mercado.

Estudos de caso: publicar somente com autorização específica e revisão do cliente. Remover domínios, usuários, IPs, evidências sensíveis e detalhes que permitam reidentificação. Um caso pode relatar controles verificados e ações concluídas; não deve inventar prejuízo evitado.

———

## 05 — Estratégia do Produto

Conclusão: a hipótese de produto mais coerente é uma ferramenta para conduzir avaliações, registrar evidências e acompanhar correções. Sua venda independente ainda precisa ser validada. A decisão sobre aproveitar componentes específicos depende da auditoria pendente.

### O scanner faz sentido?

Como ferramenta de apoio: possivelmente.

Como produto principal para PMEs genéricas: a justificativa atual é fraca.

Um scanner pode ajudar a identificar ativos e exposições, mas não responde sozinho:

- Quem controla a conta principal?
- Quem aprova uma mudança de pagamento?
- O funcionário desligado perdeu todos os acessos?
- A empresa consegue recuperar um arquivo necessário?
- Quem fará a correção?
- A correção foi verificada?

Além disso, a oferta concorrente já inclui motores estabelecidos, integrações e planos de entrada. O Intruder divulga uso de motores como Nuclei, OpenVAS e Tenable em sua estrutura de oferta. Construir um scanner próprio não é condição para construir um produto comercial. Oferta técnica divulgada pelo Intruder (https://www.intruder.io/pricing).

Recomendação: conservar o scanner como candidato a módulo interno, se a auditoria demonstrar utilidade, confiabilidade e custo de manutenção aceitável. Não ampliar seus recursos antes de saber qual entrega paga ele melhora.

### O AEGIS acrescenta valor?

Pode acrescentar se reduzir trabalho e mantiver rastreabilidade:

- Redigir uma primeira versão a partir de evidências.
- Adaptar linguagem ao destinatário.
- Sugerir perguntas que faltam.
- Organizar explicações e próximos passos.
- Apoiar a comparação entre avaliações.

Não está demonstrado que a ASTRO precise desenvolver uma camada extensa de IA agora.

O NIST reconhece a produção de conteúdo falso ou incorreto como risco de sistemas generativos. Isso torna indispensável a revisão do que é apresentado como achado técnico. NIST AI 600-1, perfil de IA generativa, 2024 (https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).

Condições para um uso futuro:

1. Cada conclusão deve apontar para uma evidência.
2. Conteúdo externo deve ser tratado como entrada não confiável.
3. A IA não deve criar vulnerabilidades ou validações inexistentes.
4. Alterações e testes precisam de autorização humana.
5. Informações de clientes exigem regras sobre processamento e fornecedores.
6. O benefício deve ser medido em tempo e qualidade.
7. O processo precisa funcionar sem depender da IA.

### O problema das estimativas financeiras automáticas

Transformar gravidade técnica diretamente em reais gera uma aparência de precisão que os dados podem não sustentar.

Uma CVE não informa, sozinha:

- Probabilidade de perda para aquela empresa.
- Duração de indisponibilidade.
- Margem perdida.
- Custo de recuperação.
- Eficácia dos controles existentes.
- Dependência entre diferentes achados.

O EPSS estima exploração observada de uma vulnerabilidade em um horizonte de 30 dias; não estima a perda financeira específica de uma empresa. FIRST, uso do EPSS (https://www.first.org/epss/using-epss).

O NIST trata avaliação de riscos em contexto organizacional, com ameaças, vulnerabilidades, impactos e incerteza. NIST SP 800-30 Rev. 1 (https://csrc.nist.gov/pubs/sp/800/30/r1/final).

Alternativa proposta: cenários preenchidos e confirmados com o cliente.

Exemplo exclusivamente ilustrativo:

- Oito horas de indisponibilidade.
- R$ 600 de margem de contribuição comprometida por hora.
- R$ 2 mil de recuperação.
- Impacto daquele cenário: R$ 6,8 mil.

Isso não fornece uma probabilidade anual, não demonstra perda evitada e não deve ser somado indiscriminadamente a cenários correlacionados.

### Comparação de direções de produto

| Direção | Atratividade inicial | Risco principal | Recomendação |
|---|---|---|---|
| Scanner genérico para PME | Baixa | Substitutos e baixa diferenciação | Não priorizar |
| Pentesting autônomo | Baixa para esta equipe | Cobertura, confiança, responsabilidade e competição | Interromper expansão |
| Plataforma de diagnósticos | Média | Virar apenas formulário e PDF | Experimentar primeiro como ferramenta interna |
| Gestão de evidências e correções | Média/alta | Categoria concorrida; adoção pode depender do serviço | Melhor hipótese a testar |
| Plataforma ampla de GRC/vCISO | Baixa inicialmente | Conteúdo, expertise e complexidade | Adiar |
| Ferramenta específica para um fluxo do nicho | Potencialmente alta | Demanda ainda desconhecida | Investigar após entregas |
| Novo CRM completo | Baixa | Desvio de foco | Usar apenas o necessário do que já está em desenvolvimento |

### Produto mínimo de apoio proposto

O primeiro valor está em manter:

- Cliente e responsável.
- Escopo autorizado.
- Ativos incluídos.
- Verificações realizadas.
- Evidências e suas datas.
- Limitações e itens não avaliados.
- Ações, responsáveis e prazos.
- Resultado da reavaliação.
- Histórico de decisões.

Isso pode começar em ferramentas existentes. O DefectDojo, por exemplo, já oferece organização de achados, importação, deduplicação e acompanhamento de vulnerabilidades. Deve ser avaliado antes de reconstruir essa categoria. Documentação do DefectDojo (https://docs.defectdojo.com/get_started/about/defectdojo_versions/).

Não significa que ele seja necessariamente a ferramenta adequada para um escritório contábil; significa que a decisão de construir precisa comparar alternativas reais.

### Comprar, integrar, reutilizar ou desenvolver

| Necessidade | Direção inicial |
|---|---|
| E-mail corporativo, identidade e cofre | Comprar ou contratar |
| EDR/MDR | Contratar parceiro quando necessário |
| Cobrança e emissão fiscal | Integrar soluções existentes |
| CRM | Usar o mínimo necessário da central informada por vocês |
| Verificações de configuração | Avaliar ferramentas e baselines existentes |
| Motor amplo de vulnerabilidades | Reutilizar ou licenciar |
| Método de entrega e priorização contextual | Desenvolver conhecimento e documentação próprios |
| Fluxo específico que ferramentas não atendem | Considerar desenvolvimento após medir a lacuna |
| Relatório assistido por IA | Experimento pequeno, com revisão |
| Pentesting autônomo | Não desenvolver inicialmente |

A CISA já disponibiliza baselines e ferramentas de avaliação para Microsoft 365 e Google Workspace no projeto SCuBA. Isso reforça a necessidade de avaliar reutilização antes de construir verificações equivalentes. CISA, FAQ do SCuBA (https://www.cisa.gov/sites/default/files/2024-04/CSSO-SCuBA-FAQ-FINAL_508c.pdf).

### Critérios para investir em produto

Proposta de portão de decisão:

- Pelo menos dez entregas pagas no mesmo perfil de cliente.
- Uma tarefa relevante repetida em cinco ou mais entregas.
- Horas medidas antes da automação.
- Três clientes dispostos a experimentar a solução.
- Redução mensurável de esforço sem perda de qualidade.
- Capacidade de manter controles e suporte.
- Evidência separada de compra, se a proposta for vender SaaS.

Clientes satisfeitos com um serviço não comprovam demanda por software de autoatendimento.

### O que parar de construir agora

Como recomendação para a etapa posterior a esta pesquisa:

- Novas funções de exploração autônoma.
- Cadeias automáticas de ataque.
- Cálculo financeiro apresentado sem premissas verificáveis.
- Vários planos comerciais antes de conhecer comprador e custo.
- Recursos que apenas ampliem a aparência de uma plataforma completa.
- Duplicações de cadastro e acompanhamento.
- Novos motores para capacidades disponíveis e suficientes no mercado.

“Parar” aqui significa suspender investimento em expansão. Não significa excluir componentes existentes sem análise.

———

## 06 — Modelo de Negócio e Viabilidade

Conclusão: serviços padronizados com acompanhamento limitado oferecem a melhor combinação inicial de receita, aprendizagem e risco. O modelo híbrido é plausível quando o software acompanha uma operação validada.

### Comparação dos cinco modelos

Valores e prazos são estimativas de planejamento, condicionados à competência e à aquisição de clientes. Investimento inicial abaixo não inclui sustento dos fundadores nem todo o capital de giro.

| Modelo | Investimento inicial hipotético | Primeira receita possível | Operação e custos | Crescimento e dependência | Adequação |
|---|---:|---|---|---|---|
| A. Consultoria tradicional | R$ 3–7 mil | Semanas, se houver acesso ao comprador | Muito trabalho personalizado; proposta e execução variam | Alta dependência dos fundadores | Útil para aprender, limitada como desenho final |
| B. Serviços padronizados | R$ 3–7 mil | Semanas após preparar a entrega | Escopo, horas e revisões mais previsíveis | Cresce com método e treinamento | Melhor ponto de partida |
| C. Serviço gerenciado de controles | R$ 6–15 mil | Após conquistar confiança e conhecer o ambiente | Ferramentas, revisões e compromissos contínuos | Exige limite de carteira e cobertura | Boa evolução; não confundir com SOC |
| D. SaaS puro | R$ 20–60 mil antes de retiradas e expansão | Meses; pode não ocorrer | Produto, aquisição, segurança, suporte e operação | Escala potencial alta, demanda incerta | Fraca adequação imediata |
| E. Híbrido | R$ 3–7 mil para serviços; produto por etapas | Serviços podem faturar antes do produto | Combina entrega com pequeno esforço de ferramenta interna | Dependência diminui se o método se repetir | Melhor trajetória proposta |

As margens não decorrem do rótulo do modelo. Uma consultoria ocupada pode ser lucrativa; um SaaS com suporte intenso e aquisição cara pode operar no prejuízo.

### Formação de preço

Modelo proposto:

> Preço = custo de trabalho e operação ÷ (1 − despesas proporcionais − margem desejada)

Exemplo hipotético:

- 16 horas de trabalho a custo econômico de R$ 60/h: R$ 960.
- Rateio de operação: R$ 400.
- Custo considerado: R$ 1.360.
- Reserva proporcional: 18%.
- Margem desejada: 35%.

Preço resultante: aproximadamente R$ 2.894.

Com 12 horas, mantendo o rateio, o preço cai para aproximadamente R$ 2.383.

Logo, um diagnóstico de R$ 2.400 só se aproxima dessa margem se a execução estiver perto de 12 horas. Com 16 horas, a margem fica menor.

Os 18% são uma reserva de simulação para tributos e despesas proporcionais, não uma alíquota aplicável à ASTRO. O enquadramento real depende de atividade, regime, folha, faturamento e outras condições.

### Capacidade dos três fundadores

Premissa de disponibilidade: 60 horas mensais por fundador, total de 180 horas.

Distribuição possível:

| Atividade | Horas mensais da equipe |
|---|---:|
| Entrega aos clientes | 75 |
| Descoberta, propostas e vendas | 45 |
| Administração e qualidade | 20 |
| Capacitação | 25 |
| Ferramenta interna e manutenção | 15 |
| Total | 180 |

Não considerar 180 horas faturáveis. Também é necessário ajustar a disponibilidade em semanas de provas e compromissos pessoais.

### Cenários mensais por modelo

Estas combinações não são previsões de vendas nem cenários de igual probabilidade.

Premissas:

- Reserva proporcional de 18% sobre receita.
- Despesas fixas mensais de R$ 1.800 para A, B e E.
- R$ 2.500 para C.
- R$ 5 mil para D, mais R$ 15 por conta.
- No cenário otimista de E, R$ 2 mil adicionais de parceiro.
- Licenças relevantes dos clientes contratadas separadamente.
- Sem retirada dos sócios no saldo apresentado.
- Sem investimento inicial, inadimplência ou atraso de recebimento.

| Modelo | Conservador: receita → saldo | Base: receita → saldo | Otimista: receita → saldo |
|---|---:|---:|---:|
| A — horas consultivas | 20 h × R$ 180: R$ 3.600 → R$ 1.152 | 50 h × R$ 200: R$ 10.000 → R$ 6.400 | 80 h × R$ 240: R$ 19.200 → R$ 13.944 |
| B — diagnósticos | 1 × R$ 1.800: R$ 1.800 → −R$ 324 | 3 × R$ 2.400: R$ 7.200 → R$ 4.104 | 4 × R$ 3.000: R$ 12.000 → R$ 8.040 |
| C — contratos recorrentes | 2 × R$ 900: R$ 1.800 → −R$ 1.024 | 6 × R$ 1.200: R$ 7.200 → R$ 3.404 | 10 × R$ 1.800: R$ 18.000 → R$ 12.260 |
| D — SaaS | 10 × R$ 149: R$ 1.490 → −R$ 3.928 | 30 × R$ 199: R$ 5.970 → −R$ 555 | 80 × R$ 299: R$ 23.920 → R$ 13.414 |
| E — híbrido | 1 diagnóstico + 2 recorrentes: R$ 3.600 → R$ 1.152 | 3 diagnósticos + 5 recorrentes: R$ 13.200 → R$ 9.024 | 3 diagnósticos + 8 recorrentes: R$ 23.400 → R$ 15.388 |

Para C, implantação deve ser orçada separadamente. Um contrato mensal não deve absorver gratuitamente o trabalho inicial.

### O que o cenário base revela

No híbrido:

- Receita: R$ 13.200.
- Saldo antes dos sócios: R$ 9.024.
- Retiradas hipotéticas de R$ 3 mil para cada fundador: R$ 9 mil.
- Restante: R$ 24.

Esse resultado não oferece reserva suficiente para crescimento, erros ou variações.

Se o custo econômico das 180 horas dos fundadores for R$ 60/h, o trabalho vale R$ 10.800. O resultado econômico mensal seria negativo em R$ 1.776, mesmo com saldo de caixa positivo antes das retiradas.

Com essas premissas, o equilíbrio econômico requer cerca de R$ 15,4 mil de receita mensal.

### Projeção anual do híbrido

Uma unidade de “cliente-mês” significa um contrato recorrente ativo por um mês.

| Cenário | Diagnósticos no ano | Clientes-mês recorrentes | Receita anual hipotética | Saldo anual antes dos sócios |
|---|---:|---:|---:|---:|
| Conservador | 11 a R$ 1.800 | 16 a R$ 900 | R$ 34.200 | R$ 1.444 |
| Base | 22 a R$ 2.400 | 59 a R$ 1.200 | R$ 123.600 | R$ 74.752 |
| Otimista | 30 a R$ 3.000 | 83 a R$ 1.800 | R$ 239.400 | R$ 152.708 |

Incluídos: reserva proporcional de 18%, R$ 21.600 de despesas fixas anuais, investimento inicial de R$ 5 mil nos dois primeiros cenários e R$ 8 mil no otimista. O otimista inclui R$ 14 mil de parceiros.

Para tornar o cenário base reproduzível:

- Diagnósticos por mês: 0, 1, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2.
- Recorrentes ativos: 0, 0, 1, 2, 3, 5, 6, 7, 8, 8, 9, 10.

Essa trajetória pressupõe aquisição e retenção que ainda não foram demonstradas. Não modela churn separadamente.

O saldo anual base equivale a aproximadamente R$ 6,2 mil mensais para os três, antes das obrigações relacionadas às retiradas. Não sustenta três retiradas de R$ 3 mil desde o primeiro mês.

### Sensibilidades importantes

- Perder dois recorrentes de R$ 1.200 reduz o saldo mensal em R$ 1.968.
- Dobrar de quatro para oito horas mensais por recorrente pode tornar a carteira incompatível com a disponibilidade.
- Receber após 30 ou 60 dias exige mais capital de giro.
- Licença cobrada em moeda estrangeira pode mudar a margem.
- Descontos permanentes podem impedir a contratação futura de ajuda.
- Um único cliente dominante aumenta risco de caixa e negociação.

### Capital para começar

Estimativas de orçamento, ainda sem cotações de contador, advogado, seguros ou equipamentos:

| Situação | Reserva proposta | Condições |
|---|---:|---|
| Descoberta e preparação educativa | R$ 0–800 | Sem entrega técnica profissional e com recursos já disponíveis |
| Implantação inicial da operação de serviços | R$ 3–7 mil | Documentos, formalização, ferramentas e preparação |
| Operação de serviços por seis meses, sem receita e sem retiradas | R$ 12–25 mil | Despesas de R$ 1,5–3 mil/mês mais implantação |
| Mesma operação com R$ 3 mil mensais por fundador | R$ 66–79 mil | Acrescenta R$ 54 mil de retiradas em seis meses |
| SaaS próprio como aposta principal | Reserva exploratória de R$ 60–150 mil | Necessita orçamento específico; exclui ou precisa explicitar sustento dos sócios |

Se vocês não dispuserem de equipamentos adequados sob seu controle, isso aumenta o investimento. Uma provisão hipotética de R$ 9–15 mil para três equipamentos deve ser cotada, não tratada como preço pesquisado de notebooks.

O domínio é um custo pequeno: o Registro.br informa R$ 40 por ano para registro regular, conforme condições da categoria e do período. Registro.br, consulta em 21/10/2026 (https://registro.br/dominio).

### Formalização e proteção da operação

Para três sócios, MEI não resolve a estrutura societária, pois não admite sócios. Uma sociedade limitada pode ser uma alternativa a discutir com contador e advogado. Porte empresarial, natureza jurídica e regime tributário são decisões distintas. DREI, perguntas frequentes (https://www.gov.br/empresas-e-negocios/pt-br/drei/arquivos/faq/perguntas-frequentes), enquadramentos empresariais (https://www.gov.br/empresas-e-negocios/pt-br/drei/orientacoes-de-abertura/tipos-de-pessoas-juridicas/enquadramentos-especificos).

Com contador:

- Atividades efetivamente prestadas e CNAEs.
- Regime tributário e eventual fator R.
- Pró-labore, contribuições e distribuição de resultados.
- Emissão fiscal e obrigações municipais.
- Regras e transições tributárias aplicáveis ao período.
- Separação financeira entre empresa e sócios.

Não assumir automaticamente tributação de 6%. A Receita descreve atividades sujeitas à relação entre folha e receita para determinação do anexo aplicável; o caso concreto precisa de enquadramento. Receita Federal, explicação sobre fator R (https://www8.receita.fazenda.gov.br/SIMPLESNACIONAL/Noticias/NoticiaCompleta.aspx?id=415ad600-7d43-4e55-971b-55df99e95ef3).

Com advogado:

- Contrato social e acordo entre fundadores.
- Propriedade intelectual e saída de sócios.
- Contrato de serviço e confidencialidade.
- Autorização técnica e regras de execução.
- Responsabilidades e limitações juridicamente adequadas.
- Contratação de parceiros e fornecedores.
- Tratamento de dados e uso de estudos de caso.
- Eventual seguro de responsabilidade profissional.

Esses pontos são orientações de pesquisa, não parecer jurídico.

### LGPD e informações dos clientes

A ASTRO pode atuar como operadora em determinadas atividades e como controladora em outras, como seu próprio CRM. Os papéis dependem das decisões e do tratamento efetivamente realizado. A LGPD prevê medidas de segurança e responsabilidades relacionadas ao tratamento. LGPD, texto compilado (https://planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm).

Requisitos operacionais propostos:

- Coletar o mínimo necessário.
- Separar informações por cliente.
- Usar contas individuais e autenticação forte.
- Limitar e registrar acessos.
- Definir retenção e descarte.
- Proteger cópias e verificar recuperação.
- Registrar fornecedores que recebem dados.
- Evitar credenciais e evidências técnicas no CRM.
- Não enviar informações confidenciais a IA sem análise e condições adequadas.

A ANPD possui guia e checklist específicos para agentes de pequeno porte. Eles ajudam a organizar a operação, mas não representam certificação de conformidade. Guia da ANPD, atualizado em 2025 (https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte).

Em incidentes sujeitos à comunicação, a regra geral informada pela ANPD é de três dias úteis. Existem disposições diferenciadas para agentes de pequeno porte elegíveis; não se deve presumir que toda pequena empresa se beneficia delas. Comunicação de incidentes (https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis), Resolução nº 2, texto atualizado (https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022).

Fornecedores internacionais de nuvem e IA também exigem avaliação das regras de transferência internacional. Resolução ANPD nº 19/2024 (https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024).

O computador da faculdade não deve ser considerado automaticamente infraestrutura comercial da ASTRO. Qualquer uso futuro precisa respeitar as condições da instituição; credenciais e informações de clientes exigem um ambiente apropriado.

———

## 07 — Roadmap Estratégico

Conclusão: os próximos meses devem ser organizados por provas de capacidade, compra e repetição. Datas de lançamento não são o principal marco.

### Cliente ideal para testar primeiro

ICP principal proposto: escritórios contábeis com aproximadamente 10–30 pessoas, uma suíte corporativa identificável e TI interno pequeno ou terceirizado.

Hipóteses favoráveis:

- Dependência de contas, documentos e prazos.
- Relacionamento com vários clientes.
- Possibilidade de fraude por personificação.
- Decisor acessível.
- Rotinas repetidas de admissão e desligamento.
- Possibilidade de indicações para outras empresas.

O CRCSP publicou alerta sobre criminosos que se passam por contadores para solicitar dados e senhas. Isso é evidência setorial de problema, não de orçamento disponível. Alerta do CRCSP (https://online.crcsp.org.br/portal/noticias/noticia.asp?c=10707).

Em relação a certificados digitais, o ITI orienta preservar a chave privada e a senha. A ASTRO não deve construir sua operação em torno de receber certificados e senhas dos clientes. Orientações do ITI (https://www.gov.br/iti/pt-br/acesso-a-informacao/perguntas-frequentes/certificacao-digital).

ICP alternativo: escritórios de serviços profissionais B2B, com 15–40 pessoas, dependência de e-mail/documentos e um evento concreto de compra, como exigência de cliente, mudança de TI ou revisão de acessos.

Evitar testar muitos segmentos simultaneamente. Isso dificulta distinguir problema de mercado de problemas de oferta.

### Comparação dos segmentos

Avaliação qualitativa proposta, sem pretensão estatística:

| Segmento | Dor potencial | Pagamento | Acesso ao decisor | Complexidade | Recorrência | Decisão |
|---|---|---|---|---|---|---|
| Contabilidades pequenas | Alta | Média | Relativamente favorável | Moderada | Alta | Primeiro teste |
| Serviços profissionais B2B | Média/alta | Média | Favorável | Moderada | Média/alta | Alternativa |
| Clínicas | Alta | Variável | Moderado | Maior por dados e operação | Alta | Depois ou com parceiro |
| Transportadoras | Alta | Variável | Moderado | Pode envolver sistemas e operação distribuída | Alta | Entrevistar antes de ofertar |
| Pequenas indústrias | Alta | Potencialmente maior | Mais difícil | Alta, sobretudo com OT | Alta | Adiar |
| Comércio pequeno | Variável | Frequentemente restrita | Favorável | Variável | Variável | Seleção rigorosa |
| Startups SaaS | Alta | Variável | Moderado | Exige AppSec e avaliações mais profundas | Alta | Via parceiro especializado |

### Divisão dos fundadores

| Papel sugerido | Responsabilidade | Evidência de boa execução |
|---|---|---|
| Fundador A — técnico | Conhecimento da stack, método e revisão técnica | Entregas reproduzíveis, limitações claras e poucas correções de relatório |
| Fundador B — operação e qualidade | Escopo, evidências, documentação e acompanhamento | Entregas dentro das horas, segurança das informações e pendências rastreáveis |
| Fundador C — comercial e finanças | Entrevistas, CRM, propostas, cobrança e caixa | Conversas qualificadas, propostas, pagamentos e motivos de perda |

Todos precisam participar de entrevistas e compreender a entrega. A divisão não deve criar um sócio que “apenas vende” sem entender limites técnicos nem dois sócios que nunca conversam com compradores.

### Capacitação e ferramentas

Prioridade de aprendizado:

1. Redes, DNS, HTTP e identidade.
2. Administração de uma suíte corporativa.
3. Recuperação, permissões e controle de mudanças.
4. Escrita técnica e comunicação com gestores.
5. Avaliação de riscos e evidências.
6. Escopo, contratos e proteção de dados.
7. Vendas consultivas e precificação.
8. Pentest especializado, conforme o caminho escolhido.

O Microsoft Learn e a certificação SC-900 podem apoiar a base conceitual, sem comprovar capacidade de implantar ambientes sozinhos. A Web Security Academy oferece treinamento gratuito em segurança web. Microsoft SC-900, página atualizada em 2026 (https://learn.microsoft.com/credentials/certifications/security-compliance-and-identity-fundamentals/), PortSwigger Academy (https://portswigger.net/web-security).

Ferramentas iniciais necessárias são modestas: e-mail corporativo, cofre, armazenamento protegido, backup, CRM, assinatura de documentos e ambiente de laboratório.

Licenças de estudo e versões gratuitas precisam ser examinadas antes do uso comercial. A página atual do Nessus Essentials, por exemplo, explicita uso não comercial. Tenable (https://www.tenable.com/products/nessus/nessus-essentials).

### Metodologias aplicadas às decisões

| Referência | Como muda a decisão da ASTRO |
|---|---|
| Customer Discovery | Entrevistar compradores antes de ampliar funcionalidades; registrar problemas e processos reais |
| Lean Startup | Usar uma entrega pequena e mensurável para aprender; não construir toda a plataforma para testar demanda |
| Jobs to Be Done | Investigar circunstâncias de compra: proteger pagamentos, recuperar acesso ou manter contrato |
| Service Design | Desenhar contato, bastidores, evidências, dependências e falhas antes de automatizar |
| Estratégia competitiva | Comparar também TI existente, ferramentas gratuitas e decisão de não comprar |
| Precificação por valor | Entender a consequência do problema, respeitando custo mínimo e sem inventar perdas |
| Product-Market Fit | Buscar pagamento, uso, renovação e indicação; elogios isolados são insuficientes |
| NIST CSF e CIS | Organizar prioridades e evidências; não prometer uma certificação por preencher checklist |

Referências: Steve Blank, Customer Development (https://steveblank.com/2012/03/29/nail-the-customer-development-manifesto/), Eric Ries, metodologia Lean Startup (https://theleanstartup.com/principles), Christensen Institute, Jobs to Be Done (https://www.christenseninstitute.org/theory/jobs-to-be-done/), NN/g, service blueprints (https://www.nngroup.com/articles/service-blueprints-definition/).

A pesquisa de “muito decepcionado sem o produto”, popularizada no caso Superhuman, pode ajudar posteriormente. Um percentual obtido com três clientes não comprova ajuste entre produto e mercado. Relato de Rahul Vohra (https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/).

### Plano de 30 dias

Objetivo: escolher um problema, um público e uma entrega segura.

Atividades:

- Realizar 20 entrevistas: sugestão de dez contabilidades, seis empresas adjacentes e quatro prestadores de TI.
- Registrar problemas recentes, consequências, soluções atuais e responsáveis pelo orçamento.
- Preparar a oferta reduzida e o modelo de relatório.
- Executar exercícios em laboratório próprio autorizado.
- Buscar revisão de profissional experiente.
- Preparar contratos e proteção da operação antes das entregas.
- Completar a auditoria do repositório quando houver acesso comum disponível.

Investimento: R$ 0–800 para descoberta; reservar R$ 3–7 mil se a operação profissional começar nesse período.

Responsáveis: C coordena entrevistas; A prepara método; B organiza qualidade e documentos.

Critérios para avançar:

- Pelo menos oito entrevistas descrevem um problema semelhante e concreto.
- Há acesso a pelo menos cinco decisores.
- A oferta pode ser explicada sem depender de demonstração de IA.
- A equipe consegue cumprir o escopo em laboratório.

Modificar a estratégia se: as dores forem muito diferentes, o comprador não for acessível ou a entrega depender de competências ainda ausentes.

Esses números são critérios de gestão propostos, não limiares científicos.

### Plano de 90 dias

Objetivo: provar que é possível entregar e cobrar.

Atividades:

- Limitar o programa gratuito a dois pilotos.
- Apresentar pelo menos oito propostas qualificadas.
- Buscar três entregas pagas.
- Medir horas, retrabalho e entendimento do cliente.
- Testar um ou dois acompanhamentos recorrentes.
- Preparar um estudo de caso autorizado, se houver resultado apropriado.
- Manter o software restrito ao apoio necessário.

Desembolso acumulado bruto estimado: R$ 7,5–16 mil, antes de receitas e sem retiradas.

Critérios para avançar:

- Três pagamentos de clientes que se aproximam do ICP.
- Entregas revisadas e dentro de um intervalo previsível de horas.
- Cliente identifica uma decisão ou ação habilitada pelo trabalho.
- Nenhuma dependência operacional escondida para cumprir a promessa.
- Pelo menos um interesse concreto em continuidade remunerada.

Modificar se: houver interesse sem pagamento, desconto obrigatório em todas as propostas ou esforço muito acima do orçamento.

### Plano de seis meses

Objetivo: tornar a operação repetível.

Atividades:

- Concentrar vendas no segmento com melhor evidência.
- Padronizar documentos e verificações.
- Revisar preço com horas reais.
- Formalizar parcerias técnicas necessárias.
- Desenvolver somente automações que reduzam trabalho medido.
- Avaliar continuidade e margem por cliente.

Desembolso acumulado bruto estimado: R$ 12–25 mil, antes de receitas, equipamentos adicionais e retiradas.

Critérios para avançar:

- Aproximadamente cinco contratos recorrentes adequados à capacidade.
- Pagamentos e pelo menos três ciclos de continuidade observados.
- Escopo mensal respeitado.
- Caixa acompanhado semanalmente.
- Qualidade não depende de improviso constante dos fundadores.

Interromper expansão se: a carteira exigir disponibilidade incompatível com os estudos, a segurança das informações não estiver controlada ou os contratos forem deficitários.

### Plano de 12 meses

Objetivo: decidir qual empresa merece ser ampliada.

Caminhos possíveis:

1. Especialista em serviços padronizados.
2. Serviço recorrente com ferramenta interna.
3. Parceria com MSPs.
4. Produto específico, com validação própria.
5. Mudança de público ou problema.
6. Encerramento de uma oferta sem viabilidade.

Desembolso bruto de referência: R$ 21–43 mil para a estrutura enxuta ao longo do ano, antes de receitas, retiradas, equipamentos e expansão por parceiros.

Critérios para considerar produto comercial:

- Dor repetida e documentada.
- Retenção e margem dos serviços.
- Clientes que desejam usar ou pagar pelo software.
- Custo de suporte conhecido.
- Segurança e operação preparadas.
- Vantagem concreta frente às alternativas.

### Aquisição dos primeiros clientes

A sequência proposta é:

1. Usar apresentações pessoais e redes profissionais.
2. Solicitar entrevistas sobre processos e acontecimentos recentes.
3. Identificar um gatilho de compra.
4. Oferecer escopo pequeno com preço e resultado definidos.
5. Entregar, revisar e receber.
6. Solicitar uma apresentação a outra empresa, após demonstrar valor.

Abordagem possível, ainda não enviada:

> Estamos estruturando a ASTRO para ajudar pequenos escritórios a organizar a proteção de contas e procedimentos contra fraudes. Queremos entender como vocês tratam acessos, desligamentos e solicitações suspeitas. A conversa inicial é de pesquisa e não envolve testes nos sistemas.

Credibilidade inicial deve vir de transparência sobre a equipe, método, exemplos de laboratório, limites e revisão técnica efetivamente contratada. Não inventar experiência, clientes ou certificações.

No CRM, registrar:

- Empresa e segmento.
- Problema e evento que o tornou relevante.
- Solução e fornecedor atuais.
- Decisor e processo de orçamento.
- Próxima ação.
- Proposta, resultado e motivo de perda.
- Receita recebida e horas de atendimento.

Não é necessário concluir uma central sofisticada para manter esse funil.

Domínio e e-mail profissional podem ser úteis cedo. Site simples deve explicar público, escopo e contato. Anúncios devem esperar evidência de conversão e margem.

### Indicadores de mudança de direção

| Sinal | Resposta proposta |
|---|---|
| 20 entrevistas sem problema recorrente | Rever segmento ou problema |
| Oito propostas qualificadas sem venda | Investigar confiança, urgência, escopo e preço |
| Todos pedem suporte geral | Decidir conscientemente entre parceria e mudança de modelo |
| Diagnóstico ultrapassa o esforço em mais de 50% repetidamente | Reduzir escopo ou recalcular preço |
| Recorrência excede seis horas por cliente/mês por três meses | Redesenhar contrato e atendimento |
| Cliente não executa nenhuma ação | Investigar barreiras de implantação e valor do relatório |
| Gratuidade gera elogios, sem próximos passos | Encerrar oferta gratuita |
| Software cresce, receita e aprendizado comercial não | Suspender novas funcionalidades |
| Um cliente determina toda a agenda | Limitar concentração e renegociar |

Nenhuma dessas atividades comerciais foi realizada nesta etapa.

———

## 08 — Resumo Executivo

Existe uma oportunidade plausível para a ASTRO, mas a tese mais defensável é de uma pequena empresa especializada em execução e acompanhamento. A tese de SaaS amplo de pentesting autônomo ainda não possui validação suficiente.

### Respostas às 14 perguntas

1. A ASTRO possui uma oportunidade de mercado plausível?
Sim. Há necessidades documentadas e contratação de categorias relacionadas. A oportunidade específica da ASTRO ainda depende de capacidade, acesso ao comprador e pagamento.

2. Qual problema resolver primeiro?
Organização da proteção de contas e dos procedimentos contra fraude, com prioridades, responsáveis e acompanhamento.

3. Qual seria o cliente ideal?
Testar primeiro contabilidades de 10–30 pessoas, uma suíte corporativa conhecida e TI pequeno ou terceirizado. É uma hipótese fundamentada, não um segmento comercialmente validado.

4. Quais serviços oferecer inicialmente?
Diagnóstico delimitado, revisão de procedimentos contra fraude, organização do ciclo de acessos e preparação básica para incidentes. Implantação técnica deve ter revisão adequada.

5. Pilotos gratuitos, serviços pagos ou ambos?
Ambos: até dois pilotos pequenos e autorizados, com ofertas pagas desde o início. Gratuidade não comprova disposição de pagamento.

6. O que está mal direcionado?
Amplitude excessiva, automação ofensiva precoce, diferenciação baseada em IA e possíveis estimativas financeiras sem informação suficiente.

7. Estamos desenvolvendo a plataforma certa?
Não há evidência suficiente para afirmar. A hipótese de ferramenta de entrega e acompanhamento parece mais adequada ao início. O código precisa da auditoria que ficou pendente.

8. O que parar de construir?
Expansão de exploração autônoma, cadeias de ataque, precificação comercial complexa e recursos sem ligação demonstrável com uma entrega paga.

9. Qual diferencial competitivo realista?
Conhecimento de um segmento, entrega consistente, evidências claras, coordenação com o TI e reavaliação das correções. Esses diferenciais precisam ser demonstrados.

10. Como conseguir os primeiros clientes?
Apresentações pessoais, entrevistas, parceiros de TI e propostas pequenas vinculadas a problemas concretos. Não depender inicialmente de anúncios.

11. Quanto capital seria necessário?
R$ 12–25 mil como reserva de seis meses de operação enxuta sem receitas e sem retiradas; R$ 66–79 mil com retiradas hipotéticas de R$ 3 mil por fundador. Equipamentos e expansão podem aumentar a necessidade.

12. O que eu faria como sócio?
Escolheria um público, entrevistaria compradores, prepararia uma entrega pequena, buscaria revisão experiente e tentaria vender antes de ampliar o software.

13. Qual o maior risco de fracasso?
Construir muito antes de provar compra, enquanto a capacidade de entrega e o caixa permanecem frágeis. Reduzir esse risco com escopo, pagamentos, horas medidas e decisões periódicas de continuidade.

14. Qual caminho oferece a melhor relação entre risco, investimento e crescimento?
Serviços padronizados → acompanhamento recorrente limitado → ferramenta interna → eventual produto validado separadamente.

### Matriz de recomendações e evidências

| Recomendação | Evidência utilizada | Confiança e limite | Próxima validação |
|---|---|---|---|
| Priorizar controles essenciais | Cetic D11 (https://cetic.br/es/tics/pesquisa/2025/empresas/D11/), CIS IG1 (https://www.cisecurity.org/controls/implementation-groups) | Forte para relevância; insuficiente para compra | Entrevistas e propostas |
| Testar contabilidades | Alerta CRCSP (https://online.crcsp.org.br/portal/noticias/noticia.asp?c=10707), processos e acesso comercial propostos | Moderada; preço desconhecido | Dez entrevistas no segmento |
| Não competir por scanner genérico | Intruder (https://www.intruder.io/pricing), Tenable (https://www.tenable.com/products/nessus/nessus-essentials) | Forte para existência de substitutos | Comparar a tarefa que o cliente paga para resolver |
| Limitar gratuidade | Strategyzer (https://www.strategyzer.com/library/testing-business-ideas-book-summary) e custo de capacidade | Recomendação gerencial | Medir aprendizagem e contratação posterior |
| Não oferecer SOC próprio | Oferta operacional Redbelt (https://www.redbelt.com.br/soc-mdr/) e disponibilidade informada dos fundadores | Forte para inadequação inicial | Orçar e avaliar parceiros |
| Automatizar a operação antes de vender SaaS | História Conviso (https://blog.convisoappsec.com/a-trajetoria-do-appsec-flow-conheca-a-historia-do-nosso-produto/), Bishop Fox (https://bishopfox.com/news/bishop-fox-expands-cosmos-with-jira-support) | Trajetória possível, sujeita a viés de sobrevivência | Medir tarefas repetidas e interesse no software |
| Revisar qualquer conteúdo de IA | NIST AI 600-1 (https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Forte para necessidade de controle | Avaliação de qualidade e rastreabilidade |
| Separar severidade de perda financeira | NIST 800-30 (https://csrc.nist.gov/pubs/sp/800/30/r1/final), FIRST EPSS (https://www.first.org/epss/using-epss) | Forte para limites da inferência | Cenários construídos com o cliente |
| Proteger evidências e contratos | Guia ANPD (https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte) | Forte para organização mínima | Revisão técnica e jurídica |
| Escolher componentes e branches somente após auditoria | Repositório acessível (https://github.com/alefkaue/astro) e falhas de acesso registradas | Confiança baixa sobre implementação | Leitura integral das branches e testes pertinentes |

### Limitações finais da pesquisa

- A auditoria integral das branches e do código não foi concluída.
- Documentação acessível não foi tratada como implementação comprovada.
- Não foram realizadas entrevistas, propostas, testes em terceiros ou contatos.
- Não há demanda, preço ou conversão validados para a ASTRO.
- Não foi produzido um dimensionamento numérico confiável do público local.
- Projeções financeiras são simulações, sem probabilidade atribuída.
- Ofertas de fornecedores foram usadas para documentar concorrência, sem assumir suas alegações de eficácia.
- Os documentos foram entregues nesta conversa; não foram salvos no repositório.
