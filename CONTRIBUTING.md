# Contributing

Contributions are welcome! Here's how to get started.

## Development Setup

1. Clone the repository
2. Install Python 3.11+ and create a virtual environment:
   ```bash
   cd app
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install pytest httpx anyio pytest-anyio ruff
   ```

## Making Changes

1. Create a feature branch from `main`
2. Make your changes following the patterns in the codebase
3. Run tests and linting before committing:
   ```bash
   cd app
   ruff check .
   pytest tests/ -v
   ```
4. Ensure Docker builds succeed: `docker build -t demo-api:test app/`
5. Submit a pull request with a clear description

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat(scope): description` — new feature
- `fix(scope): description` — bug fix
- `docs(scope): description` — documentation
- `refactor(scope): description` — code restructuring

Scopes: `app`, `infra`, `helm`, `ci`, `monitoring`, `sre`, `docs`

## Infrastructure Changes

- All Bicep changes are validated automatically on PR via `infra-validate.yml`
- Test with `az bicep build --file infra/main.bicep` locally before pushing
- Use `--what-if` for deployment previews

## Helm Changes

- Validate templates: `helm template demo-api helm/demo-api/`
- Lint the chart: `helm lint helm/demo-api/`
