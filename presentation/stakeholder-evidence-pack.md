# Stakeholder Evidence Pack

## 1) Deployment Proof
- Primary app URL: `<add-streamlit-cloud-url>`
- Backup run method: `docker compose up --build`
- Build date: `<yyyy-mm-dd>`

## 2) Technical Proof Points
- App entrypoint: `app.py`
- Monte Carlo simulation: `src/simulation/monte_carlo.py`
- Delay drivers + scenarios: `src/analytics/`
- Advisory ML scoring: `src/ml/`
- Persistence and history: `src/storage/`

## 3) Reliability Evidence
- Smoke test command:
  - `python scripts/smoke_test.py`
- CI workflow:
  - `.github/workflows/ci.yml`
- Mock-mode fallback:
  - default with `DEMO_DEFAULT_MODE=mock`

## 4) Model Governance Snapshot
- Training script: `scripts/train_risk_model.py`
- Model artifact: `models/risk_classifier.joblib`
- Metadata: `models/risk_model_metrics.json`
- Version field: `RISK_MODEL_VERSION`
- Positioning: advisory signal, not sole decision engine

## 5) Demonstration Evidence
- Script: `presentation/demo-script.md`
- Deck: `presentation/stakeholder-deck.md`
- Q&A playbook: `presentation/post-presentation-qa-playbook.md`
- Backup flow: `presentation/backup-demo.md`

## 6) Known Limitations (Transparent)
- LLM quality depends on input prompt quality.
- Advisory classifier performance is moderate and should be interpreted with simulation metrics.
- No multi-user auth or enterprise RBAC in current release.
