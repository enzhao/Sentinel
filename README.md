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

### 3.1. Prerequisites

1. **Cloud & Project Setup**: Before running the application locally, you must set up the required Google Cloud and Firebase services. Follow the step-by-step guide here:

➡️ **[./docs/google_cloud_setup.md](./docs/google_cloud_setup.md)**

2. **Firebase CLI:** Install the Firebase command-line tools, which are required to run the local emulators.

```sh
npm install -g firebase-tools
```

### 3.2. Local Development with the Firebase Emulator

Our primary development workflow uses the Firebase Emulator Suite. This runs a local version of Firebase on your machine, allowing for fast, safe, and free development.

1. **Initialize Emulators (First Time Only):**

From the project root, run `firebase login` and then initialize the emulators.

```sh
firebase init emulators
``` 

Select **Auth** and **Firestore** and use the default ports.

2. **Start the Emulators:**

Open a terminal and run the following command from the project root. Keep this terminal running.

```sh
firebase emulators:start
``` 
✅ The emulators and a UI for viewing local data are now running.

3. **Run the Backend:**

Open a **new terminal**. Navigate to the backend, set the environment, and run the server.

```sh
cd backend
# Make sure your virtual environment is activated
source venv/bin/activate
ENV=dev uvicorn src.main:app --reload
``` 
✅ The backend API should now be running at http://127.0.0.1:8000 and connected to the emulators.

4. **Run the Frontend:**

Open a **third terminal**. Navigate to the frontend and run the dev server.

```sh
cd frontend
npm install
npm run dev
```
✅ The frontend application should now be running at http://localhost:5173 and connected to the emulators.

---

## 4. Testing

All automated tests (both local and in the CI/CD pipeline) run against the Firebase Emulator Suite for high-fidelity validation. For more details, see the [`docs/testing_strategy.md`](docs/testing_strategy.md). 

To run the test suites:

```sh
# From the backend directory
ENV=test venv/bin/pytest --cov=src backend/tests/

# From the frontend directory
npm run test:spec
```

---

## 5. Deployment

The application is deployed automatically via GitHub Actions on every push to the `main` branch.
-   The **backend** is deployed to **Google Cloud Run**.
-   The **frontend** is deployed to **Firebase Hosting**.
