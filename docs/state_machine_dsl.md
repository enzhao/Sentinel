# State Machine DSL for User Interaction Flows

## 1. Purpose and Audience

This document defines the lightweight Domain-Specific Language (DSL) used within the `product_spec.md` to formally describe user interaction flows. This DSL provides a structured, unambiguous, and machine-readable format for defining state machines that model how a user moves through a specific task or process within the Sentinel application.

The primary purpose is to provide:
- **For Human Readers (Developers, PMs, Testers):** A clear, consistent, and easy-to-understand blueprint of every user flow, including all possible states, user actions, system responses, and error conditions.
- **For AI Automation Agents:** A formal, parsable specification that can be directly translated into frontend components, state management logic, and automated tests, minimizing ambiguity and implementation errors.

## 2. DSL Syntax and Keywords

Each flow is defined by a root object containing a `flowId`, an `initialState`, and a list of `states`.

### 2.1. Top-Level Keywords

- `flowId` (String, Required): A unique identifier for the entire user flow (e.g., `FLOW_CREATE_LOT_MANUAL`).
- `initialState` (String, Required): The name of the state where the flow begins. This must match the `name` of one of the defined states.
- `states` (Array, Required): A list of all possible state objects within the flow.

### 2.2. State Object Keywords

Each object within the `states` array represents a single state in the machine and has the following structure:

- `name` (String, Required): A unique, machine-friendly name for the state (e.g., `Idle`, `FormInput`, `Submitting`).
- `description` (String, Required): A human-readable sentence describing what this state represents for the user. It should clarify what the user sees or does in the UI at this stage.

A state can contain one or more of the following blocks to define its behavior:

- `events` (Object, Optional): Defines transitions triggered directly by **user actions**.
    - **Key:** The name of the user event in `UPPER_SNAKE_CASE` (e.g., `USER_CLICKS_SAVE`).
    - **Value:** The `name` of the target state to transition to.

- `entryAction` (Object, Optional): Defines an **automated action** that is executed immediately upon entering this state. This is typically used for calling services, APIs, or performing validations.
    - `service` (String, Required): A description of the service being called (e.g., `"FinancialInstrumentLookupService.search(identifier)"`, `"POST /api/users/me/holdings"`).
    - `transitions` (Object, Required): Defines the possible outcomes of the `service` call and which state to transition to for each outcome.
        - **Key:** The name of the outcome in `snake_case` (e.g., `success`, `failure`, `invalid`).
        - **Value:** The `name` of the target state.

- `exitAction` (Object, Optional): Defines an action that is executed when leaving this state. This is primarily used for navigation.
    - `action` (String, Required): The type of action to perform (e.g., `NAVIGATE_TO`).
    - `target` (String, Required): The destination of the action (e.g., a `viewId` like `VIEW_PORTFOLIO_HOLDINGS`).

## 3. Example: Manual Holding Creation Flow

The following example illustrates how the DSL is used to define the flow for a user manually adding a new holding to their portfolio.

```
flowId: FLOW_ADD_HOLDING_MANUAL
initialState: Idle
states:
  - name: Idle
    description: "The user is viewing the portfolio and has not yet initiated the process."
    events:
      USER_CLICKS_ADD_HOLDING: LookupInput

  - name: LookupInput
    description: "A modal appears prompting the user to enter a Ticker, ISIN, or WKN for the new holding."
    events:
      USER_SUBMITS_IDENTIFIER: SubmittingLookup

  - name: SubmittingLookup
    description: "The system is searching for the financial instrument."
    entryAction:
      service: "FinancialInstrumentLookupService.search(identifier)"
      transitions:
        success_unique: EnterLotDetails
        success_multiple: SelectFromMultiple
        failure: LookupError

  - name: SelectFromMultiple
    description: "The user is shown a list of matching instruments and must select one."
    events:
      USER_SELECTS_INSTRUMENT: EnterLotDetails

  - name: EnterLotDetails
    description: "The user is presented with a form to input the details of the first purchase lot (date, quantity, price)."
    events:
      USER_CLICKS_SAVE: ValidateForm

  - name: ValidateForm
    description: "The system is performing client-side validation on the form inputs."
    entryAction:
      service: "ValidationService.validate(form)"
      transitions:
        valid: SubmitHolding
        invalid: FormError

  - name: SubmitHolding
    description: "The system is submitting the new holding and lot data to the backend."
    entryAction:
      service: "POST /api/users/me/holdings"
      transitions:
        success: Success
        failure: APIError

  - name: Success
    description: "The user is shown a success message confirming the holding was added."
    exitAction:
      action: NAVIGATE_TO
      target: VIEW_PORTFOLIO_HOLDINGS

  - name: LookupError
    description: "The user is shown an error message that the instrument could not be found."
    events:
      USER_DISMISSES_ERROR: LookupInput

  - name: FormError
    description: "The user is shown an error message indicating which form fields are invalid."
    events:
      USER_DISMISSES_ERROR: EnterLotDetails

  - name: APIError
    description: "The user is shown a generic error message that the holding could not be saved."
    events:
      USER_DISMISSES_ERROR: EnterLotDetails
```
