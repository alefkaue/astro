import { createFileRoute, Link } from "@tanstack/react-router";
import { FinalCTA, PageHero, Reveal, SectionHead } from "@/components/site/ui";
import { CheckIcon, XIcon } from "@/components/site/icons";

export const Route = createFileRoute("/servicos")({
  head: () => ({
    meta: [
      { title: "Serviços — ASTRO Assessment, Exposure e Fraud & Awareness | ASTRO Cyber" },
      {
        name: "description",
        content:
          "Diagnóstico assistido de segurança e avaliação defensiva de exposição para PMEs. Escopo definido, entregáveis claros e limites honestos.",
      },
      { property: "og:title", content: "Serviços | ASTRO Cyber" },
      {
        property: "og:description",
        content: "Diagnóstico assistido de segurança e avaliação defensiva de exposição para PMEs.",
      },
    ],
  }),
  component: Servicos,
});

function List({ items, icon = "check" }: { items: string[]; icon?: "check" | "x" }) {
  return (
    <ul className="space-y-2.5">
      {items.map((i) => (
        <li key={i} className="flex gap-3">
          {icon === "check" ? (
            <CheckIcon width={18} height={18} className="mt-0.5 shrink-0 text-success" />
          ) : (
            <XIcon width={18} height={18} className="mt-0.5 shrink-0 text-muted-foreground" />
          )}
          <span>{i}</span>
        </li>
      ))}
    </ul>
  );
}

type Service = {
  id: string;
  name: string;
  tagline: string;
  desc: string;
  deliver: string[];
  ideal: string[];
  not: string[];
  badge: { text: string; tone: "success" | "neutral" };
  cta: string;
  extra?: boolean;
};

function ServiceCard(p: Service) {
  return (
    <Reveal>
      <article id={p.id} className="card scroll-mt-24 p-7 md:p-10">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h3 className="text-3xl font-semibold tracking-tight">{p.name}</h3>
            <p className="mt-1 font-mono text-xs uppercase tracking-wider text-muted-foreground">
              {p.tagline}
            </p>
          </div>
          <span
            className={`badge ${p.badge.tone === "success" ? "badge-success" : "badge-neutral"}`}
          >
            {p.badge.text}
          </span>
        </div>
        <p className="mt-4 max-w-3xl text-lg text-muted-foreground">{p.desc}</p>
        <div className="mt-8 grid gap-8 md:grid-cols-2">
          <div>
            <p className="eyebrow mb-4">
              {p.badge.tone === "success" ? "O que entregamos" : "O que estamos preparando"}
            </p>
            <List items={p.deliver} />
          </div>
          <div>
            <p className="eyebrow mb-4">Ideal para</p>
            <List items={p.ideal} />
          </div>
        </div>
        <div className="mt-8 rounded-xl bg-raised p-6">
          <p className="eyebrow mb-4">
            {p.badge.tone === "success" ? "Não inclui" : "Ainda falta antes de contratar"}
          </p>
          <List items={p.not} icon="x" />
        </div>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/contato" className="btn btn-primary">
            {p.cta}
          </Link>
          {p.extra && (
            <Link to="/como-funciona" className="btn btn-outline">
              Ver como funciona
            </Link>
          )}
        </div>
      </article>
    </Reveal>
  );
}

const available: Service[] = [
  {
    id: "assessment",
    name: "ASTRO Assessment",
    tagline: "Diagnóstico assistido de segurança empresarial",
    desc: "Avaliação defensiva da infraestrutura autorizada da sua empresa. Mapeamos serviços expostos, identificamos configurações de risco, classificamos por severidade e apresentamos tudo pessoalmente, em linguagem que o gestor entende.",
    deliver: [
      "Inventário dos serviços encontrados no escopo autorizado",
      "Identificação de configurações de risco",
      "Classificação dos achados por severidade",
      "Relatório executivo em linguagem de negócio",
      "Relatório técnico com evidências",
      "Recomendações de correção priorizadas",
      "Reunião de apresentação dos resultados",
    ],
    ideal: [
      "PMEs de 20 a 500 funcionários",
      "Empresas sem avaliação de segurança recente",
      "Gestores que precisam justificar investimento",
      "Empresas que se preparam para auditorias ou exigências de clientes",
    ],
    not: [
      "Pentest com exploração ativa de falhas",
      "Teste de aplicação web",
      "Simulação de engenharia social",
      "Monitoramento contínuo",
      "Resposta a incidentes ou perícia forense",
      "Garantia de ausência de vulnerabilidades",
    ],
    badge: { text: "Contratação sob proposta", tone: "success" },
    cta: "Solicitar orçamento",
    extra: true,
  },
  {
    id: "exposure",
    name: "ASTRO Exposure",
    tagline: "Avaliação defensiva de exposição técnica",
    desc: "Inventário objetivo dos serviços e portas acessíveis nos endereços que você autorizar — o que está aberto, qual serviço responde e o que provavelmente deveria ser fechado. Menor esforço, bom ponto de partida.",
    deliver: [
      "Mapa de serviços encontrados (endereços, portas e identificação do serviço)",
      "Destaque para serviços inesperados ou desnecessários",
      "Recomendações de fechamento ou restrição",
      "Relatório técnico resumido",
    ],
    ideal: [
      "Quem precisa de uma primeira visão da exposição",
      "Prestadores de TI que querem um diagnóstico para o cliente",
      "Ponto de partida antes de um Assessment",
    ],
    not: [
      "Análise aprofundada de configurações",
      "Exploração de falhas",
      "Relatório executivo",
      "Reunião de apresentação (disponível como adicional)",
    ],
    badge: { text: "Contratação sob proposta", tone: "success" },
    cta: "Solicitar orçamento",
  },
];

