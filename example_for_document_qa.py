from servers.document_qa.loaders.pdf_loader import PDFLoader
from servers.document_qa.splitters.recursive_character_text_splitter import RecursiveCharacterTextSplitter
from servers.document_qa.embeddings.hf_embeddings import HFEmbedding
from servers.document_qa.vectordb.faiss import FaissDB
from servers.document_qa.prompts.prompt import Prompt
from llm.Baidu_QFLLM.llama_13b_api import entry

path = "./assets/ai4s.pdf"
loader = PDFLoader(path)
pdf_content = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 600, chunk_overlap = 100)
chunks = splitter.split(pdf_content)
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HFEmbedding(
    model_name = model_name,
    model_kwargs = model_kwargs,
    encode_kwargs = encode_kwargs,
    multi_process = True
)

db = FaissDB.from_texts(chunks, hf)

query = "What are the challenges for using AI in science?"

docs = db.similarity_search(query)

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""

docs_variables = {"context": docs}
query_variables = {"question": query}

prompt = Prompt(template)

top_k = 5

input = prompt.generate_prompt_from_docs(top_k, docs_variables, query_variables)

print(entry(input))

    

