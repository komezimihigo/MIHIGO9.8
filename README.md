# MIHIGO 9.8 — integrated video factory foundation

This release connects a local Flask dashboard, persistent SQLite jobs, FFmpeg processing, rights declarations, metadata generation, and optional B2 storage / YouTube adapters. It is a functional foundation, **not yet a fully autonomous always-on service**: automatic source discovery, AI highlight scoring, caption generation, memes/effects intelligence, OAuth onboarding, scheduled multi-channel publishing, and hosted deployment still require implementation/configuration.

## Run locally or on a suitable Python host

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m orchestrator.app
```
Open `http://127.0.0.1:5000`. Upload a video you own or have permission to use. FFmpeg and FFprobe must be installed and on PATH. Processed files live in `media/outputs`; jobs persist in `data/mihigo.sqlite3`.

## Kaggle

Kaggle can run batch processing while a notebook session is active; it is not an always-on worker. Install requirements and FFmpeg in the notebook, clone/upload this repository, and use the processing functions. For persistence between sessions, configure B2 credentials through Kaggle Secrets (never paste them into source code).

## Optional B2

Install `boto3`, then set `B2_KEY_ID`, `B2_APPLICATION_KEY`, `B2_ENDPOINT`, `B2_REGION`, and `B2_BUCKET_NAME` as environment variables/secrets. `storage.b2.upload_file` provides an upload adapter; current web pipeline stores local outputs by default.

## YouTube

Publishing defaults to disabled. YouTube upload requires a Google Cloud project, enabled YouTube Data API, OAuth user consent/token, and review of generated metadata. Keep uploads private during initial setup. Do not enable publishing until credentials and channel selection are configured.

## Rights

The app requires an explicit rights confirmation. This records your declaration; it does not independently verify copyright or licensing. Publicly viewable content is not automatically reusable. Only process content you own or have permission to use.

## Checks

```bash
python -m compileall .
python -m pytest -q
python scripts/validate_project.py
```

## Deployment note

The Flask dashboard is intended for a suitable host. Free Python hosting and Kaggle sessions have storage, CPU, and uptime limits; continuous autonomous discovery/rendering/publishing cannot be guaranteed on those free tiers alone.
