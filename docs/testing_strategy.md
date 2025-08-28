# Sentinel Testing Strategy

This document outlines the comprehensive testing strategy for the Sentinel application, covering both the backend and frontend components. Its purpose is to ensure the delivery of a high-quality, reliable, and maintainable product by defining clear standards and methodologies for verification and validation.

## 1. Guiding Principles

- **Spec-Driven Testing**: All tests are designed to verify the functionality described in the `product_spec.md`. The spec is the single source of truth for expected behavior.
- **Automation First**: All tests that can be automated, should be. Manual testing is reserved for exploratory and usability testing.
- **Shift-Left Approach**: Testing is not a separate phase but an integral part of the development process. Developers are responsible for writing tests for the code they create.
- **Clarity and Maintainability**: Tests should be written to be clear, concise, and easy to maintain, serving as living documentation for the codebase.

## 2. The Testing Pyramid

We adhere to the principles of the testing pyramid, which advocates for a balanced portfolio of tests at different levels of granularity.

```
      /-------------
     / E2E Tests   \
    /---------------
   / Integration   \
  /   Tests         \
 /-------------------
/   Unit Tests      \
---------------------

```

- **Unit Tests (Base of the Pyramid)**: These form the largest portion of our tests. They are fast, isolated, and verify the smallest pieces of our application (e.g., a single function or component).
- **Integration Tests (Middle Layer)**: These tests verify that different parts of the application work together correctly. They are more complex than unit tests but are crucial for validating key workflows.
- **End-to-End (E2E) Tests (Top of the Pyramid)**: These are the least numerous tests. They simulate a full user journey through the entire deployed application, from the browser to the database.

---

## 3. Backend Testing Strategy (Python/FastAPI)

The backend testing strategy focuses on verifying the correctness of the API, business logic, and data persistence.

### 3.1. Backend Unit Tests

- **Purpose**: To test individual functions and classes in isolation.
- **Scope**:
    - Business logic within service functions (e.g., `portfolio_service.py`).
    - Utility functions and data model validation.
    - Individual FastAPI dependencies.
- **Method**: External dependencies like the external APIs are mocked using libraries like `unittest.mock`. But the database calls should run against the **Firebase Emulator Suite** (Firestore and Auth), to avoid problems with heavy mocking. 
- **Location**: `backend/tests/unit/`

### 3.2. Backend Integration Tests

- **Purpose**: To test the interaction between different backend components. This includes testing API endpoints, service-layer logic, and database interactions.
- **Scope**:
    - **API Endpoint Tests**: Verifying that API endpoints (e.g., `/api/users/me`, `/api/portfolios`) correctly process requests, trigger the appropriate business logic, and return the expected responses. These tests confirm that the web layer is correctly integrated with the service layer.
    - **End-to-End Flow Tests**: Verifying a complete data flow through the system, such as a user signing up and their data being correctly persisted in the database.
- **Method**: All integration tests are run against the **Firebase Emulator Suite** (Firestore and Auth). This provides high-fidelity testing against the same software that runs in production, without the cost or flakiness of a live network connection. A fixture automatically clears the emulator's data before each test to ensure perfect isolation.
- **Location**: `backend/tests/integration/` (e.g., `test_user_api.py`, `test_portfolio_api.py`, `test_user_integration.py`)

---

## 4. Frontend Testing Strategy (Vue.js/Vite)

The frontend testing strategy is designed to ensure a reliable and smooth user experience by verifying components, state management, and user workflows.

### 4.1. Frontend Component Tests (High-Fidelity)

- **Purpose**: To verify that individual Vue components render and behave correctly, and that they correctly interact with their immediate child components.
- **Method**: We adopt a **high-fidelity testing approach** for UI components. Instead of extensively mocking child components (especially from complex UI libraries like Vuetify), we test against the *real* child components. This is made possible by a global test setup that properly initializes the Vuetify plugin for the test environment. This approach treats each component test as a small-scale integration test, ensuring that the component not only works in isolation but is also correctly integrated with its immediate UI dependencies. For non-UI dependencies (like stores or router), we still use mocks to maintain focus and speed.
- **Goal**: To create robust, reliable tests that are less brittle and more representative of the real application behavior, avoiding the significant overhead and potential inaccuracies of mocking a complex component library.
- **Location**: `frontend/tests/components/`

### 4.2. Core Logic Unit Tests (Stores, Router, Plugins, Utilities)

- **Purpose**: To test the core logic within Pinia stores, the Vue router, application plugins, and utility files in strict isolation.
- **Method**: For stores, router, and plugins, we use real instances but mock external dependencies (like API calls, Firebase SDK) to ensure focus on the logic being tested. For utility files, strict unit testing is applied.
- **Goal**: To ensure the core application logic and state management are correct in a fast, focused manner.
- **Location**:
    - `frontend/tests/stores/`: For Pinia store logic.
    - `frontend/tests/router/`: For Vue Router configuration and guards.
    - `frontend/tests/plugins/`: For application-level plugins (e.g., Firebase initialization).
    - `frontend/tests/config.spec.ts`: For utility/configuration file testing.

