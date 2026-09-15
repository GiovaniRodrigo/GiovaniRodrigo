# Spec: GitHub Profile README Revamp (`GiovaniRodrigo/GiovaniRodrigo`)

> Status: **ready-for-agent** (pending publish to issue tracker)
> Repo: `GiovaniRodrigo/GiovaniRodrigo` (the special profile repo — its README renders on the GitHub profile page)

## Problem Statement

Giovani's current profile README undersells him and, worse, is partly **fabricated**: it
advertises four "featured projects" (`token-tracker-electron`, `intelliai-imoveis`,
`brinquefeliz-webloja`) that **do not exist** on his account, claims a U-Net thesis he does
not have, and lists a tech stack (Angular, Kubernetes, MongoDB, FastAPI) with **no
supporting repository**. As a visitor (recruiter, collaborator, peer), the profile is
visually flat and, on inspection, not trustworthy.

Giovani wants a profile that (a) looks modern and technical — a "terminal/DevOps" aesthetic
with animated and generated visuals — and (b) reflects **only real work**, drawn from his 17
genuine repositories, ranked by complexity, with descriptions taken from the repos' own
READMEs.

## Solution

Rebuild the profile README around a neutral-dark theme (`#0d1117`) with a tech-neon accent
system, composed of hosted widgets (typing banner, skillicons, shields badges, komarev views
counter) **and** self-generated SVG assets (an animated `profile.sh --live` terminal banner,
two radar charts, a self-hosted stats card, and a language-metrics SVG). All content is real:
17 verified repositories, descriptions extracted from each repo's README, a language radar
built from real GitHub language data (de-noised of vendored dependencies), and a self-rated
skill radar the owner controls via a JSON file. Generated assets are kept fresh by a GitHub
Actions workflow that regenerates and commits them on a daily cron and on push to `main`.

## User Stories

