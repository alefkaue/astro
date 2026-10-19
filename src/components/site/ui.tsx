import { Link } from "@tanstack/react-router";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { PlusIcon } from "./icons";

export function Reveal({ children, className = "", delay = 0 }: { children: ReactNode; className?: string; delay?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([e]) => {
        if (e?.isIntersecting) {
          el.classList.add("is-visible");
          io.disconnect();
        }
      },
      { threshold: 0.12 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <div ref={ref} className={`reveal ${className}`} style={{ transitionDelay: `${delay}ms` }}>
      {children}
    </div>
  );
}

export function Counter({ to, suffix = "" }: { to: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  const [v, setV] = useState(0);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(([e]) => {
      if (!e?.isIntersecting) return;
      io.disconnect();
      const start = performance.now();
      const tick = (t: number) => {
        const p = Math.min(1, (t - start) / 1400);
        setV(Math.round(to * (1 - Math.pow(1 - p, 3))));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
    io.observe(el);
    return () => io.disconnect();
  }, [to]);
  return <span ref={ref}>{v}{suffix}</span>;
}

export function SectionHead({ label, title, children, center }: { label: string; title: ReactNode; children?: ReactNode; center?: boolean }) {
  return (
    <Reveal className={`mb-12 max-w-2xl ${center ? "mx-auto text-center" : ""}`}>
      <p className="eyebrow">{label}</p>
      <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">{title}</h2>
      {children && <p className="mt-4 text-lg opacity-75">{children}</p>}
    </Reveal>
  );
}

export function PageHero({ label, title, children }: { label: string; title: ReactNode; children?: ReactNode }) {
  return (
    <section className="section-ink relative overflow-hidden">
      <div className="dot-grid absolute inset-0" aria-hidden />
      <div className="container-x relative py-20 md:py-28">
        <p className="eyebrow">{label}</p>
        <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">{title}</h1>
        {children && <p className="mt-6 max-w-2xl text-lg text-ink-muted">{children}</p>}
      </div>
    </section>
  );
}

export function FinalCTA({
  title = "Pronto para saber o que está exposto?",
  text = "Entre em contato. Sem compromisso, sem automação — conversamos diretamente com você.",
  cta = "Solicitar orçamento gratuito",
}: { title?: string; text?: string; cta?: string }) {
  return (
    <section className="section-ink">
      <div className="container-x py-20 text-center md:py-28">
        <Reveal>
          <h2 className="mx-auto max-w-2xl text-3xl font-semibold tracking-tight md:text-5xl">{title}</h2>
          <p className="mx-auto mt-5 max-w-xl text-lg text-ink-muted">{text}</p>
          <Link to="/contato" className="btn btn-invert mt-8">{cta}</Link>
        </Reveal>
      </div>
    </section>
  );
}

export function Accordion({ items }: { items: { q: string; a: string }[] }) {
  const [open, setOpen] = useState<number | null>(0);
  return (
    <div className="divide-y divide-border rounded-2xl border border-border bg-surface">
      {items.map((it, i) => {
        const isOpen = open === i;
        return (
          <div key={it.q}>
            <button
              className="flex w-full items-center justify-between gap-4 px-6 py-5 text-left font-medium"
              aria-expanded={isOpen}
              onClick={() => setOpen(isOpen ? null : i)}
            >
              <span>{it.q}</span>
              <PlusIcon className={`shrink-0 transition-transform duration-300 ${isOpen ? "rotate-45" : ""}`} />
            </button>
            <div className="overflow-hidden transition-[max-height] duration-500 ease-in-out" style={{ maxHeight: isOpen ? 240 : 0 }}>
              <p className="px-6 pb-6 text-muted-foreground">{it.a}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
