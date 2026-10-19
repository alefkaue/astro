import { createFileRoute, Link } from "@tanstack/react-router";
import { Accordion, Counter, FinalCTA, Reveal, SectionHead } from "@/components/site/ui";
import {
  ArrowRight,
  DocIcon,
  KeyIcon,
  ListIcon,
  RadarIcon,
  TargetIcon,
} from "@/components/site/icons";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "ASTRO Cyber — Sua empresa sabe o que está exposto?" },
      {
        name: "description",
        content:
          "Avaliamos a infraestrutura da sua PME, identificamos o que está vulnerável e entregamos um relatório claro, em linguagem de negócio.",
      },
      { property: "og:title", content: "ASTRO Cyber — Sua empresa sabe o que está exposto?" },
      {
        property: "og:description",
        content: "Avaliações de segurança de infraestrutura para pequenas e médias empresas.",
      },
    ],
  }),
  component: Home,
});

const faq = [
  {
    q: "Vocês testam sem a minha autorização?",
    a: "Não. Nada é executado sem contrato assinado e autorização formal de testes (Rules of Engagement).",
  },
  {
    q: "Quanto tempo dura uma avaliação?",
    a: "Depende do tamanho do ambiente e do escopo. O prazo é definido por escrito na proposta, antes de qualquer execução.",
  },
  {
    q: "Vocês fazem pentest?",
    a: "Não neste momento. Nossas avaliações são defensivas: identificamos e classificamos riscos no escopo autorizado, sem explorar falhas. Se você precisa de um pentest, dizemos isso na primeira conversa.",
  },
  {
    q: "Preciso ter uma equipe de TI para contratar?",
    a: "Não. Atendemos empresas sem equipe técnica interna. O relatório executivo é feito justamente para quem não é especialista.",
  },
  {
    q: "Vocês conseguem corrigir os problemas encontrados?",
    a: "Não diretamente. Entregamos o diagnóstico e as recomendações priorizadas. A correção fica com sua equipe ou prestador de TI.",
  },
  {
    q: "Quais sistemas vocês conseguem avaliar?",
    a: "Servidores, roteadores, firewalls e outros dispositivos de rede conectados à internet ou acessíveis na rede interna, dentro do escopo autorizado.",
  },
  {
    q: "O serviço é contínuo ou pontual?",
    a: "Pontual, com entregável definido. Não fazemos monitoramento contínuo nem operamos um SOC.",
  },
];

function RadarVisual() {
  return (
    <svg viewBox="0 0 400 400" className="h-full w-full text-ink-foreground" aria-hidden>
      <g fill="none" stroke="currentColor" opacity=".25">
        {[60, 110, 160, 190].map((r) => (
          <circle key={r} cx="200" cy="200" r={r} />
        ))}
        <path d="M10 200h380M200 10v380" strokeDasharray="2 6" />
      </g>
      <g className="scan-sweep">
        <defs>
          <linearGradient id="sw" x1="0" x2="1">
            <stop offset="0" stopColor="currentColor" stopOpacity="0" />
            <stop offset="1" stopColor="currentColor" stopOpacity=".35" />
          </linearGradient>
        </defs>
        <path d="M200 200 L390 200 A190 190 0 0 0 334 66 Z" fill="url(#sw)" />
        <path d="M200 200 L390 200" stroke="currentColor" strokeWidth="1.5" />
      </g>
      {[
        [280, 130, 0],
        [130, 260, 1],
        [300, 290, 2],
      ].map(([x, y, d]) => (
        <g key={x}>
          <circle cx={x} cy={y} r="4" fill="currentColor" />
          <circle
            cx={x}
            cy={y}
            r="4"
            fill="none"
            stroke="currentColor"
            className="ping"
            style={{ animationDelay: `${d}s` }}
          />
        </g>
      ))}
      <circle cx="232" cy="96" r="4" className="fill-critical" />
    </svg>
  );
}

