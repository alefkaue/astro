import { createFileRoute } from "@tanstack/react-router";
import { FinalCTA, PageHero, Reveal, SectionHead } from "@/components/site/ui";
import { BanIcon, ChatIcon, ClockIcon, EyeIcon, LockIcon, SirenIcon, TargetIcon, UsersIcon } from "@/components/site/icons";

export const Route = createFileRoute("/como-funciona")({
  head: () => ({
    meta: [
      { title: "Como funciona — Metodologia em 9 etapas | ASTRO Cyber" },
      { name: "description", content: "Escopo definido, autorização formal, revisão manual e reunião de entrega. Veja as 9 etapas da nossa metodologia." },
      { property: "og:title", content: "Como trabalhamos | ASTRO Cyber" },
      { property: "og:description", content: "Metodologia estruturada em 9 etapas, do primeiro contato ao acompanhamento." },
    ],
  }),
  component: ComoFunciona,
});

const steps: [string, string][] = [
  ["Primeiro contato", "Você nos conta o contexto da empresa e o que preocupa."],
  ["Reunião de descoberta", "Entendemos a infraestrutura, objetivos e restrições."],
  ["Proposta e escopo", "Definimos por escrito o que será avaliado — e o que não será."],
  ["Contrato e autorização", "Assinatura do contrato e das Rules of Engagement."],
  ["Execução dentro do escopo", "Testes apenas nos ativos e janelas autorizados."],
  ["Revisão dos achados", "Cada resultado é revisado manualmente para eliminar falsos positivos."],
  ["Relatório", "Relatório executivo e técnico, com severidade e prioridades."],
  ["Reunião de entrega", "Apresentamos os resultados e tiramos dúvidas pessoalmente."],
  ["Acompanhamento (opcional)", "Apoio na interpretação durante a correção pela sua equipe."],
];

function ComoFunciona() {
  return (
    <>
      <PageHero label="Metodologia" title="Como trabalhamos">
        Um processo previsível, documentado e autorizado do início ao fim.
      </PageHero>

      <section className="bg-raised py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Princípios" title="O que guia cada avaliação" />
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { i: TargetIcon, t: "Escopo definido primeiro", d: "Nada começa sem saber exatamente o que entra e o que fica de fora." },
              { i: EyeIcon, t: "Revisão manual dos resultados", d: "Ferramentas ajudam; pessoas validam cada achado." },
              { i: ChatIcon, t: "Linguagem de negócio", d: "Riscos explicados em impacto, não só em jargão." },
              { i: UsersIcon, t: "Reunião de entrega", d: "Apresentamos o relatório pessoalmente, sem PDF solto no e-mail." },
            ].map((c, i) => (
              <Reveal key={c.t} delay={i * 80}>
                <div className="card card-hover h-full p-6">
                  <c.i />
                  <h3 className="mt-5 font-semibold">{c.t}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{c.d}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-surface py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Processo" title="9 etapas, do contato ao acompanhamento" />
          <ol className="relative">
            <span className="absolute bottom-0 left-5 top-0 w-px bg-border md:left-1/2" aria-hidden />
            {steps.map(([t, d], i) => {
              const right = i % 2 === 1;
              return (
                <li key={t} className="relative mb-8 pl-16 md:grid md:grid-cols-2 md:gap-16 md:pl-0">
                  <span className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-full border border-border bg-background font-mono text-sm md:left-1/2 md:-translate-x-1/2">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <Reveal className={right ? "md:col-start-2" : "md:text-right"}>
                    <div className="card p-6">
                      <h3 className="font-semibold">{t}</h3>
                      <p className="mt-1 text-sm text-muted-foreground">{d}</p>
                    </div>
                  </Reveal>
                </li>
              );
            })}
          </ol>
        </div>
      </section>

      <section className="section-ink py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Limites" title="O que não fazemos" />
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { i: BanIcon, t: "Exploração ativa (por ora)", d: "Identificamos e classificamos; não exploramos falhas nos serviços atuais." },
              { i: LockIcon, t: "Sistemas sem autorização", d: "Nunca testamos nada fora do escopo assinado." },
              { i: SirenIcon, t: "Resposta a incidentes", d: "Se você está sob ataque agora, procure um time especializado em IR." },
              { i: ClockIcon, t: "Monitoramento 24×7", d: "Nossos serviços são pontuais, com entregável definido." },
            ].map((c, i) => (
              <Reveal key={c.t} delay={i * 80}>
                <div className="card-ink h-full p-6">
                  <c.i />
                  <h3 className="mt-5 font-semibold">{c.t}</h3>
                  <p className="mt-2 text-sm text-ink-muted">{c.d}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <FinalCTA />
    </>
  );
}
