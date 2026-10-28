# ASTRO Cyber — Vitrine institucional

**Área do portfólio:** [Desenvolvimento de Software](https://github.com/alefkaue#desenvolvimento-de-software) · **Contexto:** Projeto institucional em desenvolvimento

Site público da ASTRO Cyber: início, serviços, metodologia, sobre, contato e política de privacidade.
É independente da plataforma (branch `app`) — não tem login, checkout nem acesso ao SaaS.

Stack: React 19 + TanStack Start (SSR) + Tailwind 4. Editável também pelo [Lovable](https://lovable.dev/projects/db24e630-582a-4267-90b8-2219d62e3745); commits enviados para a branch conectada voltam para o editor.

## Rodar localmente

```sh
npm install        # ou: bun install
cp .env.example .env
npm run dev        # o terminal mostra o endereço local
```

## Configuração

| Variável | Para que serve | Sem ela |
|---|---|---|
| `VITE_FORMSPREE_ENDPOINT` | Endpoint do formulário de contato (`https://formspree.io/f/<id>`) | A página de contato mostra "formulário indisponível" e desativa o envio |
| `VITE_CONTACT_EMAIL` | E-mail comercial exibido no rodapé, no contato e na privacidade | O e-mail não aparece; a privacidade orienta usar o formulário |

As variáveis `VITE_` são embutidas no build: depois de alterar, gere o build de novo. Nunca coloque o `.env` no Git (já está no `.gitignore`).

## Verificações

```sh
npx tsc --noEmit   # tipos
npm run lint       # estilo (no Windows, rode `npx prettier --write .` se aparecer erro de CRLF)
npm test           # rotas existem, nenhum e-mail/endpoint/prazo inventado no conteúdo, validação da config
npm run build      # gera .output/ (servidor + arquivos públicos)
```

## Publicar com domínio próprio

O build é gerado para **Cloudflare Workers** (padrão do `@lovable.dev/vite-tanstack-config`). O site renderiza no servidor, então não serve como página estática pura no GitHub Pages.

1. **Formulário:** crie uma conta no [Formspree](https://formspree.io), crie um formulário apontando para a caixa de e-mail comercial e copie o endpoint. Envie um teste e confirme o e-mail de ativação que o Formspree manda.
2. **Domínio:** registre o domínio (ex.: no Registro.br para `.com.br`). Adicione o domínio na Cloudflare (plano gratuito) e troque os servidores DNS no Registro.br pelos que a Cloudflare indicar.
3. **E-mail comercial:** crie a caixa no domínio (Google Workspace, Zoho etc.) e configure os registros MX na Cloudflare.
4. **Build com as variáveis reais:** preencha o `.env` com `VITE_FORMSPREE_ENDPOINT` e `VITE_CONTACT_EMAIL` e rode `npm run build`.
5. **Deploy:** `npx wrangler login` e depois `npx nitro deploy --prebuilt` (comando sugerido pelo próprio build; gera um Worker a partir de `.output/`).
6. **Domínio no Worker:** no painel da Cloudflare, em Workers & Pages → o worker → Settings → Domains & Routes → Add → Custom domain, informe o domínio (ex.: `astrocyber.com.br` e `www`).
7. **Validar em produção:** abra todas as páginas no celular e no computador, envie uma mensagem real pelo formulário e confirme que ela chegou na caixa comercial.

Alternativa sem Cloudflare: o botão **Publish** do Lovable, com domínio próprio configurado nas opções do projeto. Nesse caso, cadastre as mesmas variáveis no projeto do Lovable.

## Antes de divulgar o site

- [ ] Formulário enviando de verdade (passo 7 acima)
- [ ] E-mail comercial configurado em `VITE_CONTACT_EMAIL`
- [ ] Perfis reais dos fundadores na página Sobre (hoje são placeholders "Fundador A/B/C")
- [ ] Texto da política de privacidade revisado por advogado
- [ ] Texto sobre situação jurídica (CNPJ) atualizado na página Sobre
