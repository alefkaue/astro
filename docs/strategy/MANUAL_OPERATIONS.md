# ASTRO Cyber — Operação Manual de Serviços

Data: 2026-10-19. Processo operacional para prestação de serviços antes de automação completa.

**Princípio:** cada etapa tem documentos, ferramentas e critério de conclusão definidos. Não avançar para a próxima etapa sem completar a atual.

> Documentos marcados com _(minuta)_ devem ser revisados por advogado antes do primeiro contrato real.

---

## Fluxo de 11 Etapas

---

### Etapa 1 — Primeiro Contato

**Objetivo:** entender de onde veio o lead e qual é a necessidade inicial.

**Documentos necessários:**
- Formulário de contato (site ou e-mail)
- Planilha de prospecção (nome da empresa, contato, origem, data)

**Ferramentas:**
- E-mail profissional (domínio astrocyber.com.br ou similar)
- Planilha de leads (Google Sheets ou equivalente)

**Checklist:**
- [ ] Registrar empresa, contato, como nos conheceu, necessidade declarada
- [ ] Verificar se a empresa não está em lista de restrição (cliente de concorrente com NDA, por exemplo)
- [ ] Confirmar que há decisor acessível para agendar reunião

**Resposta padrão ao contato inicial (adaptar):**

> "Olá, [Nome]. Obrigado pelo contato com a ASTRO Cyber. Para entender melhor como podemos ajudar [empresa], gostaria de agendar uma conversa de 30 minutos. Qual é a sua disponibilidade? Podemos usar [Google Meet / Teams / presencial]."

---

### Etapa 2 — Reunião de Descoberta

**Objetivo:** entender o problema, a infraestrutura, as expectativas e qualificar se há fit para nossos serviços.

**Documentos necessários:**
- Questionário de Descoberta (abaixo)

**Ferramentas:**
- Videoconferência ou presencial
- Notas estruturadas (documento compartilhado internamente)

**Questionário de Descoberta:**

```
ASTRO Cyber — Questionário de Descoberta
Data: [DATA]   Empresa: [NOME]   Contato: [NOME/CARGO]   Entrevistador: [FUNDADOR]

1. INFRAESTRUTURA E CONTEXTO
   a. Quantos funcionários a empresa tem?
   b. Tem equipe de TI interna? Terceirizada? Quantas pessoas?
   c. Quais serviços estão hospedados internamente vs. na nuvem?
   d. Tem VPN, acesso remoto, ou serviços expostos na internet?
   e. Qual o sistema de e-mail? (Exchange, Google Workspace, etc.)
   f. Tem filiais ou escritórios remotos?

2. HISTÓRICO DE SEGURANÇA
   a. Já teve algum incidente de segurança? (ransomware, phishing, acesso não autorizado)
   b. Já fez algum tipo de avaliação de segurança antes? Quando?
   c. Usa antivírus, EDR, SIEM, ou outra ferramenta de segurança?
   d. Existe política de senhas, autenticação em dois fatores (MFA)?

3. DOR E MOTIVAÇÃO
   a. Por que está buscando esse serviço agora? O que mudou?
   b. Qual é sua maior preocupação em segurança hoje?
   c. Tem alguma regulação ou auditoria que exige controles de segurança? (LGPD, ISO, cliente grande exigindo)
   d. Como você justifica investimento em segurança para a diretoria/dono?

4. EXPECTATIVAS
   a. O que esperaria receber ao final de um serviço como esse?
   b. Quem seria o responsável por implementar as correções sugeridas?
   c. Qual seria o prazo ideal para vocês?
   d. Tem orçamento definido? Alguma referência de valor?

5. PRÓXIMOS PASSOS
   a. Quem mais precisa ser envolvido na decisão?
   b. Qual seria a próxima data possível para avançar?
```

**Critério de conclusão:** notas da reunião registradas; decisão sobre fit (avançar/não avançar).

