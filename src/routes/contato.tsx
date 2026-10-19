import { createFileRoute, Link } from "@tanstack/react-router";
import { useState, type FormEvent, type ReactNode } from "react";
import { PageHero, Reveal, SectionHead } from "@/components/site/ui";
import { CalendarIcon, CheckIcon, DocIcon, InfoIcon, MailIcon } from "@/components/site/icons";
import { CONTACT_EMAIL, FORMSPREE_ENDPOINT } from "@/lib/site-config";

export const Route = createFileRoute("/contato")({
  head: () => ({
    meta: [
      { title: "Contato — Solicitar orçamento | ASTRO Cyber" },
      {
        name: "description",
        content:
          "Fale com a ASTRO Cyber. Sem compromisso, sem automação — uma pessoa da equipe lê e responde.",
      },
      { property: "og:title", content: "Solicitar orçamento | ASTRO Cyber" },
      {
        property: "og:description",
        content: "Conte sobre sua empresa e receba uma proposta com escopo definido.",
      },
    ],
  }),
  component: Contato,
});

type Errors = Partial<Record<"nome" | "email" | "mensagem" | "consentimento", string>>;

function validate(fd: FormData): Errors {
  const e: Errors = {};
  if (!String(fd.get("nome") ?? "").trim()) e.nome = "Informe seu nome completo.";
  const email = String(fd.get("email") ?? "").trim();
  if (!email) e.email = "Informe seu e-mail.";
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) e.email = "E-mail inválido.";
  if (String(fd.get("mensagem") ?? "").trim().length < 10)
    e.mensagem = "Escreva uma mensagem com pelo menos 10 caracteres.";
  if (!fd.get("consentimento"))
    e.consentimento = "É preciso concordar com a política de privacidade para enviar.";
  return e;
}

function Field({
  id,
  label,
  error,
  children,
  required,
}: {
  id: string;
  label: string;
  error?: string | undefined;
  children: ReactNode;
  required?: boolean;
}) {
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-sm font-medium">
        {label}
        {required ? " *" : <span className="text-muted-foreground"> (opcional)</span>}
      </label>
      {children}
      {error && (
        <p id={`${id}-err`} className="mt-1.5 text-sm text-critical">
          {error}
        </p>
      )}
    </div>
  );
}

function EmailFallback() {
  if (!CONTACT_EMAIL) return null;
  return (
    <>
      {" "}
      Se preferir, escreva para{" "}
      <a className="underline" href={`mailto:${CONTACT_EMAIL}`}>
        {CONTACT_EMAIL}
      </a>
      .
    </>
  );
}

