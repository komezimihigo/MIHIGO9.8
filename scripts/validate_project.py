from pathlib import Path
required=['orchestrator/app.py','media/processor.py','workers/pipeline.py','rights/policy.py','publishing/metadata.py','tests/test_core.py']
missing=[p for p in required if not Path(p).is_file()]
if missing: raise SystemExit('Missing required files: '+', '.join(missing))
print('Project structure valid.')
