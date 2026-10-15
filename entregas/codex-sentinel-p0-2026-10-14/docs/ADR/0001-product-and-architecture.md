# ADR 0001 — Produto e arquitetura

Status: aceito conforme especificação definitiva, 14/10/2026.

Evoluir incrementalmente o monólito Flask e o frontend JS existentes. ASTRO Sentinel é o nome de produto; nomes internos cymag são preservados por compatibilidade. accounts será a origem comprovável das organizações legadas; órfãos não recebem tenant arbitrário.

PostgreSQL como alvo de produção, SQLite local/transição. Worker isolado com fila durável Redis/RQ; agente outbound Windows/Linux e CLI na fase 3. Nenhuma reescrita em framework novo, divisão em microsserviços, deploy ou scan externo nesta entrega.

Prioridade: P0 antes de contratos, motor/agente, UX, inteligência e release. Demo explícita e isolada. AEGIS somente leitura/sugestão, sem exploração autônoma, preços e perdas financeiras inventados. Até existir execução segura, rotas reais de execução devem falhar de forma explícita.
