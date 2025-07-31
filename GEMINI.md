# Gemini Guidelines for Sentinel Project

This project follows a spec-driven engineering approach. The single source of truth for what to build is `product_spec.md`.

When asked to perform a task, please follow these steps:

1.  **Consult the Spec:** Before writing any code, always read and understand the relevant sections of `product_spec.md`. This document is the ultimate prompt and defines the desired functionality.
2.  **Iterative Development:** The `product_spec.md` is a living, evolving document. The product is also built iteratively based on the spec.
3. **Consult the README.md:** For any questions about the project setup, development environment, or running the application, refer to `README.md`. This file contains essential information about the project structure and how to get started.
4.  **Clarification:** If the user's request is ambiguous or contradicts the spec, please ask for clarification.


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


## Instruction for committing code:

commit the changes I have staged, using commitlint-conform message. Link this commit to ticket #4, but do not close this ticket. 