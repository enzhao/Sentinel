# Gemini Guidelines for Sentinel Project

## How to run backend tests:

```bash
backend/venv/bin/pytest --cov=src backend/tests/
```

## How to do a release:

```bash
npm run release -- --release-as minor  # can also be major or patch
``` 
Then,

```bash
git push --follow-tags origin main
```
