import fitz
import numpy as np

from rapidocr_onnxruntime import RapidOCR
from unstructured.partition.text import partition_text

from langchain.document_loaders.unstructured import UnstructuredFileLoader

class PDFLoader(UnstructuredFileLoader):
    # extractor text and imgs in pdf
    def _get_elements(self):
        doc = fitz.open(self.file_path)
        response = ""
        ocr = RapidOCR()

        for page in doc:
            text = page.get_text()
            response += text + "\n"

            imgs = page.get_images()

            for img in imgs:
                pix = fitz.Pixmap(doc, img[0])
                img_array = np.frombuffer(pix.samples, dtype = np.uint8).reshape(pix.height, pix.width, -1)
                result, _ = ocr(img_array)

                if result:
                    ocr_result = [line[1] for line in result]
                    response += "\n".join(ocr_result)
        return partition_text(text = response, **self.unstructured_kwargs)

if __name__ == "__main__":
    loader = PDFLoader(file_path = "../../../assets/test.pdf")
    text = loader.load()
    print(text)