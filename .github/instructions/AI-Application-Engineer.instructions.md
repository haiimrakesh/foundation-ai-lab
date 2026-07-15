## Implementation Instructions

- Target: Python 3.11+, type-hinted modules, minimal dependencies.
- Secrets: never hardcode keys; provide `.env.example`.
- Packaging: follow user preference (`requirements.txt` or `pyproject.toml`).
- Tests: every scaffold must include fast `pytest` unit tests covering core behavior.
- Docs: include a short README with quick-run commands.

Suggested scaffold layout:

- `scaffold/app/main.py` — minimal FastAPI endpoints.
- `scaffold/core/model.py` — model wrapper (OpenAI + LangChain).
- `scaffold/data/indexer.py` — ingestion + embedding indexer.
- `scaffold/tests/` — pytest suites.

Evals and validation:

- Add `evals/` per agent with templates to validate prompts, I/O contracts, and integration flows.
- Provide `evals/test_agent_evals.py` pytest file that asserts expected behavior for sample inputs.

CrewAI: include local simulation snippets only; avoid live orchestration without approval.
