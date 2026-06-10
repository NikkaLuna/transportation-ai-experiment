from dotenv import load_dotenv
import sys
import os
import time
import glob

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chains.extraction_chain import basic_extraction_chain
from chains.policy_retriever import build_policy_retriever
from chains.policy_validation_chain import policy_validation_chain
from loaders.document_loader import load_pdf
from loaders.policy_loader import load_policy_documents
from utils.error_handler import safe_invoke
from validators.business_rules import validate_business_rules
from evaluators.extraction_evaluator import evaluate_extraction

load_dotenv()


def get_latest_pdf(data_dir: str) -> str:
    """Find the most recently modified PDF in the data folder"""
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {data_dir}")
    
    # Return the file with the latest modification time
    latest_pdf = max(pdf_files, key=os.path.getmtime)
    return latest_pdf


def main():
    total_start = time.time()
    print("=== PDF Document Extraction Demo ===\n")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    # Automatically get the latest PDF
    try:
        pdf_path = get_latest_pdf(data_dir)
        print(f"Using latest PDF: {os.path.basename(pdf_path)}")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return
    
    print(f"Full path: {pdf_path}\n")
    
    # Load PDF
    load_start = time.time()
    docs = load_pdf(pdf_path)
    extracted_text = docs[0].page_content
    print(f"Successfully loaded PDF ({len(extracted_text)} characters)")
    print(f"PDF load completed in {time.time() - load_start:.2f} seconds\n")
    
    # Extraction
    extraction_start = time.time()
    print("Running extraction...")
    result = safe_invoke(basic_extraction_chain, {"message": extracted_text})
    print(f"Extraction completed in {time.time() - extraction_start:.2f} seconds")
    print("\nExtracted Structured Data from PDF:")
    print(result.model_dump_json(indent=2))
    
    # RAG Policy Validation
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
    
    policy_context = "\n\n".join([doc.page_content for doc in relevant_policies])
    
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
    
    # Business Rules Validation
    business_start = time.time()
    print("\nRunning deterministic business rule validation...")
    business_rule_result = validate_business_rules(result)
    print(f"Business rule validation completed in {time.time() - business_start:.2f} seconds")
    print(f"Business rule warnings found: {len(business_rule_result['business_rule_warnings'])}")
    print("\nBusiness Rule Validation Result:")
    print(business_rule_result)

    print("\nRunning extraction evaluation...")

    expected_values = {
        "carrier": "CMA CGM",
        "weight": 18000.0,
        "origin_contains": "INDIA",
        "destination_contains": "UNITED ARAB EMIRATES",
        "pickup_date": "2019-01-16"
    }

    evaluation_result = evaluate_extraction(result, expected_values)

    print("\nExtraction Evaluation Result:")
    print(evaluation_result)
    
    print(f"\nTotal pipeline runtime: {time.time() - total_start:.2f} seconds")


if __name__ == "__main__":
    main()