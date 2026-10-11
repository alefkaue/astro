# Experiências por perfil implementadas — 2026-10-11

Pedido: interface mudou pouco; menu deve refletir o funcionamento. Codex implementou uma mudança efetiva de apresentação, consumindo as APIs existentes. Nenhum módulo inexistente foi adicionado ao menu e nenhum dado real foi substituído por demo.

## Entregue

- Gestor/owner: menu Panorama, Relatórios, Avaliações, Autorizações, Organização/equipe e Ajuda. Landing editorial, resultado confirmado destacado com limitação explícita, métricas reais, próximos pontos de atenção derivados dos dados, cobertura e avaliações recentes.
- Viewer: composição executiva de consulta; sem criação/execução ou acesso rápido a autorização no menu. As permissões reais continuam no backend; navegação não concede ou revoga direitos.
- Operador/equipe ASTRO: Centro de operações, Nova avaliação, Execuções, Escopos autorizados, Relatórios técnicos, Configurações e Método. Landing técnico com painel preto, running/falhas/escopos reais, lista operacional, triagem de severidade e cobertura.
- Sidebar redesenhada com identificação da organização, perfil, grupos próprios, ação de execução para operador e indicação de localização. Marca e paleta oficiais preservadas.
- Relatórios: galeria editorial por avaliação concluída, metadados reais e link para visualizar/exportar. Não diz que arquivos foram gerados/assinados nem inventa biblioteca de PDFs.
- Escopos: formulário e autorizações lado a lado em desktop; stack no mobile. Cadastro/autorização preservados.
- Deep links de demo por perfil: /demo?role=owner, /demo?role=operator, /demo?role=viewer. Seleção só na entrada explicitamente sintética; sessão real prevalece em /app.
- Assets de apresentação com versão na URL para evitar cache antigo.

## Contratos e limites

ASTRO_EXPERIENCE é módulo de apresentação puro, separado do roteamento e API. /api/dashboard é fonte das métricas; /api/engagements fornece autorização. Se escopos falharem, painel mostra Indisponível, não zero. Observed_hosts significa hosts com achados, não total de ativos. Distribuição por severidade não significa confirmação. Zero não equivale a segurança comprovada. Dados demo sempre identificados.

Próximos pontos de atenção são regras transparentes sobre contagens registradas (suspeitas, não classificados, avaliações com falha e falta de autorização). Não são uma priorização contextual por ativo e não comprovam correções pendentes. Conteúdo técnico/organização/alvo é escapado; eventos/relatórios continuam autorizados pelo backend existente.

Sem troca de backend, scanner, banco ou permissões. Inventário global/gestão de correções/conectores continuam planejados. Console/detalhe e wizard existentes seguem consumindo APIs reais.

## Validação e colaboração

node --check nos arquivos alterados passou. test_experience.cjs verifica diferenças de navegação e ações por perfil, demo, falha de escopos, elegibilidade de relatório, empty states e escaping de conteúdo hostil. test_workspace_boot.cjs e test_frontend_contracts.cjs passaram. 8 testes Python de dashboard/detalhe passaram; suíte completa prévia tinha 115 testes. Não afirmar nova suite completa sem repetir.

QA visual em navegador real permanece pendente; Edge automático anteriormente falhou e não foi reaberto. CSS foi inspecionado e inclui breakpoints; testes de unidade não comprovam responsividade renderizada. tests/browser_redesign.cjs atualizado, mas não executado nesta etapa.

Claude: revisão independente preparada com CLAUDE_REVIEW_LOCAL.ps1 -Task experience no terminal normal do usuário. Ferramentas somente leitura, saída em CLAUDE_EXPERIENCE_REVIEW_RESULT.json. Nenhuma execução desta tarefa ou contribuição nova Claude é alegada antes de resultado. Codex é dono exclusivo dos arquivos de apresentação até revisão/integração.
