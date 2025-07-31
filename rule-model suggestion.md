The absence of class Rule and any rule evaluation logic in the files examined strongly suggests that this functionality has not yet been implemented. The
  backend currently supports portfolio management and data synchronization, but not the core feature of evaluating rules against that data.

  Therefore, I will proceed with the following plan:

   1. Create `backend/src/models.py` Rule Models: I will add the Rule, Condition, and Alert models to models.py as defined in the product specification. This
      is the foundational step.
   2. Create `backend/src/services/rule_engine_service.py`: I will create a new service file to house the core rule evaluation logic. This service will:
       * Fetch rules from Firestore.
       * Fetch the latest market data for the relevant tickers.
       * Evaluate the conditions for each rule (SMA, VWMA, RSI, etc.) against the market data.
       * Generate Alert objects when rules are triggered.
   3. Update `backend/src/services/sync_service.py`: After the market data is synced, I will make it call the new RuleEngineService to trigger the rule
      evaluation process.

  I'll start by adding the necessary models to backend/src/models.py.


 from datetime import datetime                                                                                                            │
 │      2 - from typing import List, Optional                                                                                                        │
 │      2 + from typing import List, Optional, Dict, Any                                                                                             │
 │      3   from pydantic import BaseModel, Field                                                                                                    │
 │      4   import uuid                                                                                                                              │
 │      5 + from enum import Enum                                                                                                                    │
 │      6                                                                                                                                            │
 │      7                                                                                                                                            │
 │      8   # #############################################################################                                                          │
 │    ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════  │
 │     75       rsi14: Optional[float] = None                                                                                                        │
 │     76       atr14: Optional[float] = None                                                                                                        │
 │     77                                                                                                                                            │
 │     78 + # #############################################################################                                                          │
 │     79 + # RULE AND ALERT MODELS                                                                                                                  │
 │     80 + # #############################################################################                                                          │
 │     81                                                                                                                                            │
 │     82 + class ConditionType(str, Enum):                                                                                                          │
 │     83 +     DRAWDOWN = "DRAWDOWN"                                                                                                                │
 │     84 +     SMA = "SMA"                                                                                                                          │
 │     85 +     VWMA = "VWMA"                                                                                                                        │
 │     86 +     RSI = "RSI"                                                                                                                          │
 │     87 +     VIX = "VIX"                                                                                                                          │
 │     88 +     PROFIT_TARGET = "PROFIT_TARGET"                                                                                                      │
 │     89 +     TRAILING_DRAWDOWN = "TRAILING_DRAWDOWN"                                                                                              │
 │     90 +     AFTER_TAX_PROFIT = "AFTER_TAX_PROFIT"                                                                                                │
 │     91 +                                                                                                                                          │
 │     92 + class RuleStatus(str, Enum):                                                                                                             │
 │     93 +     ENABLED = "ENABLED"                                                                                                                  │
 │     94 +     PAUSED = "PAUSED"                                                                                                                    │
 │     95 +                                                                                                                                          │
 │     96 + class RuleType(str, Enum):                                                                                                               │
 │     97 +     BUY = "BUY"                                                                                                                          │
 │     98 +     SELL = "SELL"                                                                                                                        │
 │     99 +                                                                                                                                          │
 │    100 + class Condition(BaseModel):                                                                                                              │
 │    101 +     conditionId: str = Field(default_factory=lambda: str(uuid.uuid4()))                                                                  │
 │    102 +     type: ConditionType                                                                                                                  │
 │    103 +     parameters: Dict[str, Any] # e.g., {"period": 200, "operator": "cross_below"}                                                        │
 │    104 +                                                                                                                                          │
 │    105 + class RuleDB(BaseModel):                                                                                                                 │
 │    106 +     ruleId: str = Field(default_factory=lambda: str(uuid.uuid4()))                                                                       │
 │    107 +     portfolioId: str                                                                                                                     │
 │    108 +     ruleType: RuleType                                                                                                                   │
 │    109 +     ticker: str                                                                                                                          │
 │    110 +     conditions: List[Condition]                                                                                                          │
 │    111 +     status: RuleStatus = RuleStatus.ENABLED                                                                                              │
 │    112 +     createdAt: datetime = Field(default_factory=datetime.now)                                                                            │
 │    113 +     modifiedAt: datetime = Field(default_factory=datetime.now)                                                                           │
 │    114 +                                                                                                                                          │
 │    115 + class AlertDB(BaseModel):                                                                                                                │
 │    116 +     alertId: str = Field(default_factory=lambda: str(uuid.uuid4()))                                                                      │
 │    117 +     ruleId: str                                                                                                                          │
 │    118 +     userId: str                                                                                                                          │
 │    119 +     triggeredAt: datetime = Field(default_factory=datetime.now)                                                                          │
 │    120 +     marketData: Dict[str, Any]                                                                                                           │
 │    121 +     taxInfo: Optional[Dict[str, Any]] = None                                                                                             │
 │    122 +     notificationStatus: str = "PENDING"                                                                                                  │
 │    123 +                                                                                                                                          │
 │    124 +                                                                                                                                          │
 │    125   # #############################################################################                                                          │
 │    126   # COMPUTED INFO MODELS (for API responses)                                                                                               │
 │    127   # #############################################################################         

