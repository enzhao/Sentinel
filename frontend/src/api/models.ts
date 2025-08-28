/**
 * TypeScript interfaces for the Sentinel API, generated from the OpenAPI spec.
 * These interfaces are used for type safety in the frontend application.
 */

// #############################################################################
// ENUMS
// #############################################################################

/** Reference: product_spec.md#9.2.1-primary-stored-models */
export type NotificationChannel = "EMAIL" | "PUSH";

/** Reference: product_spec.md#82-data-models */
export enum SubscriptionStatus {
    FREE = "FREE",
    PREMIUM = "PREMIUM",
}

/** Reference: product_spec.md#321-primary-stored-models */
export enum Currency {
    EUR = "EUR",
    USD = "USD",
    GBP = "GBP",
}

/** Reference: product_spec.md#421-primary-stored-models */
export enum SecurityType {
    STOCK = "STOCK",
    ETF = "ETF",
    FUND = "FUND",
}

/** Reference: product_spec.md#421-primary-stored-models */
export enum AssetClass {
    EQUITY = "EQUITY",
    CRYPTO = "CRYPTO",
    COMMODITY = "COMMODITY",
}

/** Reference: product_spec.md#621-stored-data-models */
export enum ParentType {
    PORTFOLIO = "PORTFOLIO",
    HOLDING = "HOLDING",
}

/** Reference: product_spec.md#621-stored-data-models */
export enum RuleType {
    BUY = "BUY",
    SELL = "SELL",
}

/** Reference: product_spec.md#621-stored-data-models */
export enum LogicalOperator {
    AND = "AND",
    OR = "OR",
}

/** Reference: product_spec.md#622-supported-conditions */
export enum ConditionType {
    DRAWDOWN_FROM_HIGH = "DRAWDOWN_FROM_HIGH",
    RSI_LEVEL = "RSI_LEVEL",
    PRICE_VS_SMA = "PRICE_VS_SMA",
    PRICE_VS_VWMA = "PRICE_VS_VWMA",
    MACD_CROSSOVER = "MACD_CROSSOVER",
    VIX_LEVEL = "VIX_LEVEL",
    PROFIT_TARGET = "PROFIT_TARGET",
    STOP_LOSS = "STOP_LOSS",
    TRAILING_STOP_LOSS = "TRAILING_STOP_LOSS",
}

/** Reference: product_spec.md#621-stored-data-models */
export enum RuleStatus {
    ENABLED = "ENABLED",
    PAUSED = "PAUSED",
}

/** Reference: product_spec.md#72-data-models */
export enum NotificationStatus {
    PENDING = "PENDING",
    SENT = "SENT",
    FAILED = "FAILED",
}

/** Reference: product_spec.md#335-p_5000-unified-transaction-import */
export enum AnnotatedTransactionAction {
    CREATE = "CREATE",
    UPDATE = "UPDATE",
}

// #############################################################################
// BASE & REUSABLE INTERFACES
// #############################################################################

/** Reference: product_spec.md#componentsschemasuuid */
export type UUID = string;

/** Reference: product_spec.md#componentsschemasisodatetime */
export type ISODateTime = string;

/** Reference: product_spec.md#componentsschemaserror */
export interface Error {
    code: string;
    message: string;
}

// #############################################################################
// USER INTERFACES
// #############################################################################

/** Reference: product_spec.md#82-data-models */
export interface User {
    readonly uid: string;
    username: string;
    readonly email: string;
    defaultPortfolioId: UUID;
    subscriptionStatus: SubscriptionStatus;
    notificationPreferences: NotificationChannel[];
    readonly createdAt: ISODateTime;
    readonly modifiedAt: ISODateTime;
}

/** Reference: product_spec.md#82-data-models */
export interface UpdateUserSettingsRequest {
    defaultPortfolioId: UUID;
    notificationPreferences?: NotificationChannel[];
}

// #############################################################################
// PORTFOLIO INTERFACES
// #############################################################################

/** Reference: product_spec.md#321-primary-stored-models */
export interface CashReserve {
    totalAmount: number;
    warChestAmount: number;
}

