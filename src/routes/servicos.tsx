import { createFileRoute, Link } from "@tanstack/react-router";
import { FinalCTA, PageHero, Reveal, SectionHead } from "@/components/site/ui";
import { CheckIcon, XIcon } from "@/components/site/icons";

export const Route = createFileRoute("/servicos")({
  head: () => ({
    meta: [
      { title: "Serviços — ASTRO Assessment e Exposure | ASTRO Cyber" },
      { name: "description", content: "Conheça o ASTRO Assessment e o ASTRO Exposure: escopo definido, entregáveis claros e limites honestos." },
      { property: "og:title", content: "Serviços | ASTRO Cyber" },
      { property: "og:description", content: "Diagnóstico completo e inventário de superfície de ataque para PMEs." },
    ],
  }),
  component: Servicos,
});

function List({ items, icon = "check" }: { items: string[]; icon?: "check" | "x" }) {
  return (
    <ul className="space-y-2.5">
      {items.map((i) => (
        <li key={i} className="flex gap-3">
          {icon === "check" ? <CheckIcon width={18} height={18} className="mt-0.5 shrink-0 text-success" /> : <XIcon width={18} height={18} className="mt-0.5 shrink-0 text-muted-foreground" />}
          <span>{i}</span>
        </li>
      ))}
    </ul>
  );
}

function ServiceCard(p: { name: string; desc: string; deliver: string[]; ideal: string[]; not: string[]; extra?: boolean }) {
  return (
    <Reveal>
      <article className="card p-7 md:p-10">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h3 className="text-3xl font-semibold tracking-tight">{p.name}</h3>
          <span className="badge badge-success">Disponível</span>
        </div>
        <p className="mt-4 max-w-3xl text-lg text-muted-foreground">{p.desc}</p>
        <div className="mt-8 grid gap-8 md:grid-cols-2">
          <div><p className="eyebrow mb-4">O que entregamos</p><List items={p.deliver} /></div>
          <div><p className="eyebrow mb-4">Ideal para</p><List items={p.ideal} /></div>
        </div>
        <div className="mt-8 rounded-xl bg-raised p-6">
          <p className="eyebrow mb-4">Não inclui</p>
          <List items={p.not} icon="x" />
        </div>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/contato" className="btn btn-primary">Solicitar orçamento</Link>
          {p.extra && <Link to="/como-funciona" className="btn btn-outline">Ver como funciona</Link>}
        </div>
      </article>
    </Reveal>
  );
}

const rows: [string, string, string][] = [
  ["Inventário de portas", "✓", "✓"],
  ["Classificação por severidade", "✓", "—"],
  ["Relatório executivo", "✓", "—"],
  ["Relatório técnico", "✓", "Simples"],
  ["Reunião de apresentação", "✓", "—"],
  ["Recomendações priorizadas", "✓", "De fechamento"],
  ["Duração típica", "3–7 dias úteis", "1–3 dias úteis"],
  ["Valor médio (faixa)", "Sob orçamento", "Sob orçamento"],
];

function Servicos() {
  return (
    <>
      <PageHero label="Catálogo de serviços" title="O que fazemos">
        Cada serviço tem escopo definido, entregáveis claros e limites explícitos. Você sabe exatamente o que recebe — e o que não está incluído.
      </PageHero>

      <section className="bg-background py-20 md:py-28">
        <div className="container-x space-y-8">
          <SectionHead label="Disponível agora" title="Serviços ativos" />
          <ServiceCard
            extra
            name="ASTRO Assessment"
            desc="Diagnóstico completo da infraestrutura da sua empresa. Mapeamos o que está exposto, identificamos configurações de risco, classificamos por severidade e apresentamos tudo pessoalmente, em linguagem que o gestor entende."
            deliver={["Inventário de serviços expostos", "Identificação de configurações de risco", "Classificação por severidade", "Relatório executivo", "Relatório técnico", "Reunião de apresentação", "Recomendações priorizadas"]}
            ideal={["PMEs de 20 a 500 funcionários", "Empresas sem avaliação recente", "Gestores que precisam justificar investimento", "Empresas que se preparam para auditorias"]}
            not={["Pentest com exploração ativa", "Teste de aplicação web", "Engenharia social", "Monitoramento contínuo", "Resposta a incidentes"]}
          />
          <ServiceCard
            name="ASTRO Exposure"
            desc="Inventário objetivo da sua superfície de ataque: o que a internet enxerga da sua empresa. Rápido, direto, e um bom ponto de partida."
            deliver={["Mapa de serviços expostos (IPs, portas, banners)", "Identificação de serviços inesperados", "Resumo de exposição com recomendações de fechamento", "Relatório técnico simples"]}
            ideal={["Quem precisa de uma visão rápida de exposição", "Prestadores de TI", "Ponto de partida antes de um Assessment"]}
            not={["Análise de vulnerabilidades", "Exploração", "Relatório executivo", "Reunião de apresentação"]}
          />
        </div>
      </section>

      <section className="bg-surface py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Comparativo" title="Assessment ou Exposure?" />
          <Reveal>
            <div className="overflow-x-auto rounded-2xl border border-border">
              <table className="w-full min-w-[560px] text-left">
                <thead className="bg-raised">
                  <tr>
                    <th className="p-4 font-medium text-muted-foreground">Item</th>
                    <th className="p-4 font-semibold">Assessment</th>
                    <th className="p-4 font-semibold">Exposure</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map(([k, a, e]) => (
                    <tr key={k} className="border-t border-border">
                      <td className="p-4">{k}</td>
                      <td className={`p-4 font-mono text-sm ${a === "✓" ? "text-success" : ""}`}>{a}</td>
                      <td className={`p-4 font-mono text-sm ${e === "✓" ? "text-success" : e === "—" ? "text-muted-foreground" : ""}`}>{e}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="bg-raised py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Em desenvolvimento" title="Próximos serviços" />
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {[
              { n: "ASTRO Pentest", s: "Em preparação", d: "Testes de intrusão com exploração ativa e controlada." },
              { n: "ASTRO Continuous", s: "Em preparação", d: "Acompanhamento recorrente da sua superfície de ataque." },
              { n: "ASTRO Fraud & Awareness", s: "Em estudo", d: "Conscientização de equipes e prevenção a fraudes." },
            ].map((c, i) => (
              <Reveal key={c.n} delay={i * 100}>
                <div className="card h-full p-7 opacity-90">
                  <span className="badge badge-neutral">{c.s}</span>
                  <h3 className="mt-5 text-xl font-semibold">{c.n}</h3>
                  <p className="mt-2 text-muted-foreground">{c.d}</p>
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
