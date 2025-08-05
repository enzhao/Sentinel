# View DSL for Sentinel Frontend

## 1. Purpose and Audience

This document defines the lightweight Domain-Specific Language (DSL) used within `product_spec.md` to formally describe the static structure and components of a single frontend "View" (e.g., a screen or a modal).

This DSL is designed to work in tandem with the **Flow DSL** (defined in `state_machine_dsl.md`). While the Flow DSL describes the dynamic, event-driven user journey *between* views, this View DSL describes the static layout, data requirements, and component composition *of each individual view*.

The primary purpose is to provide:
- **For Human Readers (Developers, PMs, Testers):** A clear, declarative blueprint of every screen in the application, detailing what it shows, what data it needs, and what user interactions it supports.
- **For AI Automation Agents:** A formal, parsable specification that can be directly translated into frontend component code, including data bindings, conditional rendering logic, and event handlers.

## 2. Relationship to the Flow DSL

The View DSL and Flow DSL are complementary and work together:

- **View DSL (This document):** Defines the **"What"**.
    - What components are on the screen? (`components`)
    - What data does the screen need? (`data`)
    - Under what conditions are components visible? (`shownIf`)
    - What events can the user trigger? (`events`)

- **Flow DSL (`state_machine_dsl.md`):** Defines the **"How"**.
    - How does the application respond to an event from a view?
    - How does the user navigate from one view to another?
    - How is application state managed during a user journey?

A `View` dispatches an `event`. A `Flow` (state machine) listens for that `event` and determines the application's response.

## 3. View DSL Syntax and Keywords

Each view is defined by a root object with a unique `viewId`.

### 3.1. Top-Level Keywords

- `viewId` (String, Required): A unique identifier for the view, following the `VIEW_XXXX` convention (e.g., `VIEW_2000`, `VIEW_PORTFOLIO_DETAIL`).
- `title` (String, Required): The user-facing title of the view, often used in the AppBar or as the page title.
- `description` (String, Required): A human-readable explanation of the view's purpose.
- `data` (Array, Optional): A list of data objects the view requires to render. Each object has:
    - `name` (String): The variable name for the data (e.g., "portfolio").
    - `type` (String): The data type (e.g., "Portfolio", "Array<Holding>").
    - `description` (String): A description of the data.
- `components` (Array, Required): A list of UI components that make up the view's layout.

### 3.2. Component Object Keywords

Each object in the `components` array represents a single UI element.

- `type` (String, Required): The type of the component (e.g., `AppBar`, `Button`, `HoldingList`, `EmptyState`).
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
- `actions` (Array, Optional): A list of actions, typically for components like a Floating Action Button. Each action object has:
    - `label` (String, Required): The text for the action.
    - `event` (String, Required): The `UPPER_SNAKE_CASE` event name dispatched when the action is triggered.

## 4. Example: Holding Overview View

The following example illustrates how the DSL is used to define the main dashboard view.

```yaml
viewId: VIEW_2000
title: "Holding Overview"
description: "The main dashboard view, displaying a summary of the user's default portfolio and a list of their holdings."

# The data this view requires to render.
data:
  - name: "portfolio"
    type: "Portfolio"
    description: "The user's default portfolio, including a summary list of its holdings."

# The components that build the UI.
components:
  - type: "AppBar"
    props:
      title: "My Portfolio"

  - type: "PortfolioSummaryCard"
    # Declarative rendering based on data state.
    shownIf: "portfolio.holdings.length > 0"
    # Declarative data binding.
    bindings:
      totalValue: "portfolio.computed.currentValue"
      gainLoss: "portfolio.computed.preTaxGainLoss"

  - type: "HoldingList"
    shownIf: "portfolio.holdings.length > 0"
    # Describes how to render each item in a list.
    item:
      # Binds each item in the list to the 'holding' variable.
      forEach: "holding in portfolio.holdings"
      component:
        type: "HoldingListItem"
        bindings:
          name: "holding.ticker"
          value: "holding.computed.currentValue"
        # User interactions dispatch events with a payload.
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

  - type: "FloatingActionButton"
    props:
      icon: "add"
    # Actions within a component also dispatch events.
    actions:
      - label: "Add Holding"
        event: "USER_CLICKS_ADD_HOLDING"
      - label: "Import File"
        event: "USER_CLICKS_IMPORT"
```