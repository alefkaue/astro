import { Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { ArrowUp, MenuIcon, MoonIcon, SunIcon, XIcon } from "./icons";

export function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2.5 font-semibold tracking-tight" aria-label="ASTRO Cyber — início">
      <svg width="26" height="26" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden>
        <circle cx="16" cy="16" r="13" />
        <circle cx="16" cy="16" r="8" opacity=".55" />
        <circle cx="16" cy="16" r="3" opacity=".35" />
        <path d="M16 16 L25 7" strokeLinecap="round" />
        <circle cx="16" cy="16" r="1.6" fill="currentColor" />
      </svg>
      <span className="text-lg">ASTRO Cyber</span>
    </Link>
  );
}

const links = [
  { to: "/servicos", label: "Serviços" },
  { to: "/como-funciona", label: "Como funciona" },
  { to: "/sobre", label: "Sobre" },
] as const;

function ThemeToggle() {
  const [dark, setDark] = useState(false);
  useEffect(() => setDark(document.documentElement.classList.contains("dark")), []);
  const toggle = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem("theme", next ? "dark" : "light");
  };
  return (
    <button onClick={toggle} aria-label={dark ? "Ativar tema claro" : "Ativar tema escuro"} className="rounded-full p-2 text-ink-muted transition-colors hover:text-ink-foreground">
      {dark ? <SunIcon width={20} height={20} /> : <MoonIcon width={20} height={20} />}
    </button>
  );
}

export function Nav() {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
  }, [open]);
  return (
    <header className="section-ink sticky top-0 z-50 border-b border-ink-border">
      <div className="container-x flex h-16 items-center justify-between">
        <Logo />
        <nav className="hidden items-center gap-8 md:flex" aria-label="Principal">
          {links.map((l) => (
            <Link key={l.to} to={l.to} className="text-sm text-ink-muted transition-colors hover:text-ink-foreground" activeProps={{ className: "!text-ink-foreground font-medium" }}>
              {l.label}
            </Link>
          ))}
          <ThemeToggle />
          <Link to="/contato" className="btn btn-invert !py-2 text-sm">Solicitar orçamento</Link>
        </nav>
        <div className="flex items-center gap-1 md:hidden">
          <ThemeToggle />
          <button className="p-2" aria-label="Abrir menu" onClick={() => setOpen(true)}><MenuIcon /></button>
        </div>
      </div>
      <div className={`fixed inset-0 z-50 md:hidden ${open ? "" : "pointer-events-none"}`}>
        <div className={`absolute inset-0 bg-ink/70 transition-opacity ${open ? "opacity-100" : "opacity-0"}`} onClick={() => setOpen(false)} />
        <div className={`section-ink absolute inset-x-0 bottom-0 rounded-t-3xl border-t border-ink-border p-6 pb-10 transition-transform duration-300 ${open ? "translate-y-0" : "translate-y-full"}`}>
          <div className="mb-6 flex items-center justify-between">
            <span className="eyebrow">Menu</span>
            <button aria-label="Fechar menu" onClick={() => setOpen(false)}><XIcon /></button>
          </div>
          <div className="flex flex-col gap-1">
            {links.map((l) => (
              <Link key={l.to} to={l.to} onClick={() => setOpen(false)} className="py-3 text-xl" activeProps={{ className: "font-semibold" }}>{l.label}</Link>
            ))}
            <Link to="/contato" onClick={() => setOpen(false)} className="btn btn-invert mt-4">Solicitar orçamento</Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="section-ink border-t border-ink-border">
      <div className="container-x grid gap-10 py-14 md:grid-cols-4">
        <div className="md:col-span-2">
          <Logo />
          <p className="mt-4 max-w-sm text-sm text-ink-muted">Avaliações de segurança de infraestrutura para pequenas e médias empresas brasileiras.</p>
        </div>
        <div className="flex flex-col gap-2 text-sm">
          <span className="eyebrow mb-2">Navegação</span>
          {links.map((l) => <Link key={l.to} to={l.to} className="text-ink-muted hover:text-ink-foreground">{l.label}</Link>)}
          <Link to="/contato" className="text-ink-muted hover:text-ink-foreground">Contato</Link>
        </div>
        <div className="flex flex-col gap-2 text-sm">
          <span className="eyebrow mb-2">Legal</span>
          <Link to="/privacidade" className="text-ink-muted hover:text-ink-foreground">Privacidade (LGPD)</Link>
          <a href="mailto:contato@astrocyber.com.br" className="text-ink-muted hover:text-ink-foreground">contato@astrocyber.com.br</a>
        </div>
      </div>
      <div className="container-x border-t border-ink-border py-6 font-mono text-xs text-ink-muted">© {new Date().getFullYear()} ASTRO Cyber</div>
    </footer>
  );
}

export function ScrollTop() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const on = () => setShow(window.scrollY > 400);
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  return (
    <button
      aria-label="Voltar ao topo"
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      className={`btn btn-primary fixed bottom-6 right-6 z-40 !p-3 shadow-lg transition-all ${show ? "opacity-100" : "pointer-events-none translate-y-4 opacity-0"}`}
    >
      <ArrowUp width={20} height={20} />
    </button>
  );
}
