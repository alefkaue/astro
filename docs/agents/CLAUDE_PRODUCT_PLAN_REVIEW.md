# Parecer Claude — PLAN-CLAUDE-01

Salvo por Codex a partir do resultado original concluído. Claude não conseguiu gravar o documento: Write exigiu aprovação indisponível na sessão, e a operação foi negada. Nenhuma permissão foi contornada. Texto abaixo preserva o parecer; decisões de integração estão em PRODUCT_PLAN_INTEGRATION.md.

## Recommendation
I agree with the direction: a web SaaS with an optional per-network connector, no per-endpoint agent, and no arbitrary command execution. I disagree with the order and with some technical choices:

1. **Widen S0 before any connector work.** I found three tenant-isolation and authorization gaps (below).
2. **Don't add Celery+Redis in S1.** A `jobs` table in the database with leases (time-limited claims on a job) gives durable jobs, retries and cancellation with fewer moving parts. The connector will use the same pull model anyway. Add Redis only if measured load needs it.
3. **PostgreSQL shouldn't block S1.** First add versioned migrations on SQLite (`schema_migrations` instead of `_migrate()`). Move to PostgreSQL later (S2b), with fixtures and a tested restore.
4. **The internal runner should become the first "worker" using the same lease/event/evidence protocol.** The connector is then just a remote worker with its own identity, so there is one execution path, not two.

## Findings from the code
- **Managed review is visible across tenants.** `/api/reviews` and `/api/scans/<id>/review` (`app/scans/routes.py:245-269`) have no `login_required`. `list_review_queue` (`app/db.py:619`) returns every tenant's pending scans. `get_scan(scan_id)` has no tenant filter, and the review is not checked against a managed-plan contract, an assignment or the current status.
- **`role_required` lets `admin` through everywhere** (`app/auth/decorators.py:104`). There is no separate "organization admin" role; roles are global strings.
- **The legacy unscoped helpers are still there:** `get_scan`, `get_engagement` and `get_scan_findings` drop the tenant filter when `account_id=None`, and `get_scan_findings_with_ids` never filters. This is item F2, still open.
- **Execution is not durable.** `/api/scan` runs inside the HTTP request. The autonomous mode uses a daemon thread with events kept in memory (`app/autonomous/runner.py`), so a restart loses them. There is no cancellation, and the concurrency cap is per process.
- **The quota check isn't atomic.** It counts, then inserts (`enforce_scan_quota` vs `create_scan`). `max_ips` in `core/plans.py` is never enforced.
- **Scope is only a list of IPs/CIDRs.** There is no version, expiry, exclusions, `network_id` or per-port limits. The same IP in two networks of one tenant can't be told apart.
- **No CSRF token.** Protection relies only on SameSite=Lax, and the API accepts JSON sent with any content type (`force=True`).
- **Owner budget reveals whether a finding exists.** It answers 403 "n├úo pertence ├á sua conta" for another tenant's finding instead of 404.

## Minimal data model
- **`networks`**: `id`, `account_id`, `name`, `kind` (public/internal), `created_by`.
- **`scopes`** (versioned, linked to `engagements`): `network_id`, `version`, `cidrs`, `exclusions`, `ports_policy`, `max_hosts`, `valid_until`, `authorized_by`, `authorized_at`. Once authorized, a version is never changed.
- **`connectors`**: `account_id`, `network_id`, `name`, `status` (pending/active/revoked), `token_hash`, `token_rotated_at`, `last_seen_at`, `version`, `revoked_at`, `revoked_by`.
- **`enrollment_tokens`**: `token_hash`, `account_id`, `network_id`, `expires_at` (short), `used_at`, `created_by`.
- **`jobs`**: `account_id`, `network_id`, `scope_id` plus `scope_version`, `profile` plus `profile_version`, `executor` (internal/connector), `connector_id`, `status`, `idempotency_key` (unique per account), `attempt`, `max_attempts`, `lease_owner`, `lease_expires_at`, `cancel_requested_at`, `scan_id`, timestamps, `error_code`.
- **`job_attempts`** (one row per attempt).
- **`job_events`**: `job_id`, `attempt_id`, `seq` (unique per job, server-checked to increase), `ts`, `phase`, `message`, bounded `data`.
- **`evidence`**: `account_id`, `job_id`, `finding_id`, `kind`, `sha256`, `size`, `source` (connector/worker plus version), `collected_at`, `redacted` (bool), `retention_until`.
- **`findings`**: add `account_id`, `network_id` and an asset key `(network_id, host, port)`.
- **`review_assignments`**: `account_id`, `scan_id`, `reviewer_id`, `granted_by`, `expires_at`.

## Job state machine
`queued ÔåÆ leased ÔåÆ running ÔåÆ {succeeded | partial | failed | cancelled}`

