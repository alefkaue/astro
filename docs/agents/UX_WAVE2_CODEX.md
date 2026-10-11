# UX Onda 2 — tarefa para Codex (após Onda 1 revisada)

Mesmas regras da Onda 1 (`UX_WAVE1_CODEX.md`): só frontend, identidade preservada, sem funcionalidades fingidas, testes ao final, sem commit/push, registrar em CHANGELOG_AGENTS.md.
Itens de origem: UX-01, 02, 03, 07, 08, 09, 10, 11, 17, 18 (ver `ANALISE_VISUAL_E_UX.md`).

**Correção da Onda 1:** você criou `CHANGELOG_AGENTS.md` na raiz do projeto por engano. O oficial é `docs/agents/CHANGELOG_AGENTS.md`: mova o conteúdo da Onda 1 para lá (acrescentando, sem apagar o histórico existente) e remova o arquivo da raiz. Registre a Onda 2 no oficial.
Também: valide visualmente se possível (ex.: servir o app e checar largura 390px) ou diga explicitamente que não foi possível.

## Evidência de pesquisa que fundamenta as decisões
- Painel responde UMA pergunta principal de relance; a métrica mais importante é o maior elemento, topo-esquerda; usuário não técnico → layout mais simples, técnico → mais denso (TechTarget; Au Fait UX; DEV/DesignMonks).
- Divulgação progressiva em 3 níveis: sempre visível (manchete) → sob demanda → detalhe oculto (Au Fait UX).
- Rótulos em linguagem simples; métricas relacionadas agrupadas (MetricsWatch).
- Painel executivo: toda métrica deve provocar discussão/decisão/ação, senão sai; tendência > retrato isolado, MAS só com dados comparáveis (IANS, Bugcrowd) → no ASTRO mostrar tendência apenas quando houver ≥2 avaliações comparáveis; caso contrário dizer "sem dados suficientes".
- Tabelas: filtros fora da tabela, múltiplos, ativos como chips removíveis; ordenação por coluna no cabeçalho; cabeçalho sticky; alternância de densidade (compacto/confortável) persistida (SAP design system, setproduct, shadcn density).
- Contraste WCAG AA: texto normal ≥4.5:1, grande ≥3:1; cinza-sobre-preto é falha comum; não inverter tema sem revalidar; evitar branco puro sobre preto (halação) — usar off-white sobre cinza muito escuro; #767676 em branco = 4,48:1 (reprova), usar ≤#757575.

## Itens
1. **UX-01** Panorama Dono/Diretoria: o número-herói passa a ser a situação ("17 achados aguardando revisão técnica"), com "0 confirmados" ao lado em hierarquia secundária e uma frase: "Zero confirmados não significa ausência de risco". Próximo passo explícito logo abaixo.
2. **UX-02** Resumo da avaliação: mostrar a decomposição registrados = confirmados + suspeitas + não classificados (nunca contadores que pareçam se contradizer).
3. **UX-07** Reduzir banner institucional nos panoramas; fila "Próximo trabalho"/revisão pendente acima da dobra para Analista.
4. **UX-08** Diretoria: síntese executiva própria (situação conhecida, pendências, limites da conclusão, data humanizada) usando só dados reais da API; tendência só com ≥2 avaliações comparáveis, senão "sem dados suficientes para comparar". Sem prejuízo financeiro inventado: "ainda não há dados suficientes para estimar impacto".
5. **UX-09/10/11** Achados: busca + filtros (severidade, ativo, validação) como chips removíveis acima da tabela; ordenação por coluna; cabeçalho sticky; painel de metadados recolhível; descrição completa só no detalhe; sem truncamento abrupto; toggle de densidade (compacto/confortável) em localStorage; voltar da análise preserva posição.
6. **UX-03** Modal "Analisar": selo visível "Dado sintético"/"Sem classificação" quando aplicável, origem da orientação, separação evidência × resultado × sugestão; botão copiar; botão renomeado "Ver orientação de análise".
7. **UX-17** Contraste: auditar tokens de texto secundário nos dois temas; ajustar para ≥4.5:1 (script de verificação simples em `tests/` ou doc com razões medidas); aumentar tamanho mínimo de rótulos pequenos (≥12px, preferir 13px).
8. **UX-18** Console sem histórico: estado "histórico indisponível" destacado, controles desabilitados visualmente + link para resultados.

Entregar: arquivos tocados, razões de contraste antes/depois, testes.
