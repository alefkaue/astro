# ASTRO Cyber — Go-to-Market e Validação Comercial

Data: 2026-10-18. Estratégia baseada em validação progressiva, não lançamento amplo.

---

## 1. Princípio

Antes de vender, validar que o problema existe e que a ASTRO resolve. Antes de escalar, validar que o custo de atendimento é sustentável.

**Sequência:** entrevistas → demo funcional → piloto gratuito/subsidiado → primeira venda real → replicar → parceiros.

---

## 2. Fase de entrevistas (antes de qualquer piloto)

### Objetivo

Confirmar (ou refutar) as hipóteses de CUSTOMER_AND_VALUE.md com pessoas reais.

### Critério de sucesso desta fase

- Entrevistar 10+ gestores/analistas de TI de PMEs
- Pelo menos 5 descrevem espontaneamente um dos problemas mapeados
- Pelo menos 3 mencionam disposição de pagar por uma solução parecida

### Perguntas-chave (ver CUSTOMER_AND_VALUE.md §6 para o roteiro completo)

1. Você sabe hoje o que está exposto na internet da sua empresa?
2. Como você prioriza o que corrigir em segurança?
3. Você já teve incidente? O que aconteceu?
4. Como você convence o dono/diretoria a aprovar verba de segurança?
5. Se eu te mostrasse uma ferramenta que faz X, você usaria? Pagaria?

### Como encontrar entrevistados

- Rede pessoal dos fundadores (faculdade, trabalhos anteriores)
- LinkedIn: conectar com analistas de TI e CTOs de PMEs
- Grupos e comunidades de TI no WhatsApp/Telegram/LinkedIn
- Prestadores de TI que os fundadores conhecem

---

## 3. Demo funcional

### Quando usar

Após entrevistas confirmarem problema; antes de oferecer piloto.

### Formato recomendado

1. **Contexto** (5min): "Vou mostrar o que identificamos em uma rede similar à sua"
2. **Avaliação** (10min): mostrar execução em ambiente de laboratório autorizado, não na rede do cliente
3. **Achados** (10min): classificação, evidências, orientação de correção
4. **Visão do gestor** (5min): resumo em português, estimativa de prioridade
5. **Relatório** (5min): mostrar PDF que seria entregue
6. **Perguntas e feedback** (15min)

### O que NÃO fazer na demo

- Não executar scan na rede do cliente sem engagement assinado
- Não mostrar dados reais de outro cliente (mesmo anonimizados)
- Não prometer cobertura de vulnerabilidades que o scanner não detecta
- Não usar modo de demonstração client-side como se fossem dados reais

### Material necessário

- Ambiente de laboratório: VMs com serviços propositalmente vulneráveis (DVWA, Vulhub, ou similar)
- Relatório de exemplo com achados reais do laboratório
- Roteiro de apresentação de 30–45min

---

## 4. Piloto

### Critérios para iniciar um piloto

1. Gates G0 atingidos (mínimo de segurança)
2. Contrato de piloto assinado (mesmo que gratuito)
3. Engagement assinado com escopo definido por escrito
4. Responsável técnico do cliente identificado
5. Expectativas alinhadas por escrito: o que entregamos, o que não entregamos, limitações

### Estrutura de um piloto

| Etapa | Entrega | Prazo sugerido |
|---|---|---|
| Onboarding | Conta criada, escopo acordado, engagement autorizado | Dia 1 |
| Avaliação inicial | Execução, revisão de achados, relatório provisório | Dias 2–5 |
| Entrega | Reunião de resultados, relatório final | Dia 7 |
| Acompanhamento | Revisão de 2 semanas: o que foi corrigido? | Dia 21 |
| Retrospectiva | Feedback do cliente, decisão de continuar ou não | Dia 30 |

### O que medir no piloto

| Métrica | Meta | Real |
|---|---|---|
| Tempo do onboarding ao primeiro relatório | <7 dias | ? |
| Achados que o cliente considerou úteis | >50% | ? |
| Achados que o cliente corrigiu | >1 | ? |
| Horas da equipe ASTRO por piloto | <20h | ? |
| O cliente pagaria? Por quanto? | Sim | ? |

---

## 5. Funil B2B simplificado

```
1. Prospecção
   └─ Rede pessoal, LinkedIn, indicações, comunidades de TI
   
2. Qualificação
   └─ Tem profissional de TI? Tem infraestrutura? Tem decisor acessível?
   
3. Entrevista de descoberta
   └─ Entender o problema; não vender ainda
   
4. Demo funcional
   └─ Mostrar o produto com dados de laboratório
   
5. Proposta
   └─ Escopo, entrega, limitações, preço, prazo
   
6. Contrato + engagement
   └─ Assinatura obrigatória antes de qualquer varredura
   
7. Piloto / Entrega
   └─ Executar, revisar, entregar, reunião
   
8. Renovação / upgrade
   └─ Acompanhamento recorrente ou próxima avaliação
```

---

## 6. Mensagens por público

### Para o gestor

> "Você sabe o que um hacker veria se olhasse para a rede da sua empresa agora? Nós identificamos as exposições, explicamos o risco em linguagem de negócio e acompanhamos a equipe de TI até a correção."

### Para o analista de TI

> "Você recebe uma lista priorizada de exposições com evidências técnicas e orientação de correção em português. Sem precisar interpretar uma lista de CVEs."

### Para o prestador de TI / MSP

> "Você entrega um diagnóstico de segurança para seu cliente sem precisar de equipe especializada. A ASTRO faz a avaliação; você entrega o resultado com seu nome."

---

## 7. Respostas a objeções comuns

| Objeção | Resposta honesta |
|---|---|
| "Você garante que não há vulnerabilidades?" | Não garantimos. Identificamos o que o nosso scanner defensivo consegue detectar dentro do escopo autorizado. Zero achados não significa segurança. |
| "Vocês fazem pentest completo?" | Não. Fazemos avaliação defensiva de infraestrutura: inventário de serviços expostos e classificação de achados. Não fazemos exploração manual, pentest de aplicação web ou teste de engenharia social. |
| "Já tenho antivírus/firewall, preciso disso?" | Antivírus e firewall não identificam o que está acessível de fora nem o que um atacante veria. São camadas diferentes. |
| "Isso não é obrigatório para nós (sem regulação)" | Não é obrigatório. Mas quando um incidente acontece, a pergunta é: você sabia do risco antes? |
| "É caro demais" | Depende de comparar com o custo de um incidente. O que a ferramenta faz é ajudar a priorizar onde investir. Podemos dimensionar o escopo para o orçamento disponível. |

---

## 8. Critérios para decidir se o negócio merece mais investimento

Responda essas perguntas após os primeiros 3 pilotos:

1. Pelo menos 1 cliente pagou o que pedimos?
2. Pelo menos 1 cliente corrigiu algum achado baseado na nossa entrega?
3. O custo de atendimento por cliente é menor que o preço de venda?
4. Os fundadores conseguem atender mais clientes sem contratar?
5. Algum cliente indicou outro cliente?

Se 3+ dessas forem "sim", continuar. Se <2 forem "sim", revisar hipótese antes de continuar.
