# ASTRO Cyber — Estratégia de Vitrine Comercial

Data: 2026-10-19. Decisão sobre como apresentar a ASTRO publicamente sem expor a aplicação interna.

---

## 1. O Problema

O app atual é uma ferramenta técnica de segurança com:
- Rotas de admin, scan, engagements, findings, AEGIS
- Credenciais de demo (`dono@pme.com`, `admin@cymag.com`, `ti@pme.com`)
- Modo demo client-side que simula dados
- Checkout simulado de planos

Nada disso deve ser exposto a visitantes de um site comercial. Um prospect não precisa e não deveria ver um painel de pentest para decidir contratar um serviço.

---

## 2. Comparação: Alternativa A vs. Alternativa B

| Critério | A — Reorganizar frontend existente | B — Site estático independente |
|---|---|---|
| **Custo** | Baixo (nenhum novo servidor) | Baixo (hospedagem estática gratuita: Vercel, Netlify, GitHub Pages) |
| **Esforço inicial** | Alto — requer modificar o app Flask, separar rotas públicas de privadas, garantir que nada interno vaze | Baixo — criar HTML/CSS/JS separado; app continua intacto |
| **Risco de segurança** | Alto — qualquer erro de rota expõe o app interno; credenciais de demo, rotas de admin, checkout falso ficam no mesmo processo | Nenhum — o site não tem backend; não há nada para vazar |
| **Manutenção** | Alta — cada mudança no app pode afetar o site; acoplamento permanente | Baixa — site muda de forma independente; app muda de forma independente |
| **Escalabilidade** | Limitada — o app Flask precisa rodar para o site funcionar | Total — CDN global sem custo; o app roda separado |
| **Velocidade de lançamento** | Lenta — requer refatoração do app antes de publicar | Rápida — site pronto em 1–2 semanas sem tocar no app |
| **Reversibilidade** | Difícil — mudanças no app para separar as experiências são difíceis de desfazer | Total — o app não foi tocado |
| **Identidade do produto** | Confusa — o site e o app teriam o mesmo domínio, tornando difícil separar a vitrine da ferramenta | Clara — domínio principal é a vitrine; app fica em subdomínio ou URL separada |

**Veredicto: Alternativa B — site estático independente.**

---

## 3. Arquitetura Recomendada

```
astrocyber.com.br (ou similar)
├── / (site institucional estático)
│   ├── index.html          — página inicial
│   ├── servicos.html       — catálogo de serviços
│   ├── como-funciona.html  — metodologia
│   ├── sobre.html          — equipe
│   ├── contato.html        — formulário de contato / orçamento
│   └── privacidade.html    — política de privacidade e LGPD
│
app.astrocyber.com.br (subdomínio separado, acesso restrito)
└── /                       — plataforma ASTRO (app Flask atual, intacto)
```

O site institucional nunca chama a API do app. O app nunca é exposto no domínio principal.

---

## 4. O que o Site Institucional Deve Ter

### Página inicial

- Quem somos e o que fazemos (1–2 frases diretas)
- Problema que resolvemos (linguagem do cliente, não jargão técnico)
- Serviços disponíveis (links para a página de serviços)
- Call to action principal: "Solicitar orçamento" → formulário de contato
- **Não:** depoimentos falsos, logos de clientes inexistentes, certificações que não temos, anos de experiência inventados

### Serviços

Para cada serviço ativo (Assessment, Exposure):
- O que é (2–3 frases)
- Para quem é (perfil do cliente)
- O que entregamos (lista de entregáveis)
- O que **não** fazemos (honestidade sobre limitações)
- Como solicitar

**Não incluir** serviços que não estão prontos (Pentest, Continuous, Fraud) como se estivessem disponíveis.

### Como Funciona

Explicar o processo em linguagem acessível:
1. Você nos conta sobre sua infraestrutura
2. Definimos escopo e assinamos a autorização
3. Executamos a avaliação
4. Entregamos relatório e fazemos reunião de resultados

