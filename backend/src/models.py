from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


# #############################################################################
# BASE MODELS (for Firestore storage)
# #############################################################################

class LotDB(BaseModel):
    lotId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    purchaseDate: datetime
    quantity: float = Field(..., gt=0)
    purchasePrice: float = Field(..., gt=0)

class HoldingDB(BaseModel):
    holdingId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticker: str
    lots: List[LotDB] = []

class TaxSettings(BaseModel):
    capitalGainTaxRate: float = Field(default=26.4, ge=0, le=100)
    taxFreeAllowance: float = Field(default=1000.0, ge=0)

class CashReserve(BaseModel):
    totalAmount: float = Field(default=0.0, ge=0)
    warChestAmount: float = Field(default=0.0, ge=0)

class PortfolioDB(BaseModel):
    portfolioId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    name: str
    holdings: List[HoldingDB] = []
    cashReserve: CashReserve = Field(default_factory=CashReserve)
    taxSettings: TaxSettings = Field(default_factory=TaxSettings)
    createdAt: datetime = Field(default_factory=datetime.now)
    modifiedAt: datetime = Field(default_factory=datetime.now)

class MarketDataDB(BaseModel):
    """
    Represents the daily market data for a single ticker stored in Firestore.
    """
    date: datetime = Field(default_factory=datetime.now)
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: int


# #############################################################################
# COMPUTED INFO MODELS (for API responses)
# #############################################################################

class LotComputedInfo(BaseModel):
    currentPrice: float = 0.0
    currentValue: float = 0.0
    preTaxProfit: float = 0.0
    capitalGainTax: float = 0.0
    afterTaxProfit: float = 0.0

class HoldingComputedInfo(BaseModel):
    totalCost: float = 0.0
    currentValue: float = 0.0
    preTaxGainLoss: float = 0.0
    afterTaxGainLoss: float = 0.0
    gainLossPercentage: float = 0.0

class PortfolioComputedInfo(BaseModel):
    totalCost: float = 0.0
    currentValue: float = 0.0
    preTaxGainLoss: float = 0.0
    afterTaxGainLoss: float = 0.0
    gainLossPercentage: float = 0.0


# #############################################################################
# API RESPONSE MODELS (DB models + Computed Info)
# #############################################################################

class Lot(LotDB, LotComputedInfo):
    pass

class Holding(HoldingDB, HoldingComputedInfo):
    lots: List[Lot] = []

class Portfolio(PortfolioDB, PortfolioComputedInfo):
    holdings: List[Holding] = []


# #############################################################################
# API REQUEST MODELS (for POST/PUT requests)
# #############################################################################

class CreatePortfolioRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class UpdatePortfolioRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    cashReserve: Optional[CashReserve] = None
    taxSettings: Optional[TaxSettings] = None

class AddHoldingRequest(BaseModel):
    ticker: str
    lots: List[LotDB]