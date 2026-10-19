import { createFileRoute } from "@tanstack/react-router";
import { PageHero } from "@/components/site/ui";

export const Route = createFileRoute("/privacidade")({
  head: () => ({
    meta: [
      { title: "Política de Privacidade (LGPD) | ASTRO Cyber" },
      { name: "description", content: "Como a ASTRO Cyber coleta, usa e protege seus dados, conforme a LGPD." },
      { property: "og:title", content: "Política de Privacidade | ASTRO Cyber" },
      { property: "og:description", content: "Dados coletados, uso, retenção e seus direitos pela LGPD." },
    ],
  }),
  component: Privacidade,
});

const sections = [
  { t: "1. Quais dados coletamos", p: ["Pelo formulário de contato: nome, e-mail, empresa, telefone (opcional) e a mensagem enviada.", "Dados de navegação básicos, necessários ao funcionamento do site. Não utilizamos rastreadores de terceiros."] },
  { t: "2. Como usamos", p: ["Usamos seus dados exclusivamente para responder ao seu contato e elaborar propostas.", "Não compartilhamos seus dados com terceiros e não os utilizamos para marketing sem o seu consentimento."] },
  { t: "3. Por quanto tempo", p: ["Os dados do formulário são mantidos por até 2 anos, ou até que você solicite a exclusão — o que ocorrer primeiro."] },
  { t: "4. Seus direitos (LGPD)", p: ["Você pode solicitar a qualquer momento: acesso aos seus dados, correção, exclusão e portabilidade, nos termos da Lei nº 13.709/2018."] },
  { t: "5. Contato", p: ["Para exercer seus direitos ou tirar dúvidas, escreva para privacidade@astrocyber.com.br."] },
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
              {s.p.map((p) => <p key={p} className="mt-3 text-muted-foreground">{p}</p>)}
            </div>
          ))}
          <p className="font-mono text-sm text-muted-foreground">Última atualização: outubro de 2026</p>
        </article>
      </section>
    </>
  );
}
