from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class DomainResult:
    domain: str
    ok: bool
    data: dict[str, Any]
    error: str | None = None

class DomainAdapter(ABC):
    domain_name: str

    @abstractmethod
    def process(self, event: dict[str, Any]) -> DomainResult:
        raise NotImplementedError