Opcional: incluir pergunta "Por que isso é importante?" com linguagem de negócio.

### Sobre

- Quem são os fundadores (nome, área de atuação)
- Por que criamos a ASTRO
- O que nos diferencia (ferramenta própria, entrega presencial, linguagem acessível)
- **Não:** cargos inflados, experiências inventadas, fotos de stock como se fossem a equipe

### Contato / Orçamento

Formulário simples:
- Nome
- Empresa
- E-mail
- Telefone (opcional)
- "O que você precisa?" (texto livre)
- Envio por e-mail (Formspree, Netlify Forms, ou similar — gratuito)

### Política de Privacidade

Texto adequado à LGPD para o site (o que coletamos: nome, e-mail pelo formulário; como usamos; como excluir). Redigir com advogado ou usar gerador confiável e revisar.

---

## 5. O que NÃO colocar no site

- Rotas do app (login, /api, /admin, /engagements)
- Credenciais de demo
- Checkout ou planos de assinatura (não temos pagamento real)
- Logos de clientes (não temos clientes)
- Depoimentos (não temos)
- Certificações (não temos — nem citar "equipe certificada" sem especificar)
- Estatísticas inventadas ("X clientes atendidos", "Y vulnerabilidades encontradas")
- CNPJ antes de ter um
- Garantias de resultado

---

## 6. O que Fazer com o App Atual

**Nada.** O app continua rodando intacto. Nenhuma mudança de arquitetura necessária.

Ajustes pontuais recomendados (não bloqueadores do site):
- Garantir que `CYMAG_ENV=production` desabilita o seed de demo
- Remover ou ocultar o modo demo client-side do ambiente de produção (`cymag-demo.js`)
- Verificar que nenhuma rota do app retorna dados de outro tenant se acessada sem autenticação

---

## 7. Stack do Site Institucional

**Opção recomendada para lançamento rápido:** HTML + CSS + JavaScript vanilla.

- Zero dependências
- Qualquer fundador consegue editar
- Hospedagem gratuita em Vercel, Netlify ou GitHub Pages
- Sem build step, sem framework

**Design:**
- Usar identidade visual já existente: logos em `static/brand/`, paleta de cores do `astro.css`
- Exportar as SVGs e o sistema de cores para o site estático (sem copiar o app inteiro)
- Não usar Bootstrap, Tailwind ou qualquer framework CSS antes de justificar a necessidade

---

## 8. Domínio e Hospedagem

| Item | Opção | Custo |
|---|---|---|
| Domínio .com.br | Registro.br | R$40/ano |
| Domínio .com | Namecheap, Cloudflare | ~US$10/ano |
| Hospedagem site estático | GitHub Pages, Vercel, Netlify | Gratuito |
| Hospedagem app (produção) | VPS básico (Hetzner, Contabo) | R$30–R$80/mês |
| E-mail profissional | Zoho Mail (gratuito até 5 contas) ou Google Workspace (R$30/mês) | R$0–R$90/mês |

**Decisão mínima para o site:** domínio + GitHub Pages = ~R$40/ano.

---

## 9. Sequência de Execução

1. Comprar domínio (`astrocyber.com.br` ou equivalente disponível)
2. Criar repositório separado para o site institucional
3. Desenvolver as 5–6 páginas estáticas (1–2 semanas)
4. Configurar formulário de contato (Formspree gratuito)
5. Publicar no GitHub Pages / Netlify
6. Configurar e-mail profissional no domínio
7. Revisar com os 3 fundadores antes de divulgar
8. Só após: divulgar em LinkedIn, grupos de TI, rede pessoal

---

## 10. O que Não Fazer

- Não usar o app como site institucional (expõe o painel interno)
- Não colocar link público para o app antes de ter controle de acesso robusto
- Não lançar o site sem política de privacidade (LGPD)
- Não lançar com serviços que não estão prontos para entrega
- Não contratar designer antes de validar o texto com 3–5 pessoas do público-alvo