**Critérios para NÃO avançar:**
- Empresa quer pentest ofensivo completo (não temos esta capacidade agora)
- Escopo inclui sistemas de terceiros sem autorização desses terceiros
- Decisor não acessível ou budget inexistente
- Infraestrutura regulada com exigências que não conseguimos cumprir (BACEN, ANS, etc.)

---

### Etapa 3 — Definição de Necessidades e Limites

**Objetivo:** traduzir o que o cliente quer no que podemos entregar, com limites claros.

**Documentos necessários:**
- Rascunho do escopo (interno, para revisão antes da proposta)

**Checklist:**
- [ ] Definir IPs/CIDRs específicos que serão avaliados
- [ ] Confirmar que todos os ativos no escopo pertencem ao cliente
- [ ] Definir o que NÃO está no escopo e comunicar ao cliente
- [ ] Identificar janela de execução (horário de menor impacto)
- [ ] Identificar contato de emergência do cliente para paralisação imediata se necessário
- [ ] Estimar esforço interno (horas de equipe)
- [ ] Calcular preço com base no escopo

---

### Etapa 4 — Proposta Comercial

**Objetivo:** apresentar formalmente o serviço, escopo, entregáveis, prazo e preço.

**Template de Proposta Comercial _(minuta — revisar com advogado)_:**

```
PROPOSTA COMERCIAL — ASTRO Cyber
Nº [SEQUENCIAL]   Data: [DATA]   Validade: 15 dias

CONTRATANTE: [RAZÃO SOCIAL], CNPJ [CNPJ], representada por [NOME/CARGO]
PRESTADOR:   ASTRO Cyber [CNPJ quando disponível], representada por [FUNDADOR]

1. SERVIÇO PROPOSTO
   [ASTRO Assessment / ASTRO Exposure]

2. ESCOPO
   Ativos avaliados: [IPs/CIDRs específicos]
   Janela de execução: [DATA/PERÍODO]
   O que está FORA do escopo:
   - Aplicações web e APIs (não avaliamos código ou lógica de aplicação)
   - Engenharia social ou simulação de phishing
   - Exploração ativa de vulnerabilidades (apenas identificação e evidência de banner)
   - Sistemas não listados acima

3. METODOLOGIA
   Utilizamos scanner de rede defensivo, inventário TCP e análise de banners de serviço.
   Os resultados são classificados por severidade e revisados manualmente pela equipe.
   A plataforma ASTRO é utilizada internamente para execução e geração do relatório.

4. ENTREGÁVEIS
   - Relatório executivo (linguagem de negócio)
   - Relatório técnico (achados com evidências e recomendações)
   - Reunião de apresentação de resultados (1–2h)
   - Termo de entrega

5. PRAZO
   Início: após assinatura do contrato e do RoE
   Entrega do relatório: [X] dias úteis após início
   Reunião de resultados: [DATA]

6. LIMITAÇÕES E ISENÇÕES
   - Zero achados não significa ausência de vulnerabilidades
   - As estimativas financeiras são de ordem de grandeza para priorização
   - A ASTRO não se responsabiliza por vulnerabilidades fora do escopo acordado
   - Este serviço não substitui auditoria de conformidade regulatória

7. INVESTIMENTO
   Valor: R$ [VALOR]
   Forma de pagamento: [50% na assinatura, 50% na entrega / à vista / etc.]
   Emissão de nota fiscal: sim

8. PRÓXIMOS PASSOS
   1. Aprovação desta proposta
   2. Assinatura do contrato de prestação de serviços
   3. Assinatura do RoE (documento técnico de autorização)
   4. Início do serviço

[Assinaturas]
```

---

### Etapa 5 — Contrato, NDA e Autorização de Escopo (RoE)

**Objetivo:** formalizar a relação, proteger ambas as partes, autorizar tecnicamente o serviço.

**Documentos necessários _(todos são minutas — revisar com advogado)_:**

#### Contrato de Prestação de Serviços (itens mínimos)

