Transportation AI Experiment
============================

Overview
--------

This project demonstrates a production-style AI document processing pipeline built with **LangChain**, **OpenAI**, and **Retrieval Augmented Generation (RAG)**.

The system extracts structured shipment data from Bills of Lading (PDFs), retrieves relevant transportation policies using vector search, and performs AI-powered compliance validation against those policies.

The goal is to simulate how modern logistics organizations can combine traditional document processing with LLM-powered reasoning and policy enforcement.

* * * * *

Features
--------

### PDF Document Extraction

Extracts shipment information directly from Bill of Lading PDFs.

Examples:

-   Shipment ID
-   Origin
-   Destination
-   Carrier
-   Load Type
-   Weight
-   Pickup Date
-   Delivery Date
-   Freight Status

* * * * *

### Structured Outputs

Uses OpenAI Structured Output generation with Pydantic schemas to ensure reliable and predictable JSON responses.

Example:

```
{  "shipment_id": "CEXP190150",  "carrier": "CMA CGM",  "weight": 18000,  "origin": "CHENNAI, INDIA",  "destination": "JEBEL ALI, UAE"}
```

* * * * *

### Retrieval Augmented Generation (RAG)

Company transportation policies are embedded and stored in a vector database.

When a shipment is extracted:

1.  Relevant policies are retrieved using semantic search.
2.  The retrieved context is provided to the LLM.
3.  The model validates the shipment against company policies.

* * * * *

### AI-Powered Policy Validation

The system evaluates extracted shipment data against transportation rules.

Examples:

-   Missing delivery dates
-   Weight restrictions
-   Carrier-specific requirements
-   International customs requirements
-   Confidence-based manual review thresholds

Example output:

```
{  "policy_matches": [    "International shipments require customs documentation review."  ],  "compliance_warnings": [    "Delivery date is required for final shipment approval."  ],  "recommended_actions": [    "Request delivery date before shipment approval."  ]}
```

* * * * *

Architecture
------------

```
Bill of Lading PDF        │        ▼PDF Loader        │        ▼OpenAI + LangChain Extraction Chain        │        ▼Structured Shipment JSON        │        ▼Policy Retriever (RAG)        │        ▼Vector Search        │        ▼Relevant Policy Context        │        ▼Policy Validation Chain        │        ▼Compliance Warnings & Recommendations
```

* * * * *

Technologies Used
-----------------

### AI / LLM

-   OpenAI GPT-4o Mini
-   OpenAI Embeddings
-   LangChain

### RAG Components

-   FAISS Vector Store
-   Semantic Retrieval
-   Embeddings
-   Prompt Engineering

### Data Processing

-   PyMuPDF
-   Pydantic
-   Python

* * * * *

Project Structure
-----------------

```
transportation-ai-experiment/├── chains/│   ├── extraction_chain.py│   ├── policy_retriever.py│   └── policy_validation_chain.py│├── data/│   ├── sample_bill_of_lading.pdf│   └── policies/│├── loaders/│   ├── document_loader.py│   └── policy_loader.py│├── prompts/│   ├── shipment_extraction.py│   └── policy_validation.py│├── schemas/│   ├── shipment.py│   └── policy_validation.py│├── config.py├── main.py└── requirements.txt
```

* * * * *

Example Workflow
----------------

### Input

Bill of Lading PDF

### Extraction Output

```
{  "shipment_id": "CEXP190150",  "carrier": "CMA CGM",  "weight": 18000,  "origin": "CHENNAI, INDIA",  "destination": "JEBEL ALI, UAE"}
```

### RAG Validation Output

```
{  "policy_matches": [    "Shipment weight must be greater than 0.",    "International shipments require customs documentation review."  ],  "compliance_warnings": [    "Delivery date is required for final shipment approval."  ],  "recommended_actions": [    "Request delivery date before shipment approval."  ]}
```

* * * * *

Future Enhancements
-------------------

Planned improvements:

-   Agentic workflows using LangChain Agents
-   Tool calling for business rule validation
-   Evaluation framework for extraction accuracy
-   Tracing and observability
-   Azure OpenAI integration
-   Cost and token monitoring
-   Multi-document shipment processing
-   Human-in-the-loop review workflow

* * * * *

Learning Objectives
-------------------

This project was built to gain hands-on experience with:

-   LangChain
-   OpenAI APIs
-   Prompt Engineering
-   Structured Outputs
-   Embeddings
-   Vector Search
-   Retrieval Augmented Generation (RAG)
-   AI-powered validation workflows
-   Production-style AI application architecture