/** Reference: product_spec.md#321-primary-stored-models */
export interface Portfolio {
    readonly portfolioId: UUID;
    readonly userId: string;
    name: string;
    description?: string | null;
    defaultCurrency: Currency;
    cashReserve: CashReserve;
    ruleSetId?: UUID | null;
    readonly createdAt: ISODateTime;
    readonly modifiedAt: ISODateTime;
}

/** Reference: product_spec.md#322-time-series-subcollections */
export interface DailyPortfolioSnapshot {
    date: ISODateTime;
    totalCost: number;
    currentValue: number;
    preTaxGainLoss: number;
    afterTaxGainLoss: number;
    gainLossPercentage: number;
    sma7?: number | null;
    sma20?: number | null;
    sma50?: number | null;
    sma200?: number | null;
}

/** Reference: product_spec.md#331-p_1000-portfolio-creation */
export interface PortfolioCreationRequest {
    name: string;
    description?: string | null;
    defaultCurrency: Currency;
    cashReserve: CashReserve;
}

/** Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval */
export interface PortfolioSummary {
    portfolioId: UUID;
    name: string;
    currentValue: number;
}

/** Reference: product_spec.md#3331-p_3000-portfolio-update-manual */
export interface PortfolioUpdateRequest {
    name: string;
    description?: string | null;
    defaultCurrency: Currency;
    cashReserve: CashReserve;
}

/** Reference: product_spec.md#335-p_5000-unified-transaction-import */
export interface AnnotatedTransaction {
    ticker: string;
    purchaseDate: ISODateTime;
    quantity: number;
    purchasePrice: number;
    action: AnnotatedTransactionAction;
}

/** Reference: product_spec.md#335-p_5000-unified-transaction-import */
export interface TransactionImportReview {
    portfolioId: UUID;
    transactions: AnnotatedTransaction[];
}

/** Reference: product_spec.md#335-p_5000-unified-transaction-import */
export interface TransactionImportConfirmRequest {
    portfolioId: UUID;
    transactions: AnnotatedTransaction[];
}

// #############################################################################
// HOLDING & LOT INTERFACES
// #############################################################################

/** Reference: product_spec.md#522-on-the-fly-computed-models */
export interface ComputedInfoLot {
    currentPrice: number;
    currentValue: number;
    preTaxProfit: number;
    capitalGainTax: number;
    afterTaxProfit: number;
}

/** Reference: product_spec.md#521-primary-stored-models */
export interface Lot {
    readonly lotId: UUID;
    purchaseDate: ISODateTime;
    quantity: number;
    purchasePrice: number;
    readonly createdAt: ISODateTime;
    readonly modifiedAt: ISODateTime;
    computedInfo?: ComputedInfoLot;
}

/** Reference: product_spec.md#421-primary-stored-models */
export interface Holding {
    readonly holdingId: UUID;
    readonly portfolioId: UUID;
    readonly userId: string;
    ticker: string;
    ISIN?: string | null;
    WKN?: string | null;
    securityType: SecurityType;
    assetClass: AssetClass;
    currency: Currency;
    annualCosts?: number | null;
    readonly createdAt: ISODateTime;
    readonly modifiedAt: ISODateTime;
    lots: Lot[];
}

export interface MACD {
    value: number;
    signal: number;
    histogram: number;
}

/** Reference: product_spec.md#422-time-series-subcollections */
export interface DailyHoldingSnapshot {
    date: ISODateTime;
    totalCost: number;
    currentValue: number;
    preTaxGainLoss: number;
    afterTaxGainLoss: number;
    gainLossPercentage: number;
    sma7?: number | null;
    sma20?: number | null;
    sma50?: number | null;
    sma200?: number | null;
    vwma7?: number | null;
    vwma20?: number | null;
    vwma50?: number | null;
    vwma200?: number | null;
    rsi14?: number | null;
    macd?: MACD | null;
}

/** Reference: product_spec.md#4311-h_1000-financial-instrument-lookup */
export interface Instrument {
    ticker: string;
    ISIN?: string | null;
    WKN?: string | null;
    securityType: SecurityType;
    assetClass: AssetClass;
    currency: Currency;
}

