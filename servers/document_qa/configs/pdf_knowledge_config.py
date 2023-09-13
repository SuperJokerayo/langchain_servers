import os

API_KEY = "79SrUUTLX5B3cSs5eCRswihm"

SECRET_KEY = "asiwKEgewTVq54lbnjdxVL8Qumbp71RG"

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec-paraphrase": "shibing624/text2vec-base-chinese-paraphrase",
    "text2vec-sentence": "shibing624/text2vec-base-chinese-sentence",
    "text2vec-multilingual": "shibing624/text2vec-base-multilingual",
    "text2vec-bge-large-chinese": "shibing624/text2vec-bge-large-chinese",
    "m3e-small": "moka-ai/m3e-small",
    "m3e-base": "moka-ai/m3e-base",
    "m3e-large": "moka-ai/m3e-large",
    "bge-small-zh": "BAAI/bge-small-zh",
    "bge-base-zh": "BAAI/bge-base-zh",
    "bge-large-zh": "BAAI/bge-large-zh",
    "bge-large-zh-noinstruct": "BAAI/bge-large-zh-noinstruct",
    "piccolo-base-zh": "sensenova/piccolo-base-zh",
    "piccolo-large-zh": "sensenova/piccolo-large-zh",
    "text-embedding-ada-002": os.environ.get("OPENAI_API_KEY")
}

# 选用的 Embedding 名称
EMBEDDING_MODEL = "m3e-base"

CHUNK_SIZE = 250

OVERLEP_SIZE = 50  

# 基于本地知识问答的提示词模版（使用Jinja2语法，简单点就是用双大括号代替f-string的单大括号
PROMPT_TEMPLATE = """<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，不允许在答案中添加编造成分，答案请使用中文。 </指令>

<已知信息>{{ context }}</已知信息>

<问题>{{ question }}</问题>"""