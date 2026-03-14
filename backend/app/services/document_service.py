from fastapi import UploadFile
from pathlib import Path
from app.config import settings
import aiofiles
import pdfplumber
from PIL import Image
import pytesseract

class DocumentService:
    @staticmethod
    async def save_file(file: UploadFile, user_id: str) -> str:
        user_dir = Path(settings.STORAGE_PATH) / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / (file.filename or "document")
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        return str(file_path)

    @staticmethod
    async def extract_text(file_path: str, content_type: str) -> str:
        if "pdf" in content_type:
            return DocumentService._extract_pdf(file_path)
        elif "image" in content_type:
            return DocumentService._extract_image(file_path)
        return ""

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return ""

    @staticmethod
    def _extract_image(file_path: str) -> str:
        try:
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Image extraction error: {e}")
            return ""