```
CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE DIAGNÓSTICO DE SEGURANÇA
_(minuta — revisar com advogado)_

CLÁUSULAS ESSENCIAIS:

1. OBJETO: prestação de serviço de avaliação de segurança de infraestrutura conforme
   proposta comercial anexa (Nº [NÚMERO], data [DATA]).

2. ESCOPO AUTORIZADO: definido exclusivamente no RoE anexo. Qualquer ativo não listado
   no RoE está fora do escopo e não será avaliado.

3. OBRIGAÇÕES DO CONTRATANTE:
   a. Fornecer autorização escrita e lista de ativos
   b. Garantir que possui autorização legal sobre todos os ativos do escopo
   c. Designar responsável técnico para contato de emergência
   d. Não usar os relatórios como prova de conformidade regulatória

4. OBRIGAÇÕES DO PRESTADOR:
   a. Executar o serviço dentro do escopo autorizado
   b. Manter sigilo sobre os dados do contratante
   c. Não revelar resultados a terceiros sem autorização
   d. Suspender imediatamente se detectar comprometimento ativo e notificar o contratante

5. LIMITAÇÃO DE RESPONSABILIDADE:
   a. Zero achados não garante ausência de vulnerabilidades
   b. O prestador não responde por danos causados por vulnerabilidades fora do escopo
   c. O prestador não responde por incidentes anteriores ao serviço
   d. Responsabilidade limitada ao valor pago pelo serviço

6. CONFIDENCIALIDADE (NDA mútuo):
   a. ASTRO não revela dados do cliente (topologia, achados, relatórios)
   b. Cliente não revela metodologia, ferramentas ou relatórios da ASTRO a concorrentes

7. PROTEÇÃO DE DADOS (LGPD):
   a. Dados coletados: endereços IP, banners de serviço, configurações de rede
   b. Não coletamos dados pessoais de funcionários do cliente
   c. Retenção: [X] meses após entrega; exclusão mediante solicitação
   d. Não enviamos dados do cliente para APIs externas sem autorização

8. PRAZO E PAGAMENTO: conforme proposta comercial anexa.

9. RESCISÃO: com aviso de [X] dias; dados do cliente excluídos em [X] dias após rescisão.
```

#### RoE — Rules of Engagement (Autorização Técnica)

```
AUTORIZAÇÃO DE ESCOPO TÉCNICO — RULES OF ENGAGEMENT
_(minuta — revisar com advogado)_

Data: [DATA]
Empresa contratante: [RAZÃO SOCIAL]
Representante autorizado: [NOME / CARGO / CPF]
Prestador: ASTRO Cyber

AUTORIZAÇÃO:
Autorizo a ASTRO Cyber a executar avaliação de segurança de infraestrutura nos
seguintes ativos de nossa propriedade ou operação:

ATIVOS AUTORIZADOS:
[ ] IPs/CIDRs: [LISTA]
[ ] Domínios: [LISTA — se aplicável]

JANELA DE EXECUÇÃO AUTORIZADA:
Data de início: [DATA]   Término: [DATA]
Horário permitido: [ex: 08h–18h em dias úteis / 24h]

CONTATO DE EMERGÊNCIA (para paralisação imediata):
Nome: [NOME]   Telefone: [TELEFONE]   E-mail: [E-MAIL]

RESTRIÇÕES EXPLÍCITAS:
[ ] Não executar nada fora dos IPs/CIDRs listados acima
[ ] Não realizar exploração ativa (nenhum exploit)
[ ] Não acessar dados de usuários finais
[ ] [OUTRAS RESTRIÇÕES ESPECÍFICAS DO CLIENTE]

DECLARAÇÃO:
Declaro que tenho autorização legal para conceder permissão de avaliação sobre todos
os ativos listados acima e que estes são de propriedade ou responsabilidade de nossa
organização.

Assinatura do representante autorizado: _______________
Data: _______________
```

**Critério de conclusão:** contrato assinado + RoE assinado ANTES de qualquer varredura.

---

### Etapa 6 — Planejamento e Execução

**Objetivo:** executar o serviço dentro do escopo, documentando cada passo.

