from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

folder = 'word_embeddings/'

# embeddings = [
#     ('GoogleNews-vectors-negative300.bin', 'GoogleNews'),
#     ('lexvec.enwiki+newscrawl.300d.W.pos.vectors', 'lexvec'),
#     ('deps.words', 'deps')
# ]

# for infile,outfile in embeddings:
#     loadEmbedding(folder, infile, outfile)

# googleNews = 'word_embeddings/GoogleNews'
# model = KeyedVectors.load_word2vec_format('word_embeddings/GoogleNews-vectors-negative300.bin', binary=True)
# model.init_sims(replace=True)
# model.save(googleNews + '.model')
# model.save_word2vec_format(outfile + '.model.bin', binary=True)
# model.save_word2vec_format(outfile + '.model.txt', binary=False)


def loadEmbedding(folder, infile, outfile):
    model = KeyedVectors.load_word2vec_format(folder + infile, binary=False)
    model.init_sims(replace=True)
    model.save(folder + outfile)



loadEmbedding(folder, 'wiki.simple.bin', 'wiki_simple')

#loadEmbedding(folder, 'GoogleNews-vectors-negative300.bin', 'GoogleNews')


# glove2word2vec(folder + 'glove.6B.300d.txt', folder + 'glove.6b.300d.bin')
# loadEmbedding(folder, 'glove.6B.300d.bin', 'Glove6B300')

#loadEmbedding(folder, 'lexvec.enwiki+newscrawl.300d.W.pos.vectors', 'lexvec')
#loadEmbedding(folder, 'deps.words', 'deps')