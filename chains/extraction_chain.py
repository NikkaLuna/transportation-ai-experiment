from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE
from schemas.shipment import ShipmentRequest
from prompts.shipment_extraction import EXTRACTION_PROMPT

# LLM Setup
llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

# Structured output (forces clean JSON)
structured_llm = llm.with_structured_output(ShipmentRequest)

# Basic chain
basic_extraction_chain = EXTRACTION_PROMPT | structured_llm