__all__ = ["load_embedding"]

def load_embedding(
    embedding_type = "hf",
    embedding_device = "cpu",
    **kwards
):
    
    if embedding_type == "openai":
        import sys
        sys.path.append("..")
        from configs.pdf_knowledge_config import CHUNK_SIZE
        from langchain.embeddings.openai import OpenAIEmbeddings
        assert "openai_api_key" in kwards.keys(), "OpenAI key needed!"
        embedding = OpenAIEmbeddings(openai_api_key = kwards["openai_api_key"], chunk_size = CHUNK_SIZE)
    elif embedding_type == "hf":
        from langchain.embeddings.huggingface import HuggingFaceEmbeddings
        assert "model_name" in kwards.keys(), "model_name needed!"
        embedding = HuggingFaceEmbeddings(model_name = kwards["model_name"], model_kwargs={'device': embedding_device})
    elif embedding_type == "wenxin":
        from langchain_wenxin.embeddings import WenxinEmbeddings
        from configs.pdf_knowledge_config import API_KEY, SECRET_KEY
        embedding = WenxinEmbeddings(model="embedding-v1", baidu_api_key=API_KEY, baidu_secret_key=SECRET_KEY)
    else:
        raise Exception("Developing......")

    return embedding