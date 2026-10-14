# Handoff para IA — Plano de aplicação da ideia

> Arquivo de contexto. Data da pesquisa: 2026-10-13. As fontes são majoritariamente blogs de contabilidade (não texto legal direto); as conclusões são consistentes entre elas, mas números tributários de 2026 devem ser confirmados com contador.

---

## PROMPT (cole isto para a outra IA)

```
Você é um consultor de negócios e produto. Com base no CONTEXTO abaixo,
crie um PLANO DE APLICAÇÃO prático e faseado para lançar nossa plataforma
de tecnologia (automações + cibersegurança + software/SaaS), feita por 3
sócios, SEM produto pronto e SEM clientes ainda, com orçamento próximo de
zero no início.

Entregue:
1. Roadmap em fases (0 = agora/sem custo → formalização só quando houver receita).
2. MVP: menor versão vendável do produto, escopo enxuto e prazo.
3. Validação: como conseguir os primeiros clientes antes de investir.
4. Estrutura legal/tributária por fase (ver conclusões já definidas abaixo —
   respeite-as, não recomende LTDA agora).
5. Divisão entre os 3 sócios (papéis + acordo simples escrito).
6. Checklist de "gatilhos": o que dispara cada próximo passo (ex.: 1º cliente pagante).
7. Riscos e como mitigar com custo baixo.

Seja concreto, priorize o mais barato e simples para começar JÁ.
Não repita teoria genérica; foque em ações.
```

---

## CONTEXTO DA IDEIA

- **Produto base já em desenvolvimento:** "ASTRO Cyber" — SaaS de segurança (scanner de vulnerabilidades, Flask + SQLite, scanner em Go; multi-tenant com isolamento por conta). Código legado chamado `cymag_saas`.
- **Nova visão:** plataforma de tecnologia geral — **automações, cibersegurança e software/SaaS**.
- **Time:** 3 sócios.
- **Estágio:** sem produto finalizado, sem clientes, sem caixa para arcar com custos de abertura, contador mensal e advogado agora.
- **País:** Brasil.
- **Objetivo imediato:** começar a atuar e oferecer serviços da forma mais simples e barata possível, formalizando só quando necessário.

## CONCLUSÕES DA CONSULTORIA (já decididas — a IA deve respeitar)

1. **MEI está VEDADO para o core** (desenvolvimento de software, consultoria/auditoria de segurança da informação, automação). Esses CNAEs (6201, 6202, 6203, 6204, 6209) não estão na lista de ocupações do MEI. Usar MEI com CNAE incompatível = risco de cancelamento retroativo do CNPJ. Teto do MEI segue em R$ 81 mil/ano (2026).
2. **Cibersegurança digital ≠ segurança privada regulada** (Lei 7.102/83 / Polícia Federal). Não precisa dessa licença. O que importa é contrato com escopo/autorização de teste por escrito.
3. **Faseamento recomendado:**
   - **Fase 0 (agora, R$ 0):** não abrir empresa. Desenvolver o produto + fazer um acordo simples escrito entre os 3 sócios (% de cada um, papéis, regra de saída). Sem cartório/advogado caro ainda.
   - **Fase 1 (primeiro dinheiro esporádico):** receber como **pessoa física** via carnê-leão / RPA (se cliente for PJ, ele retém INSS e IRRF). Sem CNPJ, sem mensalidade. Atenção: alguns municípios (ex.: São Paulo) passaram a exigir NFS-e de autônomo inscrito no CCM em 2026 — confirmar na prefeitura local.
   - **Fase 2 (cliente recorrente / precisa emitir nota):** abrir o CNPJ mais simples = **Empresário Individual (EI) no Simples Nacional** por um dos sócios (sem contrato social, sem capital mínimo). Contador ~R$ 150–350/mês só então.
   - **Fase 3 (produto validado + faturamento):** converter para **LTDA** com os 3 sócios formalizados; aí entram contrato social, acordo de sócios com vesting (cliff, good/bad leaver, drag/tag along), e calibragem de pró-labore x distribuição de lucros via **Fator R** (≥28% mantém Anexo III a ~6% em vez do Anexo V a ~15,5%).
