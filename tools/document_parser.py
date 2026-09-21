import io
from typing import Dict, Any
from pypdf import PdfReader

def extract_text_from_pdf(pdf_source: Any) -> Dict[str, Any]:
    """
    Extract text content from a PDF file using pypdf.
    
    Args:
        pdf_source: BytesIO, bytes, or file-like object containing PDF data.
        
    Returns:
        dict: {
            "success": bool,
            "text": str,
            "page_count": int,
            "error": str or None
        }
    """
    try:
        if isinstance(pdf_source, bytes):
            pdf_file = io.BytesIO(pdf_source)
        else:
            pdf_file = pdf_source
            
        reader = PdfReader(pdf_file)
        page_count = len(reader.pages)
        
        if page_count == 0:
            return {
                "success": False,
                "text": "",
                "page_count": 0,
                "error": "The uploaded PDF file contains no pages."
            }
            
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text.strip())
                
        full_text = "\n\n".join(extracted_pages).strip()
        
        if not full_text:
            return {
                "success": False,
                "text": "",
                "page_count": page_count,
                "error": "No readable text found in the PDF. It may contain scanned images or be password-protected."
            }
            
        return {
            "success": True,
            "text": full_text,
            "page_count": page_count,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": f"Failed to parse PDF file: {str(e)}"
        }
