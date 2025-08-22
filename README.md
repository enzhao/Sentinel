# Sentinel Invest 

![Status](https://img.shields.io/badge/status-Work%20In%20Progress-orange) ![Coverage](https://img.shields.io/badge/coverage-81%25-green)

An automated, strategy-driven tool to help long-term investors make disciplined, data-driven decisions without the need for constant market-watching.

## 1. Core Philosophy

Sentinel is designed to be a **behavioral guardrail**. It helps investors stick to their own long-term strategy by filtering out short-term market noise and providing timely, actionable alerts based on pre-defined, data-driven rules.

For a full breakdown of the project's vision, features, and architecture, please see the `product_spec.md`.

---

## 2. Project Structure

```bash
.
├── .github/              # CI/CD workflows
├── backend/              # Python FastAPI backend
├── docs/                 # Project documentation & specifications
├── frontend/             # Vue.js frontend source
├── util/                 # Standalone utility scripts
├── product_spec.md       # The single source of truth for project requirements
└── README.md
``` 

---

## 3. Getting Started

> **Note for Developers:** For detailed information on testing, commit conventions, the release process, and other development workflows, please see the **[Developer Guide](./docs/developer_guide.md)**.

### 3.1. Cloud & Project Setup

Before running the application locally, you must set up the required Google Cloud and Firebase services. Follow the step-by-step guide here:

➡️ **[./docs/google_cloud_setup.md](./docs/google_cloud_setup.md)**

### 3.2. Local Development

After completing the cloud setup, follow these steps to run the application on your local machine.

#### 3.2.1 Backend Setup

1.  **Prerequisites:**
    * Ensure you have `pyenv` and `pip-tools` installed.
    * Place your `serviceAccountKey.json` file in the `/backend` directory.
    * Create your `backend/.env` file from the example and add your Alpha Vantage API key.
2.  **Run the Build Script:** From the project root, run the setup script:
    ```bash
    chmod +x run_local_backend.sh
    ./run_local_backend.sh
    ```
3.  **Run the Server:** After setup, you can run the server at any time:
    ```bash
    # Make sure your virtual environment is activated
    source backend/venv/bin/activate
    uvicorn src.main:app --reload
    ```
    ✅ The backend API should now be running at `http://127.0.0.1:8000`.

#### 3.2.2. Frontend Setup
1.  Open a **new terminal** and navigate to the frontend directory: `cd frontend`
2.  Install dependencies: `npm install`
3.  Run the frontend server: `npm run dev`
    ✅ The frontend application should now be running at `http://localhost:5173`.

---

## 4. Testing

The overall testing strategy is documented in [`docs/testing_strategy.md`](docs/testing_strategy.md). To run the backend test suite, activate the virtual environment and run `pytest`.

---

## 5. Deployment

The application is deployed automatically via GitHub Actions on every push to the `main` branch.
-   The **backend** is deployed to **Google Cloud Run**.
-   The **frontend** is deployed to **Firebase Hosting**.

