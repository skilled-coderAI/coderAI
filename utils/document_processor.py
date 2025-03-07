import os
import tempfile
from typing import Dict, List, Any, Optional, BinaryIO, Union
import base64

class DocumentProcessor:
    """Utility for processing various document types"""
    
    @staticmethod
    def extract_text_from_txt(file_content: Union[str, bytes]) -> str:
        """
        Extract text from a TXT file
        
        Args:
            file_content: Content of the TXT file
            
        Returns:
            Extracted text
        """
        if isinstance(file_content, bytes):
            # Try to decode with utf-8, fallback to latin-1
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                return file_content.decode('latin-1')
        return file_content
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extract text from a PDF file
        
        Args:
            file_content: Content of the PDF file
            
        Returns:
            Extracted text
        """
        try:
            # Import here to avoid loading dependencies unless needed
            import PyPDF2
            import io
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
            
            # Extract text
            text = ""
            with open(temp_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text() + "\n\n"
            
            # Remove temporary file
            os.unlink(temp_path)
            
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """
        Extract text from a DOCX file
        
        Args:
            file_content: Content of the DOCX file
            
        Returns:
            Extracted text
        """
        try:
            # Import here to avoid loading dependencies unless needed
            import docx
            import io
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
            
            # Extract text
            doc = docx.Document(temp_path)
            text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # Remove temporary file
            os.unlink(temp_path)
            
            return text
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_md(file_content: Union[str, bytes]) -> str:
        """
        Extract text from a Markdown file
        
        Args:
            file_content: Content of the Markdown file
            
        Returns:
            Extracted text
        """
        if isinstance(file_content, bytes):
            # Try to decode with utf-8, fallback to latin-1
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                return file_content.decode('latin-1')
        return file_content
    
    @staticmethod
    def extract_text(file_content: Union[str, bytes], file_type: str) -> str:
        """
        Extract text from a file based on its type
        
        Args:
            file_content: Content of the file
            file_type: Type of the file (txt, pdf, docx, md)
            
        Returns:
            Extracted text
        """
        file_type = file_type.lower()
        
        if file_type == 'txt':
            return DocumentProcessor.extract_text_from_txt(file_content)
        elif file_type == 'pdf':
            if isinstance(file_content, str):
                file_content = file_content.encode('utf-8')
            return DocumentProcessor.extract_text_from_pdf(file_content)
        elif file_type == 'docx':
            if isinstance(file_content, str):
                file_content = file_content.encode('utf-8')
            return DocumentProcessor.extract_text_from_docx(file_content)
        elif file_type == 'md':
            return DocumentProcessor.extract_text_from_md(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to split
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            List of text chunks
        """
        chunks = []
        
        if len(text) <= chunk_size:
            chunks.append(text)
        else:
            start = 0
            while start < len(text):
                end = min(start + chunk_size, len(text))
                
                # Adjust end to avoid cutting words
                if end < len(text):
                    # Find the last space within the chunk
                    last_space = text.rfind(' ', start, end)
                    if last_space != -1:
                        end = last_space
                
                # Add chunk
                chunks.append(text[start:end])
                
                # Move start position for next chunk
                start = end - overlap
                
                # Adjust start to avoid cutting words
                if start > 0:
                    # Find the first space after start
                    first_space = text.find(' ', start)
                    if first_space != -1 and first_space < start + overlap:
                        start = first_space + 1
        
        return chunks
