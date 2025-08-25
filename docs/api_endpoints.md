# Sentinel API Endpoints (v0.1)

This document provides a comprehensive list of all API endpoints for the Sentinel v0.1 MVP. All endpoints are prefixed with `/api/users/me/`.

---

## Portfolios & Settings

- `POST /portfolios`
  - Creates a new portfolio.

- `GET /portfolios`
  - Retrieves a summary list of all of the user's portfolios.

- `GET /portfolios/{portfolioId}`
  - Retrieves the full details of a single portfolio.

- `PUT /portfolios/{portfolioId}`
  - Updates a specific portfolio's settings.

- `DELETE /portfolios/{portfolioId}`
  - Deletes an entire portfolio.

- `POST /portfolios/{portfolioId}/transactions/import`
  - Initiates a transaction import from a file for a specific portfolio.

- `POST /portfolios/{portfolioId}/transactions/import/confirm`
  - Confirms the parsed data from the transaction import.
  
- **`GET /portfolios/{portfolioId}/chart-data`**
  - **Retrieves aggregated, time-series data for performance charts.**

- `PUT /settings`
  - Updates user-level settings, such as the default portfolio.

---

## Holdings

- `POST /holdings/lookup`
  - Searches for a financial instrument by an identifier.

- `POST /holdings`
  - Creates a new, empty holding within a portfolio.

- `GET /portfolios/{portfolioId}/holdings`
  - Retrieves a list of all holdings for a specific portfolio.

- `GET /holdings/{holdingId}`
  - Retrieves the full details of a single holding, including its lots.

- `PUT /holdings/{holdingId}`
  - Updates a specific holding's metadata.

- `DELETE /holdings/{holdingId}`
  - Deletes an entire holding.

- `POST /holdings/{holdingId}/move`
  - Moves a holding to a different portfolio.

- **`GET /holdings/{holdingId}/chart-data`**
  - **Retrieves aggregated, time-series data for performance charts.**

---

## Lots (Purchases)

- `POST /holdings/{holdingId}/lots`
  - Adds a new purchase lot to an existing holding.

- `PUT /holdings/{holdingId}/lots/{lotId}`
  - Updates the details of a specific lot.

- `DELETE /holdings/{holdingId}/lots/{lotId}`
  - Deletes a specific lot from a holding.

---

## Strategy Rules

- `POST /rulesets`
  - Creates a new `RuleSet` for a portfolio or holding.

- `GET /holdings/{holdingId}/effective-rules`
  - Retrieves the effective (specific or inherited) `RuleSet` for a holding.

- `PUT /rulesets/{ruleSetId}`
  - Updates an existing `RuleSet`.

- `DELETE /rulesets/{ruleSetId}`
  - Deletes a `RuleSet`.

---

## Alerts (Notifications)

- `GET /alerts`
  - Retrieves a list of all historical alerts for the user.

- `GET /alerts/{alertId}`
  - Retrieves the details of a single alert.

- `PATCH /alerts`
  - Updates the status of one or more alerts (e.g., marks them as read).