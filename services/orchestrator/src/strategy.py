from abc import ABC, abstractmethod
from typing import Any

class RoutingStrategy(ABC):
    domain_name: str

    @abstractmethod
    def matches(self, event: dict[str, Any]) -> bool:
        raise NotImplementedError

class FintechRoutingStrategy(RoutingStrategy):
    domain_name = "fintech"

    def matches(self, event: dict[str, Any]) -> bool:
        return "tx_amount" in event

class ProptechRoutingStrategy(RoutingStrategy):
    domain_name = "proptech"
 
    def matches(self, event: dict[str, Any]) -> bool:
        return "electricity_kw" in event or "hvac_temp" in event
 
 
class NoRouteFound(Exception):
    """Raised when an event doesn't match any registered strategy."""

class EventRouter:
    def __init__(self, strategies: list[RoutingStrategy] | None = None):
        self.strategies = strategies or [
            FintechRoutingStrategy(),
            ProptechRoutingStrategy(),
        ]