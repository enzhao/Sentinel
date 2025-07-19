# Product Specification for Sentinel v0.1 (MVP)

## 0. Introduction

### 0.1. Purpose and Audience

Sentinel is a personal investment strategy automation tool designed for disciplined, long-term retail investors. This document outlines the product specifications for the Minimum Viable Product (MVP) of Sentinel, serving as the foundational agreement for the initial development cycle.

The primary purpose of this document is to establish a single source of truth that eliminates ambiguity and ensures a shared, precise understanding of the MVP's scope, functionality, and underlying logic.

This document is written for the following audience:

- The Product Owner/Lead Developer: To provide a clear and structured vision of the end product, ensuring all development efforts are aligned with the core objectives.
- Future Development & Testing Teams: To serve as a systematic guide for implementation and a comprehensive reference for validation and quality assurance.

### 0.2. Core Problem and Vision

The modern retail investor faces several core challenges:

1.  Time & Energy Deficit: A lack of time and energy to constantly monitor markets.
2.  Cost Barrier: The high cost of professional wealth management services.
3.  The Behavioral Gap: The well-documented gap between a market index's theoretical return (Beta) and the average investor's actual, lower return. This gap is caused almost entirely by emotional decision-making (e.g., panic selling during crashes, euphoric buying at peaks) that derails even the simplest long-term strategies.

Sentinel is envisioned to solve these problems by empowering users to encode their own long-term investment philosophy into a set of clear, automated rules. The app will act as a tireless, unemotional **behavioral guardrail**, providing timely, actionable notifications based on the user's own strategy. This allows the user to remain in complete control of their capital and decisions, while delegating the tedious task of market-watching and opportunity-spotting to the tool.

### 0.3. Document Structure

This document is organized to provide a systematic overview of the product, from high-level strategy to detailed functional requirements.

- Chapter 0: Introduction: This section.
- Chapter 1: Core Investment Strategies: A concise description of the investment philosophies that the Sentinel MVP will be built to support. This is the "Why" behind the features.
- Chapter 2: Functional Requirements: A detailed breakdown of the app's features and user-facing components for the MVP.
- Chapter 3: Non-Functional Requirements: Specifications regarding data sources, security, and performance.

---

## 1. Core Investment Strategies

Sentinel is not a tool for day trading or market speculation. It is built upon a hybrid "Core-Satellite" investment model designed for patient capital accumulation and risk management. The MVP will support the following two interconnected strategies.

### 1.1. Core Strategy: Systematic Accumulation

This strategy forms the stable foundation of the user's portfolio. It is a non-emotional, automated approach to building wealth over the long term by consistently investing in broad market index funds (ETFs).

- Mechanism: The user allocates a fixed portion of their monthly disposable income to a "无脑定投" (Systematic Regular Investment) plan.
- Objective: To achieve market-average returns (Beta) through dollar-cost averaging, thereby smoothing out market volatility and ensuring the user is always participating in the market's long-term upward trend.

### 1.2. Satellite Strategy: Opportunistic Rebalancing

This strategy is designed to enhance returns (Alpha) by making disciplined, rule-based decisions during periods of extreme market sentiment. It consists of two sides of the same coin: buying during market panic and selling during market euphoria. The funds for this strategy are sourced from the other portion of the user's monthly disposable income, which is accumulated as a cash "war chest."

#### 1.2.1. Buy Triggers ("捡便宜" - Buying the Dip)

This is the process of deploying the accumulated cash reserve when market downturns present attractive entry points. The objective is to acquire quality assets at a significant discount to their recent highs. The MVP will support triggers based on:

- Significant Market Drawdowns: Buying when a target index (e.g., NASDAQ-100) falls by a predefined percentage (e.g., 10%, 20%, 30%) from its recent peak.
- Extreme Fear Indicators: Buying when market sentiment indicators signal capitulation (e.g., VIX index spiking above a certain level, RSI entering an "oversold" state).

#### 1.2.2. Sell Triggers ("锁定利润" - Locking in Profits)

This is a risk-management process designed to systematically secure paper profits and rebalance the portfolio when the market becomes over-extended and euphoric. The objective is to reduce risk exposure and replenish the cash "war chest" for future buying opportunities. The MVP will support triggers based on:

- Portfolio Rebalancing: Selling a portion of an asset when its weight in the portfolio exceeds a predefined target due to significant appreciation.
- Extreme Greed Indicators: Selling when market sentiment indicators signal euphoria (e.g., RSI entering an "overbought" state, price extending significantly above its long-term moving average).

