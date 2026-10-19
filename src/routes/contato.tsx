import { createFileRoute } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { PageHero, Reveal, SectionHead } from "@/components/site/ui";
import { CalendarIcon, CheckIcon, DocIcon, MailIcon } from "@/components/site/icons";

export const Route = createFileRoute("/contato")({
  head: () => ({
    meta: [
      { title: "Contato — Solicitar orçamento | ASTRO Cyber" },
      { name: "description", content: "Fale com a ASTRO Cyber. Sem compromisso, sem automação — uma pessoa responde você." },
      { property: "og:title", content: "Solicitar orçamento | ASTRO Cyber" },
      { property: "og:description", content: "Conte sobre sua empresa e receba uma proposta com escopo definido." },
    ],
  }),
  component: Contato,
});

// Configure o endpoint em VITE_FORMSPREE_ENDPOINT (ex.: https://formspree.io/f/xxxxxx)
const ENDPOINT = import.meta.env["VITE_FORMSPREE_ENDPOINT"] as string | undefined;

type Errors = Partial<Record<"nome" | "email" | "mensagem", string>>;

function validate(fd: FormData): Errors {
  const e: Errors = {};
  if (!String(fd.get("nome") ?? "").trim()) e.nome = "Informe seu nome completo.";
  const email = String(fd.get("email") ?? "").trim();
  if (!email) e.email = "Informe seu e-mail.";
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) e.email = "E-mail inválido.";
  if (String(fd.get("mensagem") ?? "").trim().length < 10) e.mensagem = "Escreva uma mensagem com pelo menos 10 caracteres.";
  return e;
}

function Field({ id, label, error, children, required }: { id: string; label: string; error?: string | undefined; children: React.ReactNode; required?: boolean }) {
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-sm font-medium">{label}{required ? " *" : <span className="text-muted-foreground"> (opcional)</span>}</label>
      {children}
      {error && <p id={`${id}-err`} className="mt-1.5 text-sm text-critical">{error}</p>}
    </div>
  );
}

function Contato() {
  const [errors, setErrors] = useState<Errors>({});
  const [status, setStatus] = useState<"idle" | "loading" | "ok" | "fail">("idle");

  async function onSubmit(ev: FormEvent<HTMLFormElement>) {
    ev.preventDefault();
    const fd = new FormData(ev.currentTarget);
    const e = validate(fd);
    setErrors(e);
    if (Object.keys(e).length) return;
    setStatus("loading");
    try {
      if (!ENDPOINT) throw new Error("Formspree não configurado");
      const res = await fetch(ENDPOINT, { method: "POST", body: fd, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error();
      setStatus("ok");
    } catch {
      setStatus("fail");
    }
  }

  const inv = (k: keyof Errors) => ({ "aria-invalid": !!errors[k], "aria-describedby": errors[k] ? `${k}-err` : undefined });

  return (
    <>
      <PageHero label="Contato" title="Vamos conversar">Conte um pouco sobre sua empresa. Respondemos em até 2 dias úteis.</PageHero>

      <section className="bg-raised py-20 md:py-24">
        <div className="mx-auto max-w-[680px] px-5">
          <Reveal>
            <p className="mb-6 rounded-xl border border-border bg-surface p-5 text-muted-foreground">
              Quem lê esta mensagem é uma pessoa da nossa equipe, não um robô. Não se preocupe com termos técnicos — escreva do seu jeito, e a gente pergunta o que precisar.
            </p>
            {status === "ok" ? (
              <div className="card p-10 text-center" role="status">
                <CheckIcon width={40} height={40} className="mx-auto text-success" />
                <h2 className="mt-4 text-2xl font-semibold">Mensagem enviada</h2>
                <p className="mt-2 text-muted-foreground">Obrigado! Entraremos em contato em breve pelo e-mail informado.</p>
              </div>
            ) : (
              <form noValidate onSubmit={onSubmit} className="card space-y-5 p-6 md:p-8">
                <Field id="nome" label="Nome completo" required error={errors.nome}><input id="nome" name="nome" className="field" autoComplete="name" {...inv("nome")} /></Field>
                <Field id="empresa" label="Empresa"><input id="empresa" name="empresa" className="field" autoComplete="organization" /></Field>
                <div className="grid gap-5 md:grid-cols-2">
                  <Field id="email" label="E-mail" required error={errors.email}><input id="email" name="email" type="email" className="field" autoComplete="email" {...inv("email")} /></Field>
                  <Field id="telefone" label="Telefone"><input id="telefone" name="telefone" type="tel" className="field" autoComplete="tel" /></Field>
                </div>
                <div className="grid gap-5 md:grid-cols-2">
                  <Field id="servico" label="Serviço de interesse">
                    <select id="servico" name="servico" className="field">
                      <option>Não sei ainda</option><option>ASTRO Assessment</option><option>ASTRO Exposure</option><option>Outro</option>
                    </select>
                  </Field>
                  <Field id="ips" label="Nº aproximado de servidores/IPs">
                    <select id="ips" name="ips" className="field">
                      <option>Menos de 10</option><option>10–50</option><option>50–200</option><option>Mais de 200</option><option>Não sei</option>
                    </select>
                  </Field>
                </div>
                <Field id="mensagem" label="Mensagem" required error={errors.mensagem}><textarea id="mensagem" name="mensagem" rows={5} className="field" {...inv("mensagem")} /></Field>
                {status === "fail" && <p className="text-sm text-critical" role="alert">Não foi possível enviar agora. Tente novamente ou escreva para contato@astrocyber.com.br.</p>}
                <button type="submit" className="btn btn-primary w-full" disabled={status === "loading"}>{status === "loading" ? "Enviando…" : "Enviar mensagem"}</button>
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
              { i: MailIcon, t: "Resposta pessoal", d: "Respondemos em até 2 dias úteis para entender seu contexto." },
              { i: CalendarIcon, t: "Reunião de descoberta", d: "Uma conversa curta, sem custo, para definir o escopo." },
              { i: DocIcon, t: "Proposta", d: "Você recebe uma proposta escrita com escopo, prazo e valor." },
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
