# Run in your normal authenticated PowerShell; no credentials/proxies are changed.
param([ValidateSet('redesign','product-plan','experience','commercial','pilot-security')][string]$Task = 'redesign')
$ErrorActionPreference = 'Stop'
$astroRepository = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$astroClaudeExecutable = Join-Path $env:USERPROFILE '.local/bin/claude.exe'
if (-not (Test-Path -LiteralPath $astroClaudeExecutable)) {
    throw 'Claude executable not found. Check your Claude Code installation.'
}
$astroReviewPrompt = @'
You are reviewing the ASTRO Cyber redesign jointly with Codex. Read docs/agents/REDESIGN.md, app/assessment_views.py, app/main.py, app/engagements/routes.py, tests/test_assessment_views.py, static/astro-routes.js and static/astro-workspace.js. Review tenant isolation, role permissions, API/frontend mismatches, async navigation, and accidental exposure of synthetic data as real. READ ONLY: do not edit files, run shell commands, start scanners, read secrets, commit or push. Return concrete issues with filename, line, severity, explanation and proposed correction. If none are found, say so and identify limits of the review. Codex will inspect your findings and implement/test accepted fixes. Do not claim browser tests were run.
'@
$astroResultPrefix = 'CLAUDE_LOCAL_REVIEW'
$astroTools = 'Read,Glob,Grep'
$astroAllowedTools = @('Read','Glob','Grep')
$astroMaxTurns = 10
if ($Task -eq 'pilot-security') {
    $astroResultPrefix = 'CLAUDE_PILOT_SECURITY'
    $astroMaxTurns = 18
    $astroReviewPrompt = @'
Work with Codex on implementation task SCOPE-DENY. Read core/scope.py, app/scope.py, core/scanner.py, core/plans.py and relevant existing scope tests. Codex exclusively owns app/features.py, app/__init__.py, app/ai/aegis.py, tests/test_deployment_gates.py and integration docs: do not modify those. Your deliverable is an exact unified diff in your final response for core/scope.py, app/scope.py and a new tests/test_scope_safety.py. READ ONLY tools: do not edit, run commands, scan networks, start browsers, read secrets, commit or push. Implement deny rules for loopback, link-local/cloud metadata, multicast, unspecified and configured CYMAG_SCOPE_DENY CIDRs, including IPv6. Reject unsupported IPv6 execution and networks exceeding the scanner's 64 candidate limit; do not silently truncate. Enforce account plan max_ips after tenant-scoped resolution; preserve authorized private IPv4 LANs in development but require explicit deployment allowlist in hosted environments. Fail closed on malformed policy. Validate discovered hosts with the same deny rules. Avoid iterating huge networks. Explain host counting /31 and /32, backwards compatibility, testing requirements, and safety limits (allowlist is not legal proof of authorization). Finish within 18 turns. Codex will inspect and apply the patch and run the tests; do not claim implementation or tests were executed.
'@
}
if ($Task -eq 'commercial') {
    $astroResultPrefix = 'CLAUDE_COMMERCIAL_REVIEW'
    $astroMaxTurns = 18
    $astroReviewPrompt = @'
Review ASTRO Cyber jointly with Codex as a product intended for commercial cybersecurity services. Read docs/agents/COMMERCIAL_READINESS.md, PRODUCT_PLAN_INTEGRATION.md and EXPERIENCE_UI.md, then inspect relevant backend and UI. READ ONLY: no code/file edits, commands, scanners, browser launches, dependency changes, credentials, commits or pushes. Challenge the proposed customer journey, service-vs-SaaS positioning, accessibility/light-dark/mobile assumptions, settings, security/operations/retention, and launch gates. Do not treat proposed functions as implemented. Focus on blocking P0 issues, overlooked client pain and contradictions. Return prioritized backend tasks with exclusive file ownership, acceptance tests, dependencies and a credible smallest assisted-pilot scope. Distinguish code-confirmed findings, product hypotheses and items needing browser/customer/legal review. No claims of completed tests or compliance. Batch reading and finish within 18 turns; Codex owns product document/UI/integration and will review your proposals.
'@
}
if ($Task -eq 'experience') {
    $astroResultPrefix = 'CLAUDE_EXPERIENCE_REVIEW'
    $astroMaxTurns = 16
    $astroReviewPrompt = @'
Work jointly with Codex to review the IMPLEMENTED role-specific ASTRO Cyber UI. Read docs/agents/EXPERIENCE_UI.md, static/astro-experience.js, static/astro-workspace.js, static/astro-workspace.css, index.html, tests/test_experience.cjs and tests/test_workspace_boot.cjs. Verify executive vs operator navigation, capabilities preserved on backend, demo provenance, failed scopes fetch distinct from zero, truthful metrics, XSS escaping, links/report eligibility, async navigation and responsive CSS. READ ONLY; do not edit files, execute commands, launch browser/scans, read secrets, install dependencies or commit/push. Return concrete issues with file/line/severity, distinguish confirmed bugs from concerns needing browser verification, and do not claim visual tests. Codex owns these files and will integrate accepted findings. Batch reads and deliver final review within 16 turns.
'@
}
if ($Task -eq 'product-plan') {
    $astroResultPrefix = 'CLAUDE_PRODUCT_PLAN'
    $astroTools = 'Read,Glob,Grep,Write'
    $astroAllowedTools += 'Write(docs/agents/CLAUDE_PRODUCT_PLAN_REVIEW.md)'
    $astroMaxTurns = 20
    $astroReviewPrompt = @'
Work jointly with Codex on ASTRO Cyber task PLAN-CLAUDE-01. Read docs/agents/PRODUCT_PLAN.md, ARCHITECTURE.md and CLAUDE_REVIEW_INTEGRATION.md, then inspect relevant existing backend code. Codex owns research, PRODUCT_PLAN.md, TASKS.md and frontend; do not change those. Your sole writable deliverable is docs/agents/CLAUDE_PRODUCT_PLAN_REVIEW.md. Review the proposed web SaaS + optional local network connector architecture against the real code. Produce: existing-vs-proposed capability matrix; objections and recommendation; minimal tenant/network/connector/job/event/evidence data model; job state machine and API contracts; security requirements for enrollment, outbound HTTPS, token revocation, scope enforcement, retries/replay, offline and cancellation; migration sequence preserving existing Flask/SQLite code; prioritized backend tasks with file ownership, dependencies, acceptance criteria and meaningful regression tests. Explain role/capability separation and managed-review visibility. Do not blindly endorse Codex. No code edits, no shell commands, scans, installers, dependency changes, external browsing, secrets, commits or pushes. Write only the specified new Markdown deliverable using Write; then summarize your recommendation in the final response. Do not invent implementation or test results. Keep investigation focused, batch reads, and finish within 20 turns.
'@
}
$astroResumeArguments = @()
$astroExistingResultPath = Join-Path $PSScriptRoot ($astroResultPrefix + '_RESULT.json')
if (Test-Path -LiteralPath $astroExistingResultPath) {
    try {
        $astroExistingResult = Get-Content -LiteralPath $astroExistingResultPath -Raw | ConvertFrom-Json
        if ($astroExistingResult.subtype -eq 'error_max_turns' -and $astroExistingResult.session_id) {
            $astroResumeArguments = @('--resume', [string]$astroExistingResult.session_id)
            $astroReviewPrompt = 'Continue the existing Codex/Claude review. You reached the tool-turn limit after reading the files. Do not use any more tools or re-read files. Return your final review NOW from the context already collected: concrete findings with file/line, severity and suggested correction, or no findings. Clearly identify unverified concerns and review limitations. Do not modify files or claim tests were run.'
            if ($Task -eq 'product-plan') { $astroReviewPrompt = 'Conclude PLAN-CLAUDE-01 now from context already gathered. Do not read more files. Write only docs/agents/CLAUDE_PRODUCT_PLAN_REVIEW.md with your architectural recommendation, backend contracts, objections, task ownership and acceptance gates. Then return a final summary. Do not edit code or claim tests or implementation.' }
            Write-Host 'Retomando a sessao anterior para concluir o parecer, sem reler arquivos.' -ForegroundColor Cyan
        }
    } catch { Write-Host 'Resultado anterior nao pode ser lido; iniciando nova revisao.' }
}
Push-Location $astroRepository
try {
    $astroReviewResultPath = Join-Path $PSScriptRoot ($astroResultPrefix + '_RESULT.json')
    $astroReviewLogPath = Join-Path $PSScriptRoot ($astroResultPrefix + '_STREAM.jsonl')
    $astroReviewFinalResult = $null
    if ($astroResumeArguments.Count -eq 0) { Set-Content -LiteralPath $astroReviewLogPath -Value '' -Encoding UTF8 }
    Write-Host 'Iniciando revisao com Claude Code...' -ForegroundColor Cyan
    Write-Host "Projeto: $astroRepository"
    Write-Host 'Aguardando conexao e resposta. Ctrl+C interrompe esta execucao.'
    Write-Host "Log incremental: $astroReviewLogPath"
    & $astroClaudeExecutable @astroResumeArguments -p $astroReviewPrompt --safe-mode --strict-mcp-config --tools $astroTools --allowedTools $astroAllowedTools --permission-prompts none --max-turns $astroMaxTurns --verbose --output-format stream-json | ForEach-Object {
        $astroReviewLine = [string]$_
        Add-Content -LiteralPath $astroReviewLogPath -Value $astroReviewLine -Encoding UTF8
        try { $astroReviewEvent = $astroReviewLine | ConvertFrom-Json } catch { Write-Host $astroReviewLine; return }
        if ($astroReviewEvent.type -eq 'system' -and $astroReviewEvent.subtype -eq 'init') {
            Write-Host 'Sessao iniciada; aguardando resposta da API.' -ForegroundColor Cyan
        }
        if ($astroReviewEvent.type -eq 'assistant') {
            foreach ($astroReviewBlock in $astroReviewEvent.message.content) {
                if ($astroReviewBlock.type -eq 'text') { Write-Host $astroReviewBlock.text }
                if ($astroReviewBlock.type -eq 'tool_use') { Write-Host ("Revisando: " + $astroReviewBlock.name + ' ' + $astroReviewBlock.input.file_path) -ForegroundColor DarkCyan }
            }
        }
        if ($astroReviewEvent.type -eq 'result') {
            $astroReviewFinalResult = $astroReviewEvent
            $astroReviewEvent | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath $astroReviewResultPath -Encoding UTF8
            Write-Host $astroReviewEvent.result
        }
    }
    $astroReviewExitCode = $LASTEXITCODE
    Write-Host "Claude exit code: $astroReviewExitCode"
    if ($null -eq $astroReviewFinalResult) { throw "Claude terminou sem resultado. Consulte $astroReviewLogPath" }
    Write-Host "Review result: $astroReviewResultPath"
    if ($astroReviewExitCode -ne 0 -or $astroReviewFinalResult.is_error) { throw 'Claude review failed; inspect the recorded result.' }
} finally {
    Pop-Location
}