**Checklist pré-execução:**
- [ ] Contrato assinado
- [ ] RoE assinado e IPs verificados
- [ ] Engagement criado na plataforma ASTRO com IPs do RoE
- [ ] Ambiente de execução preparado (servidor, .env, backup)
- [ ] Horário de execução dentro da janela autorizada
- [ ] Contato de emergência do cliente salvo

**Checklist de execução:**
- [ ] Iniciar scan na plataforma ASTRO dentro do engagement autorizado
- [ ] Monitorar execução; interromper se houver sinal de serviço instável no cliente
- [ ] Ao final: revisar todos os achados manualmente antes de classificar
- [ ] Eliminar falsos positivos (verificar banner, versão, contexto)
- [ ] Classificar achados: observação / suspeita / confirmado (nunca "confirmado" sem evidência)
- [ ] Registrar evidências: captura de banner, resposta do serviço, versão detectada

---

### Etapa 7 — Registro de Evidências

**Objetivo:** documentar o que foi encontrado com rastreabilidade.

**Controle de Evidências:**

```
CONTROLE DE EVIDÊNCIAS
Avaliação: [CLIENTE / DATA]   Executor: [NOME]   Revisado por: [NOME]

ID | Host | Porta | Serviço | Severidade | Evidência | Classificação | Revisor
---|------|-------|---------|------------|-----------|---------------|--------
E001 | 192.168.1.10 | 22 | SSH OpenSSH 7.4 | Alta | banner: SSH-2.0-OpenSSH_7.4 | Confirmado | [NOME]
...

NOTAS:
- [Observações sobre o ambiente]
- [Serviços que não responderam mas estavam no escopo]
- [Anomalias que não se enquadram como achado]

LIMITAÇÕES DESTA AVALIAÇÃO:
- [O que não foi testado dentro do escopo]
- [Serviços que não estavam acessíveis no momento da avaliação]
```

---

### Etapa 8 — Revisão Técnica

**Objetivo:** garantir qualidade antes de entregar ao cliente.

**Checklist de revisão (feito por fundador diferente do executor):**
- [ ] Todos os achados "confirmado" têm evidência de banner ou resposta do serviço
- [ ] Nenhum achado inventado, exagerado ou sem evidência
- [ ] Classificação de severidade coerente com o impacto real
- [ ] Estimativas financeiras com disclaimer obrigatório
- [ ] Relatório executivo legível por alguém sem conhecimento técnico
- [ ] Relatório técnico com recomendação clara por achado
- [ ] Limitações da avaliação declaradas explicitamente
- [ ] Nenhuma promessa de ausência de vulnerabilidades

---

### Etapa 9 — Relatório

**Objetivo:** entregar documentos que o cliente consegue entender e agir.

#### Estrutura do Relatório Executivo

```
RELATÓRIO EXECUTIVO — ASTRO Assessment
[CLIENTE]   [DATA]   Confidencial

1. RESUMO EXECUTIVO (1 parágrafo)
   "Esta avaliação identificou X achados em Y ativos avaliados. Os achados de maior
   risco são [A, B, C]. Recomendamos priorizar [ação] nas próximas [X] semanas."

2. O QUE AVALIAMOS
   - Ativos: [lista de IPs/CIDRs]
   - Período: [data/hora]
   - Metodologia: scanner defensivo de rede (inventário TCP)

3. RESULTADOS
   [Gráfico ou tabela: crítico/alto/médio/baixo/informativo]
   
4. TOP 3 PRIORIDADES
   Para cada:
   - O que é
   - Por que é um risco para o negócio
   - O que fazer para corrigir
   - Complexidade de correção: baixa / média / alta

5. O QUE NÃO AVALIAMOS
   (aplicações web, engenharia social, dispositivos de usuário, etc.)

6. LIMITAÇÕES
   "Zero achados não significa ausência de vulnerabilidades. Esta avaliação cobre
   [escopo específico] e não representa uma auditoria de segurança completa."

7. PRÓXIMOS PASSOS RECOMENDADOS
```

#### Estrutura do Relatório Técnico

