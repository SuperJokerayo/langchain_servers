from __future__ import annotations

from typing import Optional, Mapping, Any, Iterator

import os

from ..document import Document

try:
    import fitz
except ImportError:
    raise ImportError(
        "`fitz` package not found, please install it with "
        "`pip install PyMuPDF`"
    )

import numpy as np

class PDFLoader():
    """
    use PyMuPDF as base loader
    """
    def __init__(
        self, 
        file_path: str, 
        extract_images: bool = False, 
        text_kwargs: Optional[Mapping[str, Any]] = None
    ) -> None:
        if not os.path.exists(file_path):
            raise "No such file exists!"
        if len(file_path) < 4 or file_path[-4:] != ".pdf":
            raise "Not a correct PDF file!"
        
        self.file_path = file_path
        self.extract_images = extract_images
        self.text_kwargs = text_kwargs or {}

    def load(self) -> Iterator[Document]:
        doc = fitz.open(self.file_path)

        pdf_content = []

        for page in doc:
            page_content = page.get_text(**self.text_kwargs)

            if self.extract_images:
                page_content += self._extract_images_from_page(doc, page)

            metadata = doc.metadata
            metadata["page"] = page.number
            metadata["total_pages"] = len(doc)

            pdf_content.append(
                Document(
                    content = page_content,
                    metadata = metadata
                )
            )
        return pdf_content

    def _extract_images_from_page(
        self, 
        doc:fitz.fitz.Document, 
        page: fitz.fitz.Page
    ) -> str:
        try:
            from rapidocr_onnxruntime import RapidOCR
            ocr = RapidOCR()
        except ImportError:
            raise ImportError(
                "`rapidocr-onnxruntime` package not found, please install it with "
                "`pip install rapidocr-onnxruntime`"
            )
        text = ""
        img_list = page.get_images()
        for img in img_list:
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, -1)
            result, _ = ocr(img_array)

            if result:
                result = [r[1] for r in result]
                text += "\n".join(result)
        return text
