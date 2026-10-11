# Contencao de execucao — 2026-10-11

Claude concluiu a tarefa com resultado success/completed, mas informou bloqueio interno de seguranca na geracao do diff. Nenhum patch foi produzido ou aplicado por Claude. Codex implementou os controles diretamente, considerando suas observacoes. Parecer preservado em CLAUDE_PILOT_SECURITY_REVIEW.md.

## Implementado

- Rejeicao de loopback, link-local (inclusive metadata), multicast, faixa 0/8 e faixa 240/4. IPv6 nao suportado e rejeitado explicitamente.
- CYMAG_SCOPE_DENY: lista de IPs/CIDRs separados por virgulas. Qualquer intersecao bloqueia todo o alvo. Configuracao malformada impede execucao.
- CYMAG_SCOPE_ALLOW: lista da implantacao, obrigatoria fora de development/test/demo. Alvo inteiro deve estar contido em uma entrada. Deny prevalece sobre allow.
- Contagem aritmetica de candidatos, sem expandir redes grandes. /31 conta dois; /32 conta um. Acima de 64 candidatos retorna erro, sem truncamento silencioso. /26 permite 62 candidatos; /24 e recusado.
- max_ips do plano aplicado apos resolucao tenant-scoped do engagement. Comunidade permite apenas um candidato.
- Politica aplicada na descoberta e antes da sondagem individual. Hosts inesperados sao refiltrados, inclusive com escopo vazio no motor legado.
- valid_scope continua validando a sintaxe do contrato: contrato amplo pode existir, mas cada execucao precisa selecionar um alvo menor e permitido. Sem alvo explicito, primeira faixa ampla e rejeitada.

## Validacao

139 testes Python passaram, 17 avisos de depreciacao do FPDF. Testes offline de redes especiais, IPv6, limites, /31-/32, overlap, configuracao invalida, allow/deny, hosts descobertos, plano e chamada direta do scanner. Sem varreduras de rede, sem alteracao do banco real.

## Limites de implantacao

A allowlist operacional nao comprova propriedade ou autorizacao legal. Deve ser configurada exclusivamente pelo operador ASTRO a partir de escopo verificado. Nao liberar redes gerais como 0.0.0.0/0. Adicionar ao deny TODOS os enderecos e redes da propria ASTRO, infraestrutura hospedada, servicos administrativos e terceiros proibidos; ainda nao ha descoberta automatica confiavel desses limites. Controles de rede/egress isolados continuam necessarios.

Redes privadas autorizadas permanecem possiveis no desenvolvimento. Em hospedagem, qualquer execucao exige allowlist: nao equivale a disponibilizar um conector interno. Politicas devem ser definidas antes do boot e processo reiniciado; nao mudar durante execucoes ativas.

Ainda pendentes: validade/exclusoes versionadas do engagement, evidencia de autorizacao, cobertura/erros persistidos, quotas atomicas, durabilidade, cancelamento e CSRF/sessoes. Resultado vazio nao comprova seguranca. Piloto hospedado continua nao liberado.
