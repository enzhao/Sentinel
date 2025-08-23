# View DSL for Sentinel Frontend

## 1. Purpose and Audience

This document defines the lightweight Domain-Specific Language (DSL) used within `product_spec.md` to formally describe the static structure and components of a single frontend "View" (e.g., a screen or a modal).

The primary purpose is to provide:
- **For Human Readers (Developers, PMs, Testers):** A clear, declarative blueprint of every screen in the application.
- **For AI Automation Agents:** A formal, parsable specification that can be directly translated into frontend component code.

## 2. Core Principles: Structure, Behavior, and Presentation

This DSL is designed to integrate cleanly with two other key parts of the system: the **Flow DSL** for behavior and **CSS** for presentation. Understanding the separation of concerns is essential.

- **View DSL (This document) defines *Structure*:** It specifies *what* components are present on a view and their logical grouping. It answers: What does this screen contain?

- **Flow DSL (`state_machine_dsl.md`) defines *Behavior*:** It describes the dynamic, event-driven user journey. It answers: How does the application state change when the user interacts with the view?

- **CSS (in application codebase) defines *Presentation*:** It controls the visual appearance, including layout, orientation, and responsiveness. It answers: How should this component look on a mobile phone versus a desktop?

A `View` (defined here) dispatches an `event`. A `Flow` (state machine) listens for that `event` and determines the application's response.

### The Semantic Component with Full Design Flexibility

This DSL intentionally omits keywords for defining layout orientation (e.g., `direction: 'horizontal'`). This is a deliberate design choice. Instead of describing visual layout, the DSL focuses on describing **semantic components**.

A semantic component is a component defined by its *meaning or purpose*, not its appearance.

For example, instead of a generic `ButtonGroup` with an `orientation` property, the DSL specifies a `FormActions` component.

- **The DSL specifies:** "This view must include the primary and secondary form actions."
- **The CSS implements:** The `FormActions` component uses CSS (e.g., Flexbox, Grid, media queries) to display its buttons side-by-side on a wide screen and stacked vertically on a narrow mobile screen.

This approach ensures the specification is not brittle. It gives designers and developers the flexibility to create a fully responsive UI without being constrained by the logical spec, which correctly remains focused on structure and purpose.

## 3. View DSL Syntax and Keywords

Each view is defined by a root object with a unique `viewId`.

### 3.1. Top-Level Keywords

- `viewId` (String, Required): A unique identifier for the view, following the `VIEW_XXXX` convention (e.g., `VIEW_2000`, `VIEW_PORTFOLIO_DETAIL`).
- `title` (String, Required): The user-facing title of the view, often used in the AppBar or as the page title.
- `requiresAuth` (Boolean, Required): If `true`, the user must be authenticated to access this view. If `false`, it is a public view (e.g., Login, Signup).
- `description` (String, Required): A human-readable explanation of the view's purpose.
- `data` (Array, Optional): A list of data objects the view requires to render. Each object has:
    - `name` (String): The variable name for the data (e.g., "portfolio").
    - `type` (String): The data type (e.g., "Portfolio", "Array<Holding>").
    - `description` (String): A description of the data.
- `components` (Array, Required): A list of UI components that make up the view's layout. Typically, this will be a single "Layout Component".

### 3.2. Component Object Keywords

Each object in the `components` array represents a single UI element.

- `type` (String, Required): The type of the component. This can be the name of a **primitive component** (e.g., `Button`, `TextField`) or the **`viewId` of another view** to include it compositionally. See the "View Composition" section for details.
- `shownIf` (String, Optional): A declarative condition, based on the view's `data`, that determines if the component is rendered. (e.g., `"portfolio.holdings.length > 0"`).
- `props` (Object, Optional): A key-value map of static properties passed to the component (e.g., `title: "My Portfolio"`).
- `bindings` (Object, Optional): A key-value map that declaratively binds data from the `data` block to the component's properties (e.g., `totalValue: "portfolio.computed.currentValue"`). This is also used to pass data to child views.
- `item` (Object, Optional): Used for list components. It describes how to render each item in a collection.
    - `forEach` (String, Required): Defines the loop variable and the data source (e.g., `"holding in portfolio.holdings"`).
    - `component` (Object, Required): A standard component object definition for the list item.
- `events` (Object, Optional): Defines user interactions that dispatch events to the controlling Flow (state machine).
    - **Key:** The name of the interaction handler (e.g., `onTap`, `onClick`).
    - **Value:** An object describing the event:
        - `name` (String, Required): The event name in `UPPER_SNAKE_CASE` (e.g., `USER_SELECTS_HOLDING`).
        - `payload` (Object, Optional): A key-value map of data to send with the event (e.g., `holdingId: "holding.holdingId"`).
- `leadingAction` (Object, Optional): Defines a singular, primary action, typically positioned on the "leading" (left) side of a component. This is distinct from the `actions` array and is most often used in an `AppBar`.
    - `event` (String, Required): The `UPPER_SNAKE_CASE` event name dispatched when the action is triggered.
    - `label` (String, Optional): The text label for the action.
    - `icon` (String, Optional): The name of the icon for the action.
    - **Note**: At least one of `label` or `icon` must be provided.
