# Sentinel Invest 

![Status](https://img.shields.io/badge/status-Work%20In%20Progress-orange)

An automated, strategy-driven tool to help long-term investors make disciplined, data-driven decisions without the need for constant market-watching.

## Core Philosophy

Sentinel is designed to be a **behavioral guardrail**. It helps investors stick to their own long-term strategy by filtering out short-term market noise and providing timely, actionable alerts based on pre-defined, data-driven rules. The core methodology is a hybrid **"Core-Satellite"** model, combining systematic accumulation with opportunistic, tax-aware rebalancing.

For a full breakdown of the project's vision, features, and architecture, please see the `product_spec.md`.

---

## Project Structure

```bash
.
├── .github/workflows/      # CI/CD pipelines
├── backend/                # Python FastAPI backend
├── docs/                   # Project documentation
│   └── google_cloud_setup.md
├── frontend/               # Vue.js frontend
├── .gitignore
├── product_spec.md         # The official product specification
└── README.md               # This file
``` 

---

## Getting Started

### 1. Cloud & Project Setup

Before running the application locally, you must set up the required Google Cloud and Firebase services. Follow the step-by-step guide here:

➡️ **[./docs/google_cloud_setup.md](./docs/google_cloud_setup.md)**

### 2. Local Development

After completing the cloud setup, follow these steps to run the application on your local machine.

#### Backend Setup
1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Set Local Python Version:**
    ```bash
    pyenv local 3.13.3
    ```

3.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    This project uses `pip-tools` for precise dependency management.
    ```bash
    pip install pip-tools
    pip-sync
    ```

5.  **Set Environment for Local Development:**
    For the backend to connect to Firestore locally, it needs credentials.
    - Place your `serviceAccountKey.json` file in the `/backend` directory.
    - Set the required environment variable:
    ```bash
    export ENV=local
    ```

6.  **Run the Backend Server:**

    ```bash
    uvicorn src.main:app --reload
    ```
    ✅ The backend API should now be running at `http://127.0.0.1:8000`.

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

