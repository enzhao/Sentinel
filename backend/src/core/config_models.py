"""
Pydantic models for loading and validating configuration files.
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from src.api.models import AssetClass

class TaxRule(BaseModel):
    """
    Defines a single tax rule for an asset class.
    Reference: backend/config/tax_config.yaml
    """
    description: str
    taxRate: float = Field(..., ge=0, le=100)
    condition: Optional[str] = None

class TaxConfig(BaseModel):
    """
    Represents the structure of the tax_config.yaml file.
    """
    EQUITY: List[TaxRule]
    CRYPTO: List[TaxRule]
    COMMODITY: List[TaxRule]

class MarketMonitorConfig(BaseModel):
    """
    Represents the structure of the market_monitor_config.yaml file.
    Reference: backend/config/market_monitor_config.yaml
    """
    system_required_tickers: List[str]
