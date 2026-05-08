import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import util

class SearchService:
    def __init__(self, documents, model):
        self.documents = documents
        self.model = model

    def keyword_search(self, query, k=5):
        contents = [doc['content'] for doc in self.documents]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(contents)
        query_vec = vectorizer.transform([query])
        scores = (tfidf_matrix * query_vec.T).toarray().flatten()
        
        sorted_indices = np.argsort(scores)[::-1]
        return [self.documents[i]["id"] for i in sorted_indices if scores[i] > 0]

    def semantic_search(self, query, threshold=0.35):
        contents = [doc['content'] for doc in self.documents]
        doc_embeddings = self.model.encode(contents, convert_to_tensor=True)
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, doc_embeddings)[0]
        
        results = []
        for i, score in enumerate(cos_scores):
            if score > threshold:
                results.append((self.documents[i]["id"], float(score)))
                
        results.sort(key=lambda x: x[1], reverse=True)
        return [res[0] for res in results]

    def hybrid_search(self, query, k=5):
        kw_ids = self.keyword_search(query)
        sm_ids = self.semantic_search(query)
        
        rrf_scores = {}
        k_constant = 60
        
        for rank, doc_id in enumerate(kw_ids):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (k_constant + rank + 1)
            
        for rank, doc_id in enumerate(sm_ids):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (k_constant + rank + 1)
            
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_docs[:k]:
            doc = next(d for d in self.documents if d["id"] == doc_id)
            results.append({
                "id": doc_id,
                "type": doc["type"],
                "score": round(score, 4),
                "content": doc["content"]
            })
            
        return results
