# Gemini Guidelines for Sentinel Project

## How to run backend tests:

```bash
venv/bin/pytest --cov=src backend/tests/
```

## How to do a release:

```bash
npm run release -- --release-as minor  # can also be major or patch
``` 
then,

```bash
git push --follow-tags origin main
```
