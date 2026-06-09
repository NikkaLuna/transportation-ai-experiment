from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from typing import List, Optional
import re


def clean_text(text: str) -> str:
    """Clean up messy PDF text for better LLM extraction"""
    # Remove excessive newlines (3 or more → 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def load_pdf(pdf_path: str) -> List[Document]:
    """Load and clean text from a PDF file"""
    try:
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()
        
        # Clean the text in each page
        for doc in docs:
            doc.page_content = clean_text(doc.page_content)
        
        print(f"✅ Loaded and cleaned PDF: {pdf_path} ({len(docs)} pages)")
        return docs
        
    except Exception as e:
        raise Exception(f"Failed to load PDF '{pdf_path}': {str(e)}")


def load_text(text: str, metadata: Optional[dict] = None) -> List[Document]:
    """Load raw text string (useful for testing)"""
    if metadata is None:
        metadata = {}
    return [Document(page_content=text, metadata=metadata)]


def load_documents(path: str) -> List[Document]:
    """Auto-detect file type and load"""
    if path.lower().endswith('.pdf'):
        return load_pdf(path)
    elif path.lower().endswith('.eml'):
        try:
            from langchain_community.document_loaders import UnstructuredEmailLoader
            loader = UnstructuredEmailLoader(path)
            return loader.load()
        except ImportError:
            raise ImportError("UnstructuredEmailLoader requires the 'unstructured' package")
    else:
        raise ValueError(f"Unsupported file type: {path}")