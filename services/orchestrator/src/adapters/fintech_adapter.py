import logging
 
import requests
 
from .base import DomainAdapter, DomainResult

logger = logging.getLogger(__name__)

class FintechRiskAdapter(DomainAdapter):
    domain_name = "fintech"

    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def process(self, event: dict) -> DomainResult:
        try:
            response = requests.post(
                f"{self.base_url}/api/score",
                json=event,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return DomainResult(domain=self.domain_name, ok=True, data=response.json())
        except requests.exceptions.RequestException as exc:
            logger.error("fintech-risk-engine call failed: %s", exc)
            return DomainResult(domain=self.domain_name, ok=False, data={}, error=str(exc))