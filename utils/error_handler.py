from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError, APIConnectionError, APIError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=lambda retry_state: isinstance(retry_state.outcome.exception(), (RateLimitError, APIConnectionError, APIError))
)
def safe_invoke(chain, input_data):
    """Safely run any chain with automatic retries"""
    return chain.invoke(input_data)