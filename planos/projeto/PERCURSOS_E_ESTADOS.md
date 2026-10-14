# Mapa de páginas e estados

## Páginas

| Área | Rota | Tarefa principal |
| --- | --- | --- |
| Site | `#/` | Entender as duas linhas e os limites da demonstração |
| Site | `#/servicos` | Conhecer Segurança e IA/Automações |
| Site | `#/seguranca`, `#/ia` | Entender entrada, revisão e resultado |
| Site | `#/como-funciona` | Entender escopo → preparo → acompanhamento |
| Site | `#/plataforma`, `#/sobre` | Conhecer portal e trio sem prova social inventada |
| Contato | `#/contato` | Preparar/baixar mensagem; sem envio |
| Entrada | `#/acesso` | Escolher empresa fictícia; sem login real |
| Núcleo | `#/portal/inicio`, `#/portal/servicos` | Próximo passo, serviços e solicitação simulada |
| Segurança | `#/portal/seguranca/ambientes` | Fonte, escopo, autorização e cobertura |
| Segurança | `#/portal/seguranca/importar` | Arquivo/JSON, erros, prévia e confirmação |
| Segurança | `#/portal/seguranca/avaliacoes` | Revisar origem e avaliação importada |
| Segurança | `#/portal/seguranca/achados[/<id>]` | Rever confiança e evidência, criar ação |
| Segurança | `#/portal/seguranca/acoes` | Responsável, prazo, comentário, evidência e revalidação |
| IA | `#/portal/rotinas` | Configurar, testar cinco pedidos, revisar, ativar/pausar |
| IA | `#/portal/execucoes` | Fila, revisão, efeito registrado e recuperação |
| Extensão | `#/portal/assistente`, `#/portal/fontes` | Exemplo de resposta com referência/insuficiência |
| Núcleo | `#/portal/aprovacoes`, `#/portal/relatorios` | Aprovar ato exato; ler resumo/baixar/imprimir |
| Núcleo | `#/portal/atividade`, `#/portal/suporte` | Histórico contextual e solicitação fictícia |
| Configuração | `#/portal/configuracoes/equipe` | Entender perfis, sem convidar usuários reais |
| Configuração | `#/portal/configuracoes/conexoes` | Conexão fictícia, renovação/revogação |
| Configuração | `#/portal/configuracoes/consumo` | Contrato, volume e bloqueio sem cobrança |
| Configuração | `#/portal/configuracoes/conector` | Encaixe opcional, sem instalador |
| Interna | `#/portal/interno` | Empresa atribuída Aurora; administração do cliente não entra |

## Percurso completo de Segurança

1. Conferir empresa, ambiente, origem e autorização de exemplo. Se faltar autorização, a UI indica o que falta.
2. Colar JSON fictício ou ler arquivo local de até 100 KB. Gerar prévia; validar versão, empresa, ambiente, fonte, data, IDs, campos, confiança e ativos `*.empresa.example`.
3. Se houver erro, preservar avaliações anteriores e mostrar a causa. Fonte vazia nunca produz selo de segurança.
4. Confirmar prévia válida. A fonte entra “Em revisão”; os resultados mantêm a confiança original. Modificar o texto invalida a prévia.
5. A revisão humana confere cobertura e interpretação; avaliação pode então ser concluída. Salvar confiança exige justificativa ao escolher “Confirmado”.
6. Criar ação com responsável, prazo e comentário. Avançar para execução, anexar evidência e solicitar revalidação pelo método comparável indicado.
7. Registrar verificação simulada: inconclusiva permanece pendente; problema persiste reabre; correção verificada encerra a ação. A confiança do achado não muda por isso.
8. Consultar relatório com fonte, revisão, IDs e cobertura. Imprimir resumo A4; TXT inclui todas as avaliações, achados e ações. Resultados extras não são descartados para cumprir cinco prioridades.

### Estados de Segurança

| Conceito | Estados da especificação | O que o protótipo demonstra |
| --- | --- | --- |
| Avaliação | Rascunho → autorizada → na fila → em andamento → em revisão → concluída; falha/cancelamento | Preparo e autorização na tela; importação local leva diretamente a “Em revisão”; revisão humana conclui. Fila/coleta/falha/cancelamento de uma avaliação executada ficam para lógica futura |
| Confiança | Observação, suspeita, confirmado, não verificado | Campo independente com origem/evidência; confirmação exige justificativa fictícia |
| Ação | Aberta → em execução → aguardando verificação → encerrada; reabertura | Percurso completo com evidência, responsável e prazo |
| Verificação | Não realizada, inconclusiva, problema persiste, correção verificada | Resultado separado; problema persiste reabre; inconclusiva não certifica correção |
| Importação | Sem prévia, prévia válida, erro, importada | Validada localmente sem API; edição invalida a prévia |

