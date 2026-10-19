# ASTRO Cyber — Cliente e Proposta de Valor

Data: 2026-10-18. Hipóteses baseadas em raciocínio de produto, sem entrevistas com clientes reais.

---

## 1. ICP — Ideal Customer Profile

### Segmento primário (validar primeiro)

| Critério | Especificação |
|---|---|
| Porte | PME: 20–500 funcionários |
| TI | Tem 1–3 pessoas de TI internas, ou terceiriza para prestador |
| Setor | Indústria, varejo, serviços profissionais, logística, saúde não-hospitalar |
| Infraestrutura | Servidores on-premises ou IaaS (AWS/Azure/OCI), VPN, câmeras, switches gerenciáveis |
| Problema percebido | Já sofreu incidente, ou recebeu notificação de risco (banco, seguradora, cliente grande) |
| Decisão de compra | Dono ou diretor aprova; analista de TI recomenda |
| Orçamento esperado | R$3.000–R$15.000 por avaliação assistida; R$1.500–R$5.000/mês para acompanhamento — **hipótese a validar** |
| Não exige | Certificação ISO 27001, conformidade formal LGPD auditada, SOC 24x7 |

### Segmento secundário (validar após piloto)

**Prestadores de TI / MSPs** com carteira de 5–30 PMEs que precisam de ferramenta para entregar valor de segurança sem contratar especialista próprio.

---

## 2. Personas

### Gestor / Dono (comprador econômico)

- Não entende jargão técnico
- Pergunta: "o que pode me prejudicar e quanto vai custar se eu não resolver?"
- Aprova verba quando entende o risco em reais e tem responsável definido
- Desconfia de "lista de problemas" sem prioridade clara
- Quer saber se o que pediu para corrigir foi de fato resolvido
- **Não** vai operar a ferramenta diretamente

### Analista / Responsável de TI (usuário operacional)

- Sobrecarregado: acumula suporte, infraestrutura e "segurança"
- Quer prioridade clara para não perder tempo em falsos positivos
- Precisa de evidência técnica para convencer o gestor
- Quer rastrear o que mandou corrigir e confirmar que foi feito
- Já tentou OpenVAS ou Nessus e achou complexo demais para operar sozinho

### Prestador de TI / MSP (canal potencial)

- Atende múltiplas PMEs; não tem tempo para ferramenta complexa por cliente
- Precisa de relatório que possa entregar ao dono da PME sem precisar explicar cada CVE
- Prefere pagar por avaliação ou por cliente ativo, não por seat
- **Hipótese**: quer co-brand ou white-label do relatório

---

## 3. Problemas reais (não aspiracionais)

| Problema | Evidência interna de apoio |
|---|---|
| "Não sei o que está exposto na minha rede" | Razão de existência do scanner; inventário TCP resolve parcialmente |
| "Tenho uma lista de problemas mas não sei por onde começar" | `core/business.py` e visão owner foram construídos exatamente para isso |
| "Não consigo traduzir risco técnico em verba aprovada pelo dono" | Feature de orçamento/decisão (`budget_decisions` no banco) |
| "Mandei corrigir, mas não sei se foi feito" | Ciclo de revalidação ainda ausente — é gap a construir |
| "O único analista de TI que tenho não dá conta de tudo" | Razão do AEGIS e do agente autônomo (hoje desativado em exploração) |

---

## 4. Hipóteses de proposta de valor (a validar em entrevistas)

| Hipótese | O que valida | O que invalida |
|---|---|---|
| H1: Gestor paga para saber "o que está em risco em reais" | Gestor cita isso como problema; autoriza compra após demo | Gestor prefere só o relatório técnico; não liga para financeiro |
| H2: Analista de TI quer priorização contextual, não lista de CVEs | Analista menciona dificuldade de priorizar; adota a ferramenta | Analista quer dados brutos e faz sua própria priorização |
| H3: PME paga por avaliação assistida, não por assinatura de SaaS | Compra sem resistência de modelo; prefere projeto fechado | Prefere assinatura mensal previsível |
| H4: MSP paga por cliente ativo gerenciado pela ASTRO | MSP contrata primeiro piloto para cliente da carteira | MSP prefere white-label self-service |
| H5: Ciclo de correção + revalidação é o diferencial principal | Cliente menciona "não saber se foi corrigido" como dor real | Correção é resolvida internamente sem ajuda de ferramenta |

---

## 5. Clientes a evitar inicialmente

| Perfil | Por quê evitar |
|---|---|
| Empresa que precisa de certificação ISO 27001 / PCI / SOC 2 | ASTRO não é auditor; relatório não tem validade de certificação |
| Empresa que quer garantia de ausência de vulnerabilidades | Scanner TCP não é cobertura completa; não prometer o que não temos |
| Empresa sem profissional de TI e sem prestador externo | Sem responsável técnico para agir sobre os achados, o valor é zero |
| Empresas em setores com regulação específica (banco, saúde hospitalar) | Requisitos de segurança além da nossa cobertura; risco jurídico |
| Empresa que quer pentest de aplicação web | Nosso scanner é de rede/serviços, não pentest web (DAST/SAST) |
| Empresa que exige SLA de disponibilidade 24x7 | Não temos infraestrutura nem equipe para isso agora |

---

## 6. Perguntas para entrevistas de descoberta

### Para o gestor

1. Você já teve algum incidente de segurança? O que aconteceu?
2. Você sabe hoje o que está exposto na internet da sua empresa?
3. Quando seu analista de TI te fala de segurança, o que você entende?
4. Você já aprovou verba para segurança? O que te convenceu?
5. Se eu te dissesse que tenho uma lista de 10 problemas de segurança na sua rede, o que você faria com essa informação?
6. Quanto você gastaria para saber que os 3 maiores riscos foram corrigidos?

### Para o analista de TI

1. Como você descobre hoje o que está exposto na rede?
2. Você já usou scanner de segurança? O que te incomoda nele?
3. Quando você encontra uma vulnerabilidade, como decide o que corrigir primeiro?
4. Como você comprova para o gestor que um problema foi resolvido?
5. Quanto tempo por semana você dedica a segurança hoje?
6. O que te faria adotar uma ferramenta nova?

### Para o prestador de TI / MSP

1. Quantos clientes você atende? Quantos te pedem segurança?
2. Como você entrega segurança hoje para seus clientes?
3. O que seu cliente te pede quando sofre um incidente?
4. Você usaria uma ferramenta que gera relatório para o dono do seu cliente automaticamente?
5. Como seria o modelo de negócio ideal para você: por cliente, por avaliação, mensalidade?
