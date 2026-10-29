# Security policy

This project should never commit secrets, OAuth tokens, API keys, real user uploads, downloaded media, or generated output media.

## Required security practices
- Store credentials only in `.env` or a secret manager.
- Use environment variables; never hardcode tokens.
- Redact secrets in logs and alerts.
- Keep Cloudflare, Kaggle, Google, email, and YouTube credentials out of Git.

## Reporting a security issue
Please open a private issue or contact the maintainer privately.
