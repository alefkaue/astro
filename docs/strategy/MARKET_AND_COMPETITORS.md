# ASTRO Cyber — Mercado e Concorrentes

Data: 2026-10-18. Fontes: documentação pública dos produtos, sites oficiais e materiais técnicos linkados em PRODUCT_PLAN.md. Preços de concorrentes sem referência pública são marcados como **[hipótese]**.

---

## 1. Contexto de mercado (sem TAM inventado)

O mercado de segurança para PMEs cresce globalmente porque:
- Ataques a PMEs aumentaram (ransomware como serviço reduziu a barreira de entrada para atacantes)
- Regulamentações (LGPD no BR) criam pressão de conformidade
- PMEs raramente têm equipe dedicada de segurança

**Não temos dados confiáveis de:** TAM Brasil, número de PMEs dispostas a pagar, preço médio aceito, market share de competidores no BR. Não inventar esses números.

---

## 2. Análise de concorrentes

### Horizon3.ai NodeZero
| Aspecto | Detalhe |
|---|---|
| Produto | Plataforma de pentest autônomo baseada em atacante real |
| Público-alvo | Empresas médias e grandes com equipe de segurança interna |
| Proposta de valor | "Atacar como um adversário real, verificar e corrigir" — orientado a ação |
| Funcionalidades efetivas | Exploração autônoma, caminho de ataque, verificação de correção, integração com ferramentas de remediação |
| Distribuição | Runner instalado na rede do cliente; portal web SaaS |
| Preço | **[hipótese]** Alto; voltado para enterprise/mid-market |
| Pontos fortes | Exploração real (não só detecção), cadeia de ataque visual, verificação de correção |
| Limitações | Não é para PME sem equipe técnica; preço elevado |
| O que a ASTRO aprende | Ciclo de verificação de correção é diferencial real; orientação em ação supera lista de CVEs |

### Pentera
| Aspecto | Detalhe |
|---|---|
| Produto | Validação contínua de controles de segurança por simulação de ataque |
| Público-alvo | Empresas com equipe de segurança (SOC/red team interno) |
| Proposta de valor | Validar que os controles existentes realmente funcionam contra ataques reais |
| Funcionalidades efetivas | Simulação de ataques, relatórios de controles falhos, integração SIEM |
| Distribuição | Appliance/VM na rede + portal SaaS |
| Preço | **[hipótese]** Enterprise; não público |
| Pontos fortes | Cobertura ampla de vetores, sem precisar de credenciais |
| Limitações | Não adequado para PME; foco é validar controles existentes, não descobrir exposições |
| O que a ASTRO aprende | Público diferente; não competir diretamente |

### runZero
| Aspecto | Detalhe |
|---|---|
| Produto | Descoberta de ativos de rede (asset inventory) sem credenciais |
| Público-alvo | Equipes de TI e segurança que precisam saber o que existe na rede |
| Proposta de valor | Inventário de ativos preciso, rápido, sem agente, sem credenciais |
| Funcionalidades efetivas | Port scan avançado, fingerprinting de OS/serviços, integração com CMDBs |
| Distribuição | SaaS + explorer instalado na rede |
| Preço | Gratuito até 256 ativos; planos pagos por ativo (dados do site) |
| Pontos fortes | Excelente na descoberta; interface limpa; fácil instalação |
| Limitações | Não classifica vulnerabilidades; sem análise de risco; sem relatório para gestor |
| O que a ASTRO aprende | Descoberta de ativos é onde deve ser simples; ASTRO precisa cobrir o que vem depois |

### Greenbone / OpenVAS
| Aspecto | Detalhe |
|---|---|
| Produto | Scanner de vulnerabilidades open-source com feed NVD/CVE |
| Público-alvo | Organizações que querem controle total e têm capacidade técnica interna |
| Proposta de valor | Cobertura ampla de CVEs, open-source, sem custo de licença |
| Funcionalidades efetivas | Scan de vulnerabilidades com CVE real, plugins, relatórios técnicos |
| Distribuição | On-premises; imagem appliance |
| Preço | Open-source (gratuito); Greenbone Enterprise (pago, **[hipótese]** ~US$15k/ano+) |
| Pontos fortes | Cobertura real de vulnerabilidades; feed NVD/KEV |
| Limitações | Complexo de instalar/operar; sem UX para gestor; sem português; sem ciclo de correção |
| O que a ASTRO aprende | Cobertura real de CVE é necessária para crediblidade técnica; ASTRO deve planejar integração com feeds quando tiver recursos |