- `actions` (Array, Optional): A list of actions, typically for the "trailing" (right) side of an `AppBar` or for a Floating Action Button's speed-dial menu. Each action object is defined as follows:
    - `event` (String, Required): The `UPPER_SNAKE_CASE` event name dispatched when the action is triggered.
    - `label` (String, Optional): The text label for the action.
    - `icon` (String, Optional): The name of the icon for the action.
    - **Note**: At least one of `label` or `icon` must be provided.
- `slots` (Object, Optional): Used by "Layout Components" to define named regions where other components are placed.
    - **Key:** The name of the slot (e.g., `header`, `body`, `fab`).
    - **Value:** An array of component objects to be rendered inside that slot.

## 4. The Layout Component Pattern

To ensure a consistent structure across different views, we use a "Layout Component" pattern. Instead of listing every component (like AppBars and FABs) in every view, a view's `components` array will typically contain a single, top-level Layout Component (e.g., `StandardLayout`).

This Layout Component defines named `slots` (like `header`, `body`, and `fab`), and the view places all its content components inside these slots. This approach makes the overall structure of the application explicit, reusable, and easy to understand.

## 5. View Composition and Reusability

To promote modularity and a DRY (Don't Repeat Yourself) design, the View DSL supports the inclusion of one view within another. This allows complex UIs to be composed from smaller, self-contained, and reusable view components.

### 5.1. The Inclusion Convention

The mechanism for inclusion is simple and declarative:
> If a component's `type` value matches the `viewId` of another defined view, it is treated as an **inclusion** of that view.

### 5.2. Passing Data to Child Views

A parent view passes data to an included child view using the standard `bindings` keyword. The child view must declare the data it requires in its own `data` block. The parent view's `bindings` then fulfill this data contract.

### 5.3. Example of View Composition

Here, `VIEW_HOLDING_DETAIL` is a parent view that needs to display a list of lots. Instead of defining the list inline, it **includes** the `VIEW_LOTS_LIST`.

**Child View (`VIEW_LOTS_LIST`)**

This view is defined once. It declares that it needs a list of `lots` and a `mode` to function.

```yaml
viewId: VIEW_LOTS_LIST
requiresAuth: true
description: "A reusable view component that displays a list of purchase lots."

data:
  # This view declares its data dependencies.
  - name: "lots"
    type: "Array<Lot>"
  - name: "mode"
    type: "String"

components:
  - type: "LotList"
    # ... (rest of the list definition)
``` 

**Parent View (`VIEW_HOLDING_DETAIL`)**

This view includes `VIEW_LOTS_LIST` and uses `bindings` to pass the required data down to it.

```yaml
viewId: VIEW_HOLDING_DETAIL
title: "Holding Details"
requiresAuth: true
description: "A detail view for a specific holding."

data:
  - name: "holding"
    type: "Holding"
  - name: "currentMode"
    type: "String"

components:
  - type: "StandardLayout"
    slots:
      body:
        - type: "HoldingSummaryCard"
          # ...
        # Here we include the child view by using its viewId as the type.
        - type: "VIEW_LOTS_LIST"
          # We use bindings to pass data from the parent (holding, currentMode)
          # to the child's declared data requirements (lots, mode).
          bindings:
            lots: "holding.lots"
            mode: "currentMode"
```


## 6. Example: Holding Overview View

The following example illustrates how the DSL is used to define the main dashboard view, using the Layout Component pattern.

```yaml
viewId: VIEW_2000
title: "Holding Overview"
requiresAuth: true
description: "The main dashboard view, displaying a summary of the user's default portfolio and a list of their holdings."

data:
  - name: "portfolio"
    type: "Portfolio"
    description: "The user's default portfolio, including a summary list of its holdings."

components:
  - type: "StandardLayout"
    slots:
      # The header slot contains the AppBar.
      header:
        - type: "AppBar"
          props:
            title: "My Portfolio"

      # The body slot contains the main content of the view.
      body:
        - type: "PortfolioSummaryCard"
          shownIf: "portfolio.holdings.length > 0"
          bindings:
            totalValue: "portfolio.computed.currentValue"
            gainLoss: "portfolio.computed.preTaxGainLoss"

        - type: "HoldingList"
          shownIf: "portfolio.holdings.length > 0"
          item:
            forEach: "holding in portfolio.holdings"
            component:
              type: "HoldingListItem"
              bindings:
                name: "holding.ticker"
                value: "holding.computed.currentValue"
              events:
                onTap:
                  name: "USER_SELECTS_HOLDING"
                  payload:
                    holdingId: "holding.holdingId"

        - type: "EmptyState"
          shownIf: "portfolio.holdings.length == 0"
          props:
            title: "Your portfolio is empty"
            message: "Add a holding or import a file to get started."

      # The fab slot contains the Floating Action Button.
      fab:
        - type: "FloatingActionButton"
          props:
            icon: "add"
          actions:
            - label: "Add Holding"
              event: "USER_CLICKS_ADD_HOLDING"
            - label: "Import File"
              event: "USER_CLICKS_IMPORT"
```