import { createFileRoute } from "@tanstack/react-router";
import { PageHero } from "@/components/site/ui";
import { CONTACT_EMAIL } from "@/lib/site-config";

export const Route = createFileRoute("/privacidade")({
  head: () => ({
    meta: [
      { title: "Política de Privacidade (LGPD) | ASTRO Cyber" },
      {
        name: "description",
        content: "Como a ASTRO Cyber coleta, usa e protege seus dados, conforme a LGPD.",
      },
      { property: "og:title", content: "Política de Privacidade | ASTRO Cyber" },
      {
        property: "og:description",
        content: "Dados coletados, uso, retenção e seus direitos pela LGPD.",
      },
    ],
  }),
  component: Privacidade,
});

const sections = [
  {
    t: "1. Quais dados coletamos",
    p: [
      "Pelo formulário de contato: nome, e-mail, empresa (opcional), telefone (opcional), serviço de interesse, porte aproximado do ambiente e a mensagem enviada.",
      "Não usamos cookies de rastreamento, pixels de anúncio nem ferramentas de analytics. Sua preferência de tema claro/escuro fica salva apenas no seu navegador.",
    ],
  },
  {
    t: "2. Como usamos",
    p: [
      "Usamos seus dados exclusivamente para responder ao seu contato e, se você pedir, elaborar uma proposta.",
      "Não vendemos seus dados e não os utilizamos para marketing sem o seu consentimento.",
    ],
  },
  {
    t: "3. Serviços de terceiros",
    p: [
      "O envio do formulário é processado pelo Formspree, que recebe a mensagem e a encaminha para a nossa equipe. As fontes do site são carregadas do Google Fonts, que recebe o endereço IP do seu navegador ao carregar a página. A hospedagem do site também registra dados técnicos de acesso (como IP e data), conforme a política do provedor.",
    ],
  },
  {
    t: "4. Por quanto tempo",
    p: [
      "Os dados do formulário são mantidos por até 2 anos, ou até que você solicite a exclusão — o que ocorrer primeiro.",
    ],
  },
  {
    t: "5. Seus direitos (LGPD)",
    p: [
      "Você pode solicitar a qualquer momento: acesso aos seus dados, correção, exclusão e portabilidade, nos termos da Lei nº 13.709/2018.",
    ],
  },
  {
    t: "6. Contato",
    p: [
      CONTACT_EMAIL
        ? `Para exercer seus direitos ou tirar dúvidas, escreva para ${CONTACT_EMAIL}.`
        : "Para exercer seus direitos ou tirar dúvidas, use o formulário da página de contato e indique no assunto “Privacidade”.",
    ],
  },
];

function Privacidade() {
  return (
    <>
      <PageHero label="Legal" title="Política de Privacidade" />
      <section className="bg-surface py-20">
        <article className="mx-auto max-w-[720px] space-y-10 px-5 text-lg leading-relaxed">
          {sections.map((s) => (
            <div key={s.t}>
              <h2 className="text-2xl font-semibold tracking-tight">{s.t}</h2>
              {s.p.map((p) => (
                <p key={p} className="mt-3 text-muted-foreground">
                  {p}
                </p>
              ))}
            </div>
          ))}
          <p className="font-mono text-sm text-muted-foreground">
            Última atualização: outubro de 2026
          </p>
        </article>
      </section>
    </>
  );
}
