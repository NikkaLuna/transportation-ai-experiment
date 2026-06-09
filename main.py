from dotenv import load_dotenv
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chains.extraction_chain import basic_extraction_chain
from chains.policy_retriever import build_policy_retriever
from chains.policy_validation_chain import policy_validation_chain
from loaders.document_loader import load_pdf
from loaders.policy_loader import load_policy_documents
from utils.error_handler import safe_invoke
from validators.business_rules import validate_business_rules

load_dotenv()

def main():
    total_start = time.time()

    print("=== PDF Document Extraction Demo ===\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "data", "sample_bill_of_lading.pdf")

    print(f"Looking for PDF at: {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: PDF file not found at {pdf_path}")
        return

    load_start = time.time()
    docs = load_pdf(pdf_path)
    extracted_text = docs[0].page_content
    print(f"Successfully loaded PDF ({len(extracted_text)} characters)")
    print(f"PDF load completed in {time.time() - load_start:.2f} seconds\n")

    extraction_start = time.time()
    print("Running extraction...")
    result = safe_invoke(basic_extraction_chain, {"message": extracted_text})
    print(f"Extraction completed in {time.time() - extraction_start:.2f} seconds")

    print("\nExtracted Structured Data from PDF:")
    print(result.model_dump_json(indent=2))

    rag_start = time.time()
    print("\nRunning policy RAG validation...")

    policy_dir = os.path.join(base_dir, "data", "policies")
    policy_docs = load_policy_documents(policy_dir)
    print(f"Policy docs loaded: {len(policy_docs)}")

    retriever = build_policy_retriever(policy_docs)

    retrieval_start = time.time()
    relevant_policies = retriever.invoke(result.model_dump_json(indent=2))
    print(f"Retrieved {len(relevant_policies)} relevant policy chunk(s)")
    print(f"Policy retrieval completed in {time.time() - retrieval_start:.2f} seconds")

    policy_context = "\n\n".join(
        [doc.page_content for doc in relevant_policies]
    )

    validation_start = time.time()
    validation_result = safe_invoke(
        policy_validation_chain,
        {
            "shipment_data": result.model_dump_json(indent=2),
            "policy_context": policy_context
        }
    )
    print(f"Policy validation completed in {time.time() - validation_start:.2f} seconds")
    print(f"Policy warnings found: {len(validation_result.compliance_warnings)}")
    print(f"Total RAG validation completed in {time.time() - rag_start:.2f} seconds")

    print("\nPolicy Validation Result:")
    print(validation_result.model_dump_json(indent=2))

    business_start = time.time()
    print("\nRunning deterministic business rule validation...")
    business_rule_result = validate_business_rules(result)
    print(f"Business rule validation completed in {time.time() - business_start:.2f} seconds")
    print(f"Business rule warnings found: {len(business_rule_result['business_rule_warnings'])}")

    print("\nBusiness Rule Validation Result:")
    print(business_rule_result)

    print(f"\nTotal pipeline runtime: {time.time() - total_start:.2f} seconds")

if __name__ == "__main__":
    main()