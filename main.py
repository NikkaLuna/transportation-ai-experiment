from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chains.extraction_chain import basic_extraction_chain
from chains.policy_retriever import build_policy_retriever
from chains.policy_validation_chain import policy_validation_chain
from loaders.document_loader import load_pdf
from loaders.policy_loader import load_policy_documents
from utils.error_handler import safe_invoke

load_dotenv()

def main():
    print("=== PDF Document Extraction Demo ===\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "data", "sample_bill_of_lading.pdf")

    print(f"Looking for PDF at: {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: PDF file not found at {pdf_path}")
        return

    docs = load_pdf(pdf_path)
    extracted_text = docs[0].page_content

    print(f"Successfully loaded PDF ({len(extracted_text)} characters)\n")

    print("Running extraction...")
    result = safe_invoke(basic_extraction_chain, {"message": extracted_text})

    print("\nExtracted Structured Data from PDF:")
    print(result.model_dump_json(indent=2))

    print("\nRunning policy RAG validation...")

    policy_dir = os.path.join(base_dir, "data", "policies")
    policy_docs = load_policy_documents(policy_dir)
    retriever = build_policy_retriever(policy_docs)

    relevant_policies = retriever.invoke(result.model_dump_json(indent=2))

    policy_context = "\n\n".join(
        [doc.page_content for doc in relevant_policies]
    )

    validation_result = safe_invoke(
        policy_validation_chain,
        {
            "shipment_data": result.model_dump_json(indent=2),
            "policy_context": policy_context
        }
    )

    print("\nPolicy Validation Result:")
    print(validation_result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()