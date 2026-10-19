# ASTRO Cyber — Especificação do Produto

Data: 2026-10-18. Separado em: MVP (pode entregar hoje como serviço assistido) / Pós-piloto / Longo prazo.

---

## 1. Jornada principal (MVP — serviço assistido)

```
1. Equipe ASTRO cria organização do cliente
2. Equipe ASTRO cadastra engagement (escopo acordado por escrito)
3. Admin ASTRO autoriza engagement
4. Operador executa avaliação dentro do escopo
5. Analista revisa achados, classifica (observação/suspeita/confirmado)
6. Visão owner mostra resumo em português com estimativa de prioridade
7. AEGIS gera orientação de correção por achado (fallback offline se sem API)
8. Relatório PDF gerado do backend (não de payload do cliente)
9. Equipe ASTRO entrega relatório e faz reunião com cliente
10. Cliente marca responsável e prazo para cada achado
11. (Pós-piloto) Revalidação: nova avaliação confirma se foi corrigido
```

---

## 2. Funcionalidades do MVP

### F-01: Autenticação e gestão de acesso
| | |
|---|---|
| **Problema** | Acesso não controlado expõe dados de outros clientes |
| **Implementado** | Login, sessões, RBAC 5 papéis, isolamento tenant, CSRF, rate-limit |
| **Pendente MVP** | MFA para admin/operador; recuperação de senha; convite de usuário |
| **Custo técnico** | Médio (MFA); Baixo (email de reset) |
| **Critério de aceite** | Admin não consegue acessar dados de outro tenant; operador sem MFA bloqueado em produção |

### F-02: Engagements (escopo autorizado)
| | |
|---|---|
| **Problema** | Varredura sem autorização documentada é ilegal e gera responsabilidade |
| **Implementado** | Criação, autorização por admin, vinculação ao tenant, validação de alvo |
| **Pendente MVP** | Validade do engagement (data de expiração); prova de controle do alvo |
| **Custo técnico** | Baixo (campo de expiração); Médio (prova de controle) |
| **Critério de aceite** | Scan sem engagement autorizado retorna 403; engagement expirado bloqueia nova avaliação |

### F-03: Scanner TCP defensivo
| | |
|---|---|
| **Problema** | Cliente não sabe o que está exposto |
| **Implementado** | Fallback Go→Nmap→socket; bloqueio redes especiais; limite 64 candidatos |
| **Pendente MVP** | Cobertura estruturada (o que foi testado, erros de coleta, parcial) |
| **Custo técnico** | Médio |
| **Critério de aceite** | Resultado inclui: alvos tentados, alvos testados, erros ocorridos; zero achados não aparece como "sem vulnerabilidades" |

### F-04: Achados e evidências
| | |
|---|---|
| **Problema** | Lista de porta aberta não é evidência; analista precisa saber o que confirmar |
| **Implementado** | Classificação obs/suspeita/confirmado; evidence e banner no banco |
| **Pendente MVP** | AEGIS não pode receber payload livre; deve receber finding_id; IDs estáveis entre avaliações |
| **Custo técnico** | Médio (finding_id estável); Baixo (refactoring AEGIS para finding_id) |
| **Critério de aceite** | Remediação AEGIS recebe finding_id autenticado; sem conteúdo livre do frontend |

### F-05: Visão do gestor (owner)
| | |
|---|---|
| **Problema** | Gestor não entende lista técnica; precisa de prioridade e valor |
| **Implementado** | Resumo por severidade, estimativa financeira com disclaimer, decisão de orçamento |
| **Pendente MVP** | Estimativas financeiras são heurísticas; presenter deve explicar isso ao cliente |
| **Custo técnico** | Baixo (documentar limitação claramente) |
| **Critério de aceite** | Disclaimer "estimativa de ordem de grandeza" visível em todo valor R$; observações mostram "Não estimado" |

### F-06: AEGIS (orientação de correção)
| | |
|---|---|
| **Problema** | Analista precisa de orientação de correção sem precisar pesquisar no Google |
| **Implementado** | Groq API + fallback offline; sanitização anti-injection |
| **Pendente MVP** | Chave IA em texto puro (A11); AEGIS aceita payload livre |
| **Custo técnico** | Médio (secret manager básico com env var cifrada) |
| **Critério de aceite** | Chave não em texto puro em `instance/`; AEGIS usa finding_id, não payload livre |

### F-07: Relatórios PDF
| | |
|---|---|
| **Problema** | Cliente precisa de documento para apresentar internamente |
| **Implementado** | PDF do backend a partir de scan_id; fpdf2; narrativa AEGIS |
| **Pendente MVP** | Seção de metodologia e limitações; revisão humana antes de entrega |
| **Custo técnico** | Baixo |
| **Critério de aceite** | Relatório inclui: metodologia, escopo, limitações, classificação dos achados, data; nenhum achado aparece como "confirmado" sem evidência |

### F-08: Jobs duráveis (bloqueador de confiabilidade)
| | |
|---|---|
| **Problema** | Thread em memória: reinício do servidor perde estado da avaliação em andamento |
| **Implementado** | Thread em memória; polling em memória |
| **Pendente MVP** | Tabela de jobs com lease; worker que recupera após reinício; cancelamento |
| **Custo técnico** | Alto |
| **Critério de aceite** | Avaliação em andamento sobrevive a reinício; cancelamento funciona; status partial/error persiste |

### F-09: Backup e restore
| | |
|---|---|
| **Problema** | Banco SQLite sem backup = dados de cliente perdidos em falha |
| **Implementado** | Ausente |
| **Pendente MVP** | Script de backup do SQLite; teste de restore; rotação |
| **Custo técnico** | Baixo |
| **Critério de aceite** | Backup executado e restore testado com dados reais antes de qualquer piloto |

---

## 3. Pós-piloto (após primeiros clientes validados)

| Funcionalidade | Justificativa |
|---|---|
| Ciclo de correção: responsável, prazo, status | Fechar o loop descoberta→ação→revalidação |
| Revalidação com evidência (antes/depois) | Diferencial principal; exige jobs e IDs estáveis |
| MFA para todos os usuários | Segurança do produto antes de distribuição ampla |
| Convidar usuário por email | Onboarding do cliente sem intervenção ASTRO |
| Histórico comparável entre avaliações | Mostrar evolução, não só snapshot |
| Conector local (rede interna) | Avaliações sem expor backend da ASTRO à LAN do cliente |

---

## 4. Longo prazo (não iniciar sem demanda validada)

| Funcionalidade | Bloqueio / risco |
|---|---|
| Conector por ambiente (Fase S4) | Requer jobs duráveis, enrollment seguro, mTLS |
| SaaS self-service (G3) | Requer billing real, onboarding sem assistência, suporte escalável |
| Integração CVE/CVSS real (NVD/CISA KEV) | Licenciamento de feed; qualidade de matching |
| Agente por endpoint | Outra arquitetura; custos de suporte multiplataforma |
| Monitoramento contínuo | Custos de infra e IA por cliente; necessidade não validada |
| White-label para MSP | Exige maturidade operacional; billing, suporte e marca |

---

## 5. O que não construir agora

- Checkout real com Stripe/PagSeguro — billing é risco de produto, não falta de código
- Dashboard animado com charts complexos — gestor precisa de texto claro, não gráfico bonito
- Integração SIEM/EDR — diferente produto, diferente comprador
- Análise de aplicação web (DAST) — fora do escopo do scanner TCP atual
- Módulo de conformidade LGPD/ISO — diferente produto, exige auditoria humana
