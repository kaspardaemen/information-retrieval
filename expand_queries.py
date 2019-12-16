from gensim.models import KeyedVectors

# Load Google's pre-trained Word2Vec model.
word_vectors = KeyedVectors.load_word2vec_format("./data/GoogleNews-vectors-negative300.bin", binary=True)
result = word_vectors.similar_by_word("cat")
print(result)
# print("{}: {:.4f}".format(*result[0]))
