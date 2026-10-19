# ASTRO Cyber — Log de Decisões

Decisões com impacto significativo no produto, arquitetura, segurança ou negócio. Formato: data, decisão, alternativas rejeitadas, justificativa.

---

## 2026-10-10

### D-001 — Iniciar com isolamento multi-tenant antes de qualquer feature nova
**Decisão:** Implementar `account_id` em `engagements` e `scans` e fechar IDOR/BOLA em todas as rotas antes de qualquer trabalho de produto.
**Alternativa rejeitada:** Continuar adicionando features e tratar segurança depois.
**Justificativa:** Um vazamento cross-tenant em ambiente com dados reais de clientes é irreversível em termos de reputação. Custo de corrigir antes é baixo; depois é alto.

---

### D-002 — Não usar ORM (manter SQL direto com SQLite)
**Decisão:** Manter consultas SQL explícitas sem SQLAlchemy ou outro ORM.
**Alternativa rejeitada:** Migrar para SQLAlchemy para facilitar queries e migrations.
**Justificativa:** O código existente funciona; ORM acrescenta abstração sem benefício imediato para uma equipe pequena. Revisitar quando o volume de tabelas/relações justificar.

---

### D-003 — Papel do usuário revalidado no banco a cada request
**Decisão:** `current_user()` sempre lê o papel do banco, não confia apenas na sessão Flask.
**Alternativa rejeitada:** Usar papel da sessão diretamente.
**Justificativa:** Sessão pode estar desatualizada (mudança de papel, desativação de conta). Revalidar no banco é mais seguro; custo de performance desprezível para o volume atual.

---

## 2026-10-11

### D-004 — Lançar como serviço assistido, não SaaS self-service
**Decisão:** Primeira oferta é ASTRO Diagnóstico (avaliação pontual com entrega humana), não portal self-service.
**Alternativa rejeitada:** Lançar diretamente como SaaS com cadastro e billing.
**Justificativa:** Conector, billing real, MFA e jobs duráveis estão pendentes. Serviço assistido permite receita real sem esses requisitos; permite aprender o que o cliente valoriza antes de automatizar.

---

### D-005 — Não renomear identificadores internos CYMAG (rebrand é P2)
**Decisão:** Marca comercial é ASTRO / ASTRO Cyber; nome de código interno permanece `cymag` (módulos, variáveis de ambiente, banco).
**Alternativa rejeitada:** Renomear tudo para ASTRO agora.
**Justificativa:** Rebrand de identificadores internos não entrega valor ao cliente; aumenta risco de regressão. Fazer quando o produto estiver estável.

---

### D-006 — Seed fail-closed em produção (`CYMAG_ENV=production`)
**Decisão:** Em `CYMAG_ENV=production`, o banco não é semeado com dados de demonstração e qualquer usuário demo não é criado.
**Alternativa rejeitada:** Permitir seed em produção com flag separada.
**Justificativa:** Dado de demo em produção é risco de privacidade e confusão de suporte. Fail-closed é o padrão correto.

---

### D-007 — Classificação de achados: observação/suspeita/confirmado (sem "confirmado" automático)
**Decisão:** O scanner nunca marca um achado como "confirmado" automaticamente; exige evidência técnica explícita além de porta aberta.
**Alternativa rejeitada:** Marcar todo achado com porta aberta como "confirmado".
**Justificativa:** Porta aberta não é vulnerabilidade confirmada. Falso positivo vendido como "confirmado" é risco jurídico e de reputação. Honestidade de detecção é diferencial de produto.

---

### D-008 — Codex coordenador do frontend; Claude responsável por segurança e backend
**Decisão:** Divisão de propriedade por área: Claude Code cuida de autenticação, autorização, isolamento e segurança; Codex cuida de UI e motores de detecção.
**Alternativa rejeitada:** Um único agente para tudo.
**Justificativa:** Evita conflitos de edição simultânea; cada agente trabalha em arquivos diferentes.

---

### D-009 — Não usar Redis, Celery ou fila externa para jobs iniciais
**Decisão:** Job queue será tabela SQLite com leases, sem dependência externa.
**Alternativa rejeitada:** Redis + Celery imediatamente.
**Justificativa:** Uma equipe de 3 fundadores sem clientes ainda não precisa de infraestrutura distribuída. Fila em banco é suficiente para os primeiros pilotos; migrar quando o volume exigir.

---

## 2026-10-18

### D-010 — Chave IA cifrada com Fernet + PBKDF2-HMAC-SHA256 (A11)
**Decisão:** `api_key_enc` no `ai_config.json` usa Fernet derivado do `SECRET_KEY` Flask via PBKDF2 (100k iterações, salt fixo por aplicação).
**Alternativa rejeitada:** (a) Manter texto puro; (b) Usar variável de ambiente exclusiva para cifração.
**Justificativa:** Texto puro é risco A11 se o servidor for comprometido. Salt fixo por aplicação (não aleatório por registro) é intencional: permite que uma nova instância com o mesmo SECRET_KEY decifre a chave sem precisar de armazenamento adicional. Compatibilidade com legado (arquivo sem `api_key_enc`) mantida.

---

### D-011 — Rota `/api/remediation` suporta `finding_id` como caminho preferencial (AI-001)
**Decisão:** Cliente pode enviar `finding_id` em vez de `vuln` dict; backend carrega do banco com isolamento de tenant. Caminho legado (`vuln` dict) mantido mas sanitizado.
**Alternativa rejeitada:** Remover caminho legado imediatamente.
**Justificativa:** Quebra compatibilidade com frontend atual sem ganho imediato; sanitização já mitiga o risco. Migrar o frontend para `finding_id` é G0-S13 pendente de conclusão.

---

### D-012 — Não migrar para PostgreSQL agora
**Decisão:** Permanecer em SQLite até volume real de dados ou multi-worker exigir.
**Alternativa rejeitada:** Migrar agora "para estar pronto".
**Justificativa:** Zero clientes, zero dados reais. SQLite é suficiente e reduz complexidade operacional. Migração custosa sem benefício mensurável hoje.
