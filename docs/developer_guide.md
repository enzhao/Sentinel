# Sentinel Developer Guide 🚀

This guide provides essential information for developers working on the Sentinel project. It covers key development processes, workflows, and architectural strategies to ensure consistency and quality.

## 1. Core Development Processes ⚙️

### 1.1. Testing Strategy 🧪

A comprehensive testing strategy is crucial for maintaining the stability and reliability of the application. Our approach includes unit, integration, and end-to-end tests for both the frontend and backend.

For complete details, please see the **[Testing Strategy Document](./testing_strategy.md)**.

### 1.2. Message Handling 💬

To ensure a consistent user experience, all user-facing text (including errors, confirmations, and UI labels) is managed through a centralized, spec-driven system. All messages are derived from `product_spec.md`.

For instructions on how to add, update, and manage messages, please see the **[Message Handling Strategy Document](./message_handling.md)**.

### 1.3. Specification-Driven UI Workflows 🎨

The project uses a specification-driven approach for the UI, where formal YAML documents define the structure and behavior of the frontend.

- `docs/specs/views_spec.yaml`: Defines the static structure of all UI views.
- `docs/specs/ui_flows_spec.yaml`: Defines the user interaction state machines (flows).

#### 1.3.1. Step 1: Generating UI Flow Diagrams

To visualize the flow definitions, we use a script to automatically generate Mermaid code from the `ui_flows_spec.yaml` file.

1.  Ensure your utility virtual environment is active (`source util_env/bin/activate`).
2.  Run the script from the project root:
    ```bash
    python util/generate_ui_flow_visuals_mermaid.py docs/specs/ui_flows_spec.yaml
    ```
3.  This will generate the source-of-truth diagrams in `docs/ui_flow_diagrams.md`.

#### 1.3.2. Step 2: Synchronizing Diagrams into the Product Spec

After generating the diagrams, use this second script to automatically insert them into the main `product_spec.md`. **Never edit the Mermaid diagrams in the product spec manually**.

-   **Prerequisite**: The `product_spec.md` file must contain placeholder comments where the diagrams should be inserted (e.g., ```mermaid).

-   **Usage**:
    1.  Ensure your utility virtual environment is active.
    2.  Run the script from the project root, providing the source diagrams file and the target spec file.
        ```bash
        python util/update_flow_diagrams_in_product_spec.py docs/ui_flow_diagrams.md product_spec.md
        ```
    3.  The script will find the placeholders and replace them with the latest diagrams. It will then print a report summarizing which diagrams were updated or if any are out of sync.
    
> **Tip for Testing**: You can provide an optional third argument (`--output` or `-o`) to write the results to a new file instead of overwriting the original. This is useful for verifying the script's output before committing changes.
> ```bash
> python util/update_flow_diagrams_in_product_spec.py docs/ui_flow_diagrams.md product_spec.md -o product_spec_test.md
> ```

> **Caution**: This script relies on the specific formatting of the placeholder comments in `product_spec.md` and the `## Flow: ...` headings in `docs/ui_flow_diagrams.md`. Significant changes to these formats may break the script. If the script fails, ensure these structures have not been altered.

---

## 2. Development Workflow 🔄

This project uses a standardized workflow to ensure a clean, understandable, and automated version history.

### 2.1. Commit Messages

All commit messages must follow the [**Conventional Commits**](https://www.conventionalcommits.org/) specification. This is enforced automatically by a `commit-msg` hook. The basic format is:
`<type>(<scope>): <subject>`

### 2.2. Creating a Release

Creating a new version, generating a changelog, and tagging the release is an automated process.

1.  Ensure you are on the `main` branch and have pulled the latest changes.
2.  Run the release script from the project root:
    ```bash
    npm run release
    ```
3.  Push the new commit and the tag to GitHub:
    ```bash
    git push --follow-tags origin main
    ```

---

## 3. Advanced Workflows 🛠️

### 3.1. Managing Backend Dependencies

-   To add or remove a package, edit the `backend/requirements.in` file.
-   After editing, run `pip-compile backend/requirements.in` to update `backend/requirements.txt`.
-   Then, run `pip-sync` to update your local virtual environment.

### 3.2. Local Docker Testing

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

## 4. Cloud and Deployment Notes ☁️

### 4.1. Cloud Run Security

For security, public access to the backend API on Google Cloud Run is disabled by default in the deployment workflow. To test the live cloud instance, you must temporarily enable public access:
1.  Navigate to **Cloud Run** in the Google Cloud Console.
2.  Select the `sentinel-invest-backend` service.
3.  Go to the **Security** tab and allow public (unauthenticated) access.

### 4.2. Instance Configuration

To manage costs, the Cloud Run service is configured with a **maximum of 1 instance**. This setting can be adjusted in the service's main configuration tab if higher concurrency is needed.

---

## 5. Future Development Workflow 🛣️

To ensure the project remains robust and maintainable, we are transitioning to a spec-driven development process. All future development should follow these steps:

1.  **Update the Product Spec**: Before writing any code, define the new business requirements or changes in `product_spec.md`. This is the human-readable source of truth.

2.  **Update the OpenAPI Spec**: Manually translate the business requirements from the product spec into a formal API contract by editing `api/sentinel-invest-backend.yaml`. This file is the machine-readable source of truth for the API.

3.  **Regenerate the API Skeleton**: Use an OpenAPI generator tool to create or update the boilerplate for the API routers and models from the YAML spec.
    ```bash
    npx @openapitools/openapi-generator-cli generate -i api/sentinel-invest-backend.yaml -g python-fastapi -o api/generated_backend_fastapi
    ```

4.  **Implement the Business Logic**: With the API skeleton in place, write or modify the business logic in the `services` directory (e.g., `portfolio_service.py`). The generated API endpoints will call these services.

5.  **Write Tests**: Create unit and integration tests for the new business logic to ensure it is correct and robust.

