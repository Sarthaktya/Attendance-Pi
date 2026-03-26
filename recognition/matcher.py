import numpy as np


class IdentityMatcher:
    def __init__(self, known_embeddings, threshold=0.65):
        self.known_embeddings = known_embeddings
        self.threshold = threshold

    def match(self, embedding):
        best_name = None
        best_score = -1.0

        for name, ref_emb in self.known_embeddings.items():
            score = float(np.dot(embedding, ref_emb))
            if score > best_score:
                best_score = score
                best_name = name

        if best_score >= self.threshold:
            return best_name, best_score

        return None, best_score
