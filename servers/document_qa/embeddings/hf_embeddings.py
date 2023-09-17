from __future__ import annotations

from typing import Any, List, Dict

from .embedding import BaseEmbedding

class HFEmbedding(BaseEmbedding):
    """HuggingFace Embedding"""
    def __init__(
            self, 
            model_name: str, 
            cache_folder: str = None,
            model_kwargs: Dict[str, Any] = None,
            encode_kwargs: Dict[str, Any] = None,
            multi_process: bool = False

        ) -> None:
        super().__init__()
        self.encode_kwargs = encode_kwargs
        self.multi_process = multi_process

        try:
            import sentence_transformers
        except ImportError:
            raise ImportError(
                "`langchain` package not found, please install it with "
                "`pip install sentence_transformers`"
            )
        
        self.client = sentence_transformers.SentenceTransformer(
            model_name_or_path = model_name,
            cache_folder = cache_folder,
            **model_kwargs,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        
        texts = list(map(lambda x: x.replace("\n", " "), texts))

        if self.multi_process:
            import sentence_transformers
            pool = self.client.start_multi_process_pool()
            embeddings = self.client.encode_multi_process(texts, pool)
            sentence_transformers.SentenceTransformer.stop_multi_process_pool(pool)
        else:
            embeddings = self.client.encode(texts, **self.encode_kwargs)

        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
    

        

