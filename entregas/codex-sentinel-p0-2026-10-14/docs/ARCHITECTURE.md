# Arquitetura observada após incremento P0

Monólito Flask e frontend JS existentes preservados. `app/security.py` concentra controles de requisição e bloqueio da execução legada. `app/auth/decorators.py` consulta identidade/membership/papéis atuais; `app/db.py` persiste recursos com tenant e migra SQLite. `core/redaction.py` remove padrões conhecidos de segredos em evidências novas.

PDF existente reutilizado com seleção de dados no servidor. AEGIS oferece sugestão determinística rastreada ao finding, sem uso de provedor externo neste estágio. Suporte legado não tem bypass para conteúdos de clientes. Produção e staging falham ao iniciar porque o adaptador PostgreSQL e o restante P0 não estão prontos.

Worker persistente, Redis/RQ, agente Go, CLI segura e API v1 permanecem futuros, na ordem da especificação. Não existem novos serviços, framework frontend ou deploy nesta entrega.
