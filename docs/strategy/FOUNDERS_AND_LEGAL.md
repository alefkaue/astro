# ASTRO Cyber — Fundadores e Pendências Jurídicas/Empresariais

Data: 2026-10-18. **Este documento é um checklist de orientação geral. Nenhum item constitui aconselhamento jurídico ou contábil. Contratar advogado e contador antes de formalizar qualquer acordo.**

---

## 1. Constituição da empresa

| Item | Estado | Ação |
|---|---|---|
| Escolha do tipo societário (Ltda, SAS, EIRELI) | Pendente | Avaliar com advogado: Ltda com contrato social é a mais comum para startups BR |
| Participação de cada sócio (% capital) | Pendente | Definir antes de qualquer receita; não presumir igualdade |
| Vesting dos fundadores | Pendente | Recomendar 4 anos, 1 ano cliff; formalizar no contrato ou acordo de sócios |
| Cláusula de saída de fundador | Pendente | O que acontece com as cotas se um fundador sair antes do vesting? |
| Administração e poderes de representação | Pendente | Quem assina contratos? Precisa de dois sócios? |
| Endereço fiscal | Pendente | Coworking ou escritório virtual aceitos pela maioria dos municípios |
| Enquadramento tributário (Simples, Lucro Presumido) | Pendente | Avaliar com contador; Simples Nacional é mais simples para o início |
| Abertura do CNPJ e inscrição municipal | Pendente | CNAE de desenvolvimento de software + CNAE de consultoria de TI |

---

## 2. Propriedade intelectual e código

| Item | Estado | Ação |
|---|---|---|
| Titularidade do código desenvolvido por fundadores | Pendente | Cesão expressa de PI para a empresa no contrato social ou contrato separado |
| Código desenvolvido antes da empresa | Pendente | Licenciar ou transferir para a empresa — não deixar ambíguo |
| Contribuições de código de terceiros (faculdade, TCC) | Pendente | Verificar se há direitos da instituição sobre o trabalho; consultar orientador/advogado |
| Registro de marca "ASTRO" e "ASTRO Cyber" | Pendente | Pesquisar disponibilidade no INPI antes de investir em marca; marcas homônimas existem |
| Licenças das dependências de software | Pendente | Flask (BSD), SQLite (público domínio), fpdf2 (LGPL), groq (MIT), cryptography (Apache-2.0) — verificar compatibilidade ao distribuir |
| Nmap: licença GPLv2 com exceção de uso em varredura | Pendente | Verificar se o uso como subprocesso (não distribuição) exige licenciamento adicional |

---

## 3. Contratos com clientes

| Item | Estado | Ação |
|---|---|---|
| Proposta comercial e escopo de serviço | Pendente | Deve conter: o que é feito, o que não é feito, prazo, entrega, metodologia, limitações |
| Contrato de prestação de serviços | Pendente | Incluir: escopo autorizado por escrito, limitação de responsabilidade, prazo de vigência, sigilo |
| Autorização de escopo técnico (RoE) | Pendente | Documento separado, assinado, com IPs/CIDRs autorizados, janela de tempo, contato de emergência |
| Limitação de responsabilidade | Pendente | Não garantir ausência de vulnerabilidades; não responder por danos derivados de falsos negativos |
| Confidencialidade (NDA) | Pendente | Mútua: nós não revelamos dados do cliente; cliente não revela nossa metodologia |
| SLA e disponibilidade | Pendente | Não fazer SLA de uptime antes de G1-O03 (alertas) e infra de produção estável |
| Termos de cancelamento e offboarding | Pendente | Prazo de aviso, entrega de dados do cliente, exclusão de dados da plataforma |

---

## 4. LGPD e proteção de dados

| Item | Estado | Ação |
|---|---|---|
| Mapeamento de dados pessoais tratados | Pendente | Identificar quais dados coletamos: nome, e-mail, dados de acesso, endereços IP, banners de serviços |
| Base legal para tratamento | Pendente | Execução de contrato e legítimo interesse para dados operacionais |
| Contrato de tratamento de dados (DPA) | Pendente | Necessário se dados pessoais de funcionários do cliente forem tratados |
| Retenção e exclusão de evidências | Pendente | Definir política: quanto tempo guardamos resultados de scan; como excluímos ao encerrar contrato |
| Provedores externos: Groq (IA) | Pendente | Não enviar dados pessoais para o Groq; enviar apenas dados técnicos de vulnerabilidade; revisar termos do provedor |
| Comunicação de incidentes | Pendente | LGPD exige comunicação à ANPD em 72h em casos de vazamento de dados pessoais |
| Encarregado de dados (DPO) | Pendente | Obrigatório; pode ser um dos fundadores |

---

## 5. Divisão de responsabilidades dos fundadores

Proposta de referência (3 fundadores) — ajustar conforme perfis reais.

| Área | Fundador referência | Decisão conjunta obrigatória |
|---|---|---|
| Produto e estratégia de negócio | F1 | Sim para roadmap e precificação |
| Engenharia de segurança (scanner, achados, metodologia) | F2 | Sim para mudanças de metodologia que impactam contratos |
| Plataforma e operações (infra, deploy, dados, suporte) | F3 | Sim para mudanças que afetam disponibilidade e dados de clientes |
| Vendas e relacionamento comercial | Todos | Primeiro piloto exige decisão conjunta |
| Contratações e finanças | Todos | Qualquer despesa acima de valor a definir exige consenso |

**Pontos que exigem acordo explícito antes de operar:**
- Participação societária e vesting de cada fundador
- Dedicação esperada (full-time, part-time, prazo de transição)
- Retirada de pró-labore: quando começa e qual valor
- O que acontece se a empresa precisar de capital externo (diluição)
- Critério de decisão em caso de empate entre sócios

---

## 6. Modelo leve de gestão para equipe fundadora

| Prática | Frequência | Objetivo |
|---|---|---|
| Reunião de alinhamento | Semanal (30–60min) | Prioridades, bloqueadores, decisões pendentes |
| Revisão do backlog | Quinzenal | Verificar se estamos construindo o que os clientes precisam |
| Reunião financeira | Mensal | Receita, custos, projeção de caixa |
| Revisão de segurança e incidentes | Mensal | Revisão de logs, patches, backup, chave de API |
| Documentação de decisões | Por evento | Registrar em `DECISION_LOG.md` toda decisão com impacto significativo |

**O que não fazer:**
- Reuniões sem pauta ou sem decisão
- Backlog sem responsável definido
- Nenhum processo de revisão de segurança até incidente acontecer

---

## 7. Próximos passos imediatos

1. Definir participação societária e vesting (os fundadores entre si, sem o advogado ainda)
2. Contratar advogado para contrato social, cessão de PI e contratos com clientes
3. Contratar contador para escolha do regime tributário e abertura do CNPJ
4. Pesquisar disponibilidade da marca "ASTRO Cyber" no INPI antes de qualquer divulgação pública
5. Redigir modelo de proposta comercial e RoE para o primeiro piloto
6. Definir política de retenção de dados e redigir cláusula de LGPD para o contrato de serviço
