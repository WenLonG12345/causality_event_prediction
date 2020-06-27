from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

glove_file = datapath('D:\Downloads\glove.6B\glove.6B.200d.txt')
tmp_file = get_tmpfile("D:\Downloads\glove.6B\glove.6B.200d.word2vec")

glove2word2vec(glove_file, tmp_file)
