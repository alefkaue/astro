import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";

const SRC = join(__dirname, "..");

function siteSources() {
  const dirs = [join(SRC, "routes"), join(SRC, "components", "site")];
  return dirs.flatMap((d) =>
    readdirSync(d)
      .filter((f) => f.endsWith(".tsx"))
      .map((f) => ({ file: f, text: readFileSync(join(d, f), "utf8") })),
  );
}

describe("conteúdo público da vitrine", () => {
  it.each([
    ["e-mail institucional fixo no código", /@astrocyber\.com\.br/],
    ["marca legada CYMAG", /cymag/i],
    ["endpoint placeholder", /formspree\.io\/f\/(PLACEHOLDER|SEU_FORM_ID)/i],
    ["prazo de resposta garantido", /até \d+ dias? úte/i],
    ["promessa de segurança ofensiva", /segurança ofensiva/i],
  ])("não contém %s", (_label, pattern) => {
    const hits = siteSources()
      .filter((s) => pattern.test(s.text))
      .map((s) => s.file);
    expect(hits).toEqual([]);
  });
});

describe("site-config", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.resetModules();
  });

  async function load(env: Record<string, string>) {
    for (const [k, v] of Object.entries(env)) vi.stubEnv(k, v);
    return import("@/lib/site-config");
  }

  it("rejeita o placeholder do .env.example", async () => {
    const c = await load({ VITE_FORMSPREE_ENDPOINT: "https://formspree.io/f/SEU_FORM_ID" });
    expect(c.FORMSPREE_ENDPOINT).toBeUndefined();
  });

  it("rejeita endpoints que não são do Formspree", async () => {
    const c = await load({ VITE_FORMSPREE_ENDPOINT: "https://exemplo.com/f/abc123" });
    expect(c.FORMSPREE_ENDPOINT).toBeUndefined();
  });

  it("aceita um endpoint válido", async () => {
    const c = await load({ VITE_FORMSPREE_ENDPOINT: "https://formspree.io/f/xyzabcd1" });
    expect(c.FORMSPREE_ENDPOINT).toBe("https://formspree.io/f/xyzabcd1");
  });

  it("não expõe e-mail quando a variável está vazia", async () => {
    const c = await load({ VITE_CONTACT_EMAIL: "" });
    expect(c.CONTACT_EMAIL).toBeUndefined();
  });
});
