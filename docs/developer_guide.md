# Sentinel Developer Guide 👩‍💻

Welcome to the Sentinel project! This guide provides essential information for developers, covering the local environment setup, core development workflows, project standards, and deployment procedures to ensure consistency and quality across the board.

## 1. Getting Started: Local Development Environment 💼

To manage different configurations effectively, we use a consistent environment naming scheme across both the frontend and backend.

### 1.1. Environment Overview

- **`dev`**: This is the primary environment for all local development and automated testing. It is configured to connect to the **Firebase Emulator Suite**.
- **`local-prod`**: This is a special-purpose environment used to connect your local backend to the **live, cloud-hosted Firebase database**. It should only be used for specific tasks like data validation or migration and requires a `serviceAccountKey.json` file.
- **`production`**: This refers to the live, deployed environment running on Google Cloud.

### 1.2. Standard Workflow (`dev` mode)

This is the standard workflow for all typical development tasks.

1.  **Start the Emulators**: In your first terminal, navigate to the project root and start the Firebase emulators. Keep this process running.
    ```bash
    firebase emulators:start
    ```
2.  **Start the Backend**: In a second terminal, activate the virtual environment and start the FastAPI server in `dev` mode.
    ```bash
    cd backend
    source venv/bin/activate
    ENV=dev uvicorn src.main:app --reload
    ```
3.  **Start the Frontend**: In a third terminal, start the Vite development server. The environment is automatically set to `dev` by the `frontend/.env.development` file.
    ```bash
    cd frontend
    npm run dev
    ```

### 1.3. Connecting to Production Data (`local-prod` mode)

**Warning**: Use this mode with extreme caution, as you will be interacting with live production data.

1.  Place your `serviceAccountKey.json` file in the `/backend` directory.
2.  Start the backend server using the `local-prod` environment variable.
    ```bash
    cd backend
    source venv/bin/activate
    ENV=local-prod uvicorn src.main:app --reload
    ```

## 2. The Core Development Process 🔄

This section outlines the standardized processes for building features, committing code, and creating releases.

### 2.1. Spec-Driven Development for New Features

All new development must follow a spec-driven process to ensure the project remains robust and maintainable.

1.  **Update the Product Spec**: Before writing code, define the new business requirements in `product_spec.md`. This document serves as the human-readable source of truth.
2.  **Update the OpenAPI Spec**: Translate the business requirements into a formal API contract by editing `api/sentinel-invest-backend.yaml`. This is the machine-readable source of truth for the API.
3.  **Regenerate the API Skeleton**: Use an OpenAPI generator to create or update the boilerplate code for API routers and models from the YAML spec.
    ```bash
    npx @openapitools/openapi-generator-cli generate -i api/sentinel-invest-backend.yaml -g python-fastapi -o api/generated_backend_fastapi
    ```
4.  **Implement the Business Logic**: With the API skeleton generated, write the required business logic within the `services` directory (e.g., `portfolio_service.py`).
5.  **Write Tests**: Create comprehensive unit and integration tests for the new logic to ensure correctness and reliability.

### 2.2. Commit Message Standards

All commit messages are required to follow the [**Conventional Commits**](https://www.conventionalcommits.org/) specification. This is enforced automatically by a `commit-msg` hook. The standard format is: `<type>(<scope>): <subject>`.

### 2.3. Creating a Release

The process for versioning, generating a changelog, and tagging a release is automated.

1.  Ensure you are on the `main` branch and have pulled the latest changes.
2.  Run the release script from the project root, specifying the version type.
    ```bash
    npm run release -- --release-as <major|minor|patch>
    ```
3.  Push the new commit and its associated tag to GitHub.
    ```bash
    git push --follow-tags origin main
    ```

## 3. Project Standards & Strategies 📜

### 3.1. Testing Strategy 🧪

All automated tests are executed in the `dev` environment against the Firebase Emulator Suite. This approach guarantees high-fidelity, fast, and isolated test runs. For complete details, refer to the **[Testing Strategy Document](./testing_strategy.md)**.

### 3.2. User-Facing Message Handling 💬

To maintain a consistent user experience, all user-facing text (including errors, confirmations, and UI labels) is managed via a centralized, spec-driven system. All messages are derived from `product_spec.md`. For detailed instructions, see the **[Message Handling Strategy Document](./message_handling.md)**.

### 3.3. Specification-Driven UI Workflows 🎨

The project's frontend is built using a specification-driven approach, where formal YAML documents define the UI's structure and behavior.
* `docs/specs/views_spec.yaml`: Defines the static structure of all UI views.
* `docs/specs/ui_flows_spec.yaml`: Defines the user interaction state machines, or "flows".

## 4. Common Tasks & Advanced Workflows 🛠️

This section covers specific procedures for managing dependencies, testing with Docker, and updating UI diagrams.

### 4.1. Updating UI Flow Diagrams

#### Step 1: Generate UI Flow Diagrams
To visualize UI flows, a script automatically generates Mermaid diagram code from the `ui_flows_spec.yaml` file.

1.  Activate the utility virtual environment (`source util_env/bin/activate`).
2.  From the project root, run the generation script:
    ```bash
    python util/generate_ui_flow_visuals_mermaid.py docs/specs/ui_flows_spec.yaml
    ```
3.  This script outputs the source-of-truth diagrams into `docs/ui_flow_diagrams.md`.

#### Step 2: Synchronize Diagrams into the Product Spec
A second script automatically inserts the newly generated diagrams into the main `product_spec.md` file. **Never edit the Mermaid diagrams in the product spec manually**.

* **Prerequisite**: Ensure the `product_spec.md` file contains the placeholder comments (e.g., ```mermaid) where diagrams are to be inserted.
* **Usage**:
    1.  Activate the utility virtual environment.
    2.  Run the update script from the project root:
        ```bash
        python util/update_flow_diagrams_in_product_spec.py docs/ui_flow_diagrams.md product_spec.md
        ```
    3.  The script will replace the placeholders and print a summary report.

> **Tip for Testing**: You can use the `--output` (`-o`) flag to write the results to a new file for verification before overwriting the original.
> ```bash
> python util/update_flow_diagrams_in_product_spec.py docs/ui_flow_diagrams.md product_spec.md -o product_spec_test.md
> ```

### 4.2. Managing Backend Dependencies

* To add or remove a Python package, modify the `backend/requirements.in` file.
* After editing, run `pip-compile backend/requirements.in` to update the locked `backend/requirements.txt` file.
* Finally, run `pip-sync` to align your local virtual environment with the locked requirements file.

### 4.3. Local Docker Testing

To test the production container on your local machine, follow these steps from the project root:

1.  **Build the image**:
    ```bash
    docker build -t sentinel-backend ./backend
    ```
2.  **Run the container**:
    ```bash
    docker run --rm -p 8000:8000 -e ENV=dev -v $(pwd)/backend/serviceAccountKey.json:/app/serviceAccountKey.json sentinel-backend
    ```

## 5. Cloud Deployment & Operations ☁️

### 5.1. Cloud Run Security

By default, public access to the backend API on Google Cloud Run is disabled for security. To test a live cloud instance, you must temporarily enable public access:
1.  Navigate to **Cloud Run** in the Google Cloud Console.
2.  Select the `sentinel-invest-backend` service.
3.  Go to the **Security** tab and choose to allow public (unauthenticated) access.

### 5.2. Cloud Run Instance Configuration

To manage costs, the Cloud Run service is configured to use a **maximum of 1 instance**. If higher concurrency is required, this setting can be adjusted in the service's main configuration tab.

