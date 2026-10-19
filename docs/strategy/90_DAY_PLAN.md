# ASTRO Cyber — Plano de 90 Dias

Data: 2026-10-19. Plano executável para os 3 fundadores.

**Convenções:**
- F1 = fundador responsável por negócio/produto
- F2 = fundador responsável por segurança/entrega técnica
- F3 = fundador responsável por plataforma/operação
- Todos = decisão conjunta obrigatória

**Princípio:** cada semana tem tarefas específicas com responsável e critério de conclusão. Não avançar para a próxima fase sem cumprir os critérios de go/no-go.

---

## Fase 1 — Semanas 1–4: Fundação (Outubro/Novembro 2026)

**Objetivo:** ter a estrutura mínima para se apresentar como empresa e conduzir as primeiras conversas comerciais.

### Semana 1

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Reunião dos 3 fundadores: definir participação societária, vesting e pró-labore | Todos | Acordo documentado por escrito (mesmo que informal) |
| Definir divisão de responsabilidades (F1/F2/F3) conforme FOUNDERS_AND_LEGAL.md §5 | Todos | Documento atualizado |
| Listar os 10 contatos pessoais mais prováveis de conhecer decisores de TI em PMEs | F1 | Planilha com nome, empresa, relação, como abordar |
| Pesquisar disponibilidade do domínio (astrocyber.com.br ou alternativa) | F1 | Decisão de qual domínio registrar |
| Verificar disponibilidade da marca "ASTRO Cyber" no INPI (busca gratuita em busca.inpi.gov.br) | F1 | Resultado documentado; decisão de registrar ou ajustar nome |

### Semana 2

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Registrar domínio | F1 | Domínio ativo |
| Configurar e-mail profissional (Zoho Mail gratuito ou Google Workspace) | F3 | contato@astrocyber.com.br funcional para os 3 fundadores |
| Contratar advogado: contrato padrão + RoE + NDA (orientação inicial) | Todos | Reunião com advogado agendada |
| Contratar contador: regime tributário + abertura de CNPJ | Todos | Reunião com contador agendada |
| Criar ambiente de demo com VMs vulneráveis (VirtualBox + DVWA ou Metasploitable) | F2+F3 | Scanner da ASTRO identifica achados no ambiente de lab |

### Semana 3

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Receber rascunho de contrato do advogado e revisar internamente | Todos | Lista de itens para ajuste enviada ao advogado |
| Criar site institucional estático (páginas: início, serviços, como funciona, sobre, contato) | F1+F3 | Site publicado no GitHub Pages ou Netlify |
| Executar avaliação completa no ambiente de lab e gerar relatório | F2 | PDF gerado; relatório revisado pelos 3 fundadores |
| Criar template de proposta comercial (baseado em MANUAL_OPERATIONS.md) | F1 | Template pronto em Google Docs |
| Criar RoE template (baseado em MANUAL_OPERATIONS.md) | F1+F2 | Template pronto; revisão jurídica pendente |

### Semana 4

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Assinar contrato revisado pelo advogado | Todos | Contrato final aprovado |
| Finalizar processo de abertura de CNPJ com o contador | Todos | Protocolo enviado (CNPJ pode levar 2–5 dias) |
| Ensaiar roteiro de demonstração (30min) internamente | Todos | Apresentação executada sem interrupções ou erros técnicos |
| Iniciar abordagem aos primeiros 5 contatos da lista | F1 | 5 mensagens enviadas; pelo menos 2 respostas |
| Configurar servidor de produção (VPS + waitress + backup automático) | F3 | App sobe com `start_prod.ps1`; backup executado; HTTPS ativo |

**Go/No-Go — Fase 2:**
- [ ] CNPJ em processo ou ativo
- [ ] Contrato padrão aprovado por advogado
- [ ] RoE template pronto (mesmo que ainda sem revisão jurídica final)
- [ ] Site publicado
- [ ] Pelo menos 1 reunião de descoberta agendada
- [ ] Ambiente de demo funcional

---

## Fase 2 — Semanas 5–8: Primeiras Conversas (Novembro/Dezembro 2026)

**Objetivo:** conduzir reuniões de descoberta, afinar a proposta com feedback real, preparar e entregar o primeiro piloto.

### Semana 5

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Conduzir 3 reuniões de descoberta (usar questionário de MANUAL_OPERATIONS.md) | F1 (+F2 se técnico) | 3 notas de reunião registradas |
| Após cada reunião: registrar notas e discutir fit internamente | Todos | Decisão avançar/não avançar por empresa |
| Revisar site com base no feedback das primeiras conversas | F1+F3 | Texto ajustado se necessário |
| Acessar planilha de prospecção da Codex (se disponível) e classificar leads | F1 | Lista qualificada com prioridade |

### Semana 6

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Conduzir mais 3–5 reuniões de descoberta | F1 | Notas registradas |
| Enviar proposta para pelo menos 1 empresa com fit identificado | F1 | Proposta enviada e confirmada recebida |
| Registrar objeções recebidas e adaptar mensagem comercial | F1 | Lista de objeções com resposta documentada |
| Revisar precificação com os 3 fundadores à luz dos feedbacks | Todos | Decisão de preço para os primeiros contratos |

