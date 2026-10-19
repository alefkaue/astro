# ASTRO Cyber — Kit de Operação Manual

Ponto de entrada para atender um cliente. Os modelos já existem em [`docs/strategy/MANUAL_OPERATIONS.md`](../strategy/MANUAL_OPERATIONS.md); este arquivo indica onde está cada um e acrescenta só o que faltava.

## 1. Onde está cada material

| Material | Onde | Status |
|---|---|---|
| Resposta ao primeiro contato | MANUAL_OPERATIONS, Etapa 1 | Pronto para uso |
| Questionário de diagnóstico inicial | MANUAL_OPERATIONS, Etapa 2 | Pronto para uso |
| Critérios para **não** avançar | MANUAL_OPERATIONS, Etapa 2 | Pronto para uso |
| Definição de escopo e limites | MANUAL_OPERATIONS, Etapa 3 | Pronto para uso |
| Modelo de proposta comercial | MANUAL_OPERATIONS, Etapa 4 | **Minuta — revisão jurídica** |
| Contrato, NDA e autorização de testes (RoE) | MANUAL_OPERATIONS, Etapa 5 | **Minuta — revisão jurídica** |
| Checklist pré-execução e de execução | MANUAL_OPERATIONS, Etapa 6 | Pronto; depende de validação técnica (§4) |
| Controle de evidências | MANUAL_OPERATIONS, Etapa 7 | Pronto; proteção em §2 deste arquivo |
| Checklist de revisão técnica | MANUAL_OPERATIONS, Etapa 8 | Pronto para uso |
| Relatório executivo e técnico | MANUAL_OPERATIONS, Etapa 9 | Estrutura pronta; validar com execução interna |
| Roteiro da reunião de entrega | MANUAL_OPERATIONS, Etapa 10 | Pronto para uso |
| Termo de entrega | MANUAL_OPERATIONS, Etapa 11 | **Minuta — revisão jurídica** |
| Registro pós-serviço (horas, custo, feedback) | MANUAL_OPERATIONS, final | Pronto para uso |
| Catálogo e limites de cada serviço | [`SERVICE_CATALOG.md`](../strategy/SERVICE_CATALOG.md) | Referência interna |

## 2. Proteção de evidências (procedimento mínimo)

Evidências de avaliação revelam pontos fracos do cliente. Trate como dado confidencial do cliente desde a coleta.

1. **Onde guardar:** uma pasta por avaliação, `ASTRO-AAAA-NNN-<cliente>`, num único local acordado entre os fundadores (ex.: drive corporativo com 2FA obrigatório em todas as contas). Nunca em e-mail, WhatsApp, pendrive pessoal ou repositório Git.
2. **Quem acessa:** só os fundadores alocados na avaliação. Sem links públicos ou "qualquer pessoa com o link".
3. **Cifrar em repouso:** antes de enviar ao armazenamento, compacte a pasta em arquivo cifrado (ex.: 7-Zip AES-256 com senha forte). A senha fica num gerenciador de senhas, nunca no mesmo local do arquivo.
4. **Integridade:** ao fechar a coleta, gere o hash de cada arquivo (`Get-FileHash -Algorithm SHA256` no PowerShell) e registre no Controle de Evidências. Assim dá para provar que o material não foi alterado depois.
5. **O que não coletar:** senhas, dados pessoais de funcionários, conteúdo de arquivos ou bancos do cliente. Se aparecer por acidente, não copie; registre apenas que existe e comunique o cliente.
6. **Envio ao cliente:** relatório em PDF, enviado por link com acesso restrito ao e-mail do responsável indicado no RoE. Senha do arquivo por outro canal.
7. **Retenção:** guardar pelo prazo definido no contrato (sugestão: 90 dias após o termo de entrega) e então excluir as evidências brutas, mantendo só o relatório final. Registrar a data da exclusão.
8. **Incidente:** se houver suspeita de vazamento de evidências, avisar o cliente sem demora e registrar o ocorrido. A obrigação de comunicar e o prazo devem constar do contrato (ver §3).

## 3. O que precisa de revisão jurídica antes do primeiro cliente real

- Proposta comercial, contrato de prestação de serviço, NDA, RoE e termo de entrega (todos marcados como _minuta_).
- Cláusula de limitação de responsabilidade e declaração de que a avaliação não garante ausência de vulnerabilidades.
- Papel da ASTRO na LGPD em cada serviço (operadora dos dados do cliente) e cláusula de tratamento e exclusão de evidências.
- Forma de contratação enquanto não houver CNPJ (pessoa física ou aguardar constituição).
- Para o futuro Fraud & Awareness: termo de consentimento dos participantes de qualquer simulação.

## 4. O que precisa de validação técnica antes do primeiro cliente real

- [ ] Executar uma avaliação completa em laboratório próprio (VMs vulneráveis) usando a plataforma ASTRO, do engagement ao PDF.
- [ ] Conferir se o relatório PDF gerado pela plataforma segue a estrutura da Etapa 9; ajustar manualmente o que faltar.
- [ ] Revisão do relatório de laboratório por um fundador que não executou.
- [ ] Testar a interrupção imediata de uma varredura em andamento (se a plataforma não permitir, definir o procedimento manual de parada).
- [ ] Confirmar que a execução sai de um IP fixo conhecido, informado ao cliente no RoE.
- [ ] Medir horas reais da execução de laboratório para calibrar o preço da proposta.

## 5. ASTRO Exposure — diferenças em relação ao Assessment

Mesmo fluxo, com estas simplificações:

- Etapas 2 a 5 iguais (descoberta, escopo, proposta, contrato e RoE são obrigatórios do mesmo jeito).
- Etapa 9: só o relatório técnico, com as seções 2, 3 (achados com host, porta, serviço, risco de exposição e recomendação de fechamento), 5 e 6. Sem relatório executivo.
- Etapa 10: reunião só se contratada como adicional.

## 6. ASTRO Fraud & Awareness

Não atender clientes ainda. Os pré-requisitos estão em `SERVICE_CATALOG.md`. O site aceita apenas registro de interesse.
