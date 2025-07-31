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
- **Method**: External dependencies like the database or external APIs are mocked using libraries like `unittest.mock`.
- **Location**: `backend/tests/unit/`

### 3.2. Backend Integration Tests

- **Purpose**: To test the interaction between different backend components. This includes testing API endpoints, service-layer logic, and database interactions.
- **Scope**:
    - **API Endpoint Tests**: Verifying that API endpoints (e.g., `/api/users/me`, `/api/portfolios`) correctly process requests, trigger the appropriate business logic, and return the expected responses. These tests confirm that the web layer is correctly integrated with the service layer.
    - **End-to-End Flow Tests**: Verifying a complete data flow through the system, such as a user signing up and their data being correctly persisted in the database.
- **Method**: These tests use a real, but separate, test database (`.env.test`) to ensure data isolation. They make HTTP requests to a test instance of the FastAPI application. Authentication is typically mocked at the API boundary to test endpoint logic without depending on live external services.
- **Location**: `backend/tests/integration/` (e.g., `test_user_api.py`, `test_portfolio_api.py`, `test_user_integration.py`)

---

## 4. Frontend Testing Strategy (Vue.js/Vite)

The frontend testing strategy is designed to ensure a reliable and smooth user experience by verifying components, state management, and user workflows.

### 4.1. Frontend Unit Tests

- **Purpose**: To verify that a single, isolated piece of the UI (a "unit") works correctly on its own. A unit is typically a single Vue component, a Pinia store, or a router file.
- **Method**: Dependencies are "mocked" or faked. For example, a test for `SignUpView.vue` would not use the *real* Pinia auth store or the *real* Vue router. Instead, it provides mock versions to confirm that the `SignUpView` component calls the correct `signup` function when a button is clicked.
- **Goal**: To ensure each individual building block is reliable. They are fast, precise, and form the foundation of our frontend testing.
- **Location**: `frontend/tests/unit/`

### 4.2. Frontend Integration Tests

- **Purpose**: To verify that several different frontend units work together correctly as a group. They test the "integration" or communication between different parts of the frontend application, simulating a real user workflow.
- **Method**: These tests use the **real** components, the **real** Pinia stores, and the **real** Vue router, all working together. The only thing that is mocked is the backend API to avoid making real network requests and to control the test conditions.
- **Goal**: To catch bugs that occur at the seams between units, such as incorrect event handling, state management issues, or routing problems that unit tests would miss.

#### Key Integration Test Scenarios for Sentinel:

Based on the `product_spec.md`, the following user journeys are critical and must be covered by integration tests:

**1. The Full User Authentication and Onboarding Flow:**
*   **What it tests:** `SignUpView` -> `auth` store -> `router` -> `LoginView` -> `AppBar` -> `PortfolioView`.
*   **Scenario:**
    1.  A new user signs up successfully (mocking the backend response).
    2.  Verify the `auth` store is updated and the router redirects to the `LoginView`.
    3.  The user logs in (mocking the backend response).
    4.  Verify the `auth` store's state becomes `AUTHENTICATED` and the router navigates to the default `PortfolioView`.
    5.  Verify the `AppBar` updates to show user-specific controls (e.g., "Logout" button).

**2. Core Portfolio Management Flow:**
*   **What it tests:** `PortfolioView` -> `portfolio` store -> child components.
*   **Scenario:**
    1.  Start as a logged-in user on the `PortfolioView`.
    2.  Mock the API call to fetch portfolio data and verify the view renders the holdings correctly.
    3.  Simulate adding a new holding via the UI.
    4.  Mock the "save" API call and verify the `PortfolioView` updates dynamically to show the new holding without a page refresh.

**3. Strategy Rule Creation and Management Flow:**
*   **What it tests:** `RulesView` -> `rules` store -> child components.
*   **Scenario:**
    1.  A logged-in user navigates to the "Strategy Rules" page.
    2.  Mock the API call to fetch existing rules and verify they are displayed.
    3.  Simulate creating a new rule via the UI form.
    4.  Mock the "save" API call and verify the new rule appears in the list.

### 4.3. End-to-End (E2E) Tests

- **Purpose**: To validate a complete user flow through the entire live system, from the browser interacting with the Vue.js frontend, through the FastAPI backend, to the database.
- **Scope**: A small, critical set of "happy path" scenarios, such as:
    1.  A user can sign up, log in, create a portfolio, add a holding, and log out.
- **Method**: These tests will be written using a framework like Playwright. They run against a deployed staging environment that mirrors production. They use real, dedicated test user credentials to perform a full, realistic login. They are the slowest and most brittle tests, so they are used sparingly.

## 5. Tools and Frameworks

- **Backend**:
    - **Test Runner**: `pytest`
    - **Mocking**: `unittest.mock`
    - **HTTP Client for Tests**: `TestClient` from FastAPI
- **Frontend**:
    - **Test Runner**: `vitest`
    - **Component Testing**: `@vue/test-utils`
    - **Mocking (API)**: Mock Service Worker (`msw`) or similar.
    - **E2E Testing**: Playwright (planned)
