# ASTRO Cyber — avaliação de produto e prontidão comercial

Data: 2026-10-11. Base: leitura do código, documentos anteriores, resultados de testes e fontes oficiais. Não houve teste com clientes, auditoria externa, QA visual ou operação em produção. Situação: produto funcional em desenvolvimento; não pronto para venda ampla como plataforma completa de segurança.

## 1. O que o cliente compra

Proposta inicial recomendada: **avaliação defensiva e acompanhamento assistido da exposição de infraestrutura para PMEs**, com evidências, ações de correção e revalidação. Plataforma web organiza o trabalho; ASTRO pode oferecer implantação, avaliação assistida, revisão técnica e acompanhamento de correções conforme contrato e capacidade da equipe.

O scanner TCP atual identifica exposições/serviços dentro de limites, não equivale a scanner completo de vulnerabilidades, pentest, SIEM, EDR ou garantia de proteção. Não anunciar SOC 24x7, detecção de incidentes em tempo real, conformidade LGPD/ISO/PCI, certificação, exploração autônoma ou cobertura que ainda não possuímos. O status signed do banco representa estado de revisão; não constitui por si assinatura digital verificável ou certificação.

Hipótese de posicionamento: PME que precisa saber o que corrigir e comprovar o acompanhamento, com responsável técnico interno ou parceiro. Validar em entrevistas com gestor, operador e prestador de TI; não supor que toda PME quer operar ferramentas de segurança. [NIST para pequenas empresas](https://www.nist.gov/itl/smallbusinesscyber/nist-cybersecurity-framework-0) apoia visão de gestão de risco; scanner é apenas parte dela, não substitui governança, recuperação e controles da organização.

## 2. Produto e serviços são ofertas distintas

| Oferta candidata | Entrega mensurável | Pré-requisito / limite |
| --- | --- | --- |
| Diagnóstico defensivo assistido | Escopo acordado, avaliações executadas, evidências revisadas, relatório e reunião de entrega | Metodologia/segurança operacional fechadas; identificar cobertura e limitações |
| Acompanhamento recorrente | Avaliações na cadência contratada, análise de mudanças e revisão das prioridades | Jobs/histórico duráveis; equipe e tempo de atendimento dimensionados |
| Correção assistida | Recomendações, tarefa atribuída, orientação e revalidação | Mudanças no ambiente feitas só com autorização e responsável; não prometer remediação automática |
| SaaS autogerenciado | Cliente instala conector e administra avaliações por conta própria | Onboarding, conector seguro, ajuda, billing, suporte e recuperação maduros |
| Pentest manual especializado | Serviço separado com metodologia, escopo, equipe competente e relatório próprio | Não comercializar o inventário TCP atual como pentest |

Começar por piloto assistido depois dos gates de segurança/operação, mantendo clara distinção entre serviço humano e recurso automático. SaaS totalmente autônomo fica posterior. Não fixar preços agora: tabelas atuais do código são provisórias/simulação e não demonstram disposição de compra ou custo sustentável.

Dimensionar custo de suporte por cliente, revisões humanas, infraestrutura por avaliação, armazenamento/retention, AEGIS, onboarding, comercial e atendimento a incidente. Entitlements e limites no servidor; alteração de plano não pode simular pagamento aprovado em produção. Cobrança via provedor externo pode ser posterior; nunca criar funções bancárias.

## 3. Jornada completa do cliente e lacunas

| Etapa | Experiência desejada | Estado atual / próximo trabalho |
| --- | --- | --- |
| Conhecer/contratar | Explicação clara do escopo, entregas e limites | Marca e demo existem; oferta/preço/contrato comercial ainda não validados |
| Primeiro acesso | Convite, senha/identidade, empresa e responsáveis | Login existe; convites, recuperação de senha, MFA e sessões revogáveis faltam |
| Configurar ambiente | Escopos autorizados, exclusões, validade e rede | IP/CIDR e autorização existem; versão, validade, network_id e prova de controle faltam |
| Instalar quando necessário | Conector identificado e teste de alcance sem varredura automática | Conector não implementado; execução atual ocorre na máquina do backend |
| Primeira avaliação | Wizard simples, limites transparentes e duração/status confiáveis | Wizard existe; cobertura estruturada, tempo global/cancelamento e jobs duráveis faltam |
| Entender resultado | Confirmação distinta de suspeita, evidência e motivo | Badges/evidências existem; modelos estáveis e qualidade dos checks precisam evoluir |
| Corrigir | Responsável, tarefa, prioridade contextual, prazo e orientação | Fluxo completo de correção ainda ausente |
| Revalidar | Repetir método comparável e registrar evidência de resolução | Ainda ausente; não encerrar por simples ausência de achado |
| Acompanhar | Histórico comparável, relatório executivo e atualização periódica | Histórico por scan/PDF existe; continuidade por ativo/achado, agendamento e alertas faltam |
| Receber serviço ASTRO | Atendimento atribuído, aprovação e trilha da revisão | Revisão agora isolada por tenant; assignments/contrato/capacidades de serviço faltam |
| Sair do produto | Exportar dados, revogar conectores/acessos e aplicar retenção contratada | Fluxo de offboarding ausente |

Gargalo de valor: atualmente o cliente consegue consultar avaliações, mas ainda não fecha com confiança o ciclo **descoberta → evidência → ação → responsável → revalidação → evolução**. Esse ciclo deve guiar o backlog, não a quantidade de telas.

## 4. Usabilidade, responsividade e acessibilidade

Existem layouts distintos por perfil, temas claros/escuros/sistema, sidebar mobile, labels em alguns formulários, skip link, Escape/foco em modal/menu e reduced motion. Esses recursos implementados não comprovam boa usabilidade ou conformidade WCAG. QA visual e testes com pessoas continuam pendentes.

### Requisitos de layout e uso

- Desktop: operador investiga tabelas/evidências e mantém contexto. Gestor visualiza prioridades e limites antes de detalhes técnicos.
- Tablet: painéis se reorganizam sem perder ações. Inspector abaixo do conteúdo quando necessário.
- Celular: consulta, aprovações permitidas e acompanhamento completos; formulários operáveis. Tabelas densas podem ter rolagem local rotulada; página inteira não deve transbordar. Não excluir funcionalidade essencial por tamanho de tela.
- 320/375/768/1024/1440/1920px e zoom 200%; testar alvos/IPs longos, nomes longos, muitos registros e mensagens de erro. Registrar bugs reproduzíveis com perfil/página/tema.
- Filtros na URL, voltar preserva contexto, confirmação antes de ações críticas, mensagens úteis e retry seguro. Empty/error/offline/stale/partial são estados diferentes.
- Tipografia não deve depender de microtexto decorativo; unidades/horário/fonte explicados. Usuário escolhe fuso para datas humanas; evidência técnica conserva UTC original.
- Conector offline e falha de coleta nunca aparecem como 'seguro' ou 'sem vulnerabilidades'.

### Claro/escuro

Tema sistema/claro/escuro já funciona com preferência local. Console operacional preto é intencional e deve manter leitura/controles em ambos os temas. Revisar estados hover/focus/disabled, gráficos, logotipo, PDFs, inputs nativos e modais. Preferência por usuário e seletor em Configurações são evolução, não persistência na conta já entregue.

### Achado mensurado e ajuste seguro realizado

Cálculo de contraste da paleta existente: verde #1F9D55 em branco = 3,49:1, âmbar #B7791F em branco = 3,64:1; vermelho #D93025 em #141414 = 3,86:1. Falham no limiar de 4,5:1 para texto normal. [W3C contraste](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) define esse requisito; o cálculo de tokens não substitui verificar o estilo efetivamente renderizado.

Codex alterou badges semânticos para texto monocromático e borda indicadora na cor oficial. Erros de formulário/console também usam texto legível e sinal semântico. Microtextos relevantes de 9/10px foram ampliados; seletor de tema ganhou área de uso maior e conteúdo tem espaço inferior para evitar sobreposição. Não declarar AA após esses ajustes.

### Gate de acessibilidade

Alvo [WCAG 2.2 AA](https://www.w3.org/WAI/WCAG22/Understanding/): teclado completo, foco visível/não encoberto, mensagens de estado sem interromper a leitura, contraste texto/não texto, labels/nome/role/value, erros associados ao campo, autenticação compatível com gerenciador de senhas/colar e sem obstáculos cognitivos desnecessários. Não depender de cor ou hover. Testar leitor de tela e reduced motion; auditoria automática é auxiliar, não aprovação final.

## 5. Configurações como domínio real

| Área | Recurso proposto | Prioridade / responsável |
| --- | --- | --- |
| Perfil | Nome, idioma, fuso, preferência de apresentação/tema | P1 Codex UX + Claude API quando persistência existir |
| Segurança pessoal | Alterar senha, MFA, sessões ativas/revogação e recuperação | P0 Claude backend + Codex fluxos |
| Organização | Responsáveis, ambientes, dados de contato e identidade de relatório | P1 ambos |
| Equipe | Convidar/remover, capacidades, permissões e trilha de alteração | P0 ambos; validação sempre no backend |
| Avaliações | Perfis permitidos, horários, limites/exclusões e autorização válida | P0 backend antes de distribuir conector |
| Conectores | Instalar, validar alcance, saúde, versão e revogar | P1 após jobs; não exibir conector fictício |
| Dados | Retenção, exportação, exclusão e destino dos relatórios | P0 política antes do piloto, implementação com backup/offboarding |
| Notificações | Eventos relevantes, canal, frequência e quem recebe | P1 após scheduler/eventos; evitar spam e segredos em e-mail |
| AEGIS | Consentimento/política, provedor, dados enviados e limites | P0 políticas; segredos fora do frontend e logs |
| Serviços/assinatura | Entregas, cadência, utilização e contato de suporte | P1; billing atual é simulado, não contratação válida |

Hoje Configurações principalmente consulta conta/equipe/plano e disponibiliza painel IA admin. Não existe gerenciamento completo de equipe, MFA, preferências cloud, retenção ou integrações. Evitar telas cheias de opções sem API efetiva.

## 6. Segurança, operação e privacidade para comercialização

P0 antes de piloto com dados reais:

- Helpers tenant obrigatórios, capacidades explícitas sem bypass global admin, CSRF/content-type/rate limiting, sessões revogáveis, segredo protegido e autenticação robusta. Testes adversariais por ação/tenant, não só menus. [OWASP multi-tenant](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) orienta isolamento também em armazenamento/logs/cache.
- Jobs/eventos/resultados duráveis, tentativas/leases idempotentes, quota atômica, max_ips real, cancelamento e limite de tempo global. Testar crash/reinício, coleta parcial e indisponibilidade.
- Escopo com exclusões/validade/prova de controle e identificação de rede. Sem varredura intrusiva ou shell arbitrário; operador precisa saber alcance/impacto.
- Staging/prod separados, HTTPS, servidor de aplicação apropriado (não Flask dev), configuração validada, rollback, backups protegidos e restauração comprovada. RPO/RTO e disponibilidade são objetivos a medir/acordar, não promessas atuais.
- Métricas/alertas para API, falhas/leases, duração dos jobs, conectores offline, storage e dependências IA. Correlation ID sem dados sensíveis; audit log por organização com controle de acesso e retenção.
- Procedimento para incidente, atendimento, comunicação, revogação e resposta a acesso indevido. Definir quem atende, horário, severidades e capacidade; não vender SLA não sustentado.
- Inventariar os dados coletados e fornecedores; minimizar/redigir evidência, controlar envio ao AEGIS e registrar acesso/exportação. Definir retenção/exclusão e documentação contratual/privacidade com revisão competente. [Guia ANPD](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-publica-guia-de-seguranca-para-agentes-de-tratamento-de-pequeno-porte) orienta medidas de segurança; não torna a plataforma automaticamente conforme à LGPD.
- Avaliar licença/distribuição de scanners, feeds, bibliotecas, fontes e assets antes da distribuição comercial; SBOM, atualização e vulnerabilidades das próprias dependências.

## 7. Evidência de valor e critérios de sucesso

Piloto deve medir: tempo do primeiro acesso à primeira avaliação útil, proporção de onboarding concluído sem assistência, sucesso/falha/cobertura das avaliações, qualidade e taxa de validação dos achados, tempo para atribuir ação, correções revalidadas com evidência, horas de suporte por cliente e custo por avaliação/cliente. Metas numéricas só depois de baseline; não inventar taxa de detecção ou economia financeira.

Entrevistar gestor e operador separados. Pedir que executem tarefas sem explicação prévia: entrar, entender demo vs real, autorizar escopo, iniciar avaliação, encontrar evidência, explicar um achado, obter relatório e pedir suporte. Anotar onde hesitam; preferência estética não substitui execução correta.

## 8. Gates e sequência de entrega

| Gate | Entrega mínima | Evidência exigida |
| --- | --- | --- |
| G0 laboratório | Fechar arquitetura/RBAC/dados e matriz de capacidades; método defensivo definido | Threat model, contratos e testes adversariais |
| G1 piloto assistido | Identidade/isolamento, jobs e cobertura duráveis, backup/restore, instalação segura, onboarding/relatório e canais humanos | Fluxo ponta a ponta em staging com dados autorizados, falhas/reinício/cancelamento, QA dos temas/mobile/teclado e plano de suporte |
| G2 oferta recorrente | Modelos estáveis de ativos/achados, tarefas de correção, comparação e revalidação | Cliente conclui ciclo de correção; custo/capacidade de atendimento medidos |
| G3 SaaS autogerenciado | Conector distribuível, onboarding autônomo, gestão de acessos, billing/retention/offboarding e operação escalável | Clientes usam com suporte previsível, tenant isolation revisado, recuperação e observabilidade comprovadas |

Sequência: S0 segurança/configuração essencial → migrações e jobs duráveis → ativos/achados/correção → conector seguro e piloto assistido → recorrência/autogerenciamento. UX trabalha em paralelo com contratos reais, não inventando módulos para preencher menu. Sem calendário fechado antes de estimativa e staffing.

Claude próximo foco: revisar gates e transformar P0 em tarefas backend pequenas, com arquivos exclusivos e regressões; Codex mantém jornada/UX/testes e integração. Pareceres anteriores já foram integrados. Nova revisão comercial pode ser executada com CLAUDE_REVIEW_LOCAL.ps1 -Task commercial no terminal normal; preparada, não executada nesta sessão.
