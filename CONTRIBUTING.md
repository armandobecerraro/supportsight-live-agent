# Contributing to SupportSight Live

## Branching
- `main` — production-ready, tagged releases
- `develop` — integration branch
- `feature/<name>` — feature branches

## Commit convention
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests only
- `chore:` build/infra

## Testing
Run all tests before opening a PR:
```bash
# Python
pytest backend-orchestrator/tests/

# Rust
cargo test --manifest-path logs-service/Cargo.toml

# Java
cd actions-service && mvn test

# Frontend
cd frontend && npm run type-check
```

## Security
- Never commit API keys, secrets, or `.env` files
- All destructive actions must require confirmation
- Input validation required on every API endpoint