### Semana 7

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Fechar e assinar contrato do primeiro piloto (gratuito ou subsidiado) | Todos | Contrato + RoE assinados |
| Criar engagement na plataforma ASTRO para o cliente do piloto | F2+F3 | Engagement ativo com IPs corretos |
| Executar avaliação do piloto | F2 | Scan concluído; achados revisados manualmente |
| Redigir relatório executivo e técnico | F2 | Relatório revisado por F1 (legibilidade executiva) |

### Semana 8

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Reunião de entrega do primeiro piloto | F1+F2 | Reunião realizada; feedback coletado |
| Registrar horas reais, custo real e feedback do piloto | Todos | Planilha preenchida (usar template de MANUAL_OPERATIONS.md §fim) |
| Decisão: o cliente pagaria? Por quanto? O processo funcionou? | Todos | Decisão documentada no DECISION_LOG.md |
| Continuar abordagem a outros leads: mais 5 contatos | F1 | Funil atualizado |

**Go/No-Go — Fase 3:**
- [ ] Pelo menos 1 piloto entregue com feedback positivo
- [ ] Custo real por avaliação registrado
- [ ] Pelo menos 1 proposta enviada para cliente pagante
- [ ] Processo de entrega executado do início ao fim sem bloqueio crítico

---

## Fase 3 — Semanas 9–12: Primeiras Receitas (Dezembro 2026 / Janeiro 2027)

**Objetivo:** fechar o primeiro contrato pago e iniciar o segundo piloto. Identificar o que precisa melhorar no produto.

### Semana 9

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Acompanhamento dos leads com proposta enviada | F1 | Pelo menos 1 negociação ativa |
| Fechar e faturar o primeiro contrato pago | Todos | NF emitida; pagamento recebido |
| Iniciar segundo cliente (piloto ou pago) | F2+F3 | Contrato + RoE assinados; engagement criado |
| Registrar fricção da operação (formulário de PRODUCT_EVOLUTION.md) | Todos | Backlog de fricção preenchido após o primeiro piloto |

### Semana 10

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Executar avaliação do segundo cliente | F2 | Scan + revisão manual completa |
| Identificar o maior gargalo de tempo no processo de entrega | Todos | Item específico registrado |
| Revisar site com base no que aprendemos (linguagem, serviços, FAQ) | F1+F3 | Site atualizado |
| Abordagem a novos leads (manter funil ativo) | F1 | 5 novos contatos abordados |

### Semana 11

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Entrega do segundo cliente | F1+F2 | Relatório + reunião + termo assinado |
| Coletar feedback estruturado: o que foi útil, o que faltou, pagaria de novo? | F1 | Feedback registrado |
| Calcular custo real por avaliação (infra + IA + horas) com 2 clientes | F3 | Planilha com custo vs. preço; margem calculada |
| Decidir: continuar no preço atual, ajustar, ou mudar escopo | Todos | Decisão documentada no DECISION_LOG.md |

### Semana 12

| Tarefa | Responsável | Critério de conclusão |
|---|---|---|
| Retrospectiva dos 90 dias: o que aprendemos sobre cliente, processo e produto | Todos | Documento de 1 página com conclusões |
| Atualizar BUSINESS_MODEL.md com dados reais (tempo, custo, preço) | F1+F3 | Tabela de economia unitária preenchida com dados reais |
| Definir meta para os próximos 90 dias: quantos clientes, qual receita, qual desenvolvimento | Todos | Meta acordada e documentada |
| Identificar o 1 item do backlog de produto que mais dói na operação | Todos | Tarefa técnica criada no backlog com justificativa |
| Acompanhamento do primeiro cliente (30 dias): o que foi corrigido? | F1 | E-mail enviado; resposta registrada |

---

## Critérios de Sucesso dos 90 Dias

| Métrica | Meta | Real |
|---|---|---|
| Reuniões de descoberta conduzidas | ≥10 | ? |
| Pilotos entregues | ≥2 | ? |
| Contratos pagos fechados | ≥1 | ? |
| Receita gerada | ≥R$3.000 | ? |
| CNPJ ativo | Sim | ? |
| Custo real por avaliação medido | Sim | ? |
| Pelo menos 1 cliente corrigiu um achado | Sim | ? |
| Processo de entrega executado sem bloqueio | Sim | ? |

---

## O que NÃO fazer nestes 90 dias

- Não construir novas funcionalidades sem evidência de fricção operacional
- Não refatorar o backend para "preparar para escala"
- Não contratar funcionários
- Não integrar pagamento antes de ter 3 clientes pagando manualmente
- Não lançar planos de assinatura antes de validar recorrência
- Não abordar mais clientes do que a equipe consegue atender com qualidade
- Não aceitar projeto com escopo que não conseguimos entregar (pentest, forense, SOC)
- Não prometer resultado ao cliente antes de executar

---

## Dependências Críticas

| Dependência | Impacto se atrasar | Responsável externo |
|---|---|---|
| Advogado (contrato + RoE) | Sem contrato → sem venda paga | Fundadores (contratar semana 2) |
| Contador (CNPJ) | Sem CNPJ → sem NF → sem venda formal | Fundadores (iniciar semana 2) |
| Planilha de prospecção (Codex) | Afeta velocidade do funil, não bloqueia | Codex |
| Marca ASTRO disponível no INPI | Se indisponível, ajustar nome antes de divulgar | INPI (verificar semana 1) |
