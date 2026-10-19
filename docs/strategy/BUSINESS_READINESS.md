# ASTRO Cyber — Prontidão para o Primeiro Contrato

Data: 2026-10-19. Checklist de condições mínimas antes da primeira venda real.

> Este documento NÃO é conselho jurídico ou contábil. Contratar advogado e contador antes de formalizar qualquer acordo.

---

## 1. Checklist por Área

### Legal e Empresarial

| Condição | Necessidade | Estado |
|---|---|---|
| Participação societária definida entre os 3 fundadores | Obrigatório antes de qualquer receita | Pendente |
| Acordo de vesting documentado (mesmo que informal inicialmente) | Forte recomendação | Pendente |
| CNPJ ativo (Ltda ou SAS) | Necessário para emitir nota fiscal | Pendente |
| Regime tributário definido (Simples Nacional recomendado para início) | Necessário para CNPJ | Pendente |
| Conta bancária PJ | Necessário para receber pagamento | Pendente |
| Contrato padrão de prestação de serviços revisado por advogado | Obrigatório antes do primeiro contrato pago | Pendente |
| RoE template revisado por advogado | Obrigatório antes de qualquer varredura | Pendente |
| NDA mútuo revisado por advogado | Obrigatório | Pendente |
| Cessão de propriedade intelectual do código para a empresa | Necessário para evitar disputa futura | Pendente |
| Pesquisa de marca "ASTRO" e "ASTRO Cyber" no INPI | Necessário antes de divulgação pública | Pendente |
| DPO designado (pode ser um fundador) | Obrigatório pela LGPD | Pendente |
| Política de retenção de dados redigida | Obrigatório antes de tratar dados de clientes | Pendente |

**Mínimo absoluto para o primeiro piloto gratuito:** RoE template + contrato básico revisado por advogado + CNPJ ou acordo claro de quem assina como responsável (PF enquanto o CNPJ não está pronto, mas atentar para implicações fiscais).

**Mínimo para a primeira venda paga:** CNPJ ativo + conta PJ + contrato revisado + nota fiscal.

---

### Técnico

| Condição | Necessidade | Estado |
|---|---|---|
| Gate G0 completo | Obrigatório para qualquer dado real de cliente | Completo |
| Ambiente de produção com waitress (não Flask dev) | Obrigatório | Script pronto — executar |
| Backup automático configurado e testado | Obrigatório antes de dados de cliente | Script pronto — configurar |
| HTTPS em produção | Obrigatório | Config pronta — executar |
| Seed de demo desabilitado em produção (CYMAG_ENV=production) | Obrigatório | Configuração existe |
| SECRET_KEY forte e armazenada fora do repositório | Obrigatório | Documentado em DEPLOY.md |
| Engagement criado para cada cliente antes de qualquer scan | Obrigatório | Funcionalidade pronta |
| Ambiente de demo com VMs vulneráveis para apresentações | Necessário para demo comercial | Pendente |
| Roteiro de demonstração (30min, dados de laboratório) | Necessário antes de abordar clientes | Pendente |

---

### Comercial

| Condição | Necessidade | Estado |
|---|---|---|
| Template de proposta comercial | Obrigatório | Rascunho em MANUAL_OPERATIONS.md |
| Processo de descoberta documentado | Obrigatório | Documentado em MANUAL_OPERATIONS.md |
| Preço definido e validado com os 3 fundadores | Obrigatório | Pendente (hipóteses em BUSINESS_MODEL.md) |
| Planilha de prospecção (lista de leads) | Necessário | Pendente (Codex trabalhando) |
| E-mail profissional no domínio da ASTRO | Necessário antes de abordar clientes formalmente | Pendente |
| Site institucional estático | Necessário para credibilidade | Pendente |
| LinkedIn da empresa | Recomendável | Pendente |
| Capacidade de emitir nota fiscal | Obrigatório para venda paga | Dependente do CNPJ |

---

### Financeiro e Operacional

| Condição | Necessidade | Estado |
|---|---|---|
| Caixa mínimo para cobrir 3 meses sem receita | Forte recomendação | Verificar com fundadores |
| Definição de pró-labore (quando começa, qual valor) | Obrigatório entre sócios | Pendente |
| Processo para reembolso de despesas operacionais | Necessário | Pendente |
| Responsável por finanças definido | Necessário | Pendente |

---

## 2. Cenários de Orçamento

> Todos os valores são estimativas para planejamento. Verificar preços atuais antes de comprometer.

### Cenário 1 — Validação Mínima (primeiras conversas, sem clientes pagantes)

Objetivo: conseguir ter as primeiras reuniões comerciais com credibilidade.