- `leased`/`running` ÔåÆ `queued` when the lease expires and `attempt < max_attempts`. Otherwise ÔåÆ `failed` (`lease_expired`).
- `queued` ÔåÆ `cancelled` happens immediately.
- `running` with cancellation requested ÔåÆ `cancelling` ÔåÆ `cancelled` once the worker confirms or the lease expires.
- Final states never change. Every transition is a conditional `UPDATE ÔÇª WHERE status=? AND lease_owner=?`.

## API contracts
**User side (session plus capability):**
- `POST /api/jobs` with `Idempotency-Key` ÔåÆ 202 `{job_id}`. Quota is checked in the same transaction.
- `GET /api/jobs/<id>`
- `GET /api/jobs/<id>/events?after_seq=`
- `POST /api/jobs/<id>/cancel`

**Connector side (Bearer token; tenant and network come from the token, never from the payload):**
- `POST /api/connector/enroll` ÔåÆ token returned once.
- `POST /api/connector/heartbeat`
- `POST /api/connector/jobs/lease` ÔåÆ one job plus the fixed scope snapshot plus the profile.
- `POST /api/connector/jobs/<id>/events` (sequenced, size-limited)
- `POST /api/connector/jobs/<id>/evidence` (hash checked, size cap)
- `POST /api/connector/jobs/<id>/complete`

Every connector call includes `attempt_id` and the lease. A stale attempt gets 409.

## Security requirements
- **Enrollment:** single-use token with a short expiry, stored only as a hash and audited. The connector is bound to the network on the server side.
- **Outbound connection:** the connector only makes outbound HTTPS calls, validates certificates and supports a proxy. It opens no listening port.
- **Revocation and rotation:** these take effect on the next request, which must return 401. Revoking a connector also releases its leases and fails its running jobs.
- **Scope:** checked on the server when the job is created and again by the connector using the snapshot. Hostnames are resolved and every address checked (including IPv6). Loopback, link-local and cloud metadata addresses are always blocked. Profiles are a fixed list; no free-form commands.
- **Retries and replay:** deduplicate on `idempotency_key` and `(job_id, seq)`. A completed attempt can't be completed again. Retries are never automatic after a partial run without a decision.
- **Offline:** the connector keeps a bounded local buffer, and its local limits stay in force. When the lease expires the server re-queues or fails the job; it never assumes "zero findings".
- **Cancellation:** cooperative, checked between hosts. The cancel flag comes back in heartbeat and event responses.

## Roles, capabilities and managed-review visibility
Map roles to capabilities in the backend (`scope.authorize`, `job.run`, `connector.manage`, `report.read`, `review.perform`). Replace the implicit `admin` bypass with explicit capabilities. Platform staff get no cross-tenant access by default.

Managed review should only be visible when all of these hold: the tenant's plan includes managed service, there is an active, unexpired assignment, and the queue is filtered by those assignments. Every read and every signature is recorded in the audit log under the tenant's `account_id`. The customer can see who reviewed their data.

## Migration sequence and backend tasks
| Step | Change | Main files | Depends on | Acceptance criteria and regression tests |
| --- | --- | --- | --- | --- |
| B0 | Split the data helpers into explicit `*_scoped` and `*_internal` versions; tenant-scope the review routes and add assignments; replace the admin bypass with capabilities; add a CSRF token; make owner budget answer 404 | `app/db.py`, `app/auth/decorators.py`, `app/scans/routes.py`, `app/owner/routes.py` | ÔÇö | Cross-tenant tests for each route, a user with no tenant, staff without an assignment, and `admin` blocked on customer routes |
| B1 | Migration runner (`schema_migrations`) that keeps current tables | `app/db.py`, new `app/migrations/` | B0 | Migrating an existing database keeps all data and running it twice changes nothing |
| B2 | `jobs`/`job_events` tables plus an internal lease-based worker; `/api/scan` and the autonomous mode create jobs while keeping their old routes as wrappers | `app/autonomous/runner.py`, new `app/jobs/` | B1 | Survives a restart; an expired lease is retried; the same idempotency key gives one job; cancellation works; quota stays correct under concurrent requests |
| B3 | Networks, versioned scopes, `network_id` on findings, `max_ips` enforced | `app/scope.py`, `core/scope.py`, `app/engagements/routes.py` | B1 | Same IP in two networks stays separate; an expired scope is refused; exclusions work, including resolved hostnames and IPv6 |
| B4 | Connector API (enroll, heartbeat, lease, events, evidence, complete, revoke) | new `app/connector/` | B2, B3 | Token reuse refused; revoked connector gets 401; another tenant's job is never leased; stale attempt gets 409; oversized upload refused; replayed `seq` ignored |
| B5 | Move to PostgreSQL | `app/db.py` | B1ÔÇôB4 stable | Fixtures moved over, restore tested, all tests pass on both databases |

I couldn't verify one thing within the turn budget: whether report and PDF exports leak data across tenants beyond `get_scan` with `account_id` (`app/reports/routes.py:38-43`). That needs its own check in B0.