4. **Tributação de lucros em 2026 tem divergência entre fontes** (Lei 15.270/2025 teria criado isenção de IR no pró-labore até R$ 5 mil/mês e retenção de 10% sobre distribuição acima de R$ 50 mil/mês por sócio). Confirmar com contador.
5. **Orientação gratuita recomendada antes de formalizar:** SEBRAE e/ou 1ª conversa com contador (geralmente sem custo). Não assinar plano mensal sem receita.

## PERGUNTAS QUE O PLANO DEVE AJUDAR A RESPONDER

- Qual o MVP mínimo do ASTRO que já dá para vender/demonstrar?
- Como conseguir os 3–5 primeiros clientes sem gastar?
- Em que ordem fazer: produto → validação → formalização.
- Como dividir trabalho e participação entre os 3 de forma justa e barata.

---

## FONTES PESQUISADAS

### Enquadramento / MEI para TI
- https://wetax.com.br/programador-pode-ser-mei-em-2026
- https://contabilidade.com/blog/consultor-em-ti-pode-ser-mei-em-2026-veja-como-abrir-seu-cnpj-corretamente-e-pagar-menos-impostos/
- https://www.meucontadoronline.com.br/blog/mei-em-ti-atividades-permitidas-riscos-fiscais/
- https://www.contabilizei.com.br/contabilidade-online/profissional-de-ti-pode-ser-mei/

### CNAE para tecnologia
- https://www.meucontadoronline.com.br/blog/cnae-ti-tudo-para-desenvolvedores-consultores-empresas-de-ti
- https://agilize.com.br/artigos/?p=4222

### Simples Nacional / Anexo III x V / Fator R
- https://www.e-auditoria.com.br/blog/anexo-iii-ou-anexo-v-simples-nacional/
- https://simplifique.contmatic.com.br/blogs/fator-r-simples-nacional-o-que-e-como-calcular
- https://contabilidade.com/blog/simples-nacional-2026-guia-completo-de-anexos-fator-r-limites-e-das/

### Limite / teto do MEI 2026
- https://www.infinitepay.io/blog/limite-faturamento-mei-2026
- https://simplifique.contmatic.com.br/blogs/mei-2026-limite-faturamento-o-que-muda

### Natureza jurídica (SLU, EI, LTDA)
- https://contaja.com.br/blog/sociedade-limitada-unipessoal/
- https://www.contabilizei.com.br/contabilizei-responde/diferenca-entre-empresario-em-nome-individual-e-sociedade-unipessoal/

### Pró-labore x distribuição de lucros (2026)
- https://treeunfe.com.br/blog/simples-nacional-distribuicao-de-lucros-pro-labore-e-como-dividir
- https://contaja.com.br/blog/pro-labore-ou-distribuicao-de-lucros/
- https://valorfinal.com.br/guia/distribuicao-de-lucros-como-funciona

### Acordo de sócios / vesting
- https://startups.com.br/coluna/freitasferrazadvogados/contratos-de-vesting-o-que-voce-precisa-saber-antes-de-usa-lo-na-sua-startup/
- https://querobolsa.com.br/revista/cliff-e-vesting

### Pessoa física / carnê-leão / RPA / NFS-e autônomo
- https://agilize.com.br/artigos/?p=4003
- https://triviumcontabil.com.br/?p=17647
- https://www.contabilizei.com.br/contabilizei-responde/como-declarar-rpa-no-imposto-de-renda/

### MVP / lançamento de SaaS
- https://aws.amazon.com/startups/learn/prove-whats-possible-startup-mvp-offers-max-value-potential?lang=pt-BR
- https://judit.io/blog/ia-dados-juridicos/como-construir-um-saas/
- https://payproglobal.com/pt_br/como/crie-um-mvp-para-saas/

### Custos de abertura / contador
- https://www.meucontadoronline.com.br/blog/quanto-custa-contador-para-me/
- https://agilize.com.br/artigos/?p=1910
