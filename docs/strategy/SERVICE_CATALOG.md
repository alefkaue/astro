# ASTRO Cyber — Catálogo de Serviços

Data: 2026-10-19. Baseado em capacidades verificadas da plataforma e capacidade real da equipe.

**Princípio:** não oferecer o que não conseguimos entregar com qualidade agora. Cada serviço tem critérios explícitos de quando está pronto para venda.

---

## Serviços disponíveis agora (com preparação de 2–4 semanas)

---

### ASTRO Assessment

**Problema que resolve**

A maioria das PMEs não sabe o que está exposto na internet. Um analista de TI sobrecarregado não tem tempo para verificar periodicamente. O dono não entende relatórios técnicos e não consegue justificar investimento em segurança para a diretoria.

**O que entregamos**

Diagnóstico de segurança de infraestrutura: inventário de serviços expostos, identificação de configurações de risco, classificação de achados por severidade, estimativa de prioridade e relatório em linguagem executiva.

**O que NÃO entregamos**

- Pentest manual com exploração ativa
- Teste de aplicação web (OWASP)
- Teste de engenharia social
- Garantia de ausência de vulnerabilidades
- Resposta a incidentes
- Monitoramento contínuo

**Cliente ideal**

PME com 20–500 funcionários, com alguma infraestrutura de TI (servidores, VPN, e-mail corporativo, serviços internos expostos). Tem analista de TI ou prestador de TI. Decisor acessível (dono, gerente de TI ou CTO).

**Pré-requisitos de conhecimento**

- Fundadores: scanner TCP, interpretação de banners e serviços, classificação de severidade, capacidade de redigir relatório executivo claro.
- Ferramentas: plataforma ASTRO G0, Nmap opcional, acesso SSH/RDP ao servidor de execução.
- Documentos: proposta comercial, RoE assinado, engagement criado na plataforma.

**Metodologia**

1. Reunião de descoberta (30–60min): entender infraestrutura, escopo, expectativas.
2. Definição de escopo: IPs/CIDRs autorizados, janela de execução, contato de emergência.
3. Assinatura de contrato e RoE.
4. Criação de engagement na plataforma.
5. Execução do scanner no escopo autorizado.
6. Revisão manual dos achados: eliminar falsos positivos, classificar evidências.
7. Redação do relatório executivo e técnico.
8. Reunião de entrega: apresentação dos achados, recomendações, perguntas.
9. Entrega do relatório PDF assinado.
10. Acompanhamento opcional em 30 dias: o que foi corrigido?

**Limites operacionais**

- Escopo limitado a IPs/CIDRs que o cliente possui ou opera. Nunca testar sistemas de terceiros.
- Não executar exploração ativa (confirmar banners de versão é permitido; lançar exploit não é).
- Se encontrarmos indício de comprometimento ativo, pausar e comunicar o cliente — não investigar além do escopo.

**Tempo e esforço estimados**

| Etapa | Tempo estimado |
|---|---|
| Reunião de descoberta | 1h |
| Definição de escopo e documentos | 2h |
| Execução e revisão dos achados | 2–4h |
| Redação do relatório | 2–3h |
| Reunião de entrega | 1–2h |
| **Total por avaliação** | **8–12h de equipe** |

**Custo operacional estimado**

| Item | Estimativa |
|---|---|
| Infra (servidor de execução) | R$50–R$150 |
| AEGIS (tokens Groq por avaliação) | R$5–R$30 |
| Ferramentas adicionais (Nmap, etc.) | R$0 (open-source) |
| **Total operacional** | **R$55–R$180** |

**Preço sugerido (hipótese para validar)**

R$2.500–R$6.000 por avaliação, dependendo do escopo (número de IPs, complexidade, porte do cliente).

**Riscos legais e técnicos**

- Risco legal: executar scan sem autorização escrita é crime no Brasil (Lei 14.155/2021). O RoE elimina este risco.
- Risco técnico: falso negativo — o scanner pode não detectar todas as vulnerabilidades. Declarar explicitamente no relatório.
- Risco reputacional: nunca exagerar a cobertura ou garantir que "não há mais vulnerabilidades".

**Entregáveis**

- Relatório executivo (1–2 páginas em linguagem de negócio)
- Relatório técnico (achados com evidências, severidade, recomendação por achado)
- Reunião de apresentação de resultados
- Termo de entrega assinado

**Critérios de qualidade**

- Todo achado classificado como "confirmado" tem evidência de banner ou resposta do serviço.
- Nenhum achado classificado como "confirmado" sem revisão manual da equipe.
- Relatório executivo não contém jargão técnico não explicado.
- Disclaimer de limitação presente em todos os relatórios.
- Estimativas financeiras com disclaimer obrigatório.

