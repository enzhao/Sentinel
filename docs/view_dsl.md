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

- `viewId` (String, Required): A unique identifier for the view, following the `VIEW_XXXX` convention (e.g., `VIEW_DASHBOARD`, `VIEW_PORTFOLIO_DETAIL`).
- `title` (String, Required): The user-facing title of the view, often used in the AppBar or as the page title.
- `requiresAuth` (Boolean, Required): If `true`, the user must be authenticated to access this view. If `false`, it is a public view.
- `description` (String, Required): A human-readable explanation of the view's purpose.
- `data` (Array, Optional): A list of data objects the view requires to render. Each object has:
    - `name` (String): The variable name for the data (e.g., "portfolio").
    - `type` (String): The data type (e.g., "Portfolio", "Array<Holding>").
    - `description` (String): A description of the data.
- `components` (Array, Required): A list of UI components that make up the view's layout.

### 3.2. Component Object Keywords

Each object in the `components` array represents a single UI element.

- `type` (String, Required): The type of the component. This can be the name of a **primitive component** (e.g., `Button`, `TextField`) or the **`viewId` of another view** to include it compositionally.
- `shownIf` (String, Optional): A declarative condition, based on the view's `data`, that determines if the component is rendered. (e.g., `"portfolio.holdings.length > 0"`).
- `props` (Object, Optional): A key-value map of static properties passed to the component (e.g., `title: "My Portfolio"`).
- `bindings` (Object, Optional): A key-value map that declaratively binds data from the `data` block to the component's properties (e.g., `totalValue: "portfolio.computed.currentValue"`).
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
- `alertAction` (Object, Optional): Defines the dedicated notification alert action, typically an icon with a badge, within a component like an `AppBar`.
    - `icon` (String, Required): The name of the icon to display.
    - `event` (String, Required): The `UPPER_SNAKE_CASE` event name dispatched when the action is triggered.
    - `bindings` (Object, Optional): Used to bind data to the action's properties, such as the visibility of a notification badge (e.g., `badgeVisible: "alertInfo.hasUnread"`).
- `actions` (Array, Optional): A list of actions, typically for the "trailing" (right) side of an `AppBar` or for a Floating Action Button's speed-dial menu. Each action object is defined as follows:
    - `event` (String, Required): The `UPPER_SNAKE_CASE` event name dispatched when the action is triggered.
    - `label` (String, Optional): The text label for the action.
    - `icon` (String, Optional): The name of the icon for the action.
    - **Note**: At least one of `label` or `icon` must be provided.
- `slots` (Object, Optional): Used by "Layout Components" to define named regions where other components are placed.
    - **Key:** The name of the slot (e.g., `header`, `body`, `fab`).
    - **Value:** An array of component objects to be rendered inside that slot.
- `MultiSelect` (Object, Optional): A component for selecting multiple options from a predefined list.
    - `type` (String, Required): Must be `"MultiSelect"`.
    - `props` (Object, Required):
        - `label` (String, Required): The label for the multi-select input.
        - `options` (Array<String>, Required): The list of available options to choose from.
    - `bindings` (Object, Required):
        - `selected` (String, Required): Binds to a data property that holds the currently selected options (e.g., `"user.notificationPreferences"`).
    - `events` (Object, Required):
        - `onUpdate` (Object, Required):
            - `name` (String, Required): The event name dispatched when the selection changes (e.g., `USER_UPDATES_NOTIFICATION_PREFERENCES`).
            - `payload` (Object, Required):
                - `value` (String, Required): The new array of selected options (e.g., `"$event.value"`).

## 4. Core Patterns: Composition and Layout

To promote a modular, consistent, and DRY (Don't Repeat Yourself) design, the View DSL relies on two core patterns: View Composition and the Layout Component.

### 4.1. View Composition and Reusability

The most powerful feature of the DSL is the ability to include one view within another. This allows complex UIs to be composed from smaller, self-contained, and reusable view components.

- **The Inclusion Convention**: If a component's `type` value matches the `viewId` of another defined view, it is treated as an **inclusion** of that view.
- **Passing Data to Child Views**: A parent view passes data to an included child view using the standard `bindings` keyword. The child view must declare the data it requires in its own `data` block. The parent view's `bindings` then fulfill this data contract.

### 4.2. The Layout Component Pattern

To ensure a consistent structure across different screens, a view's `components` array will typically contain a single, top-level Layout Component (e.g., `StandardLayout`). This component defines named `slots` (like `header`, `body`, and `fab`), and the view places all its content components inside these slots. This approach makes the overall structure of the application explicit and easy to understand.

## 5. Example: Holding Detail View

The following example for `VIEW_HOLDING_DETAIL` illustrates how all the core patterns of the DSL work together. It uses a `StandardLayout`, composes other views like `VIEW_APP_BAR` and `VIEW_LOTS_LIST`, passes data via `bindings`, and defines a Floating Action Button with a speed-dial menu.

```yaml
# A detail view for a specific holding, which also embeds the Lot List component.
viewId: VIEW_HOLDING_DETAIL
title: "Holding Details"
requiresAuth: true
description: "A detail view for a specific holding, which also embeds the Lot List component."

data:
  - name: "holding"
    type: "Holding"
  - name: "currentMode"
    type: "String"

components:
  - type: "StandardLayout"
    slots:
      # It includes the reusable AppBar and binds the required data.
      header:
        - type: "VIEW_APP_BAR"
          bindings:
            title: "holding.ticker"
            leadingAction:
              icon: "arrow_back"
              event: "USER_CLICKS_BACK"
            actions:
              - icon: "logout"
                event: "USER_CLICKS_LOGOUT"
      
      # The body contains primitive components and another composed view.
      body:
        - type: "HoldingSummaryCard"
          bindings:
            totalCost: "holding.computed.totalCost"
            currentValue: "holding.computed.currentValue"
            preTaxGainLoss: "holding.computed.preTaxGainLoss"

        - type: "VIEW_LOTS_LIST"
          bindings:
            lots: "holding.lots"
            mode: "currentMode"
      
      # The FAB uses a speed-dial menu for contextual actions.
      fab:
        - type: "FloatingActionButton"
          props:
            icon: "more_vert"
          actions:
            - icon: "rule"
              label: "Manage Rules"
              event: "USER_CLICKS_MANAGE_RULES"
            - icon: "edit"
              label: "Edit Holding"
              event: "USER_CLICKS_EDIT"
            - icon: "swap_horiz"
              label: "Move Holding"
              event: "USER_CLICKS_MOVE"
            - icon: "delete"
              label: "Delete Holding"
              event: "USER_CLICKS_DELETE"
```
