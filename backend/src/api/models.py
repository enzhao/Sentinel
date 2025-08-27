"""
Pydantic models for the Sentinel API, generated from the OpenAPI spec.
These models are used for request and response validation.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4
from enum import Enum

# #############################################################################
# ENUMS
# #############################################################################

class SubscriptionStatus(str, Enum):
    """ Reference: product_spec.md#82-data-models """
    FREE = "FREE"
    PREMIUM = "PREMIUM"

class NotificationChannel(str, Enum):
    """ Reference: product_spec.md#921-primary-stored-models """
    EMAIL = "EMAIL"
    PUSH = "PUSH"

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

class Error(BaseModel):
    """ Reference: product_spec.md#componentsschemaserror """
    code: str
    message: str

# #############################################################################
# USER MODELS
# #############################################################################

class NotificationPreferences(BaseModel):
    """ Reference: product_spec.md#921-primary-stored-models """
    __root__: List[NotificationChannel]

class User(BaseModel):
    """ Reference: product_spec.md#82-data-models """
    uid: str
    username: str
    email: str
    defaultPortfolioId: UUID4
    subscriptionStatus: SubscriptionStatus
    notificationPreferences: NotificationPreferences
    createdAt: datetime
    modifiedAt: datetime

class UpdateUserSettingsRequest(BaseModel):
    """ Reference: product_spec.md#82-data-models """
    defaultPortfolioId: UUID4
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
    portfolioId: UUID4
    userId: str
    name: str
    description: Optional[str] = None
    defaultCurrency: Currency
    cashReserve: CashReserve
    ruleSetId: Optional[UUID4] = None
    createdAt: datetime
    modifiedAt: datetime

class DailyPortfolioSnapshot(BaseModel):
    """ Reference: product_spec.md#322-time-series-subcollections """
    date: datetime
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
    portfolioId: UUID4
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
    purchaseDate: datetime
    quantity: float
    purchasePrice: float
    action: AnnotatedTransactionAction

class TransactionImportReview(BaseModel):
    """ Reference: product_spec.md#335-p_5000-unified-transaction-import """
    portfolioId: UUID4
    transactions: List[AnnotatedTransaction]

class TransactionImportConfirmRequest(BaseModel):
    """ Reference: product_spec.md#335-p_5000-unified-transaction-import """
    portfolioId: UUID4
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
    lotId: UUID4
    purchaseDate: datetime
    quantity: float
    purchasePrice: float
    createdAt: datetime
    modifiedAt: datetime
    computedInfo: Optional[ComputedInfoLot] = None

class Holding(BaseModel):
    """ Reference: product_spec.md#421-primary-stored-models """
    holdingId: UUID4
    portfolioId: UUID4
    userId: str
    ticker: str
    ISIN: Optional[str] = None
    WKN: Optional[str] = None
    securityType: SecurityType
    assetClass: AssetClass
    currency: Currency
    annualCosts: Optional[float] = None
    createdAt: datetime
    modifiedAt: datetime
    lots: List[Lot]

class MACD(BaseModel):
    value: float
    signal: float
    histogram: float

class DailyHoldingSnapshot(BaseModel):
    """ Reference: product_spec.md#422-time-series-subcollections """
    date: datetime
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
    portfolioId: UUID4
    confirmedInstrument: Instrument
    annualCosts: Optional[float] = None

class HoldingSummary(BaseModel):
    """ Reference: product_spec.md#4331-h_2000-holding-list-retrieval-portfolio-details-view """
    holdingId: UUID4
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
    destinationPortfolioId: UUID4

class LotCreationRequest(BaseModel):
    """ Reference: product_spec.md#5311-l_1000-manual-creation """
    purchaseDate: datetime
    quantity: float
    purchasePrice: float

class LotUpdateRequest(BaseModel):
    """ Reference: product_spec.md#513-manual-update-of-a-single-lot """
    purchaseDate: datetime
    quantity: float
    purchasePrice: float

# #############################################################################
# RULESET MODELS
# #############################################################################

class Condition(BaseModel):
    """ Reference: product_spec.md#621-stored-data-models """
    conditionId: UUID4
    type: ConditionType
    parameters: Dict[str, Any]

class Rule(BaseModel):
    """ Reference: product_spec.md#621-stored-data-models """
    ruleId: UUID4
    ruleType: RuleType
    logicalOperator: LogicalOperator = LogicalOperator.AND
    conditions: List[Condition]
    status: RuleStatus

class RuleSet(BaseModel):
    """ Reference: product_spec.md#621-stored-data-models """
    ruleSetId: UUID4
    userId: str
    parentId: str
    parentType: ParentType
    rules: List[Rule]
    createdAt: datetime
    modifiedAt: datetime

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
    alertId: UUID4
    userId: str
    holdingId: UUID4
    ruleSetId: UUID4
    ruleId: UUID4
    triggeredAt: datetime
    isRead: bool = False
    marketDataSnapshot: MarketDataSnapshot
    triggeredConditions: List[TriggeredCondition]
    taxInfo: Optional[TaxInfo] = None
    notificationStatus: NotificationStatus

class AlertUpdateRequest(BaseModel):
    """ Reference: product_spec.md#743-a_3000-mark-alerts-as-read """
    alertId: UUID4
    isRead: bool = True
