# ProjectSense AI - PowerPoint Ready Deck (12 Slides)

Use this file to build the final `.pptx` quickly.  
One slide = one section below.

## Slide 1 - Title
AI-Powered Project Planning & Risk Forecasting  
Capstone Project | 4 Weeks | 2 Teammates

Subtitle:
From deterministic planning to probability-based decision support.

## Slide 2 - Problem
- Teams commit to single-date plans without uncertainty modeling.
- Delays appear late, when mitigation is expensive.
- Stakeholders need risk-aware commitments, not only task lists.

## Slide 3 - Solution
ProjectSense AI:
- Generates a structured task plan from plain-language project input.
- Validates dependencies and durations.
- Simulates timeline risk with Monte Carlo.
- Recommends safer execution scenarios.

## Slide 4 - Architecture (Only What Is Needed)
Flow:
1. User project description
2. LLM task generation (or mock fallback)
3. Schema validation (Pydantic)
4. DAG + critical path
5. Monte Carlo simulation
6. Metrics + scenarios + exports

Tech:
- Streamlit, Groq, Pydantic, NetworkX, NumPy/Pandas, Plotly, SQLite

## Slide 5 - Live App Walkthrough
Show the 6 tabs:
- Executive Brief
- Task Plan
- Workflow
- Risk Dashboard
- Scenario Lab
- History & Export

## Slide 6 - Forecast Metrics
Explain:
- Mean completion time
- P50 (median outcome)
- P80 (recommended commitment date)
- Delay probability against selected deadline

Decision message:
Use P80 for realistic commitments under uncertainty.

## Slide 7 - Risk Drivers
- Critical-path frequency ranking identifies bottleneck tasks.
- Prioritize mitigation on top-ranked drivers first.
- Result: higher schedule reliability with targeted effort.

## Slide 8 - Scenario Decision Support
Three scenarios:
- Baseline
- Aggressive deadline (-15%)
- Increased capacity (+15% faster)

Explain how recommendation is selected:
lowest delay probability.

## Slide 9 - Product & Engineering Quality
- Input validation and graph checks
- Session persistence with SQLite
- Exportable CSV/JSON outputs
- Smoke test + unit test suite
- CI pipeline via GitHub Actions
- Dockerized local reproducibility

## Slide 10 - Team Workflow (4 Weeks)
- Week 1: scope + architecture + base app
- Week 2: analytics engine + notebook
- Week 3: scenarios + persistence + test hardening
- Week 4: CI + rehearsal + final packaging

Include DoR/DoD and ownership split between both teammates.

## Slide 11 - Responsible AI (Right-Sized for Scope)
- No personal data required for this demo.
- User input transparency: generated plan is editable and reviewable.
- Risk note: LLM outputs can be imperfect; schema validation and manual review are required.

Why included:
shows practical AI governance without over-scoping the project.

## Slide 12 - Results, Limits, Next Steps
Results:
- Faster planning cycle
- Earlier risk visibility
- Better commitment quality

Current limits:
- Single-project scope
- No multi-user auth/integrations

Next steps:
- Portfolio view
- Jira/Asana connectors
- Optional cloud deployment