### 4.3. View & Workflow Tests (High-Fidelity Integration Tests)

#### Key User Workflow Scenarios for Sentinel:

- **Purpose**: To verify that entire "View" components (which often orchestrate multiple smaller components, stores, and router interactions) work together correctly to fulfill a user workflow as defined in `docs/specs/ui_flows_spec.yaml`.
- **Method**: These tests mount entire "View" components (e.g., `UserSettingsView.vue`). They use the **real** components, the **real** Pinia stores (with mocked API calls), and a **real** Vue router instance. This provides a high-fidelity test environment that closely mimics the actual application runtime. For tests requiring a backend, the frontend application connects to the **Firebase Emulator Suite**, allowing for full-stack testing of the frontend against a realistic, but local and controllable, backend.
- **Goal**: To catch bugs that occur at the seams between major application features, such as incorrect event handling, state management issues, or routing problems that component-level tests would miss.
- **Location**: `frontend/tests/views/`
- **User Workflows Scenarios:** These tests (to be added in the future) will be placed under `frontend/tests/flows/`

Based on the `product_spec.md`, the following user workflows are critical and must be covered by these high-fidelity integration tests:

**1. The Full User Authentication and Onboarding Flow:**
- **What it tests:** `LoginForm.vue` -> `auth` store -> `router` -> `StandardLayout.vue` -> `DashboardView.vue`.
-  **Scenario:**
-    1.  A user logs in using the `LoginForm.vue` (connecting to the Auth emulator).
-    2.  Verify the `auth` store's state becomes `AUTHENTICATED` and the router navigates to the `DashboardView`.
-    3.  Verify the `StandardLayout`'s `AppBar` updates to show user-specific controls (e.g., "Logout" button).

**2. User Settings Management Flow:**
- **What it tests:** `StandardLayout.vue` -> `router` -> `UserSettingsView.vue` -> `userSettings` store -> child components.
-  **Scenario:**
-    1.  Start as a logged-in user.
-    2.  The test sets the `userSettings` store state to simulate a successful API call.
-    3.  Simulate a click on the "Settings" button in the `AppBar` to navigate to the settings view.
-    4.  Verify that `UserSettingsView.vue` renders the form correctly with the initial data.
-    5.  Simulate changing a value (e.g., the default portfolio) and clicking "Save".
-    6.  Verify the store's `updateUserSettings` action was called with the correct payload and that the router navigated back.

**3. Core Portfolio Management Flow:**
- **What it tests:** `PortfolioView` -> `portfolio` store -> child components.
- **Scenario:**
    1.  Start as a logged-in user on the `PortfolioView`.
    2.  Mock the API call to fetch portfolio data and verify the view renders the holdings correctly.
    3.  Simulate adding a new holding via the UI.
    4.  Mock the "save" API call and verify the `PortfolioView` updates dynamically to show the new holding without a page refresh.

**4. Strategy Rule Creation and Management Flow:**
- **What it tests:** `RulesView` -> `rules` store -> child components.
- **Scenario:**
    1.  A logged-in user navigates to the "Strategy Rules" page.
    2.  Mock the API call to fetch existing rules and verify they are displayed.
    3.  Simulate creating a new rule via the UI form.
    4.  Mock the "save" API call and verify the new rule appears in the list.

**5. Automatic Market Monitoring and Alert Triggering Flow:**


-**6. Alert Viewing Flow:**
- **What it tests:** `StandardLayout.vue` -> `AlertsListView.vue` -> `AlertDetailView.vue` -> `alerts` store.
-  **Scenario:**
-    1.  Start as a logged-in user.
-    2.  The test sets the `alerts` store state with mock read and unread alerts.
-    3.  Verify the `AppBar` in `StandardLayout` shows a badge for unread alerts.
-    4.  Simulate navigation to the `AlertsListView` and verify all alerts are displayed.
-    5.  Simulate a click on an unread alert and verify navigation to `AlertDetailView` with the correct data.

### 4.4. End-to-End (E2E) Tests

- **Purpose**: To validate a complete user flow through the entire live system, from the browser interacting with the Vue.js frontend, through the FastAPI backend, to the emulated database.
- **Scope**: A small, critical set of "happy path" scenarios, such as:
    1.  A user can sign up, log in, create a portfolio, add a holding, and log out.
- **Method**: These tests will be written using a framework like Playwright. They run against a deployed staging environment that mirrors production. They use real, dedicated test user credentials to perform a full, realistic login. They are the slowest and most brittle tests, so they are used sparingly.

## 5. Tools and Frameworks

- **Backend**:
    - **Test Runner**: `pytest`
    - **Test Environment**: Firebase Emulator Suite
    - **HTTP Client for Tests**: `TestClient` from FastAPI
- **Frontend**:
    - **Test Runner**: `vitest`
    - **Component Testing**: `@vue/test-utils`
    - **Test Environment**: JSDOM with Firebase Emulator Suite
- **E2E Testing**: Playwright (planned)