function Home() {
  return (
    <>
      <section className="section-ink relative overflow-hidden">
        <div className="dot-grid absolute inset-0" aria-hidden />
        <div className="container-x relative grid items-center gap-12 py-20 md:grid-cols-[1.2fr_1fr] md:py-32">
          <div>
            <p className="eyebrow">Avaliação de segurança para PMEs</p>
            <h1 className="mt-5 text-5xl font-semibold leading-[1.02] tracking-tight md:text-7xl">
              Sua empresa sabe o que está <span className="underline-anim">exposto</span>?
            </h1>
            <p className="mt-7 max-w-xl text-lg text-ink-muted">
              Avaliamos a infraestrutura da sua empresa, identificamos o que está vulnerável e
              entregamos um relatório claro — em linguagem de negócio, não só técnica.
            </p>
            <div className="mt-9 flex flex-wrap gap-3">
              <Link to="/contato" className="btn btn-invert">
                Solicitar orçamento
              </Link>
              <Link to="/servicos" className="btn btn-ghost">
                Ver serviços
              </Link>
            </div>
          </div>
          <div className="mx-auto aspect-square w-full max-w-md">
            <RadarVisual />
          </div>
        </div>
      </section>

      <section className="bg-background py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="O problema" title="A maioria das PMEs não sabe o que está exposto" />
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                i: ListIcon,
                t: "Inventário desatualizado",
                d: "Serviços que foram instalados e nunca desligados.",
              },
              {
                i: KeyIcon,
                t: "Configurações padrão",
                d: "Painéis de admin com senha padrão, bancos sem autenticação.",
              },
              {
                i: DocIcon,
                t: "Relatórios incompreensíveis",
                d: "Técnico demais para o dono aprovar o investimento.",
              },
            ].map((c, idx) => (
              <Reveal key={c.t} delay={idx * 100}>
                <div className="card card-hover h-full p-7">
                  <c.i />
                  <h3 className="mt-5 text-lg font-semibold">{c.t}</h3>
                  <p className="mt-2 text-muted-foreground">{c.d}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-surface py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="O que fazemos" title="Diagnóstico claro, resultado concreto" />
          <div className="grid gap-5 md:grid-cols-2">
            {[
              {
                i: TargetIcon,
                h: "assessment",
                t: "ASTRO Assessment",
                d: "Diagnóstico assistido de segurança: inventário, configurações de risco, severidade, relatório executivo e técnico, e reunião de entrega.",
              },
              {
                i: RadarIcon,
                h: "exposure",
                t: "ASTRO Exposure",
                d: "Avaliação defensiva de exposição: quais serviços estão acessíveis nos endereços autorizados e o que deveria ser fechado.",
              },
            ].map((c, idx) => (
              <Reveal key={c.t} delay={idx * 100}>
                <Link
                  to="/servicos"
                  hash={c.h}
                  className="card card-hover group flex h-full flex-col bg-background p-8"
                >
                  <div className="flex items-center justify-between">
                    <c.i width={28} height={28} />
                    <span className="badge badge-success">Sob proposta</span>
                  </div>
                  <h3 className="mt-6 text-2xl font-semibold">{c.t}</h3>
                  <p className="mt-3 flex-1 text-muted-foreground">{c.d}</p>
                  <span className="mt-6 inline-flex items-center gap-2 text-sm font-medium">
                    Ver detalhes{" "}
                    <ArrowRight
                      width={16}
                      height={16}
                      className="transition-transform group-hover:translate-x-1"
                    />
                  </span>
                </Link>
              </Reveal>
            ))}
          </div>
          <p className="mt-6 text-sm text-muted-foreground">
            Em preparação:{" "}
            <Link to="/servicos" hash="fraud-awareness" className="underline">
              ASTRO Fraud &amp; Awareness
            </Link>
            , prevenção de fraudes digitais e conscientização da equipe.
          </p>
        </div>
      </section>

      <section className="section-ink py-20 md:py-28">
        <div className="container-x">
          <SectionHead
            label="Como funciona"
            title="Escopo combinado antes, relatório explicado depois"
          />
          <div className="grid gap-5 md:grid-cols-3">
            {["Reunião de descoberta", "Proposta e autorização", "Avaliação e relatório"].map(
              (s, i) => (
                <Reveal key={s} delay={i * 120}>
                  <div className="card-ink h-full p-7">
                    <span className="font-mono text-sm text-ink-muted">0{i + 1}</span>
                    <h3 className="mt-4 text-xl font-semibold">{s}</h3>
                  </div>
                </Reveal>
              ),
            )}
          </div>
          <Link to="/como-funciona" className="btn btn-ghost mt-10">
            Ver metodologia completa
          </Link>
        </div>
      </section>

      <section className="bg-raised py-20">
        <div className="container-x grid gap-10 text-center md:grid-cols-3">
          {[
            { n: 9, s: "", l: "etapas", d: "Processo estruturado e documentado" },
            { n: 2, s: "", l: "relatórios", d: "Executivo + técnico por avaliação" },
            { n: 100, s: "%", l: "autorizado", d: "Nenhuma execução sem contrato assinado" },
          ].map((m) => (
            <Reveal key={m.l}>
              <p className="font-mono text-5xl font-medium md:text-6xl">
                <Counter to={m.n} suffix={m.s} />
              </p>
              <p className="mt-2 font-semibold">{m.l}</p>
              <p className="mt-1 text-sm text-muted-foreground">{m.d}</p>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="bg-surface py-20 md:py-28">
        <div className="container-x max-w-3xl">
          <SectionHead label="Perguntas frequentes" title="Dúvidas comuns" />
          <Reveal>
            <Accordion items={faq} />
          </Reveal>
        </div>
      </section>

      <FinalCTA />
    </>
  );
}
