from langchain.text_splitter import CharacterTextSplitter
import re
from typing import List

import sys
sys.path.append("..")
from loaders.pdf_loader import PDFLoader

class AliTextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf

    def split_text(self, text: str) -> List[str]:
        if self.pdf:
            text = re.sub(r"\n{3,}", r"\n", text)
            text = re.sub('\s', " ", text)
            text = re.sub("\n\n", "", text)
        print("test")
        try:
            from modelscope.pipelines import pipeline
        except ImportError:
            raise ImportError(
                "Could not import modelscope python package. "
                "Please install modelscope with `pip install modelscope`. "
            )

        

        p = pipeline(
            task = "document-segmentation",
            model = 'damo/nlp_bert_document-segmentation_english-base',
            device = "cuda")
        result = p(documents = text)
        sent_list = [i for i in result["text"].split("\n\t") if i]
        return sent_list
    

if __name__ == "__main__":
    

    loader = PDFLoader(file_path = "../../../assets/test.pdf", autodetect_encoding = True)
    # text = loader.load()[0].page_content
    # import faulthandler
    # faulthandler.enable()
    # print(text)
    splitter = AliTextSplitter(pdf = True, chunk_size = 250, chunk_overlap = 0)
    docs = loader.load_and_split(splitter)

    print(docs[0])