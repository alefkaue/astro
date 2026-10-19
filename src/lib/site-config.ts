const env = import.meta.env as Record<string, string | undefined>;

function clean(v: string | undefined) {
  const s = v?.trim();
  return s ? s : undefined;
}

const rawEndpoint = clean(env["VITE_FORMSPREE_ENDPOINT"]);

// Placeholders do .env.example não contam como configuração válida.
export const FORMSPREE_ENDPOINT =
  rawEndpoint &&
  /^https:\/\/formspree\.io\/f\/[A-Za-z0-9]+$/.test(rawEndpoint) &&
  !/SEU_FORM_ID|PLACEHOLDER/i.test(rawEndpoint)
    ? rawEndpoint
    : undefined;

const rawEmail = clean(env["VITE_CONTACT_EMAIL"]);
export const CONTACT_EMAIL =
  rawEmail && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(rawEmail) ? rawEmail : undefined;
