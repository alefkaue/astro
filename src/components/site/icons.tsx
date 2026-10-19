import type { ReactNode, SVGProps } from "react";

type P = SVGProps<SVGSVGElement>;
const Base = ({ children, ...p }: P & { children: ReactNode }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...p}>
    {children}
  </svg>
);

export const RadarIcon = (p: P) => (
  <Base {...p}><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" opacity=".6" /><path d="M12 12l6.5-6.5" /><circle cx="12" cy="12" r="1" fill="currentColor" /></Base>
);
export const ListIcon = (p: P) => (<Base {...p}><path d="M9 6h11M9 12h11M9 18h11" /><path d="M4 6h.01M4 12h.01M4 18h.01" /></Base>);
export const KeyIcon = (p: P) => (<Base {...p}><circle cx="8" cy="15" r="4" /><path d="M11 12l9-9M17 6l3 3M15 8l2 2" /></Base>);
export const DocIcon = (p: P) => (<Base {...p}><path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z" /><path d="M14 3v5h5M9 13h6M9 17h4" /></Base>);
export const TargetIcon = (p: P) => (<Base {...p}><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1" /></Base>);
export const EyeIcon = (p: P) => (<Base {...p}><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></Base>);
export const ChatIcon = (p: P) => (<Base {...p}><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z" /></Base>);
export const UsersIcon = (p: P) => (<Base {...p}><circle cx="9" cy="8" r="3.5" /><path d="M2.5 20a6.5 6.5 0 0 1 13 0" /><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6" /></Base>);
export const BoltIcon = (p: P) => (<Base {...p}><path d="M13 2L4 14h7l-1 8 9-12h-7z" /></Base>);
export const BanIcon = (p: P) => (<Base {...p}><circle cx="12" cy="12" r="9" /><path d="M5.6 5.6l12.8 12.8" /></Base>);
export const LockIcon = (p: P) => (<Base {...p}><rect x="4" y="10" width="16" height="11" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></Base>);
export const SirenIcon = (p: P) => (<Base {...p}><path d="M7 18v-6a5 5 0 0 1 10 0v6M5 21h14M12 3v1M4.2 6.2l.8.8M19.8 6.2l-.8.8" /></Base>);
export const ClockIcon = (p: P) => (<Base {...p}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></Base>);
export const ServerIcon = (p: P) => (<Base {...p}><rect x="3" y="4" width="18" height="7" rx="1.5" /><rect x="3" y="13" width="18" height="7" rx="1.5" /><path d="M7 7.5h.01M7 16.5h.01" /></Base>);
export const ShieldIcon = (p: P) => (<Base {...p}><path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z" /><path d="M9 12l2 2 4-4" /></Base>);
export const InfoIcon = (p: P) => (<Base {...p}><circle cx="12" cy="12" r="9" /><path d="M12 11v5M12 8h.01" /></Base>);
export const MailIcon = (p: P) => (<Base {...p}><rect x="3" y="5" width="18" height="14" rx="2" /><path d="M3 7l9 6 9-6" /></Base>);
export const CalendarIcon = (p: P) => (<Base {...p}><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M3 10h18M8 3v4M16 3v4" /></Base>);
export const CheckIcon = (p: P) => (<Base {...p}><path d="M5 12l5 5 9-10" /></Base>);
export const XIcon = (p: P) => (<Base {...p}><path d="M6 6l12 12M18 6L6 18" /></Base>);
export const ArrowRight = (p: P) => (<Base {...p}><path d="M5 12h14M13 6l6 6-6 6" /></Base>);
export const ArrowUp = (p: P) => (<Base {...p}><path d="M12 19V5M6 11l6-6 6 6" /></Base>);
export const SunIcon = (p: P) => (<Base {...p}><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></Base>);
export const MoonIcon = (p: P) => (<Base {...p}><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z" /></Base>);
export const MenuIcon = (p: P) => (<Base {...p}><path d="M4 7h16M4 12h16M4 17h16" /></Base>);
export const PlusIcon = (p: P) => (<Base {...p}><path d="M12 5v14M5 12h14" /></Base>);
