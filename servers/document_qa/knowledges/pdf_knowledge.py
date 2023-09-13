import sys
sys.path.append("..")

from configs.pdf_knowledge_config import CHUNK_SIZE, OVERLEP_SIZE
from loaders.pdf_loader import PDFLoader
from splitters.text_splitter import AliTextSplitter

from embeds.load_embedding import load_embedding

from base_knowledge import BaseKnowledge

class PDFKnowledge(BaseKnowledge):
    def __init__(self, file_path: str, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.knowledge_name = "pdf_knowledge"
        self.doc = None
        self.doc_loader = None
        self.doc_splitter = None

    def extract_knowledge(self):
        self.doc_loader = PDFLoader(file_path = self.file_path, autodetect_encoding = True)
        splitter = AliTextSplitter(pdf = True, chunk_size = CHUNK_SIZE, chunk_overlap = OVERLEP_SIZE)
        self.doc = self.doc_loader.load_and_split(splitter)
        return self.doc


if __name__ == "__main__":
    pdf_knowledge = PDFKnowledge(file_path = "../../../assets/test.pdf")
    knowledge = pdf_knowledge.extract_knowledge()

    print(knowledge[0])

    embedding = load_embedding(embedding_type = "wenxin")
    print(embedding.embed_documents(knowledge[0].page_content))