const preparing: Service = {
  id: "fraud-awareness",
  name: "ASTRO Fraud & Awareness",
  tagline: "Prevenção de fraudes digitais e conscientização",
  desc: "Revisão de processos expostos a golpes digitais — como fraude de boleto, falso fornecedor e pedidos urgentes por e-mail ou WhatsApp — e orientação da equipe para reconhecer engenharia social. Ainda não está disponível para contratação.",
  deliver: [
    "Mapeamento dos processos financeiros e de atendimento mais expostos a golpes",
    "Recomendações práticas de verificação e dupla checagem",
    "Material de conscientização para a equipe",
  ],
  ideal: [
    "Empresas com equipe financeira ou de atendimento pequena",
    "Quem já sofreu ou quase sofreu um golpe digital",
  ],
  not: [
    "Concluir a metodologia e validá-la em uma entrega interna",
    "Revisão jurídica do protocolo de consentimento dos participantes",
    "Nenhuma simulação de phishing será feita sem consentimento formal e sem captura de senhas reais",
  ],
  badge: { text: "Em preparação", tone: "neutral" },
  cta: "Entrar na lista de interesse",
};

const rows: [string, string, string][] = [
  ["Inventário de serviços expostos", "✓", "✓"],
  ["Análise de configurações de risco", "✓", "—"],
  ["Classificação por severidade", "✓", "Simplificada"],
  ["Relatório executivo", "✓", "—"],
  ["Relatório técnico", "✓", "Resumido"],
  ["Recomendações priorizadas", "✓", "De fechamento"],
  ["Reunião de apresentação", "✓", "Adicional"],
  ["Prazo e valor", "Definidos na proposta", "Definidos na proposta"],
];

function Servicos() {
  return (
    <>
      <PageHero label="Catálogo de serviços" title="O que fazemos">
        Cada serviço tem escopo definido, entregáveis claros e limites explícitos. A contratação é
        feita depois de uma conversa, com proposta escrita e autorização formal.
      </PageHero>

      <section className="bg-background py-20 md:py-28">
        <div className="container-x space-y-8">
          <SectionHead label="Disponível sob proposta" title="Serviços que já oferecemos">
            Avaliações defensivas: identificamos e classificamos riscos dentro do escopo autorizado,
            sem explorar falhas.
          </SectionHead>
          {available.map((s) => (
            <ServiceCard key={s.id} {...s} />
          ))}
        </div>
      </section>

      <section className="bg-surface py-20 md:py-28">
        <div className="container-x">
          <SectionHead label="Comparativo" title="Assessment ou Exposure?" />
          <Reveal>
            <div className="relative overflow-x-auto rounded-2xl border border-border">
              <table className="w-full min-w-[560px] text-left">
                <caption className="sr-only">
                  Comparação entre ASTRO Assessment e ASTRO Exposure
                </caption>
                <thead className="bg-raised">
                  <tr>
                    <th scope="col" className="p-4 font-medium text-muted-foreground">
                      Item
                    </th>
                    <th scope="col" className="p-4 font-semibold">
                      Assessment
                    </th>
                    <th scope="col" className="p-4 font-semibold">
                      Exposure
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map(([k, a, e]) => (
                    <tr key={k} className="border-t border-border">
                      <th scope="row" className="p-4 font-normal">
                        {k}
                      </th>
                      <td className={`p-4 font-mono text-sm ${a === "✓" ? "text-success" : ""}`}>
                        {a === "✓" ? (
                          <>
                            <span aria-hidden>✓</span>
                            <span className="sr-only">Incluído</span>
                          </>
                        ) : (
                          a
                        )}
                      </td>
                      <td
                        className={`p-4 font-mono text-sm ${e === "✓" ? "text-success" : e === "—" ? "text-muted-foreground" : ""}`}
                      >
                        {e === "✓" ? (
                          <>
                            <span aria-hidden>✓</span>
                            <span className="sr-only">Incluído</span>
                          </>
                        ) : e === "—" ? (
                          <>
                            <span aria-hidden>—</span>
                            <span className="sr-only">Não incluído</span>
                          </>
                        ) : (
                          e
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="bg-raised py-20 md:py-28">
        <div className="container-x space-y-8">
          <SectionHead label="Em preparação" title="Ainda não disponível para contratação">
            Só passamos a vender um serviço depois de validar a metodologia internamente. Se tiver
            interesse, avise — usamos isso para priorizar.
          </SectionHead>
          <ServiceCard {...preparing} />
          <Reveal>
            <p className="max-w-3xl text-sm text-muted-foreground">
              Também não oferecemos, neste momento: pentest com exploração ativa, monitoramento 24×7
              (SOC), resposta a incidentes ou perícia forense. Se você precisa de algum desses,
              dizemos isso na primeira conversa e, quando possível, indicamos quem faz.
            </p>
          </Reveal>
        </div>
      </section>

      <FinalCTA />
    </>
  );
}
