"""
Pydantic models for data stored in Firestore.
These models represent the internal data structure and may differ from the API models.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

# Import enums from the api models to avoid duplication
from src.api.models import (
    SubscriptionStatus,
    Currency,
    SecurityType,
    AssetClass,
    ParentType,
    RuleType,
    LogicalOperator,
    ConditionType,
    RuleStatus,
    NotificationStatus,
    NotificationChannel
)

class CurrentUser(BaseModel):
    uid: str
    email: EmailStr
    username: str
    defaultPortfolioId: Optional[UUID] = Field(None, description="The ID of the user's default portfolio.")
    

# #############################################################################
# INTERNAL DB MODELS
# #############################################################################

class UserDB(BaseModel):
    """ Represents a user document in the 'users' collection. """
    """ Reference: product_spec.md#82-data-models """
    uid: str = Field(..., description="Firebase Auth UID, the document ID.")
    username: str
    email: str
    defaultPortfolioId: Optional[str] = None # UUID as string
    subscriptionStatus: SubscriptionStatus = SubscriptionStatus.FREE
    notificationPreferences: List[NotificationChannel] = Field(default_factory=lambda: [NotificationChannel.EMAIL])
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    modifiedAt: datetime = Field(default_factory=datetime.utcnow)

class CashReserveDB(BaseModel):
    """ Reference: product_spec.md#321-primary-stored-models """
    totalAmount: float
    warChestAmount: float

class PortfolioDB(BaseModel):
    """ Represents a portfolio document in the 'portfolios' collection. """
    """ Reference: product_spec.md#321-primary-stored-models """
    portfolioId: str = Field(..., description="Unique UUID, the document ID.")
    userId: str = Field(..., description="Firebase Auth UID of the owner.")
    name: str
    description: Optional[str] = None
    defaultCurrency: Currency
    cashReserve: CashReserveDB
    ruleSetId: Optional[str] = None # UUID as string
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    modifiedAt: datetime = Field(default_factory=datetime.utcnow)

class DailyPortfolioSnapshotDB(BaseModel):
    """ Represents a daily snapshot in the 'dailySnapshots' subcollection of a portfolio. """
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

class LotDB(BaseModel):
    """ Represents a lot object embedded in a holding's 'lots' array. """
    """ Reference: product_spec.md#521-primary-stored-models """
    lotId: str # UUID as string
    purchaseDate: datetime
    quantity: float
    purchasePrice: float
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    modifiedAt: datetime = Field(default_factory=datetime.utcnow)

class HoldingDB(BaseModel):
    """ Represents a holding document in the 'holdings' collection. """
    """ Reference: product_spec.md#421-primary-stored-models """
    holdingId: str = Field(..., description="Unique UUID, the document ID.")
    portfolioId: str = Field(..., description="UUID of the parent portfolio.")
    userId: str = Field(..., description="Firebase Auth UID of the owner.")
    ticker: str
    ISIN: Optional[str] = None
    WKN: Optional[str] = None
    securityType: SecurityType
    assetClass: AssetClass
    currency: Currency
    annualCosts: Optional[float] = None
    lots: List[LotDB] = []
    ruleSetId: Optional[str] = None # UUID as string
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    modifiedAt: datetime = Field(default_factory=datetime.utcnow)

class MACD_DB(BaseModel):
    value: float
    signal: float
    histogram: float

class DailyHoldingSnapshotDB(BaseModel):
    """ Represents a daily snapshot in the 'dailySnapshots' subcollection of a holding. """
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
    macd: Optional[MACD_DB] = None

class ConditionDB(BaseModel):
    """ Represents a condition object embedded in a rule. """
    """ Reference: product_spec.md#621-stored-data-models """
    conditionId: str # UUID as string
    type: ConditionType
    parameters: Dict[str, Any]

class RuleDB(BaseModel):
    """ Represents a rule object embedded in a RuleSet. """
    """ Reference: product_spec.md#621-stored-data-models """
    ruleId: str # UUID as string
    ruleType: RuleType
    logicalOperator: LogicalOperator = LogicalOperator.AND
    conditions: List[ConditionDB]
    status: RuleStatus

class RuleSetDB(BaseModel):
    """ Represents a ruleset document in the 'rulesets' collection. """
    """ Reference: product_spec.md#621-stored-data-models """
    ruleSetId: str = Field(..., description="Unique UUID, the document ID.")
    userId: str = Field(..., description="Firebase Auth UID of the owner.")
    parentId: str = Field(..., description="The portfolioId or holdingId this ruleset belongs to.")
    parentType: ParentType
    rules: List[RuleDB]
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    modifiedAt: datetime = Field(default_factory=datetime.utcnow)

class MarketDataSnapshotDB(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    closePrice: float
    rsi14: Optional[float] = None
    sma200: Optional[float] = None

class TriggeredConditionDB(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    type: ConditionType
    parameters: Dict[str, Any]
    actualValue: float

class TaxInfoDB(BaseModel):
    """ Reference: product_spec.md#72-data-models """
    preTaxProfit: float
    capitalGainTax: float
    afterTaxProfit: float
    appliedTaxRate: float

class AlertDB(BaseModel):
    """ Represents an alert document in the 'alerts' collection. """
    """ Reference: product_spec.md#72-data-models """
    alertId: str = Field(..., description="Unique UUID, the document ID.")
    userId: str
    holdingId: str
    ruleSetId: str
    ruleId: str
    triggeredAt: datetime
    isRead: bool = False
    marketDataSnapshot: MarketDataSnapshotDB
    triggeredConditions: List[TriggeredConditionDB]
    taxInfo: Optional[TaxInfoDB] = None
    notificationStatus: NotificationStatus = NotificationStatus.PENDING

class IdempotencyKeyDB(BaseModel):
    """ Represents an idempotency key document in the 'idempotencyKeys' collection. """
    """ Reference: product_spec.md#1.2-components """
    key: str = Field(..., description="The idempotency key (UUID string).")
    userId: str = Field(..., description="Firebase Auth UID of the user who made the request.")
    createdAt: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the original request.")
    response: Dict[str, Any] = Field(..., description="The JSON response body of the original request.")
    status_code: int = Field(..., description="The HTTP status code of the original request.")