## Percurso completo de IA/Automações

1. Configurar os dois sistemas genéricos e fictícios em Conexões; nenhum segredo solicitado.
2. Salvar campo de entrada e sistemas. Escolher sugestão de IA simulada ou regra simples sem IA.
3. Testar cinco pedidos. A tela mostra classificação e insuficiência; nenhuma tarefa é criada no teste.
4. Aprovador confere empresa, versão, campos, origem/destino, uso da IA e validade da aprovação. Configuração ou conexão alterada invalida o teste e a aprovação.
5. Ativar somente a versão aprovada. Colocar um dos cinco pedidos na fila.
6. Avançar a leitura e a preparação do resultado simulado. Ainda não há efeito no quadro. Aprovar/editar a classificação do pedido é um ato separado da aprovação do teste.
7. Criar a tarefa fictícia e mostrar ID do efeito, pedido, empresa, versão e aprovador. Repetir pedido concluído reutiliza o efeito e não aumenta consumo.
8. Recuperação: execução pendente não pode ser duplicada; falha antes do efeito volta à fila; parcial com efeito existente recupera a tarefa original. Cancelamento solicitado requer confirmação e não desfaz efeito anterior.

### Estados de IA

| Conceito | Estados | Comportamento |
| --- | --- | --- |
| Rotina | Rascunho, em teste, pronta para revisão, ativa, pausada, arquivada | Protótipo demonstra até pausa/reativação. Arquivamento e retenção serão implementados depois |
| Execução | Na fila, em andamento, aguardando aprovação, concluída, falhou, parcialmente concluída, cancelamento solicitado, cancelada | Todos demonstráveis em percursos/cenários; avanço manual explícito |
| Conexão | Não configurada, conectada, expirada, revogada, com erro | Cenário expirada e atos conectar/revogar; estado com erro previsto no modelo |
| Aprovação | Pendente, aprovada, rejeitada, invalidada por alteração | Teste vinculado à versão e escopo; pedido vinculado ao conteúdo/destino da execução |
| Efeito | Não registrado, tarefa registrada, efeito anterior recuperado | ID separado do estado da execução; parcial não é sucesso completo |

## Cenários obrigatórios

| Cenário | Como abrir | Resultado esperado |
| --- | --- | --- |
| Aurora | Empresa atual = Aurora | Somente Segurança; rota direta de IA mostra não contratado |
| Horizonte | Empresa atual = Horizonte | Somente IA; Segurança não contratado |
| Ponte | Empresa atual = Ponte | As duas linhas com registros próprios |
| Empresa nova | Empresa atual = Empresa nova | Catálogo e onboarding; nenhum resultado inventado |
| Leitor | Demonstração → Perfil = Leitor | Consulta permitida; alterações e execução bloqueadas |
| Operador interno | Demonstração → Perfil = Operador interno ASTRO | Área separada e seletor restrito a Aurora |
| Falha de importação | Demonstração → Falha de importação → Gerar prévia | Erro JSON, sem substituir resultados nem declarar segurança |
| Conexão expirada | Demonstração → Conexão expirada | Pendência de conexão, sem tarefa registrada |
| Ação sem permissão | Perfil operador da empresa ou leitor | Operador prepara, aprovador decide; leitor apenas consulta |
| Limite atingido | Demonstração → Limite atingido | Novos testes/pedidos bloqueados, sem cobrança |
| Terceiro serviço | Meus serviços | Software sob medida “Em planejamento”, sem ação de compra/execução |
| Parcial / falha técnica | Demonstração → respectivos cenários | Histórico, passo com efeito e recuperação explícita |

Trocar perfil conserva os dados da empresa na aba para demonstrar divisão de papéis. Isso não é RBAC real. Aplicar cenário reinicia a empresa atual. Recarregar a página reinicia todos os exemplos.

## Encaixe modular

O catálogo usa manifesto em `model.js`: identificador, nome, versão, descrição, ícone, rota, capacidades, permissões, limites e marcador `planned`. Adicionar módulo planejado não exige reconstruir a página. Serviço futuro também precisa definir proprietário, dados, suporte, escopo comercial e tipos de execução/resultados antes de ser ativo.

O protótipo não carrega plugins executáveis ou marketplace. Os dados de um serviço contratado continuam acessíveis sem obrigar a contratar outro. O backend futuro usará o manifesto como contrato organizacional, não como prova suficiente de autorização.