```
RELATÓRIO TÉCNICO — ASTRO Assessment
[CLIENTE]   [DATA]   Confidencial

1. METODOLOGIA E FERRAMENTAS
2. ESCOPO AVALIADO (IPs, janela, método)
3. ACHADOS (por severidade, decrescente)
   Para cada achado:
   - ID / Host / Porta / Serviço
   - Severidade: Crítica / Alta / Média / Baixa / Informativo
   - Classificação: Confirmado / Suspeita / Observação
   - Evidência (banner, versão, resposta)
   - Impacto potencial
   - Recomendação de correção
   - Referência (CVE se aplicável; com disclaimer de versão)
4. ACHADOS SEM CLASSIFICAÇÃO DE RISCO (informativo)
5. COBERTURA: o que foi testado e o que não foi
6. LIMITAÇÕES DESTA AVALIAÇÃO
```

---

### Etapa 10 — Reunião de Apresentação

**Objetivo:** apresentar os resultados, responder perguntas, alinhar próximos passos.

**Roteiro (60–90 min):**

```
0–5min: boas-vindas, agenda da reunião
5–15min: contexto — o que fizemos, como fizemos, o que não fizemos
15–35min: achados principais — top 3–5 com linguagem acessível
35–50min: recomendações práticas — o que fazer e em que ordem
50–60min: perguntas do cliente
60–75min: próximos passos — quem faz o quê, em quanto tempo
```

**O que NÃO fazer na reunião:**
- Não exagerar o risco para parecer mais valioso
- Não minimizar achados reais para não assustar o cliente
- Não prometer que "depois de corrigir isso você estará seguro"
- Não criticar a equipe de TI do cliente na presença do cliente

---

### Etapa 11 — Entrega e Acompanhamento

**Objetivo:** formalizar a entrega e criar oportunidade de continuidade.

**Termo de Entrega _(minuta)_:**

```
TERMO DE ENTREGA
Avaliação: [CLIENTE]   Data: [DATA]

Declaro que recebi e estou de acordo com os entregáveis do serviço ASTRO Assessment:
[ ] Relatório executivo
[ ] Relatório técnico
[ ] Reunião de apresentação realizada em [DATA]

Aceite: _______________   Data: _______________
```

**Acompanhamento em 30 dias:**
- Contato por e-mail: "Passaram-se 30 dias desde a entrega. Gostaríamos de saber: algum dos achados foi corrigido? Surgiu alguma dúvida?"
- Não pressionar venda. Coletar feedback genuíno.
- Se cliente corrigiu achados: perguntar se quer revalidação (oportunidade de ASTRO Continuous).
- Se cliente não corrigiu: entender por quê (bloqueio técnico, orçamento, prioridade).

---

## Ferramentas por Etapa

| Etapa | Ferramenta |
|---|---|
| Leads e prospecção | Planilha (Google Sheets ou Excel) |
| Reuniões | Google Meet, Teams ou presencial |
| Notas de reunião | Google Docs ou Notion |
| Propostas e contratos | Google Docs (template) ou Word |
| Assinatura de documentos | DocuSign (gratuito para volume baixo) ou e-mail com PDF assinado manualmente |
| Execução do scanner | Plataforma ASTRO (local) |
| Relatórios | Plataforma ASTRO (PDF) + revisão no Google Docs se necessário |
| Controle de evidências | Planilha ou documento compartilhado internamente |
| E-mail comercial | Google Workspace (R$30/mês por conta) ou Zoho Mail (gratuito) |
| Armazenamento de evidências | Google Drive (criptografado) ou pasta local com acesso restrito |

---

## O que registrar após cada serviço

Após cada entrega, registrar internamente:

1. Horas reais por etapa (para calibrar estimativas futuras)
2. Custo real (infra, tokens, ferramentas)
3. O que o cliente achou mais útil
4. O que o cliente não entendeu ou não valorizou
5. O que foi difícil de executar ou documentar
6. Decisão: o que automatizar, simplificar ou eliminar no próximo serviço

Este registro alimenta o `PRODUCT_EVOLUTION.md`.
