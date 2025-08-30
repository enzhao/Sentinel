# Gemini Guidelines for Sentinel Project

Our goal is to build the Sentinel app. Here is the list of files for you to reference during our collaboration:

## References 

- product_spec.md: The single source of truth for what to build. Always refer to this file first.
- docs/view_dsl.md: custom DSL for defining the views of this app.
- docs/state_machine_dsl.md: custom DSL for defining the user interaction flows of this app.
- docs/specs/view_spec.yaml: The formal defnition of all UI views, defined using the view DSL. The view IDs are referenced from other specs such as the ui_flows_spec.yaml and the product_spec.md.
- docs/specs/ui_flows_spec.yaml: The formal defnition of all user interaction flows, defined using the state machine DSL. The flow IDs are referenced from other specs such as the product_spec.md.
- README.md: Instructions for setting up the development environment and running the app.
- docs/developer_guide.md: Useful commands and guides for developers and AIs working on this project.
- docs/testing_strategy.md: The testing strategy for the project.
- docs/message_handling.md: The strategy for managing user-facing messages in the app.
- docs/google_cloud_setup.md: Instructions for setting up Google Cloud services for the project.

## Technology Stack (as defined in product_spec.md)
- Backend: Python FastAPI, Google Cloud Firestore, Firebase Admin SDK, Alpha Vantage API.
- Frontend: Vue.js v3 (TypeScript), Vuetify (Material Design), Pinia for state management, Firebase client SDK.

## Deliverables

1. **Fully functional backend:** All API endpoints, business logic, and data models implemented according to the specifications.
2. **Comprehensive backend tests:** Unit tests for services and integration tests for API endpoints, following stragies in `docs/testing_strategy.md`.
3. **Fully functional frontend:** All UI views, components, and interaction flows implemented according to the specifications.
4. **Comprehensive frontend tests:** Unit tests and integration tests for components and views, following stragies in `docs/testing_strategy.md`.
5. **Adherence to conventions:** All code must follow existing project conventions (formatting, naming, style, architectural patterns, typing).
6. **Build/Lint/Type-check:** Ensure the project builds successfully and passes all linting and type-checking checks.

## Development Approach

I expect you to adopt an iterative, vertical slice, feature-driven approach. I will show you the list of features to be built in priority order. For each feature, you should: 

1. **Plan:** Outline the specific backend and frontend components to be built, and the tests to be written.
2. **Reference to the product_spec.md:** Always refer to the product_spec.md for detailed requirements and specifications for each feature. All generated code must contain references back to the relevant sections in product_spec.md for traceability in their comments or docstrings.
3. **Implement Backend:** Implement the API endpoints, business logic, and data models.
4. **Test Backend:** Ensure the Firebase Emulators are running. Write and run unit and integration tests for the backend components using the command `ENV=test venv/bin/pytest --cov=src backend/tests/`. If any tests fail, fix the issues before proceeding.
5. **Implement Frontend:** Implement the UI views and components, integrating with the newly built backend.
6. **Test Frontend:** Ensure the Firebase Emulators are running. Write and run unit tests and integration tests for the frontend components using the command `npm --prefix frontend run test:spec`. If any tests fail, fix the issues before proceeding.
7. **End to End Testing:** Write and perform end-to-end testing of the entire feature to ensure it works as expected. If any tests fail, fix the issues before proceeding.
8. **Verify:** Run all project-specific build, linting, and type-checking commands.

The existing code in both backend and frontend for already implemented features are very important, do not rewrite them, and always ask for my permission if you want to modify them. Thanks! 

### Handling Inter-Feature Dependencies 

If inter-feature dependencies present in the product_spec.md, please follow this approach: API Contract First with Minimal Backend Implementation and Frontend Mocking. To be specific:

1. Strict Adherence to API Contracts (see api/sentinel_api.yaml)

2. Minimal Backend Implementation for Dependencies: For the dependent feature (e.g., "Holdings List" when working on "Portfolio Detail"), implement just enough backend functionality to satisfy the immediate needs of the parent feature.

3. Frontend Mocking (as an Accelerator): The frontend can initially mock API responses based on the API contract, allowing UI development to proceed even if the backend is only minimally implemented or not yet started.

In summary, when you encounter a dependency like "Portfolio Detail needs Holdings List":

1. Ensure the API contract for *both* features is defined.
2. Implement the primary feature's backend fully.
3. For the dependent feature's backend, implement *only the necessary read endpoints* to return minimal (empty or hardcoded dummy) but valid data.
4. Implement the primary feature's frontend, integrating with the real (even if minimal) backend.
5. In the next feature cycle, fully implement the dependent feature's backend and frontend.

## Prioritized Feature List

The AI should prioritize features based on their foundational nature. A logical sequence might be:

### Foundational Features (Must-Have for All Functional Features)

- [x] project scaffolding and setup, including initial CI/CD pipelines (if not already done)
- [x] Generate the OpenAPI spec from the product_spec.md, the generated file should be api/sentinel_openapi.yaml, the generated openapi spec should contain section refrences back to the relevant sections in product_spec.md for traceability.
- [x] Shared Models: Generate or define shared data models (e.g., Pydantic models for FastAPI, TypeScript interfaces for Vue) based on the product_spec.md and the api/sentinel_api.yaml spec. All generated models should contain section refrences back to the relevant sections in product_spec.md for traceability. 
- [x] setup and test the codespaces of GitHub. 

### Functional Features

- [x] Public Homepage (see product_spec.md Chapter 8, and the view with id VIEW_HOME_PAGE in the file docs/specs/views_spec.yaml). 
- [x] User Authentication (Login, Logout, Provisioning script, see product_spec.md Chapter 8). 
- [x] User Settings Management API validation and Backend (see files api/sentinel_api.yaml and product_spec.md Chapter 9).
- [x] User Settings Management Frontend (see files docs/specs/views_spec.yaml , docs/specs/ui_flows_spec.yaml , and api/sentinel_api.yaml and product_spec.md Chapter 9).
- [ ] Portfolio Management API Validation and Backend (see files api/sentinel_api.yaml and product_spec.md Chapter 3). Note that the section "P_5000: Unified Transaction Import" is for a future iteration, we do not implement this for now.   
- [ ] Portfolio Management Frontend (see files docs/specs/views_spec.yaml, docs/specs/ui_flows_spec.yaml, api/sentinel_api.yaml and product_spec.md Chapter 3). Note that the section "P_5000: Unified Transaction Import" is for a future iteration, we do not implement this for now.   
- [ ] Holding Management (CRUD, Move, Backfill trigger, see product_spec.md Chapter 4)
- [ ] Lot Management (CRUD, see product_spec.md Chapter 5)
- [ ] Strategy Rule Management (CRUD, Effective Rule Retrieval, etc., see product_spec.md Chapter 6)
- [ ] Market Monitoring (see product_spec.md Chapter 7)
- [ ] Alerts (Generation, Persistence, Frontend Consumption, see product_spec.md Chapter 7)
- [ ] Unified Transaction Import (as it builds on holdings/lots, see product_spec.md section 3.1.5)


### Continuous and Future Improvements

- [ ] check correctness of the commands in README.md, docs/developer_guide.md, run_local_backend.sh, and Taskfile.yaml
- [ ] migrate to Workload Identity Federation (WIF) for the ci build. 
- [ ] build the message system (generate app_messages.json from the prodcuts_spec.md, and further generate message bundles for both backend and frontend from this app_messages.json)


