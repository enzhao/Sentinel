# Supported Trading Rules

In Sentinel, a "rule" is made up of one or more "conditions." A condition is a specific market event that the system checks for you. You can combine multiple conditions to create a sophisticated and personal trading strategy.

This page lists all the rule conditions currently supported by Sentinel.

## Understanding the Technical Indicators

The conditions in Sentinel are based on common technical indicators used by traders and investors. Understanding what these indicators measure can help you build a more effective strategy. They are generally grouped by the type of information they provide.

### 📈 Trend Indicators
Trend indicators help you identify the direction and strength of a market trend over a period of time.

- **SMA (Simple Moving Average)**: This is the most basic trend indicator. It calculates the average price of a security over a specific number of periods (e.g., 50 days). An SMA creates a single, smoothed-out line on a chart, making it easier to see the underlying trend direction.
- **VWMA (Volume-Weighted Moving Average)**: This is a more advanced version of the SMA. It gives more weight to price points that had higher trading volume. The idea is that price movements with high volume are more significant than those with low volume.

### 🌡️ Momentum Indicators
Momentum indicators help measure the speed and strength of a security's price movement. They are often used to identify "overbought" (potentially too expensive) or "oversold" (potentially too cheap) conditions.

- **RSI (Relative Strength Index)**: This is a popular momentum indicator that measures the speed and change of price movements on a scale of 0 to 100. A reading above 70 is typically considered overbought, while a reading below 30 is considered oversold.
- **MACD (Moving Average Convergence Divergence)**: This indicator shows the relationship between two different moving averages of a security's price. When the MACD line crosses its "signal line," it can indicate a potential change in momentum (either bullish or bearish).

### 🎭 Market Sentiment Indicators
Sentiment indicators measure the overall mood of the market (e.g., fear vs. greed). They provide context about the broader market environment rather than the performance of a single security.

- **VIX (Volatility Index)**: Often called the "fear index," the VIX measures the market's expectation of volatility over the next 30 days. A high VIX reading (e.g., above 30) suggests high market fear and uncertainty, which some contrarian investors see as a potential buying opportunity.

---

## BUY Conditions 🟢

These conditions are used to create rules that trigger a "Buy" notification.

| Condition Name | Description | Parameters |
| :--- | :--- | :--- |
| **`DRAWDOWN_FROM_HIGH`** | Triggers when the price drops by a certain percentage from its 52-week high. A classic "buy the dip" signal. | `percentage`: The size of the drop (e.g., `20` for 20%). |
| **`RSI_LEVEL`** | Triggers when the Relative Strength Index (RSI) becomes oversold, suggesting the asset may be undervalued. | `threshold`: The RSI value to check against (e.g., `30`). |
| **`PRICE_VS_SMA`** | Triggers when the price crosses below a Simple Moving Average, which can signal a pullback in an uptrend. | `period`: The moving average period (e.g., `50` for the 50-day average). |
| **`PRICE_VS_VWMA`** | Triggers when the price crosses below a Volume-Weighted Moving Average. | `period`: The moving average period (e.g., `50`). |
| **`MACD_CROSSOVER`** | Triggers when the MACD line crosses above its signal line, a classic bullish momentum indicator. | None. This is a standard crossover event. |
| **`VIX_LEVEL`** | Triggers when the VIX (market fear index) rises above a certain level, used for contrarian strategies. | `threshold`: The VIX value to check against (e.g., `30`). |

## SELL Conditions 🔴

These conditions are used to create rules that trigger a "Sell" notification, either to take profit or to manage risk.

| Condition Name | Description | Parameters |
| :--- | :--- | :--- |
| **`PROFIT_TARGET`** | Triggers when your holding's pre-tax gain reaches a specific percentage, used to lock in profits. | `percentage`: The target gain (e.g., `50` for 50%). |
| **`STOP_LOSS`** | Triggers when your holding's pre-tax loss reaches a specific percentage, used for risk management. | `percentage`: The maximum loss (e.g., `10` for 10%). |
| **`TRAILING_STOP_LOSS`**| Triggers when the price drops by a percentage from its highest point since you purchased it, protecting gains. | `percentage`: The trailing drawdown (e.g., `15` for 15%). |
| **`RSI_LEVEL`** | Triggers when the Relative Strength Index (RSI) becomes overbought, suggesting the asset may be overvalued. | `threshold`: The RSI value to check against (e.g., `70`). |
| **`PRICE_VS_SMA`** | Triggers when the price crosses above a Simple Moving Average, which can signal over-extension from a trend. | `period`: The moving average period (e.g., `50`). |
| **`PRICE_VS_VWMA`** | Triggers when the price crosses above a Volume-Weighted Moving Average. | `period`: The moving average period (e.g., `50`). |
| **`MACD_CROSSOVER`** | Triggers when the MACD line crosses below its signal line, a classic bearish momentum indicator. | None. This is a standard crossover event. |