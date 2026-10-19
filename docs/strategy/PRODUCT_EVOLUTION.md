# ASTRO Cyber — Evolução do Produto Orientada pela Operação

Data: 2026-10-19. Como transformar fricção real de serviço em funcionalidade do produto.

---

## 1. Princípio

Não construir funcionalidade porque parece interessante. Construir funcionalidade quando um processo manual estiver doendo — e só depois de confirmar que automatizá-lo gera valor maior que o custo de construção e manutenção.

**A pergunta antes de qualquer nova feature:** "Quanto tempo estamos gastando nisto manualmente? Qual é o impacto de não ter isso no produto?"

---

## 2. Funcionalidades Atuais Úteis para Prestação de Serviço

Estas funcionalidades já existem e são usadas diretamente na operação de serviços:

| Funcionalidade | Uso na operação |
|---|---|
| Engagements (escopo autorizado) | Controle de autorização antes de qualquer scan — obrigatório |
| Scanner TCP com fallback | Execução da avaliação |
| Achados com severidade e estimativa financeira | Base do relatório técnico |
| AEGIS (sugestões de remediação offline) | Aceleração da seção de recomendações no relatório |
| Geração de PDF | Entregável principal |
| Multi-tenant / isolamento | Separar dados de cada cliente internamente |
| Relatório com disclaimer obrigatório | Conformidade com o que prometemos nos contratos |

---

## 3. Critérios de Decisão

Para cada atividade que aparece como gargalo na operação, avaliar com esta matriz:

| Pergunta | Continuar manual | Usar ferramenta de terceiros | Automatizar internamente | Virar feature comercial |
|---|---|---|---|---|
| Acontece em todo engajamento? | Não | Às vezes | Sim (>3 clientes) | Sim (>5 clientes) |
| Consome mais de 2h por cliente? | Não | Talvez | Sim | Sim + valor diferencial |
| É difícil de padronizar? | Sim | Talvez | Não | Não |
| Tem ferramenta gratuita/barata que resolve? | — | Sim | Não | Não |
| O cliente vê valor nisto como produto? | — | — | Talvez | Sim (paga por isso) |
| Temos capacidade de manter? | — | — | Sim | Sim |

**Regra geral:**
- Menos de 3 clientes: manter manual
- 3–5 clientes: avaliar automação interna
- 5+ clientes pagando: considerar como feature comercial

---

## 4. Exemplos de Decisão

### Geração de relatório

- Situação atual: o PDF é gerado pela plataforma; revisão e edição são manuais
- Gargalo real: formatação manual de seções, ajuste de linguagem executiva
- Decisão agora: usar o PDF da plataforma + revisão manual em Google Docs para ajustes
- Quando automatizar mais: quando mais de 5 clientes reclamarem de tempo de entrega ou quando o PDF atual não cobrir os requisitos de qualidade

### Controle de evidências

- Situação atual: planilha ou documento interno
- Gargalo real: potencial erro humano na classificação manual
- Decisão agora: manter planilha + revisão por segundo fundador
- Quando automatizar: quando o volume de achados por cliente tornar a planilha impraticável (>100 achados/cliente recorrentemente)

### Acompanhamento de correções do cliente

- Situação atual: e-mail manual + ligação
- Gargalo real: difícil rastrear o que foi corrigido sem estrutura
- Decisão agora: manter manual — ainda não temos clientes suficientes para justificar
- Quando automatizar: quando 3+ clientes pedirem acompanhamento de correções regularmente → prioridade para G2

### Propostas e contratos

- Situação atual: template Google Docs, envio por e-mail
- Gargalo real: nenhum — volume é baixo
- Decisão agora: manter manual
- Quando automatizar: nunca — contrato exige revisão humana sempre

---

## 5. Backlog Orientado por Operação

Este backlog só recebe itens depois que a operação confirmar a necessidade. Não é roadmap de funcionalidades desejadas.

### Confirmado como necessário (operação exige)

| Item | Evidência de necessidade | Gate |
|---|---|---|
| Jobs duráveis (scan sobrevive ao reinício) | Scan em andamento perdido durante reinício de servidor em piloto | G1 |
| Cancelamento real de job | Cliente pede parar; não há como sem reiniciar o servidor | G1 |
| Cobertura estruturada (o que foi testado) | Cliente pergunta "você testou X?" e não há resposta documentada | G1 |

### A confirmar (possível, mas ainda não validado)

| Item | Hipótese | Como validar |
|---|---|---|
| Módulo de acompanhamento de correções | Clientes pedem follow-up | 3 clientes com pedido explícito |
| Relatório comparativo entre avaliações | Clientes querem ver evolução | 2+ avaliações para o mesmo cliente |
| Agendamento automático de scan recorrente | Clientes querem periodicidade sem trabalho manual | 3 contratos de recorrência assinados |
| Portal do cliente (acesso aos relatórios) | Clientes perdem os PDFs e pedem novamente | 3 clientes reclamando |
| Módulo de phishing/awareness | Clientes pedem treinamento de funcionários | Validar separadamente (service catalog) |

### Não construir antes de validar

- Integração com ferramentas de terceiros (Jira, Slack, ServiceNow) — zero evidência de demanda
- Integração com feeds CVE/NVD — aumenta complexidade; zero achado classificado como "errado" por falta disso nos primeiros pilotos
- Multiregião / HA / multi-worker — irrelevante com <10 clientes
- App mobile — zero demanda identificada
- Internacionalização (inglês) — não é prioridade antes de 10 clientes pagantes em português

---

## 6. Processo de Registro de Fricção

Após cada entrega, registrar no backlog de fricção:

```
DATA: [DATA]
CLIENTE: [IDENTIFICADOR INTERNO — não nome real]
ETAPA DO SERVIÇO: [ex: geração de relatório, controle de evidências]
O QUE FOI LENTO/DIFÍCIL:
TEMPO GASTO MANUALMENTE:
FREQUÊNCIA (só neste cliente ou em todos?):
IMPACTO: [bloqueou entrega / atrasou / apenas inconveniente]
DECISÃO: [ ] manter manual [ ] ferramenta de terceiro [ ] automatizar [ ] adiar
```

Este log alimenta a priorização do backlog técnico e evita que desenvolvimento ocorra por intuição.

---

## 7. Ciclo de Revisão

| Frequência | O que revisar |
|---|---|
| Após cada entrega | Registrar fricção (formulário acima) |
| A cada 2 clientes | Revisar se algum item do backlog "a confirmar" foi validado |
| A cada 4 clientes | Revisar se a plataforma atual ainda é adequada para o volume |
| Ao fechar G1 (jobs duráveis) | Reavaliar se ASTRO Continuous é tecnicamente viável |
| Ao fechar G2 (ciclo de correção) | Revisar pricing e modelo de recorrência com dados reais |

---

## 8. O que Não Fazer

- Não adicionar módulo antes de ter evidência de fricção em pelo menos 2 clientes
- Não reescrever código que funciona para preparar para escala hipotética
- Não migrar tecnologia (PostgreSQL, Redis, Celery) sem requisito real de volume
- Não construir o que uma ferramenta gratuita de terceiro já resolve bem (contratos, e-mail, planilha)
- Não automatizar o que precisa de revisão humana (classificação de achados críticos, relatório executivo final)
