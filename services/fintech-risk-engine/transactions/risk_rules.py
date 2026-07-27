from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class RiskContext:
    amount: float
    timestamp: datetime
    recent_transaction_count: int 

class RiskRule(ABC):
    weight: float
 
    @abstractmethod
    def evaluate(self, context: RiskContext) -> tuple[bool, str | None]:
        raise NotImplementedError

class HighAmountRule(RiskRule):
    weight = 0.5
 
    def __init__(self, threshold: float = 5000.0):
        self.threshold = threshold
 
    def evaluate(self, context: RiskContext) -> tuple[bool, str | None]:
        if context.amount > self.threshold:
            return True, f"amount {context.amount} exceeds threshold {self.threshold}"
        return False, None

class OddHourRule(RiskRule):
    weight = 0.2
    ODD_HOURS = range(0, 5)
 
    def evaluate(self, context: RiskContext) -> tuple[bool, str | None]:
        hour = context.timestamp.astimezone(timezone.utc).hour
        if hour in self.ODD_HOURS:
            return True, f"transaction at odd hour ({hour}:00 UTC)"
        return False, None

class VelocityRule(RiskRule):
    weight = 0.3
 
    def __init__(self, max_recent_transactions: int = 3):
        self.max_recent_transactions = max_recent_transactions
 
    def evaluate(self, context: RiskContext) -> tuple[bool, str | None]:
        if context.recent_transaction_count >= self.max_recent_transactions:
            return True, (
                f"{context.recent_transaction_count} transactions from this "
                f"account in the lookback window"
            )
        return False, None

class RiskEngine:
    def __init__(self, rules: list[RiskRule] | None = None):
        self.rules: list[RiskRule] = rules or [
            HighAmountRule(),
            OddHourRule(),
            VelocityRule(),
        ]
 
    def score(self, context: RiskContext) -> tuple[float, list[str]]:
        total_weight = 0.0
        reasons: list[str] = []
        for rule in self.rules:
            triggered, reason = rule.evaluate(context)
            if triggered:
                total_weight += rule.weight
                if reason:
                    reasons.append(reason)
        return min(total_weight, 1.0), reasons
 
    @staticmethod
    def classify(score: float) -> str:
        if score >= 0.7:
            return "high"
        if score >= 0.3:
            return "medium"
        return "low"