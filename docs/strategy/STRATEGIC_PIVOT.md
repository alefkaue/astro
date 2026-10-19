# ASTRO Cyber — Pivô Estratégico: Service-First, Product-Later

Data: 2026-10-19. Documento de decisão estratégica baseado em auditoria real do codebase e dos documentos anteriores.

---

## 1. Auditoria do Estado Atual

### 1.1 O que a plataforma realmente faz hoje

A plataforma é um SaaS multi-tenant funcional em ambiente de laboratório. Ela faz:

- **Autenticação e RBAC real:** login, sessões assinadas, 5 papéis, isolamento por `account_id`, rate-limit de login persistido em SQLite.
- **Scanner de rede defensivo:** inventário TCP com fallback automático (Go → Nmap → socket Python); escopo obrigatório via engagement; bloqueios de loopback, link-local, metadata e OT.
- **Classificação de achados:** severidade padronizada, estimativa financeira com disclaimer, persistência em SQLite.
- **AEGIS (IA):** integração Groq com fallback offline determinístico, sanitização anti-prompt-injection, chave cifrada em repouso com Fernet + PBKDF2.
- **Geração de PDF:** relatório executivo e técnico via fpdf2.
- **Engagements:** escopo autorizado por admin antes de qualquer varredura.
- **173 testes passando**, gate G0 completo.

### 1.2 Funcionalidades implementadas e testadas

| Funcionalidade | Estado |
|---|---|
| Login / RBAC / multi-tenant | Implementado e testado |
| Scanner TCP com fallback | Implementado e testado |
| Bloqueio de escopo / safety | Implementado e testado (139 testes de escopo) |
| Engagements com autorização | Implementado e testado |
| Achados com estimativa financeira | Implementado e testado |
| AEGIS com fallback offline | Implementado e testado |
| Chave IA cifrada em repouso | Implementado e testado |
| Rate-limit SQLite multi-worker | Implementado e testado |
| Geração de PDF | Implementado (QA visual não feito) |
| Isolamento de tenant cross-cutting | Implementado e testado |

### 1.3 Funcionalidades incompletas, desativadas ou demonstrativas

| Funcionalidade | Situação real |
|---|---|
| Agente autônomo | Thread em memória; estado perdido no reinício; checks ofensivos desativados |
| Billing / planos | Catálogo existe; checkout simulado; sem integração de pagamento real |
| Jobs duráveis | Ausente; G1 |
| Cancelamento de job | Ausente |
| Cobertura estruturada | Ausente (zero achados ≠ seguro) |
| MFA | Ausente |
| Recuperação de senha | Ausente |
| IDs estáveis de achados entre avaliações | Ausente |
| Ciclo de correção / revalidação | Ausente |
| QA visual acessibilidade | Não executado |
| Modo de demonstração client-side | Funcional mas isolado do backend real |

### 1.4 O que pode ser aproveitado para prestação manual de serviços

**Aproveitável agora:**
- Scanner (execução local, ambiente autorizado)
- Engagements como controle de escopo e autorização
- Relatório PDF como entregável
- AEGIS para sugestões de remediação
- Multi-tenant para separar clientes internamente

**Requer preparação mínima:**
- Template de proposta e RoE (documento, não código)
- Ambiente de laboratório com VMs vulneráveis para demo
- Processo de entrega documentado

### 1.5 Funcionalidades que fazem sentido manter para o futuro

Toda a base atual é válida. Os módulos de autenticação, scanner, achados, AEGIS, PDF e engagements formam o núcleo do produto. Nada deve ser removido.

### 1.6 Áreas consumindo esforço sem valor comercial imediato

- **Billing / checkout simulado:** nenhum cliente pagou ainda; checkout real é G3.
- **Modo demo client-side:** útil para mostrar o produto, mas não é o caminho de venda real.
- **Agente autônomo (checks ofensivos):** desativado por razão correta; completar não é prioridade antes de clientes reais.
- **Frontend: acessibilidade WCAG 2.2 AA:** importante, mas não bloqueia os primeiros serviços.
- **Multi-worker / escalabilidade:** irrelevante com 1–3 clientes.

### 1.7 Precisamos alterar a arquitetura?

