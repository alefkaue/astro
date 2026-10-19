# ASTRO Cyber — Modelo de Negócio

Data: 2026-10-18. **Todos os preços, custos e métricas são hipóteses a validar com clientes reais. Não usar como projeção financeira.**

---

## 1. Princípio

Começar com receita real de poucos clientes, não com usuários sem pagamento. Escalar produto depois de entender custo de atendimento, qualidade de entrega e capacidade de suporte com uma equipe de 3 fundadores.

---

## 2. Três ofertas candidatas

### ASTRO Diagnóstico (oferta principal recomendada)

**O que é:** Avaliação defensiva pontual de infraestrutura. A equipe ASTRO executa, revisa, entrega relatório e faz reunião de resultados com o cliente.

| Aspecto | Detalhe |
|---|---|
| Escopo | Acordado por escrito no engagement; IPs/CIDRs específicos |
| Entrega | Relatório executivo + técnico; reunião de 1–2h |
| Duração | Avaliação: horas; entrega: 1–5 dias úteis |
| Quem faz | Equipe ASTRO opera as ferramentas e revisa os achados |
| Limitações declaradas | Scanner TCP defensivo; não é pentest, não cobre web app, não garante cobertura total |
| Preço hipotético | R$3.000–R$8.000 por avaliação (varia por escopo e porte) |
| Custo estimado (hipótese) | R$500–R$1.500 de infra + IA + tempo de equipe |
| Margem estimada (hipótese) | Alta se processo for eficiente |
| Quando lançar | Após G0 (gates de segurança mínimos) |

**Por que esta primeiro:** Receita imediata, sem conector, sem billing automatizado, sem SaaS self-service. A equipe aprende o que o cliente valoriza antes de automatizar.

---

### ASTRO Contínuo (oferta de recorrência)

**O que é:** Acompanhamento recorrente com avaliações periódicas, orientação de correção e revalidação.

| Aspecto | Detalhe |
|---|---|
| Cadência hipotética | Mensal ou bimestral |
| Entrega | Avaliação + relatório + reunião de acompanhamento |
| Diferencial | Evolução comparável, revalidação de correções, acompanhamento de responsáveis |
| Preço hipotético | R$1.500–R$5.000/mês (varia por cadência e escopo) |
| Requisitos técnicos | Jobs duráveis (G1), ciclo de correção (G2), histórico comparável (G2) |
| Quando lançar | Após G1 validado com pilotos do Diagnóstico |

---

### ASTRO Parceiro (canal MSP/prestador)

**O que é:** Capacitar prestadores de TI e MSPs a oferecer avaliações defensivas para sua carteira de clientes, usando a ASTRO como plataforma de back-office.

| Aspecto | Detalhe |
|---|---|
| Modelo | Parceiro paga por avaliação ou por cliente gerenciado; ASTRO faz back-office |
| Entrega | Relatório para co-branding ou white-label |
| Diferencial | Escalabilidade para o MSP sem precisar de equipe de segurança própria |
| Preço hipotético | R$800–R$2.000 por avaliação para o parceiro (revendem por mais) |
| Requisitos técnicos | Multi-tenant estável, relatório de qualidade, suporte documentado |
| Quando lançar | Após pelo menos 3 clientes diretos validados com Diagnóstico ou Contínuo |

---

## 3. Economia unitária paramétrica

Substitua os `?` com dados reais dos primeiros clientes.

### Por avaliação (Diagnóstico)

| Item | Hipótese inicial | Real (preencher) |
|---|---|---|
| Tempo de operador para executar e revisar | 2–4h | ? |
| Custo hora fundador | Definir com sócios | ? |
| Infra (servidor, storage) por avaliação | R$50–R$200 | ? |
| Custo AEGIS (tokens) por avaliação | R$5–R$30 | ? |
| Tempo de criação de relatório | 1–2h | ? |
| Tempo de reunião com cliente | 1–2h | ? |
| **Custo total estimado** | R$600–R$2.000 | ? |
| Preço de venda | R$3.000–R$8.000 | ? |
| **Margem de contribuição estimada** | 60–80% | ? |

### Por cliente recorrente (Contínuo)

| Item | Hipótese inicial | Real |
|---|---|---|
| Horas por cliente/mês | 3–8h | ? |
| Infra + IA/mês | R$100–R$300 | ? |
| Suporte e atendimento/mês | 1–3h | ? |
| **Custo total mensal estimado** | R$500–R$1.500 | ? |
| MRR por cliente | R$1.500–R$5.000 | ? |

---

## 4. Ponto de equilíbrio (paramétrico)

Não calcular antes de ter custo real medido. Exemplo de modelo:

```
Custo fixo mensal estimado = salários implícitos dos fundadores + infra base + ferramentas
(Definir com sócios — não presumir)

Margem de contribuição por cliente = preço - custo variável por cliente

Break-even = custo fixo / margem de contribuição por cliente
```

Só faz sentido calcular depois de 3+ clientes pagantes com custo medido.

---

## 5. Métricas-chave a medir desde o início

| Métrica | Para que serve |
|---|---|
| Tempo do primeiro acesso à primeira avaliação | Eficiência de onboarding |
| Proporção de achados classificados como confirmado vs observação | Qualidade do scanner |
| Taxa de clientes que revalidam correções | Valor real do ciclo |
| Horas de suporte por cliente por mês | Escalabilidade do modelo |
| Custo real por avaliação (infra + IA + tempo) | Viabilidade da margem |
| NPS ou feedback qualitativo após entrega | Proposta de valor real |

---

## 6. O que não fazer

- Não lançar os 5 planos do catálogo atual como preço real (não validados com cliente)
- Não integrar Stripe/pagamento antes de ter pelo menos 3 clientes que pagaram manualmente
- Não oferecer desconto por assinatura anual sem ter clientes renovando
- Não projetar crescimento ou valuation sem dados reais de churn e CAC
