# Capstone Workflow (2 People, 4 Weeks)

## 1) Project Goal
Build a presentation-ready AI app that turns project descriptions into:
- validated task plans,
- probabilistic schedule forecasts,
- scenario-based decision support.

## 2) Scope Discipline (Only Required Topics)
This capstone intentionally uses only topics needed for this product:
- Python, Pandas, NumPy
- Data cleaning and validation (Pydantic schema + checks)
- AI architecture basics (input -> LLM -> validation -> simulation -> UI)
- Applied LLM prompt engineering (task generation)
- Risk forecasting analytics (Monte Carlo + percentiles + delay probability)
- Advisory ML scoring (task-level classifier inference)
- Data visualization (Plotly, Streamlit)
- SQL basics through SQLite persistence
- Docker (reproducible local run)
- CI/CD (GitHub Actions for smoke + tests)
- PM practices: stakeholder framing, OKRs/KPIs, roadmap, prioritization, DoR/DoD

Out of scope for this capstone (not required for this use case right now):
- Advanced model tuning and enterprise-grade MLOps rollout
- RAG/agents/MCP integration
- GCP deployment
- A/B testing in production

## 3) Team Roles
Person A (Product + Story + UX):
- owns stakeholder narrative and demo flow,
- owns presentation deck quality,
- owns feature prioritization and user-facing clarity.

Person B (Engineering + Analytics):
- owns simulation and analytics correctness,
- owns data/persistence reliability,
- owns CI, testing, and release stability.

Shared ownership:
- architecture decisions,
- final QA and rehearsal,
- final submission package.

## 4) 4-Week Plan
### Week 1 - Discovery + Foundation
- Finalize problem statement and success criteria.
- Define MVP scope and non-goals.
- Implement task schema validation + mock generation path.
- Set up baseline Streamlit shell and repository structure.

Exit criteria:
- app runs locally,
- mock flow works end-to-end,
- initial architecture diagram drafted.

### Week 2 - Core Engine
- Implement DAG builder + critical path logic.
- Implement Monte Carlo simulation and forecast metrics (mean, P50, P80, delay probability).
- Add delay-driver ranking and first charts.
- Add notebook walkthrough for technical explanation.

Exit criteria:
- deterministic seeded simulation works,
- metrics and plots are reproducible,
- technical notebook is demoable.

### Week 3 - Productization
- Add scenario lab and recommendation logic.
- Add SQLite history + export (CSV/JSON).
- Add tests (schema, graph, simulation, analytics, integration).
- Add Docker + smoke test script.

Exit criteria:
- app supports full demo storyline,
- history/reload/export working,
- smoke test stable.

### Week 4 - Presentation + Hardening
- Add CI workflow on push/PR.
- Finalize stakeholder deck + demo script + backup path.
- Rehearse live demo and Q&A.
- Freeze release candidate and submission artifacts.

Exit criteria:
- CI passing,
- demo under 7 minutes,
- both teammates can run the full demo.

## 5) Delivery Cadence
- Daily 15-minute sync (blockers + priorities).
- Twice-weekly review (feature demo + decisions).
- End-of-week checkpoint against exit criteria.

## 6) Backlog Prioritization Rule
Use this order:
1. Demo reliability blockers
2. Forecast correctness
3. Stakeholder clarity in UI/output
4. Nice-to-have enhancements

## 7) Definition of Ready (DoR)
A backlog item is ready only if:
- business value is stated in one sentence,
- acceptance criteria are testable,
- dependencies are known,
- owner is assigned (A, B, or both),
- demo impact is clear.

## 8) Definition of Done (DoD)
A feature is done only if:
- implemented and runnable locally,
- covered by smoke path (and unit tests where relevant),
- no breaking regressions in core demo tabs,
- docs updated (README/notebook/deck if impacted),
- reviewed by the other teammate.

## 9) KPI Targets for Capstone
- `Demo reliability`: 0 blockers in mock mode.
- `Runtime`: one simulation run completes in practical classroom time.
- `Explainability`: speaker can justify P80, delay probability, and top delay drivers.
- `Readiness`: app + notebook + presentation assets all present in repo.

## 10) Final Submission Checklist
- Streamlit app runs from `app.py`.
- Clean notebook walkthrough is present.
- Stakeholder deck and demo scripts are present.
- CI workflow exists and runs tests.
- Docker run works for reproducibility.
- Backup demo path exists for API outage/latency.