1. As a recruiter, I want to see Giovani's real role and location at a glance, so that I can quickly assess fit.
2. As a recruiter, I want every listed project to actually exist and link to real code, so that I can trust the profile.
3. As a visitor, I want an animated terminal banner (`profile.sh --live`), so that the profile feels alive and on-brand for DevOps.
4. As a visitor, I want an animated typing tagline, so that I immediately understand what Giovani does.
5. As a visitor on a light-themed client, I want the banner and charts to render legibly, so that nothing looks broken.
6. As a visitor on a dark-themed client, I want the same, so that the neutral-dark aesthetic is intentional, not accidental.
7. As a hiring manager, I want projects ordered by complexity, so that I see his strongest work first.
8. As a hiring manager, I want the most complex projects visually emphasized (highest-contrast neon), so that emphasis matches substance.
9. As a visitor, I want concise, accurate descriptions per project (from the repo's own README), so that I understand each project without clicking through.
10. As a visitor, I want the full set of real projects (17), with the top ones as cards and the rest in a compact table, so that the page is complete but not an endless scroll.
11. As a peer developer, I want a language radar built from real repo data, so that the strengths shown are evidence-based.
12. As Giovani, I want a self-rated skill radar I can edit in one JSON file, so that I control my own self-assessment.
13. As a visitor, I want a tech-stack row (skillicons) limited to languages/tools Giovani actually uses, so that the stack is honest.
14. As a visitor, I want social links (LinkedIn, GitHub, email) as badges, so that I can reach out through my preferred channel.
15. As Giovani, I want a profile-views counter (komarev/ghpvc), so that I can see interest in my profile over time.
16. As Giovani, I want the generated stats/metrics to refresh automatically, so that the profile stays current without manual work.
17. As Giovani, I want the generators written in Python with editable data files, so that I can tweak content without reverse-engineering code.
18. As Giovani, I want the workflow to commit regenerated assets, so that the rendered README always points at current SVGs.
19. As Giovani, I want the metrics/stats generation to use a token I provide as a secret, so that no credential is hardcoded.
20. As a maintainer, I want the generators to be testable without hitting the network, so that CI is deterministic and fast.
21. As a maintainer, I want each generator to fail loudly on malformed input data, so that a bad edit to a JSON file doesn't silently ship a broken SVG.
22. As a visitor, I want horizontal content (tables, wide charts) to not break the page layout on mobile, so that the profile reads well on a phone.

## Implementation Decisions

### Content (verified against real data)
- **Identity:** DevOps & Full-Stack Engineer; São Paulo, Brazil (owner-confirmed).
- **Removed as fabricated:** the four old "featured projects", the U-Net thesis, and unsupported stack items (Angular, Kubernetes, MongoDB, FastAPI).
- **Stack (evidence-based):** Python, TypeScript, JavaScript, PHP, Go, Vue, C, Shell, HTML/CSS, Docker, Kafka, Azure — sourced from real repo languages.
- **Projects:** 17 real repos, ranked by complexity. Forks (`ai-job-search`, `ai-memory`), the profile repo itself, and empty/junk repos (`test`, `shorter_url`, `web_scraping`, `vegetation-mapping`) are excluded. Top 6 render as neon-accented cards; the remaining 11 render in a compact table. Descriptions are extracted from each repo's own README (not authored fresh, not fabricated).

### Theme / accent
- Base: GitHub neutral dark `#0d1117` + greys.
- Neon accent by project complexity (highest→lowest contrast): cyan `#00E5FF` → green `#39FF14` → amber `#FFB000` → teal `#2DD4BF`. Top-2 projects cyan; #3–4 green; #5–6 amber; remainder teal/grey.

### Hosted widgets (no build)
- komarev `ghpvc` profile-views counter (antonkomarev/github-profile-views-counter).
- `readme-typing-svg` animated tagline (3 approved lines).
- `skillicons.dev` stack row (real stack only).
- `shields.io` social badges: LinkedIn, GitHub, email.

### Generated assets (self-hosted, Python)
- `assets/banner-{dark,light}.svg` — animated `profile.sh --live` terminal banner; referenced via `<picture>` with `prefers-color-scheme`.
- `assets/radar-{dark,light}.svg` — self-rated **skill** radar, data from `assets/skills.json`.
- `assets/radar-langs-{dark,light}.svg` — **language** radar, data from `assets/langmix.json`.
- `assets/card-stats-{dark,light}.svg` — self-hosted stats card.
- `assets/metrics.languages.svg` — via `lowlighter/metrics` action.

### Radar data
- **Language radar (`langmix.json`)** — evidence-based, de-noised of vendored deps (the 53 MB Python venv in `efficiency-algorithm-blind-index` is excluded): `Python 90 · TypeScript 85 · JavaScript 75 · PHP 55 · Go 40 · Shell 45`.
- **Skill radar (`skills.json`)** — owner self-rated. Default values (Q16 defaulted to recommended option (a); owner may edit): `DevOps & Automation 85 · Backend 80 · Frontend 60 · AI/Agents 80 · Testing & QA 70 · Architecture 75`.

### Module boundaries (generators)
- Each generator separates **three concerns**: (1) *fetch* (thin adapter over the GitHub API for stats/languages), (2) *render* (pure function `render(data: dict, theme: str) -> str` returning SVG markup), (3) *write* (SVG string → file, with cache-bust versioning where the reference uses `?v=N`).
- Data files (`skills.json`, `langmix.json`) are the sole input for the radar renderers; renderers do no network I/O.

### Pipeline
- `.github/workflows/` regenerates assets on **daily cron + push to `main`**, then commits changed SVGs.
- Third-party action `lowlighter/metrics` is added.
- A **PAT secret `METRICS_TOKEN`** is required for the stats card and metrics; **created by the owner** (not by the agent). Actions must be enabled by the owner.

## Testing Decisions

- **What a good test asserts here:** externally observable output of the **render seam** — given fixed input data + theme, the returned SVG is well-formed XML, contains the expected labels/values (e.g. each radar axis name and its plotted value), and produces both a dark and a light variant. Tests assert *properties of the output*, not internal drawing calls.
- **Primary seam (single, highest):** the pure `render(data, theme) -> svg` function of each generator. This is preferred over testing files or the network because it isolates all real logic behind one in-memory boundary. Fixtures are small JSON dicts mirroring `skills.json` / `langmix.json` and a stubbed stats payload.
- **Fetch adapter:** kept thin and covered by at most one contract test (or excluded from unit tests entirely); it must not be exercised by the render tests, so CI stays offline and deterministic.
- **Failure tests:** malformed/empty data (missing axis, non-numeric value, empty dict) must raise, not emit a broken SVG (user story 21).
- **Modules tested:** the three renderers (banner, skill radar, language radar) and the stats-card renderer. The workflow YAML and the hosted widgets are **not** unit-tested.
- **Prior art:** none in this repo yet (it currently contains only `README.md`); these are the first tests. Establish a minimal Python test layout (`tests/`, `pytest`).

## Out of Scope

- Creating the `METRICS_TOKEN` PAT or enabling GitHub Actions (owner actions).
- Authoring new marketing copy for projects — descriptions come from existing repo READMEs only.
- Cleaning up the source repositories themselves (e.g. removing the vendored venv from `efficiency-algorithm-blind-index`) — only the *aggregation* de-noises it.
- Any change outside the `GiovaniRodrigo/GiovaniRodrigo` profile repo.
- Publishing this spec to the issue tracker with a triage label (blocked: tracker/label vocabulary not configured this session).

## Further Notes

- The profile repo currently contains only `README.md`; this spec introduces `assets/`, `scripts/`, `tests/`, `.github/workflows/`, and the two data JSON files.
- The komarev counter and a LinkedIn badge were already added to `README.md` in an earlier step; the revamp supersedes/absorbs them.
- Wide elements (project table, radars) must live in layouts that don't force horizontal page scroll on mobile (user story 22).
- Open owner decision at spec time: final skill-radar values (Q16) — defaulted to recommended values above, editable in `skills.json`.
