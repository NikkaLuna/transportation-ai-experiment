from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE
from schemas.policy_validation import PolicyValidationResult
from prompts.policy_validation import POLICY_VALIDATION_PROMPT

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

structured_llm = llm.with_structured_output(PolicyValidationResult)

policy_validation_chain = POLICY_VALIDATION_PROMPT | structured_llm