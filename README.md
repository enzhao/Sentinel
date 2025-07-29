# Sentinel Invest 

![Status](https://img.shields.io/badge/status-Work%20In%20Progress-orange) ![Coverage](https://img.shields.io/badge/coverage-78%25-green)

An automated, strategy-driven tool to help long-term investors make disciplined, data-driven decisions without the need for constant market-watching.

## Core Philosophy

Sentinel is designed to be a **behavioral guardrail**. It helps investors stick to their own long-term strategy by filtering out short-term market noise and providing timely, actionable alerts based on pre-defined, data-driven rules. The core methodology is a hybrid **"Core-Satellite"** model, combining systematic accumulation with opportunistic, tax-aware rebalancing.

For a full breakdown of the project's vision, features, and architecture, please see the `product_spec.md`.

---

## Project Structure

```bash
.
├── .github/              # CI/CD workflows
├── .husky/               # Git hooks for commit message linting
├── api/                  # OpenAPI specifications
├── backend/
│   ├── src/              # Python FastAPI backend source
│   │   ├── routers/      # API endpoint definitions
│   │   ├── services/     # Business logic services
│   │   ├── models.py     # Pydantic data models
│   │   ├── middleware.py # Custom middleware
│   │   ├── dependencies.py # Shared dependencies
│   │   └── main.py       # FastAPI app entrypoint
│   ├── tests/              # Unit and integration tests
│   ├── .python-version   # pyenv version file
│   ├── Dockerfile        # Production container definition
│   ├── pytest.ini        # Pytest configuration
│   ├── requirements.in   # Production dependencies
│   └── requirements-dev.in # Development/test dependencies
├── docs/                 # Project documentation
├── frontend/             # Vue.js frontend source
├── util/                 # Standalone utility scripts (e.g., live API tests)
├── .dockerignore         # Files to exclude from Docker builds
├── .gitignore
├── CHANGELOG.md
├── commitlint.config.js
├── package.json          # Root-level dev dependencies and scripts
├── product_spec.md       # The single source of truth for project requirements
├── run_local_backend.sh  # Local development setup script
└── README.md
``` 

---

## Getting Started

### 1. Cloud & Project Setup

Before running the application locally, you must set up the required Google Cloud and Firebase services. Follow the step-by-step guide here:

➡️ **[./docs/google_cloud_setup.md](./docs/google_cloud_setup.md)**

### 2. Local Development

After completing the cloud setup, follow these steps to run the application on your local machine.

#### Backend Setup
The backend setup is managed by a single script that automates the creation of a virtual environment, installation of dependencies, and setting of environment variables.

1.  **Prerequisites:**
    - Ensure you have `pyenv` installed to manage Python versions.
    - **Install pip-tools:** This is a one-time setup for your system.
      ```bash
      pip install pip-tools
      ```
    - Place your `serviceAccountKey.json` file in the `/backend` directory.
    - Create and configure your `backend/.env` file by copying the example:
      ```bash
      cp backend/.env.example backend/.env
      ```
      Then, add your Alpha Vantage API key to the new `.env` file.

2.  **Run the Backend Build Script:**
    From the project root, make the script executable and run it:
    ```bash
    chmod +x run_local_backend.sh
    ./run_local_backend.sh
    ```
    The script is the Makefile for the backend. It will run tests for backend, build a docker image and run a container.  

3.  **Run the Backend Server without Docker:**
    After the setup is complete, you can run the server at any time:
    ```bash
    # Make sure your virtual environment is activated
    source backend/venv/bin/activate
    uvicorn src.main:app --reload
    ```
    ✅ The backend API should now be running at `http://127.0.0.1:8000`.

##### Testing External Services
The project includes utility scripts to perform live tests against external services. These are not part of the main test suite and should be run manually for validation.

- **Live API Test (`live_api_test.py`):**
  This script quickly fetches all required data points from Alpha Vantage to verify that your API key is working and that the service is accessible.
  ```bash
  # Run from the project root
  backend/venv/bin/python util/live_api_test.py
  ```

- **End-to-End Pipeline Test (`e2e_data_pipeline_test.py`):**
  This script performs a full data pipeline test: it fetches real data from Alpha Vantage, writes it to your **live** Firestore database, reads it back, verifies it, and then deletes the test data. It is the ultimate confirmation that the entire data flow is working.
  ```bash
  # Run from the project root
  backend/venv/bin/python util/e2e_data_pipeline_test.py
  ```

##### Managing Backend Dependencies

- To add or remove a package, edit the `requirements.in` file.
- After editing, run `pip-compile requirements.in` to update `requirements.txt`.
- Then, run `pip-sync` to update your local virtual environment.

#### Frontend Setup
1.  Open a **new terminal** and navigate to the frontend directory: `cd frontend`
2.  Install dependencies: `npm install`
3.  Run the frontend server: `npm run dev`
    ✅ The frontend application should now be running at `http://localhost:5173`.

### 3. Local Docker Test (Optional)

To test the production container locally, run the following commands from the project root:

1.  **Build the image:**
    ```bash
    docker build -t sentinel-backend ./backend
    ```
2.  **Run the container:**

    ```bash
    docker run --rm -p 8000:8000 -e ENV=local -v $(pwd)/backend/serviceAccountKey.json:/app/serviceAccountKey.json sentinel-backend
    ```

---

## Deployment

The application is deployed automatically via the GitHub Actions workflow in `.github/workflows/deploy.yml` on every push to the `main` branch.

-   The **backend** is containerized and deployed to **Google Cloud Run**.
-   The **frontend** is built and deployed to **Firebase Hosting**.

### Live URLs

-   **Frontend:** [https://sentinel-invest.web.app](https://sentinel-invest.web.app)
-   **Backend API:** The URL is dynamic. Check the output of the `deploy-backend` job in the latest GitHub Actions run.

---

## Development Workflow

This project uses a standardized workflow to ensure a clean, understandable, and automated version history.

### Commit Messages

All commit messages must follow the [**Conventional Commits**](https://www.conventionalcommits.org/) specification. This is enforced automatically by a `commit-msg` hook.

The basic format is:
`<type>(<scope>): <subject>`

**Common Types:**
-   `feat`: A new feature (e.g., `feat(auth): add login page`)
-   `fix`: A bug fix (e.g., `fix(api): correct portfolio calculation`)
-   `docs`: Changes to documentation only (e.g., `docs(readme): update setup instructions`)
-   `style`: Code style changes (formatting, etc.)
-   `refactor`: A code change that neither fixes a bug nor adds a feature.
-   `test`: Adding or correcting tests.
-   `chore`: Changes to the build process or auxiliary tools (e.g., `chore(deps): update fastapi`)

### Creating a Release

Creating a new version, generating a changelog, and tagging the release is an automated process.

1.  Ensure you are on the `main` branch and have pulled the latest changes.
2.  Run the release script from the project root:
    ```bash
    npm run release
    ```
    This command will analyze your commits since the last tag, determine the correct new version number (e.g., v0.1.0 -> v0.2.0 if there are new `feat` commits), update the `CHANGELOG.md` file, and create a new Git tag.

    **Specifying a Release Type:**
    To override the automatic versioning, you can specify the release type. For example, to force a minor release (e.g., `v0.0.1` -> `v0.1.0`), run:
    ```bash
    npm run release -- --release-as minor
    ```
    Other options include `major`, `minor`, or `patch`.

3.  Push the new commit and the tag to GitHub:

    ```bash
    git push --follow-tags origin main
    ```