Não. A arquitetura atual suporta os primeiros serviços sem alteração estrutural. O que falta é:
- Um site institucional (vitrine comercial separada, nova).
- Documentos operacionais (proposta, RoE, relatório).
- Preparação legal (CNPJ, contratos).

### 1.8 Risco de quebrar o sistema na transição

Zero, se seguirmos a diretriz: não tocar no backend, scanner, auth ou banco para a mudança comercial. A vitrine comercial deve ser um site estático separado. Não há risco de regressão.

---

## 2. Classificação de Componentes

| Componente | Classificação | Justificativa |
|---|---|---|
| Auth / RBAC / multi-tenant | **Usar agora** | Núcleo funcional e testado |
| Scanner TCP defensivo | **Usar agora** | Entregável central dos serviços |
| Engagements (escopo/autorização) | **Usar agora** | Controle ético obrigatório |
| Achados + estimativa financeira | **Usar agora** | Diferencial da entrega |
| AEGIS offline | **Usar agora** | Remediação sem custo de API |
| Geração de PDF | **Usar agora** | Entregável de relatório |
| Agente autônomo (defensive mode) | **Desenvolver depois** | Após jobs duráveis (G1) |
| Jobs duráveis | **Desenvolver depois** | Bloqueador G1 |
| Ciclo correção/revalidação | **Desenvolver depois** | G2; exige clientes reais para validar |
| Billing / checkout real | **Desenvolver depois** | G3; não antes de 3 clientes pagando manualmente |
| IDs estáveis de achados | **Desenvolver depois** | G2 |
| MFA | **Desenvolver depois** | G1 |
| Modo demo client-side | **Ajustar pontualmente** | Desabilitar em produção pública; manter para demos internas |
| Checkout simulado / billing fake | **Ocultar** | Não expor antes de billing real |
| Credenciais de demo (`dono@pme.com`, etc.) | **Ocultar** | Nunca expor em ambiente público |
| Checks ofensivos do agente | **Ocultar** | Manter desativados até metodologia e autorizações prontas |
| Frontend: logos CYMAG remanescentes | **Ajustar pontualmente** | Consistência de marca ASTRO |

---

## 3. Comparação das Três Estratégias

### Estratégia A — Continuar construindo o SaaS antes de vender

**O que significa:** focar os próximos 3–6 meses em completar G1, G2, billing real, jobs duráveis, MFA, ciclo de correção, antes de abordar clientes.

**Pontos positivos:**
- Produto mais completo antes de comprometer com clientes.
- Menos improvisação na entrega.

**Problemas reais:**
- Validação zero. Você constrói o que acha que o cliente quer, sem confirmar.
- G1 a G3 são meses de trabalho sem receita.
- O risco de construir funcionalidades que o cliente não valoriza é alto.
- A equipe tem 3 fundadores, sem funcionários, sem caixa validado. Sustentar isso por 6+ meses sem receita é difícil.
- Já existe um produto funcional suficiente para um primeiro serviço manual. Continuar só construindo é desperdício de janela de mercado.

**Veredicto:** inviável como estratégia principal. Aceitável como parte do trabalho paralelo.

---

### Estratégia B — Abandonar temporariamente o software e operar só como consultoria

**O que significa:** pausar o desenvolvimento e usar apenas ferramentas de mercado (Nessus, Nmap manual, relatórios em Word) para entregar serviços.

**Pontos positivos:**
- Valida o mercado e a operação rapidamente.
- Sem dependência de uma plataforma imatura.

**Problemas reais:**
- Desperdiça o trabalho já feito. O scanner, AEGIS e PDF da ASTRO já são funcionais para serviços básicos.
- Custo operacional mais alto usando ferramentas pagas de terceiros.
- Diferenciação menor: você vira mais uma consultoria comum.
- Difícil retomar o produto depois, com time dividido entre operação e desenvolvimento.

**Veredicto:** inadequada. Ignora o ativo principal que já existe.

---

### Estratégia C — Começar com serviços manuais + desenvolver plataforma em paralelo

**O que significa:** usar a plataforma atual (G0 completo) para entregar os primeiros serviços com operação presencial dos fundadores, enquanto o desenvolvimento continua orientado pelo que é difícil ou lento no campo.