**Capacidade atual dos fundadores**

Suficiente para executar. Falta: processo documentado, template de proposta e RoE, ambiente de demo com VMs vulneráveis.

**O que ainda precisamos estudar**

- Como redigir um relatório executivo que o dono da PME entenda (prática, não teoria).
- Como apresentar achados sem gerar pânico desnecessário.
- Precificação real: validar com os primeiros clientes.

**Quando podemos oferecer comercialmente**

Após: (a) CNPJ ativo ou negócio informal registrado; (b) contrato padrão revisado por advogado; (c) RoE template; (d) ambiente de demo pronto; (e) pelo menos 1 execução interna com relatório revisado pelos 3 fundadores.

**Estimativa: 3–5 semanas de preparação.**

---

### ASTRO Exposure

**Problema que resolve**

Muitas PMEs têm serviços esquecidos expostos na internet (VPNs antigas, painéis de administração, RDP aberto, serviços legados). O analista de TI não tem inventário atual. O risco é invisível até virar incidente.

**O que entregamos**

Inventário de serviços expostos com contexto de risco: quais serviços estão acessíveis, qual versão, qual o risco de exposição daquele serviço naquela configuração.

**Diferença do ASTRO Assessment**

O Assessment é mais abrangente (infraestrutura + controles + configurações). O Exposure é focado: só inventário e classificação de serviços expostos. Menor esforço, menor preço, ideal como porta de entrada.

**Cliente ideal**

O mesmo do Assessment. Ideal como primeiro contato com um cliente que hesita no Assessment completo — é uma entrega menor com resultado tangível.

**Metodologia**

Subconjunto do Assessment: descoberta → escopo → scan TCP → revisão de banners → relatório de inventário com classificação de risco por serviço.

**Tempo estimado**

4–6h de equipe por cliente.

**Preço sugerido (hipótese)**

R$1.200–R$2.500. Pode ser oferecido como step inicial que converte para Assessment completo.

**Quando podemos oferecer**

Simultaneamente ao Assessment — preparação é a mesma.

---

## Serviços futuros (não disponíveis agora)

---

### ASTRO Fraud & Awareness

**Status:** não disponível agora.

**Por quê:** requer capacitação específica em engenharia social corporativa, metodologia de avaliação de processos antifraude, e — se incluir simulações de phishing — autorização rigorosa dos participantes, proteção de dados e ausência de captura de senhas reais. Nenhum desses processos está documentado nem validado.

**Pré-requisitos para lançar:**
- Capacitação em metodologia de awareness (curso, certificação ou consultor especializado).
- Template de simulação de phishing com consentimento explícito dos participantes.
- Processo de avaliação de processos antifraude documentado e revisado juridicamente.
- Pelo menos 1 entrega completa interna antes de vender.

**Quando reavaliar:** após 3 clientes de Assessment com feedback sobre necessidade de treinamento de funcionários.

---

### ASTRO Pentest

**Status:** não disponível agora.

**Por quê:** pentest manual com exploração ativa requer metodologia documentada (OWASP, PTES, OSSTMM), expertise comprovada em exploração de vulnerabilidades específicas, autorização formal mais complexa (Rules of Engagement detalhado), e responsabilidade técnica e legal mais elevada. Um falso positivo ou um incidente durante o teste tem consequências sérias.

**Pré-requisitos para lançar:**
- Definir exatamente o escopo técnico do serviço (o que exploraremos e o que não exploraremos).
- Comprovar capacidade técnica com prática em laboratórios (HackTheBox, TryHackMe, CTFs).
- Contrato revisado por advogado especializado em segurança da informação.
- Seguro de responsabilidade civil profissional.
- Pelo menos 2 fundadores com certificação ou experiência comprovada.

**Quando reavaliar:** após 1 ano de operação, com capacitação concluída e pelo menos 5 entregas de Assessment.

---

### ASTRO Continuous

**Status:** não disponível agora.

**Por quê:** requer jobs duráveis (G1), ciclo de correção com revalidação (G2), histórico comparável entre avaliações, e capacidade de atender múltiplos clientes recorrentes simultaneamente sem sobrecarregar a equipe. Nada disso está implementado ou validado.

**Quando lançar:** após 2+ clientes de Assessment completados com sucesso, G1 implementado, e pelo menos 1 cliente pedindo acompanhamento recorrente espontaneamente.

---

## Recomendação de lançamento

Lançar **ASTRO Assessment** como serviço principal e **ASTRO Exposure** como oferta de entrada. Ponto de saída do primeiro ano: validar se clientes pedem ASTRO Continuous (serviço recorrente). Não oferecer Pentest ou Fraud & Awareness antes das condições acima.
