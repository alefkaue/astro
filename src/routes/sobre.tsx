import { createFileRoute } from "@tanstack/react-router";
import { FinalCTA, PageHero, Reveal, SectionHead } from "@/components/site/ui";
import { InfoIcon, ServerIcon, ShieldIcon, UsersIcon, BoltIcon } from "@/components/site/icons";

export const Route = createFileRoute("/sobre")({
  head: () => ({
    meta: [
      { title: "Sobre — Quem somos | ASTRO Cyber" },
      { name: "description", content: "Não vendemos medo. Vendemos clareza. Conheça a ASTRO Cyber, cibersegurança feita para PMEs." },
      { property: "og:title", content: "Sobre a ASTRO Cyber" },
      { property: "og:description", content: "Cibersegurança com plataforma própria, entrega pessoal e honestidade sobre limites." },
    ],
  }),
  component: Sobre,
});

const team = [
  { n: "Fundador A", r: "Segurança ofensiva", d: "Responsável pela execução técnica das avaliações e pela plataforma." },
  { n: "Fundador B", r: "Infraestrutura e redes", d: "Experiência em ambientes corporativos, servidores e firewalls." },
  { n: "Fundador C", r: "Relacionamento e negócios", d: "Conecta achados técnicos às decisões de gestão." },
];

function Sobre() {
  return (
    <>
      <PageHero label="Quem somos" title="ASTRO Cyber" />

      <section className="bg-raised py-20 md:py-28">
        <div className="container-x max-w-3xl space-y-6 text-lg leading-relaxed">
          <Reveal><p className="eyebrow mb-4">Missão</p>
            <p>Pequenas e médias empresas são parte do mesmo alvo que grandes corporações — mas sem os mesmos recursos. Raramente têm um time de segurança, e muitas vezes nem um inventário atualizado do que está ligado à internet.</p></Reveal>
          <Reveal><p>O mercado costuma responder com dois extremos: ferramentas automáticas que geram centenas de alertas sem contexto, ou consultorias caras com relatórios que ninguém consegue ler.</p></Reveal>
          <Reveal><p>A ASTRO Cyber existe para ocupar o meio: diagnósticos com escopo claro, revisados por pessoas e explicados em linguagem de negócio.</p></Reveal>
          <Reveal><p className="border-l-2 border-foreground pt-2 pb-2 pl-6 text-3xl font-medium tracking-tight md:text-4xl">Não vendemos medo. Vendemos clareza.</p></Reveal>
        </div>
      </section>

      <section className="bg-surface py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Equipe" title="Quem está por trás" />
          <div className="grid gap-5 md:grid-cols-3">
            {team.map((p, i) => (
              <Reveal key={p.n} delay={i * 100}>
                <div className="card h-full bg-background p-7">
                  <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-foreground to-muted-foreground text-2xl font-semibold text-background">{p.n.at(-1)}</div>
                  <h3 className="mt-5 text-lg font-semibold">{p.n}</h3>
                  <p className="font-mono text-xs uppercase tracking-wider text-muted-foreground">{p.r}</p>
                  <p className="mt-3 text-muted-foreground">{p.d}</p>
                </div>
              </Reveal>
            ))}
          </div>
          <p className="mt-6 text-sm text-muted-foreground">Perfis serão atualizados antes do lançamento comercial.</p>
        </div>
      </section>

      <section className="section-ink py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Diferenciais" title="Por que a ASTRO" />
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { i: ServerIcon, t: "Plataforma própria", d: "Ferramental desenvolvido internamente para avaliações consistentes." },
              { i: UsersIcon, t: "Entrega pessoal", d: "Toda avaliação termina em uma reunião com quem decide." },
              { i: ShieldIcon, t: "Honestidade sobre limites", d: "Dizemos o que não fazemos antes de você contratar." },
              { i: BoltIcon, t: "Foco em PMEs", d: "Escopo, linguagem e formato pensados para empresas de 20 a 500 pessoas." },
            ].map((c, i) => (
              <Reveal key={c.t} delay={i * 80}>
                <div className="card-ink h-full p-6"><c.i /><h3 className="mt-5 font-semibold">{c.t}</h3><p className="mt-2 text-sm text-ink-muted">{c.d}</p></div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-raised py-20">
        <div className="container-x max-w-3xl">
          <Reveal>
            <div className="card flex gap-5 p-7">
              <InfoIcon className="shrink-0" />
              <div>
                <h3 className="font-semibold">Situação atual</h3>
                <p className="mt-2 text-muted-foreground">A ASTRO Cyber está em fase de estruturação empresarial e ainda não possui CNPJ. Por transparência: no momento, a contratação pode ser feita por pessoa física, ou agendada para após a constituição da empresa. Explicamos tudo na primeira conversa.</p>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <FinalCTA />
    </>
  );
}