/** Reference: product_spec.md#4311-h_1000-financial-instrument-lookup */
export interface InstrumentLookupRequest {
    identifier: string;
}

/** Reference: product_spec.md#4312-h_1200-holding-creation */
export interface HoldingCreationRequest {
    portfolioId: UUID;
    confirmedInstrument: Instrument;
    annualCosts?: number | null;
}

/** Reference: product_spec.md#4331-h_2000-holding-list-retrieval-portfolio-details-view */
export interface HoldingSummary {
    holdingId: UUID;
    ticker: string;
    securityType: SecurityType;
    assetClass: AssetClass;
    currency: Currency;
    totalCost: number;
    currentValue: number;
    preTaxGainLoss: number;
    gainLossPercentage: number;
}

/** Reference: product_spec.md#4341-h_3000-manual-holding-update */
export interface HoldingUpdateRequest {
    annualCosts?: number | null;
}

/** Reference: product_spec.md#437-h_6000-move-holding */
export interface MoveHoldingRequest {
    destinationPortfolioId: UUID;
}

/** Reference: product_spec.md#5311-l_1000-manual-creation */
export interface LotCreationRequest {
    purchaseDate: ISODateTime;
    quantity: number;
    purchasePrice: number;
}

/** Reference: product_spec.md#513-manual-update-of-a-single-lot */
export interface LotUpdateRequest {
    purchaseDate: ISODateTime;
    quantity: number;
    purchasePrice: number;
}

// #############################################################################
// RULESET INTERFACES
// #############################################################################

/** Reference: product_spec.md#621-stored-data-models */
export interface Condition {
    readonly conditionId: UUID;
    type: ConditionType;
    parameters: { [key: string]: any };
}

/** Reference: product_spec.md#621-stored-data-models */
export interface Rule {
    readonly ruleId: UUID;
    ruleType: RuleType;
    logicalOperator: LogicalOperator;
    conditions: Condition[];
    status: RuleStatus;
}

/** Reference: product_spec.md#621-stored-data-models */
export interface RuleSet {
    readonly ruleSetId: UUID;
    readonly userId: string;
    parentId: string;
    parentType: ParentType;
    rules: Rule[];
    readonly createdAt: ISODateTime;
    readonly modifiedAt: ISODateTime;
}

/** Reference: product_spec.md#631-r_1000-rule-set-creation */
export interface RuleSetCreationRequest {
    parentId: string;
    parentType: ParentType;
    rules: Rule[];
}

/** Reference: product_spec.md#633-r_3000-rule-set-update */
export interface RuleSetUpdateRequest {
    rules: Rule[];
}

// #############################################################################
// ALERT INTERFACES
// #############################################################################

/** Reference: product_spec.md#72-data-models */
export interface MarketDataSnapshot {
    closePrice: number;
    rsi14?: number | null;
    sma200?: number | null;
}

/** Reference: product_spec.md#72-data-models */
export interface TriggeredCondition {
    type: ConditionType;
    parameters: { [key: string]: any };
    actualValue: number;
}

/** Reference: product_spec.md#72-data-models */
export interface TaxInfo {
    preTaxProfit: number;
    capitalGainTax: number;
    afterTaxProfit: number;
    appliedTaxRate: number;
}

/** Reference: product_spec.md#72-data-models */
export interface Alert {
    readonly alertId: UUID;
    readonly userId: string;
    readonly holdingId: UUID;
    readonly ruleSetId: UUID;
    readonly ruleId: UUID;
    readonly triggeredAt: ISODateTime;
    isRead: boolean;
    marketDataSnapshot: MarketDataSnapshot;
    triggeredConditions: TriggeredCondition[];
    taxInfo?: TaxInfo | null;
    notificationStatus: NotificationStatus;
}

/** Reference: product_spec.md#743-a_3000-mark-alerts-as-read */
export interface AlertUpdateRequest {
    alertId: UUID;
    isRead: boolean;
}