### Tenable (Tenable.io / Nessus)
| Aspecto | Detalhe |
|---|---|
| Produto | Plataforma de gerenciamento de vulnerabilidades (VM) líder de mercado |
| Público-alvo | Enterprise e mid-market com equipe de segurança dedicada |
| Proposta de valor | Cobertura mais ampla de vulnerabilidades do mercado, priorização por risco |
| Funcionalidades efetivas | Scan autenticado e não-autenticado, CVSS+VPR, integração com patch management, cloud |
| Distribuição | SaaS (Tenable.io) + agente por endpoint + scanner de rede |
| Preço | **[hipótese]** A partir de ~US$2.275/ano para Nessus Pro; Tenable.io bem mais caro |
| Pontos fortes | Cobertura incomparável, VPR (Vulnerability Priority Rating) próprio, documentação |
| Limitações | Complexo para PME; caro; sem foco em português BR; sem UX para dono de negócio |
| O que a ASTRO aprende | Priorização por risco real (não só CVSS) é diferencial reconhecido; VPR considera ameaça ativa |

### Intruder.io
| Aspecto | Detalhe |
|---|---|
| Produto | SaaS de escaneamento contínuo de vulnerabilidades para PME |
| Público-alvo | PMEs e scale-ups sem equipe de segurança dedicada |
| Proposta de valor | Varredura contínua com alertas priorizados; simples de usar |
| Funcionalidades efetivas | Port scan, detecção de vulnerabilidades web e rede, alertas por e-mail, relatórios simples |
| Distribuição | SaaS puro; conector para rede interna |
| Preço | A partir de ~US$101/mês (site público, pode variar) |
| Pontos fortes | Interface simples; adequado para PME; inglês/europeu fácil de adotar |
| Limitações | EN/EU; sem relatório para gestor brasileiro; sem ciclo de correção assistida |
| O que a ASTRO aprende | Modelo de preço mensal acessível é validado para PME; simplicidade é diferencial |

---

## 3. Matriz comparativa

| Dimensão | ASTRO (atual) | NodeZero | runZero | Intruder | Greenbone | Tenable |
|---|---|---|---|---|---|---|
| Scanner TCP/porta | ✅ | ✅ | ✅✅ | ✅ | ✅ | ✅✅ |
| Vulnerabilidades CVE reais | ❌ | ✅ | ❌ | ✅ | ✅✅ | ✅✅ |
| Exploração autônoma | ❌¹ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Relatório para gestor não-técnico | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Ciclo correção/revalidação | ❌ | ✅ | ❌ | ❌ | ❌ | 🔶 |
| Interface em português BR | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Preço acessível para PME BR | 🔶² | ❌ | 🔶 | 🔶 | ✅ (gratuito) | ❌ |
| Conector para rede interna | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SaaS autogerenciado PME | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |

¹ Checks de exploração desativados no perfil defensivo atual (D-007)
² Preços no código são simulação; não validados com clientes

**Legenda:** ✅ = implementado, ✅✅ = destaque, 🔶 = parcial, ❌ = ausente/não aplicável

---

## 4. O que diferencia a ASTRO (hipóteses a validar)

1. **Relatório para gestor em português** — nenhum concorrente identificado faz isso para PME brasileira
2. **Ciclo de correção assistida** — NodeZero faz mas para enterprise; nenhum faz no BR para PME
3. **Serviço assistido como produto** — permite qualidade antes de automação
4. **Preço em real sem necessidade de cartão internacional** — reduz fricção para PME BR

---

## 5. O que NÃO é diferencial exclusivo

- Ter IA no produto (todos têm)
- Scanner de portas (commodity)
- Relatório PDF (todos têm)
- RBAC com múltiplos papéis (todos têm)

---

## 6. Concorrentes brasileiros (lacuna de pesquisa)

Não identificamos concorrentes diretos no Brasil com produto equivalente. Empresas de MSSP/SI brasileiras (Tempest, Redbelt, ISH, Cipher) oferecem serviços gerenciados de segurança mas não têm produto SaaS similar acessível para PME. **Esta é uma hipótese — pesquisa adicional necessária antes de usar como argumento de venda.**
