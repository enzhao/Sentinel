"""
Pydantic models for the Sentinel API, generated from the OpenAPI spec.
These models are used for request and response validation.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

# #############################################################################
# ENUMS
# #############################################################################

class SubscriptionStatus(str, Enum):
    """ Reference: product_spec.md#82-data-models """
    FREE = "FREE"
    PREMIUM = "PREMIUM"

class Currency(str, Enum):
    """ Reference: product_spec.md#321-primary-stored-models """
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"

class SecurityType(str, Enum):
    """ Reference: product_spec.md#421-primary-stored-models """
    STOCK = "STOCK"
    ETF = "ETF"
    FUND = "FUND"

class AssetClass(str, Enum):
    """ Reference: product_spec.md#421-primary-stored-models """
    EQUITY = "EQUITY"
    CRYPTO = "CRYPTO"
    COMMODITY = "COMMODITY"

class ParentType(str, Enum):
    """ Reference: product_spec.md#621-stored-data-models """
    PORTFOLIO = "PORTFOLIO"
    HOLDING = "HOLDING"

class RuleType(str, Enum):
    """ Reference: product_spec.md#621-stored-data-models """
    BUY = "BUY"
    SELL = "SELL"

class LogicalOperator(str, Enum):
    """ Reference: product_spec.md#621-stored-data-models """
    AND = "AND"
    OR = "OR"

class ConditionType(str, Enum):
    """ Reference: product_spec.md#622-supported-conditions """
    DRAWDOWN_FROM_HIGH = "DRAWDOWN_FROM_HIGH"
    RSI_LEVEL = "RSI_LEVEL"
    PRICE_VS_SMA = "PRICE_VS_SMA"
    PRICE_VS_VWMA = "PRICE_VS_VWMA"
    MACD_CROSSOVER = "MACD_CROSSOVER"
    VIX_LEVEL = "VIX_LEVEL"
    PROFIT_TARGET = "PROFIT_TARGET"
    STOP_LOSS = "STOP_LOSS"
    TRAILING_STOP_LOSS = "TRAILING_STOP_LOSS"

class RuleStatus(str, Enum):
    """ Reference: product_spec.md#621-stored-data-models """
    ENABLED = "ENABLED"
    PAUSED = "PAUSED"

class NotificationStatus(str, Enum):
    """ Reference: product_spec.md#72-data-models """
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class AnnotatedTransactionAction(str, Enum):
    """ Reference: product_spec.md#335-p_5000-unified-transaction-import """
    CREATE = "CREATE"
    UPDATE = "UPDATE"

# #############################################################################
# BASE & REUSABLE MODELS
# #############################################################################

class UUID(str):
    """ Reference: product_spec.md#componentsschemasuuid """
    pass

class ISODateTime(datetime):
    """ Reference: product_spec.md#componentsschemasisodatetime """
    pass

class Error(BaseModel):
    """ Reference: product_spec.md#componentsschemaserror """
    code: str
    message: str

# #############################################################################
# USER MODELS
# #############################################################################

class NotificationPreferences(BaseModel):
    """ Reference: product_spec.md#82-data-models """
    email: bool = True
    push: bool = False

class User(BaseModel):
    """ Reference: product_spec.md#82-data-models """
    uid: str
    username: str
    email: str
    defaultPortfolioId: UUID
    subscriptionStatus: SubscriptionStatus
    notificationPreferences: NotificationPreferences
    createdAt: ISODateTime
    modifiedAt: ISODateTime

class UpdateUserSettingsRequest(BaseModel):
    """ Reference: product_spec.md#82-data-models """
    defaultPortfolioId: UUID
    notificationPreferences: Optional[NotificationPreferences] = None

# #############################################################################
# PORTFOLIO MODELS
# #############################################################################

class CashReserve(BaseModel):
    """ Reference: product_spec.md#321-primary-stored-models """
    totalAmount: float
    warChestAmount: float

