import os
 
from .adapters.base import DomainAdapter
from .adapters.fintech_adapter import FintechRiskAdapter
from .adapters.proptech_adapter import ProptechRecommenderAdapter

class UnknownDomainError(Exception):
    pass

class AdapterFactory:
    def __init__(self):
        self._adapters: dict[str, DomainAdapter] = {}

    def get(self, domain: str) -> DomainAdapter:
        if domain not in self._adapters:
            self._adapters[domain] = self._build(domain)
        return self._adapters[domain]

    def _build(self, domain: str) -> DomainAdapter:
        if domain == "fintech":
            return FintechRiskAdapter(base_url=os.environ["FINTECH_SERVICE_URL"])
        if domain == "proptech":
            return ProptechRecommenderAdapter(base_url=os.environ["PROPTECH_SERVICE_URL"])
        raise UnknownDomainError(f"no adapter registered for domain: {domain}")