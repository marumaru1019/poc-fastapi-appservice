from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Sentence-BERTモデルの読み込み
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


@app.get("/")
async def read_root():
    return {"message": "Welcome to Sentence-BERT API"}


@app.get("/embed")
async def embed_sentence(sentence: str):
    # 入力文をエンベッドする
    embeddings = model.encode([sentence])
    return {"embedding": embeddings[0].tolist()}

@app.get("/similarity")
async def similarity_between_sentences(sentence1: str, sentence2: str):
    # 2つの文の埋め込みを計算
    embeddings = model.encode([sentence1, sentence2])
    
    # コサイン類似度を計算
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    return {"similarity": float(similarity)}