class Portfolio(BaseModel):
    """ Reference: product_spec.md#321-primary-stored-models """
    portfolioId: UUID
    userId: str
    name: str
    description: Optional[str] = None
    defaultCurrency: Currency
    cashReserve: CashReserve
    ruleSetId: Optional[UUID] = None
    createdAt: ISODateTime
    modifiedAt: ISODateTime

class DailyPortfolioSnapshot(BaseModel):
    """ Reference: product_spec.md#322-time-series-subcollections """
    date: ISODateTime
    totalCost: float
    currentValue: float
    preTaxGainLoss: float
    afterTaxGainLoss: float
    gainLossPercentage: float
    sma7: Optional[float] = None
    sma20: Optional[float] = None
    sma50: Optional[float] = None
    sma200: Optional[float] = None

class PortfolioCreationRequest(BaseModel):
    """ Reference: product_spec.md#331-p_1000-portfolio-creation """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    defaultCurrency: Currency
    cashReserve: CashReserve

class PortfolioSummary(BaseModel):
    """ Reference: product_spec.md#3322-p_2200-portfolio-list-retrieval """
    portfolioId: UUID
    name: str
    currentValue: float

class PortfolioUpdateRequest(BaseModel):
    """ Reference: product_spec.md#3331-p_3000-portfolio-update-manual """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    defaultCurrency: Currency
    cashReserve: CashReserve

class AnnotatedTransaction(BaseModel):
    """ Reference: product_spec.md#335-p_5000-unified-transaction-import """
    ticker: str
    purchaseDate: ISODateTime
    quantity: float
    purchasePrice: float
    action: AnnotatedTransactionAction

class TransactionImportReview(BaseModel):
    """ Reference: product_spec.md#335-p_5000-unified-transaction-import """
    portfolioId: UUID
    transactions: List[AnnotatedTransaction]

class TransactionImportConfirmRequest(BaseModel):
    """ Reference: product_spec.md#335-p_5000-unified-transaction-import """
    portfolioId: UUID
    transactions: List[AnnotatedTransaction]

# #############################################################################
# HOLDING & LOT MODELS
# #############################################################################

class ComputedInfoLot(BaseModel):
    """ Reference: product_spec.md#522-on-the-fly-computed-models """
    currentPrice: float
    currentValue: float
    preTaxProfit: float
    capitalGainTax: float
    afterTaxProfit: float

class Lot(BaseModel):
    """ Reference: product_spec.md#521-primary-stored-models """
    lotId: UUID
    purchaseDate: ISODateTime
    quantity: float
    purchasePrice: float
    createdAt: ISODateTime
    modifiedAt: ISODateTime
    computedInfo: Optional[ComputedInfoLot] = None

class Holding(BaseModel):
    """ Reference: product_spec.md#421-primary-stored-models """
    holdingId: UUID
    portfolioId: UUID
    userId: str
    ticker: str
    ISIN: Optional[str] = None
    WKN: Optional[str] = None
    securityType: SecurityType
    assetClass: AssetClass
    currency: Currency
    annualCosts: Optional[float] = None
    createdAt: ISODateTime
    modifiedAt: ISODateTime
    lots: List[Lot]

class MACD(BaseModel):
    value: float
    signal: float
    histogram: float

class DailyHoldingSnapshot(BaseModel):
    """ Reference: product_spec.md#422-time-series-subcollections """
    date: ISODateTime
    totalCost: float
    currentValue: float
    preTaxGainLoss: float
    afterTaxGainLoss: float
    gainLossPercentage: float
    sma7: Optional[float] = None
    sma20: Optional[float] = None
    sma50: Optional[float] = None
    sma200: Optional[float] = None
    vwma7: Optional[float] = None
    vwma20: Optional[float] = None
    vwma50: Optional[float] = None
    vwma200: Optional[float] = None
    rsi14: Optional[float] = None
    macd: Optional[MACD] = None