**Por que funciona aqui:**
- G0 está completo: scanner, auth, engagements, AEGIS, PDF.
- O produto já entrega o suficiente para os primeiros serviços (ASTRO Assessment, ASTRO Exposure).
- Cada hora de entrega informa o que construir a seguir, eliminando desperdício de desenvolvimento.
- Receita dos serviços sustenta o desenvolvimento do produto.
- Com 3 fundadores sem funcionários e orçamento limitado, este é o caminho de menor risco financeiro.

**Riscos reais:**
- Sobrecarga: entregar serviços e desenvolver produto ao mesmo tempo exige disciplina de separação de tempo.
- Risco de se tornar só consultoria e nunca virar produto. Requer critérios explícitos para decidir quando um processo manual vira funcionalidade.
- Qualidade de entrega depende de processo, documentação e revisão técnica rigorosos — não só da plataforma.

**Mitigação dos riscos:**
- Definir desde o início quanto tempo cada fundador dedica a operação vs. produto por semana.
- Usar `PRODUCT_EVOLUTION.md` como critério para não construir funcionalidades antes de validar.
- Não aceitar mais clientes do que a equipe consegue atender com qualidade.

**Veredicto: recomendada.**

---

## 4. Estratégia Recomendada

**ASTRO opera como empresa de serviços de cibersegurança desde agora, usando a plataforma G0 como ferramenta interna. O produto evolui orientado pela operação.**

### Critérios para revisar esta estratégia

Abandone a Estratégia C e mude para foco em produto (Estratégia A) se ocorrer qualquer um dos seguintes:

1. A equipe não consegue atender mais de 2 clientes simultaneamente sem contratar.
2. A entrega de serviços consome mais de 70% do tempo total dos fundadores por mais de 2 meses consecutivos.
3. 3 clientes potenciais confirmam que pagariam pela plataforma self-service, mas não pela consultoria.
4. Um concorrente direto lança produto equivalente com distribuição superior.

---

## 5. Respostas às 10 Perguntas Finais

1. **Devemos mudar para serviços primeiro?** Sim. A plataforma G0 já suporta os primeiros serviços. Há zero validação de mercado. Serviços primeiro eliminam esse risco.

2. **Precisamos alterar o código atual? Quanto?** Muito pouco. Nenhuma alteração estrutural. Ajustes pontuais: ocultar demo credentials de ambiente público, verificar consistência de marca ASTRO, criar site institucional estático separado.

3. **Devemos separar o site comercial do aplicativo?** Sim. O app atual não é uma vitrine — é uma ferramenta técnica. O site institucional deve ser estático, independente, sem rotas do app. Ver `WEBSITE_STRATEGY.md`.

4. **Quais serviços podemos preparar mais rapidamente?** ASTRO Assessment (diagnóstico de infraestrutura) e ASTRO Exposure (inventário de serviços expostos). Ver `SERVICE_CATALOG.md`.

5. **Quais serviços ainda não temos condições de oferecer?** ASTRO Pentest (metodologia de exploração não validada, autorização complexa), ASTRO Continuous (exige jobs duráveis, G1), ASTRO Fraud & Awareness (requer capacitação específica em engenharia social e treinamento corporativo).

6. **Como atenderíamos o primeiro cliente manualmente?** Ver `MANUAL_OPERATIONS.md`. Resumo: descoberta → proposta → contrato + RoE → execução com plataforma G0 → revisão → relatório PDF → reunião → entrega formal.

7. **O que desenvolver no software durante esse período?** Apenas o que travar a operação: jobs duráveis quando perder estado virar problema real, cancelamento de job, cobertura estruturada. Ver `PRODUCT_EVOLUTION.md`.

8. **Quanto precisamos investir inicialmente?** R$400–R$800 para validação (domínio, e-mail, site). R$1.500–R$3.500 para os primeiros serviços (infra, ferramentas mínimas, custos jurídicos básicos). Ver `BUSINESS_READINESS.md`.

9. **Quais condições precisam ser cumpridas antes da primeira venda?** CNPJ ativo, contrato padrão revisado por advogado, RoE template, ambiente de demo pronto, fundadores com escopo de responsabilidade definido. Ver `BUSINESS_READINESS.md`.

10. **Qual a ordem concreta das primeiras tarefas para os 3 fundadores?** Ver `90_DAY_PLAN.md`.