function Contato() {
  const [errors, setErrors] = useState<Errors>({});
  const [status, setStatus] = useState<"idle" | "loading" | "ok" | "fail">("idle");
  const configured = Boolean(FORMSPREE_ENDPOINT);

  async function onSubmit(ev: FormEvent<HTMLFormElement>) {
    ev.preventDefault();
    if (!FORMSPREE_ENDPOINT) return;
    const fd = new FormData(ev.currentTarget);
    const e = validate(fd);
    setErrors(e);
    if (Object.keys(e).length) return;
    setStatus("loading");
    try {
      const res = await fetch(FORMSPREE_ENDPOINT, {
        method: "POST",
        body: fd,
        headers: { Accept: "application/json" },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setStatus("ok");
    } catch {
      setStatus("fail");
    }
  }

  const inv = (k: keyof Errors) => ({
    "aria-invalid": !!errors[k],
    "aria-describedby": errors[k] ? `${k}-err` : undefined,
  });

  return (
    <>
      <PageHero label="Contato" title="Vamos conversar">
        Conte um pouco sobre sua empresa. Uma pessoa da equipe lê a mensagem e responde pelo e-mail
        informado.
      </PageHero>

      <section className="bg-raised py-20 md:py-24">
        <div className="mx-auto max-w-[680px] px-5">
          <Reveal>
            <p className="mb-6 rounded-xl border border-border bg-surface p-5 text-muted-foreground">
              Não se preocupe com termos técnicos — escreva do seu jeito, e a gente pergunta o que
              precisar. O primeiro contato e a reunião de descoberta não têm custo.
            </p>

            {!configured && (
              <div
                className="mb-6 flex gap-4 rounded-xl border border-critical/40 bg-surface p-5"
                role="status"
              >
                <InfoIcon className="shrink-0 text-critical" />
                <p className="text-sm">
                  <strong>Formulário temporariamente indisponível.</strong> O envio ainda não foi
                  ativado neste ambiente, então nenhuma mensagem seria entregue.
                  <EmailFallback />
                </p>
              </div>
            )}

            {status === "ok" ? (
              <div className="card p-10 text-center" role="status">
                <CheckIcon width={40} height={40} className="mx-auto text-success" />
                <h2 className="mt-4 text-2xl font-semibold">Mensagem enviada</h2>
                <p className="mt-2 text-muted-foreground">
                  Obrigado! Vamos responder pelo e-mail informado.
                </p>
              </div>
            ) : (
              <form
                noValidate
                onSubmit={onSubmit}
                className="card space-y-5 p-6 md:p-8"
                aria-disabled={!configured}
              >
                <input type="hidden" name="_subject" value="Novo contato pelo site — ASTRO Cyber" />
                <input
                  type="text"
                  name="_gotcha"
                  tabIndex={-1}
                  autoComplete="off"
                  className="hidden"
                  aria-hidden="true"
                />
                <fieldset
                  disabled={!configured || status === "loading"}
                  className="space-y-5 disabled:opacity-60"
                >
                  <Field id="nome" label="Nome completo" required error={errors.nome}>
                    <input
                      id="nome"
                      name="nome"
                      className="field"
                      autoComplete="name"
                      {...inv("nome")}
                    />
                  </Field>
                  <Field id="empresa" label="Empresa">
                    <input
                      id="empresa"
                      name="empresa"
                      className="field"
                      autoComplete="organization"
                    />
                  </Field>
                  <div className="grid gap-5 md:grid-cols-2">
                    <Field id="email" label="E-mail" required error={errors.email}>
                      <input
                        id="email"
                        name="email"
                        type="email"
                        className="field"
                        autoComplete="email"
                        {...inv("email")}
                      />
                    </Field>
                    <Field id="telefone" label="Telefone">
                      <input
                        id="telefone"
                        name="telefone"
                        type="tel"
                        className="field"
                        autoComplete="tel"
                      />
                    </Field>
                  </div>
                  <div className="grid gap-5 md:grid-cols-2">
                    <Field id="servico" label="Serviço de interesse">
                      <select id="servico" name="servico" className="field">
                        <option>Não sei ainda</option>
                        <option>ASTRO Assessment</option>
                        <option>ASTRO Exposure</option>
                        <option>ASTRO Fraud &amp; Awareness (lista de interesse)</option>
                        <option>Outro</option>
                      </select>
                    </Field>
                    <Field id="ips" label="Nº aproximado de servidores/IPs">
                      <select id="ips" name="ips" className="field">
                        <option>Não sei</option>
                        <option>Menos de 10</option>
                        <option>10–50</option>
                        <option>50–200</option>
                        <option>Mais de 200</option>
                      </select>
                    </Field>
                  </div>
                  <Field id="mensagem" label="Mensagem" required error={errors.mensagem}>
                    <textarea
                      id="mensagem"
                      name="mensagem"
                      rows={5}
                      className="field"
                      {...inv("mensagem")}
                    />
                  </Field>
                  <div>
                    <label className="flex items-start gap-3 text-sm">
                      <input
                        type="checkbox"
                        name="consentimento"
                        value="sim"
                        className="mt-1 h-4 w-4 shrink-0"
                        {...inv("consentimento")}
                      />
                      <span>
                        Li a{" "}
                        <Link to="/privacidade" className="underline">
                          política de privacidade
                        </Link>{" "}
                        e concordo com o uso dos meus dados para retorno deste contato. *
                      </span>
                    </label>
                    {errors.consentimento && (
                      <p id="consentimento-err" className="mt-1.5 text-sm text-critical">
                        {errors.consentimento}
                      </p>
                    )}
                  </div>
                </fieldset>
                {status === "fail" && (
                  <p className="text-sm text-critical" role="alert">
                    Não foi possível enviar agora. Tente novamente em alguns minutos.
                    <EmailFallback />
                  </p>
                )}
                <button
                  type="submit"
                  className="btn btn-primary w-full"
                  disabled={!configured || status === "loading"}
                >
                  {!configured
                    ? "Envio indisponível"
                    : status === "loading"
                      ? "Enviando…"
                      : "Enviar mensagem"}
                </button>
              </form>
            )}
          </Reveal>
        </div>
      </section>

      <section className="bg-surface py-20 md:py-24">
        <div className="container-x">
          <SectionHead label="Próximos passos" title="O que acontece depois" />
          <div className="grid gap-5 md:grid-cols-3">
            {[
              {
                i: MailIcon,
                t: "Resposta pessoal",
                d: "Uma pessoa da equipe responde para entender seu contexto.",
              },
              {
                i: CalendarIcon,
                t: "Reunião de descoberta",
                d: "Uma conversa curta, sem custo, para entender o ambiente e definir o escopo.",
              },
              {
                i: DocIcon,
                t: "Proposta",
                d: "Se fizer sentido para os dois lados, você recebe uma proposta escrita com escopo, prazo e valor.",
              },
            ].map((c, i) => (
              <Reveal key={c.t} delay={i * 100}>
                <div className="card h-full bg-background p-7">
                  <span className="font-mono text-sm text-muted-foreground">0{i + 1}</span>
                  <c.i className="mt-4" />
                  <h3 className="mt-4 font-semibold">{c.t}</h3>
                  <p className="mt-2 text-muted-foreground">{c.d}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
