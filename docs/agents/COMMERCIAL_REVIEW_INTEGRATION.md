# Revisão comercial integrada — 2026-10-11

Claude concluiu a revisão em modo somente leitura (resultado success/completed, sem negativas de permissão). Texto preservado em CLAUDE_COMMERCIAL_REVIEW.md. Codex revisou os trechos de saída executiva, catálogo e relatório e implementou a correção abaixo; os demais achados exigem confirmação e implementação próprias.

## Implementado por Codex

- Saídas executivas offline do AEGIS não inferem perdas, probabilidade, comprometimento ou conformidade a partir do título.
- Observações e severidade informativa não recebem valores financeiros heurísticos no resumo de negócio. Campos numéricos zero significam ausência de estimativa; rótulos por registro explicam isso. As heurísticas antigas para outros achados ainda precisam ser substituídas por contexto de negócio validado.
- PDF remove a coluna de probabilidade e explicita impacto não estimado.
- Catálogo remove a promessa de laudo LGPD/ISO/PCI e reduz promessas não sustentadas de automação e integrações.
- Testes verificam observações, PDF e catálogo. Não houve avaliação visual ou jurídica.

## Prioridade antes de qualquer piloto hospedado

1. Controles de execução: impedir alvos do próprio serviço, metadata, loopback e redes proibidas; verificar autorização, validade, exclusões e tamanho do escopo. Não executar scanners externos nesta etapa.
2. Desabilitar comercialização simulada e funcionalidades sensíveis em produção; consentimento e política para IA externa. Credenciais exigem proteção própria.
3. Autenticação, proteção CSRF, revogação de sessões e limitação de tentativas.
4. Migrações, cobertura registrada, quotas atômicas e tarefas duráveis. Zero registros não equivale a segurança comprovada.
5. Exportação, retenção, exclusão e teste de restauração de backup.
6. QA real: teclado, leitores de tela, temas, zoom, celulares e acessibilidade do relatório exportado.

## Escopo comercial ajustado

Primeiro piloto como serviço de avaliação defensiva assistida com ferramentas internas, escopo documentado, análise humana e reavaliação. Portal do cliente opcional e somente leitura. Instalação por cliente e analista explicitamente membro dessa organização evita criar acesso global improvisado. Não lançar como pentest completo ou promessa de conformidade.

Connector e autosserviço ficam na evolução do SaaS. Trabalhadores duráveis e isolamento continuam necessários para essa evolução; execução síncrona longa não deve virar arquitetura definitiva. Recomendações de Claude para jobs provisórios em memória exigem revisão antes de adoção.

Claude realizou a revisão; não implementou código nesta rodada. A divisão seguinte mantém Codex na experiência e integração, Claude no backend em arquivos exclusivos, começando pelos controles de escopo. A delegação executável depende do terminal local com acesso à API, conforme fluxo já estabelecido.
