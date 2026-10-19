# ASTRO Cyber — Estratégia Executiva

Data: 2026-10-18. Baseado em leitura do código e documentos internos, sem validação de mercado com clientes.

---

## 1. Problema real que resolvemos

PMEs brasileiras não têm equipe de segurança. O único profissional de TI está sobrecarregado e não sabe priorizar. O dono do negócio não entende de cibersegurança, mas é quem aprova (ou nega) verba para correção.

Resultado: exposições conhecíveis ficam abertas porque ninguém consegue traduzir risco técnico em decisão de negócio.

---

## 2. O que a ASTRO entrega

| Para quem | Entrega concreta |
|---|---|
| Analista de TI / operador | Inventário de serviços expostos, classificação de achados, evidências rastreáveis, orientação de correção em português |
| Gestor / dono | O que está em risco, prioridade, quem é responsável, o que foi corrigido — sem jargão técnico |
| Prestador de TI (MSP) | Ferramenta para atender múltiplas PMEs com uma equipe pequena |

---

## 3. Posicionamento vs concorrentes

| Concorrente | Realidade | Diferença ASTRO (hipótese a validar) |
|---|---|---|
| Tenable / Nessus | Poderoso, complexo, caro para PME | ASTRO é mais simples; não tem cobertura equivalente |
| Intruder.io | SaaS para PME, fácil, descoberta contínua | Mercado EN/US; ASTRO foca português BR e ciclo correção |
| runZero | Excelente descoberta de ativos | Sem classificação de achados ou ciclo de correção |
| Greenbone/OpenVAS | Open-source, gratuito, cobertura de CVEs | Complexo de operar; sem interface para gestor |
| NodeZero / Pentera | Pentest autônomo avançado | Custosos, voltados para equipes de segurança experientes; ASTRO não é pentest |

**Posicionamento atual honesto:** ASTRO é um **scanner TCP defensivo com organização de achados e relatório de negócio** — não é pentest, não é scanner de vulnerabilidades completo. O diferencial é a experiência em português com foco no ciclo descoberta→ação→revalidação para PME.

---

## 4. Decisão recomendada sobre oferta inicial

**Lançar como serviço de avaliação defensiva assistida**, não como SaaS self-service.

- ASTRO realiza a avaliação com ferramentas internas, escopo acordado por escrito e análise humana
- Cliente recebe relatório, reunião de entrega e acompanhamento de correções
- Portal web é opcional, somente leitura, para o cliente acompanhar status
- Não cobrar por assinatura de plataforma antes de ter billing real e conector

**Por quê este caminho:**
1. Não exige conector, billing real, MFA, nem jobs duráveis no backend
2. A equipe controla qualidade da entrega — menos risco de falso positivo vendido
3. Permite aprender com clientes reais antes de construir autoatendimento
4. Gate G1 é atingível em semanas; G3 (SaaS autogerenciado) leva meses

---

## 5. Cinco maiores riscos

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| R1 | Vender como "pentest" o que é inventário TCP — responsabilidade jurídica e reputacional | Alto | Contratos claros; limitações na entrega; sem usar a palavra "pentest" sem metodologia completa |
| R2 | Falha de isolamento entre tenants vaza dados de um cliente para outro | Alto | Jobs duráveis pendentes; hoje execução em thread sem persistência após reinício |
| R3 | Chave IA em texto puro (`instance/ai_config.json`) — se servidor comprometido, API key vazada | Médio | A11 pendente; não distribuir servidor sem resolver |
| R4 | Equipe de 3 fundadores sem vendas validadas → construir produto que ninguém compra | Alto | Iniciar entrevistas e piloto antes de mais desenvolvimento |
| R5 | Scanner TCP gera falsos positivos → gestor toma decisão errada baseada em evidência fraca | Médio | Classificação observação/suspeita/confirmado já implementada; treinar cliente a interpretar |

---

## 6. Cinco oportunidades mais relevantes

| # | Oportunidade |
|---|---|
| O1 | Prestadores de TI e MSPs como canal: eles já têm o cliente e precisam de ferramenta para entregar valor de segurança |
| O2 | Relatório em português com linguagem de negócio — nenhum concorrente direto no BR faz isso para PME |
| O3 | Ciclo de correção + revalidação: ninguém no mercado acessível para PME fecha o loop "achado → corrigido → verificado" |
| O4 | Pilotos gratuitos ou subsidiados como ferramenta de aquisição e aprendizado de produto |
| O5 | Modelo de serviço assistido reduz risco de lançamento: equipe entrega manualmente, aprende o que automatizar depois |