class Instrument(BaseModel):
    """ Reference: product_spec.md#4311-h_1000-financial-instrument-lookup """
    ticker: str
    ISIN: Optional[str] = None
    WKN: Optional[str] = None
    securityType: SecurityType
    assetClass: AssetClass
    currency: Currency

class InstrumentLookupRequest(BaseModel):
    """ Reference: product_spec.md#4311-h_1000-financial-instrument-lookup """
    identifier: str

class HoldingCreationRequest(BaseModel):
    """ Reference: product_spec.md#4312-h_1200-holding-creation """
    portfolioId: UUID
    confirmedInstrument: Instrument
    annualCosts: Optional[float] = None

class HoldingSummary(BaseModel):
    """ Reference: product_spec.md#4331-h_2000-holding-list-retrieval-portfolio-details-view """
    holdingId: UUID
    ticker: str
    securityType: SecurityType
    assetClass: AssetClass
    currency: Currency
    totalCost: float
    currentValue: float
    preTaxGainLoss: float
    gainLossPercentage: float

class HoldingUpdateRequest(BaseModel):
    """ Reference: product_spec.md#4341-h_3000-manual-holding-update """
    annualCosts: Optional[float] = None

class MoveHoldingRequest(BaseModel):
    """ Reference: product_spec.md#437-h_6000-move-holding """
    destinationPortfolioId: UUID

class LotCreationRequest(BaseModel):
    """ Reference: product_spec.md#5311-l_1000-manual-creation """
    purchaseDate: ISODateTime
    quantity: float
    purchasePrice: float

class LotUpdateRequest(BaseModel):
    """ Reference: product_spec.md#513-manual-update-of-a-single-lot """
    purchaseDate: ISODateTime
    quantity: float
    purchasePrice: float

# #############################################################################
# RULESET MODELS
# #############################################################################

class Condition(BaseModel):
    """ Reference: product_spec.md#621-stored-data-models """
    conditionId: UUID
    type: ConditionType
    parameters: Dict[str, Any]

class Rule(BaseModel):
    """ Reference: product_spec.md#621-stored-data-models """
    ruleId: UUID
    ruleType: RuleType
    logicalOperator: LogicalOperator = LogicalOperator.AND
    conditions: List[Condition]
    status: RuleStatus

class RuleSet(BaseModel):
    """ Reference: product_spec.md#621-stored-data-models """
    ruleSetId: UUID
    userId: str
    parentId: str
    parentType: ParentType
    rules: List[Rule]
    createdAt: ISODateTime
    modifiedAt: ISODateTime

class RuleSetCreationRequest(BaseModel):
    """ Reference: product_spec.md#631-r_1000-rule-set-creation """
    parentId: str
    parentType: ParentType
    rules: List[Rule]

class RuleSetUpdateRequest(BaseModel):
    """ Reference: product_spec.md#633-r_3000-rule-set-update """
    rules: List[Rule]

# #############################################################################
# ALERT MODELS
# #############################################################################

class MarketDataSnapshot(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    closePrice: float
    rsi14: Optional[float] = None
    sma200: Optional[float] = None

class TriggeredCondition(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    type: ConditionType
    parameters: Dict[str, Any]
    actualValue: float

class TaxInfo(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    preTaxProfit: float
    capitalGainTax: float
    afterTaxProfit: float
    appliedTaxRate: float

class Alert(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    alertId: UUID
    userId: str
    holdingId: UUID
    ruleSetId: UUID
    ruleId: UUID
    triggeredAt: ISODateTime
    isRead: bool = False
    marketDataSnapshot: MarketDataSnapshot
    triggeredConditions: List[TriggeredCondition]
    taxInfo: Optional[TaxInfo] = None
    notificationStatus: NotificationStatus

class AlertUpdateRequest(BaseModel):
    """ Reference: product_spec.md#743-a_3000-mark-alerts-as-read """
    alertId: UUID
    isRead: bool = True
