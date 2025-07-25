# Sentinel  Sentinel

![Status](https://img.shields.io/badge/status-Work%20In%20Progress-orange)

An automated, strategy-driven tool to help long-term investors make disciplined, data-driven decisions without the need for constant market-watching.

## Core Philosophy

Sentinel is designed to be a **behavioral guardrail**. It helps investors stick to their own long-term strategy by filtering out short-term market noise and providing timely, actionable alerts based on pre-defined, data-driven rules. The core methodology is a hybrid **"Core-Satellite"** model, combining systematic accumulation with opportunistic, tax-aware rebalancing.

For a full breakdown of the project's vision, features, and architecture, please see the `product_spec.md`.

---

## Technology Stack

This project is a monorepo containing a Vue.js frontend and a Python backend.

| Area      | Technology                                    |
| :-------- | :-------------------------------------------- |
| Frontend  | Vue.js 3 with TypeScript                      |
| Backend   | Python 3.13 with FastAPI                      |
| Database  | Google Cloud Firestore                        |
| Hosting   | Firebase Hosting (Frontend), Google Cloud Run (Backend) |
| Auth      | Firebase Authentication                       |
| CI/CD     | GitHub Actions                                |

---

## Prerequisites

- **Local Development**:
  - Python 3.13 (recommended via `pyenv local 3.13.3`)
  - Node.js 20 (LTS)
  - Docker
  - Git

- **Cloud Setup**:
  - Google Cloud Platform account with billing enabled
  - Firebase account
  - GitHub account with repository access

## Installation

### Local Setup

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Sentinel
``` 

#### 2. Backend Setup

- Install Python dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
``` 

- For local Firestore testing, place your `serviceAccountKey.json` in the `backend` directory and set `ENV=local`:

```bash
export ENV=local
``` 

- Run the app locally:

```bash
uvicorn main:app --reload
```
✅ The backend API should now be running at http://127.0.0.1:8000.

#### 3. Frontend Setup

- Open a **new terminal window** and navigate to the frontend directory from the project root:

```bash
cd frontend
npm install
npm run dev
```
✅ The frontend should now be running at http://localhost:5173.


### 4. Docker (Optional)

- Build and run the backend container from the project root:

```bash
docker build -t sentinel-backend ./backend
docker run -p 8000:8000 -e ENV=local -v /path/to/serviceAccountKey.json:/app/../serviceAccountKey.json sentinel-backend
```

## Deployment

### Google Cloud Setup

1. **Configure Google Cloud**
   - Create a project (e.g., `sentinel-invest`) in Google Cloud Console.
   - Enable Cloud Run, Firestore, and Artifact Registry APIs.
   - Set up a service account with `roles/run.admin`, `roles/datastore.user`, and `roles/artifactregistry.writer` roles.
   - Store the service account key as a GitHub Secret (`GCP_SA_KEY`) and project ID as `GCP_PROJECT_ID`.

2. **Backend Deployment**
   - The `deploy.yml` workflow automates building and pushing the Docker image to Artifact Registry, then deploying to Cloud Run.
   - Trigger deployment with a push to the `main` branch.

3. **Frontend Deployment**
   - Configure Firebase Hosting in your Firebase Console.
   - The `deploy.yml` workflow builds the Vue app and deploys it to Firebase Hosting.
   - Ensure the `VITE_API_URL` in `.env.production` matches your Cloud Run backend URL.


## Usage

- Access the frontend at `https://sentinel-invest.web.app`.
- Interact with the backend API at `https://sentinel-backend-63684098605-europe-west3.run.app/api/message` (update with actual URL).
- Monitor deployment status and logs via Google Cloud Console and GitHub Actions.


