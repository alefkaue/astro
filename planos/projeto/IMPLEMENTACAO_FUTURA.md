# Lógica futura — depois da revisão do design

## Ordem de implementação

Começar por núcleo de empresa/acesso, capacidades contratadas e registro durável de execuções. Reutilizar o Flask existente se a inspeção detalhada confirmar o encaixe; não impor troca de framework, ORM ou banco. O servidor estático do protótipo não é o backend futuro.

| Prioridade | Entrega pequena | Critérios de aceite e testes antes de ações reais |
| --- | --- | --- |
| P0.1 | Empresa, membro, perfil e atribuição interna | Autenticar; derivar empresa da sessão e do banco, não do seletor. Testes de listagem, ID estrangeiro, arquivo, exportação e alteração entre duas empresas; leitor não escreve; administrador cliente não acessa área global |
| P0.2 | Serviço e capacidade contratada | Validar serviço/capacidade, vigência e condição em cada endpoint; negar rota direta e executor sem contratação. Preservar consulta conforme contrato; testes independentes para acesso, contrato e configuração |
| P0.3 | Execução e auditoria duráveis | Persistir execução, empresa, versão, estado, eventos, pedido/efeito e chave de idempotência. Testar reinício em cada passo, concorrência do mesmo pedido, timeout e efeito criado antes de falha; no máximo um efeito por chave |
| P0.4 | Escopo/autorização e aprovação de ato exato | Vincular empresa, ambiente, origem, método, prazo e identidade. Aprovação vincula versão, conteúdo e destino. Revalidar no início e antes do efeito. Testar revogação, alteração de configuração, escopo vencido e aprovação de outro tenant |
| P1.1 | Importador de uma origem conhecida | Confirmar formato real, schema versionado e limites. Validar prévia no servidor, origem e arquivos autorizados; tratar duplicados, parsing, conteúdo malicioso e cobertura incompleta. Testar fontes vazias/falhas sem gerar avaliação segura |
| P1.2 | Revisão, ações e relatórios | Persistir confiança, andamento e verificação separadamente. Testar reabertura, revisão inconclusiva, confirmação com prova, acesso do revisor e relatório rastreável com versão/autoria/limites. Não inferir correção por ausência de achado |
| P1.3 | Uma rotina em dois sistemas aprovados | Começar com regras se bastarem. Contas e segredos fora do frontend/logs; permissões mínimas, chamadas limitadas. Testar expiração, rate limit, falha parcial e cancelamento cooperativo sem promessa de rollback externo |
| P1.4 | Consumo e orçamento operacional | Quota/reserva atômica por empresa, custo e volume definidos em contrato. Testar pedidos simultâneos no limite, reserva/reembolso por falha e não cobrança de efeito duplicado. Sem cobrança automática não contratada |
| P1.5 | Operação, dados e suporte | Procedimento de backup e restauração comprovado, retenção/exclusão por classe de documento, acesso por atribuição e substituto do trio. Testar restauração em ambiente limpo e incidentes de conexão durante entrega |
| P2 | Assistente documental ou conector local | Apenas após demanda. Recuperação de fontes isolada por empresa, referências e insuficiência; conector com credencial restrita, revogação, versão e escopo. Testar fuga de dados, texto malicioso e acesso indevido; nunca shell livre para IA |

## Arquitetura proposta sem reescrita

Um monólito modular com núcleo compartilhado e dois módulos de negócio. Adaptadores/executores separados por tipo de risco e credenciais; não exige dezenas de microsserviços.

- **Núcleo:** Empresa, Membro, Perfil/Permissão, Serviço, Capacidade contratada, Aprovação, Evento de auditoria, Arquivo, Consumo e Solicitação de suporte.
- **Segurança:** Ambiente, Autorização, Avaliação, Fonte, Resultado, Ação, Evidência, Verificação e Relatório.
- **IA/Automações:** Conexão, Rotina, Versão da rotina, Pedido/Entrada, Execução, Passo, Efeito e Aprovação do pedido. Fonte documental e resposta entram como extensão.

Cada entidade persistida precisa de vínculo à empresa e referências verificadas. Separar confirmação técnica, estado operacional e efeito externo. APIs não aceitam um objeto de “empresa atual” enviado pelo navegador como autoridade.

Fila e passos persistidos devem permitir retomada após reinício. A chave de idempotência inclui empresa, rotina e identidade estável do pedido; repetir tentativa não gera um novo efeito. Reservar consumo antes de execução e reconciliar após falha. Definir política para trabalhos iniciados quando serviço/autorização/conexão é revogado.

Texto de arquivo, documento ou modelo é conteúdo não confiável, nunca comando automático. Assistente não recebe shell nem acesso ao scanner apenas por compartilhar o portal. Separar credenciais de leitura de pedidos, escrita de tarefa e coleta autorizada.

## Avaliação da base atual antes de conectar

A documentação existente informa Flask/SQLite e execução/eventos em memória. Confirmar código, migrações, transações, concorrência, testes e restauração. Manter SQLite se a carga e o desenho transacional forem adequados; considerar migração somente com requisito concreto, esquema versionado e teste de migração/retorno.

Não copiar o scanner inteiro para dentro do portal. Se houver integração futura, expor um adaptador de inventário com formato, autorização e cobertura definidos. Validar tecnicamente o perfil ativo antes de vender uma coleta; código legado de exploração não amplia a oferta atual.

## Decisões que exigem conversa com o trio/cliente

Público inicial, origem real da fonte, os dois sistemas da primeira rotina, permissões exigidas para cada ato, volume, necessidade de IA, provedor/política de dados, motor/licença, conector e horas de suporte. Registrar decisão e teste correspondente; não transformar hipótese de interface em promessa comercial.

Antes de incorporar n8n, Dify ou qualquer fornecedor, verificar termos e licença comercial. Nenhum desses produtos foi integrado ou teve sua interface copiada nesta etapa.

## Aceite da demonstração versus produção

**Demonstração:** percursos concluíveis, estados compreensíveis, dados fictícios identificados, identidade preservada e layout adaptado a celular. As verificações aqui não provam segurança multi-tenant de produção.

**Produção:** testes reais no servidor e executor, autorização válida, isolamento, efeitos duráveis, limites, backup/restauração, procedimento de revisão humana, contrato e suporte definidos. Nenhuma integração real deve ser liberada só porque o botão funciona no protótipo.