| Item | Custo estimado |
|---|---|
| Domínio .com.br (1 ano) | R$40 |
| E-mail profissional (Zoho Mail, gratuito) | R$0 |
| Site estático (GitHub Pages ou Netlify) | R$0 |
| Templates de proposta e RoE (Google Docs) | R$0 |
| Ambiente de demo (VMs gratuitas em VirtualBox local) | R$0 |
| **Total** | **~R$40** |

Não incluído: taxas de advogado (necessárias antes da primeira venda; adiar para o Cenário 2).

---

### Cenário 2 — Primeiros Serviços (primeiro piloto e primeira venda)

Objetivo: estar pronto para faturar os primeiros R$3.000–R$8.000.

| Item | Custo estimado |
|---|---|
| Domínio .com.br (1 ano) | R$40 |
| E-mail profissional (Google Workspace, 3 contas) | R$270/ano |
| Hospedagem VPS mínima (Hetzner CX11 ou similar) | R$40–R$80/mês |
| Advogado: contrato padrão + RoE + NDA | R$800–R$2.500 (uma vez) |
| Contador: abertura de empresa + orientação regime tributário | R$300–R$800 (uma vez) |
| Registro de marca INPI (pedido inicial) | R$355–R$710 (por classe) |
| Ferramentas de assinatura digital (DocuSign básico) | R$0–R$50/mês |
| **Total estimado (primeiro ano)** | **R$2.500–R$5.000** |

**Obs:** a maior parte do custo é única (advogado, contador, INPI). Custo recorrente mensal é baixo (~R$150–R$200).

---

### Cenário 3 — Lançamento do Produto Comercial (G2/G3)

Objetivo: plataforma com billing real, múltiplos clientes simultâneos, SaaS autogerenciado.

| Item | Custo estimado |
|---|---|
| VPS ou servidor dedicado (mais robusto) | R$200–R$600/mês |
| Backup remoto | R$30–R$80/mês |
| Integração de pagamento (Stripe, Pagar.me) | 2–3% por transação |
| E-mail transacional (Mailgun, SendGrid) | R$0–R$100/mês |
| Monitoramento e alertas | R$0–R$100/mês |
| Suporte jurídico recorrente | R$300–R$800/mês |
| Custo de AEGIS (tokens Groq por cliente) | R$50–R$300/mês |
| **Total mensal estimado** | **R$600–R$2.000/mês** |

**Não ativar o Cenário 3 antes de ter pelo menos 3 clientes pagantes no Cenário 2.**

---

## 3. Separação de Despesas

| Categoria | Item | Obrigatório para |
|---|---|---|
| **Obrigatório imediato** | Domínio | Qualquer divulgação pública |
| **Obrigatório imediato** | E-mail profissional | Abordagem comercial |
| **Obrigatório antes da 1ª venda** | Advogado (contrato, RoE) | Qualquer contrato pago |
| **Obrigatório antes da 1ª venda** | CNPJ + conta PJ | Emissão de NF |
| **Obrigatório antes da 1ª venda** | Contador | Abertura de empresa |
| **Recomendável antes da 1ª venda** | VPS produção | Dados de cliente não ficarem em máquina pessoal |
| **Recomendável antes da 1ª venda** | Registro de marca | Proteção de IP |
| **Adiável** | Assinatura digital (DocuSign pago) | Apenas se volume justificar |
| **Adiável** | Monitoramento | Após 3+ clientes simultâneos |
| **Adiável** | Ferramentas pagas de pentest | Apenas com capacidade e demanda validadas |

---

## 4. Gestão de Incidentes e Limites

### Situações que exigem parada imediata do serviço

- Detecção de comprometimento ativo na infraestrutura do cliente durante o scan
- Achado que sugere atividade criminosa nos sistemas do cliente
- Erro ou anomalia no scanner que pode ter causado impacto no cliente
- Vazamento de dados do cliente (interno ou externo)

**Protocolo mínimo:**
1. Parar a execução imediatamente
2. Notificar o contato de emergência do cliente
3. Documentar o que aconteceu e quando
4. Não especular sobre causa com o cliente antes de investigar internamente
5. Consultar advogado se houver implicação legal

### Serviços que não devemos assumir ainda

- Resposta forense a incidentes ativos (requer metodologia e ferramentas específicas, cadeia de custódia)
- Investigação criminal ou suporte a processos judiciais
- Teste de engenharia social sem protocolo de consentimento e proteção de participantes documentado
- Pentest de aplicação web sem expertise comprovada e seguro de responsabilidade
- SOC 24x7 ou monitoramento contínuo automatizado
- Qualquer serviço com SLA de disponibilidade antes de infraestrutura validada

Se um cliente pedir algo que não conseguimos entregar, dizer isso claramente e, se possível, indicar um parceiro qualificado. Não assumir e subcontratar sem o cliente saber.
