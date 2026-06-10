from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIConnectionError, APIError, Timeout
from pydantic import ValidationError
import logging
from typing import Any, Callable, Optional
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_transient_error(exception):
    """Decide which errors should be retried"""
    return isinstance(exception, (RateLimitError, APIConnectionError, APIError, Timeout))


@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=3, max=20),
    retry=retry_if_exception_type(is_transient_error),
    before_sleep=lambda rs: logger.warning(
        f"[{rs.attempt_number}/4] Retrying after transient error..."
    )
)
def safe_invoke(chain: Callable, input_data: Any, operation_name: str = "chain"):
    """Run a LangChain operation with retries + fallback logic"""
    try:
        return chain.invoke(input_data)
    except Exception as e:
        logger.error(f"[{operation_name}] Failed: {type(e).__name__} - {str(e)}")
        raise  # Let tenacity retry


def safe_structured_invoke(chain, input_data: Any, max_retries: int = 2):
    """
    Special handler for structured output.
    Retries if the model returns invalid schema.
    """
    for attempt in range(max_retries + 1):
        try:
            result = safe_invoke(chain, input_data, "structured_extraction")
            return result
        except ValidationError as ve:
            logger.warning(f"Structured output validation failed (attempt {attempt+1}). Retrying...")
            if attempt == max_retries:
                logger.error("Max retries reached for structured output.")
                # Fallback: Return minimal safe object
                from schemas.shipment import ShipmentRequest
                return ShipmentRequest(
                    origin="UNKNOWN",
                    destination="UNKNOWN",
                    confidence=0.0,
                    exceptions=[f"Extraction failed after {max_retries} attempts"]
                )
        except Exception as e:
            if attempt == max_retries:
                raise
            logger.warning(f"Attempt {attempt+1} failed with {type(e).__name__}. Retrying...")

    # Final fallback
    from schemas.shipment import ShipmentRequest
    return ShipmentRequest(
        origin="UNKNOWN",
        destination="UNKNOWN",
        confidence=0.0,
        exceptions=["Critical extraction failure - manual review required"]
    )