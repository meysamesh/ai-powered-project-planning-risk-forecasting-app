# Release Checklist (Demo-Production)

## 1) Code and Test Gate
- [ ] `python -m compileall -q src app.py scripts tests`
- [ ] `python -m pytest -q`
- [ ] `python scripts/smoke_test.py`
- [ ] CI pipeline is green on main branch

## 2) Model and Data Gate
- [ ] Model artifact exists at `models/risk_classifier.joblib`
- [ ] Metrics metadata exists at `models/risk_model_metrics.json`
- [ ] `RISK_MODEL_VERSION` is set and matches release notes
- [ ] ML tab shows advisory disclaimer and non-blocking fallback behavior

## 3) App and UX Gate
- [ ] `mock` mode runs end-to-end with no external dependencies
- [ ] `real` mode verified once with valid `GROQ_API_KEY`
- [ ] History load and export tested (CSV/JSON + ML payloads)
- [ ] Scenario recommendation and key KPIs render correctly

## 4) Deployment Gate
- [ ] Streamlit Cloud deployment URL verified
- [ ] Secrets configured in platform (no secrets in repository)
- [ ] Backup Docker run succeeds (`docker compose up --build`)
- [ ] Health endpoint responds (`/_stcore/health`)

## 5) Demo Readiness Gate
- [ ] `presentation/demo-script.md` rehearsal completed twice
- [ ] Backup demo path reviewed (`presentation/backup-demo.md`)
- [ ] Stakeholder evidence pack updated
- [ ] Known limitations explicitly stated in deck/Q&A

## 6) Release Management
- [ ] Git tag created (`vX.Y.Z`)
- [ ] Changelog/release summary published
- [ ] Rollback note documented (previous stable tag + image/build)
