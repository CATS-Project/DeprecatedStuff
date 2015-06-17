# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.com"
__status__ = "Production"

from gensim.corpora import MmCorpus
from gensim.models import LdaMulticore
from gensim.models import LsiModel
from gensim.models import HdpModel
from multiprocessing import cpu_count
from market_matrix import MarketMatrix

"""
class for topic modeling
implemets:
- LDA (Latent Dirichlet Allocation)
- LSI (Latent Semantic Indexing)
- HDP (Hierarchical Dirichlet Process)

Params:
    - id2words - id with
    - filename - that points to the location of a Market Matrix file (slower)
    - corpus - in memory corpus list of list of sets where a set contains the word id and its weight (faster)
    e.g. [[(),(),...,()],[(),(),...,()],[(),(),...,()],...,[(),(),...,()]]

    use either the filename or the corpus

"""


class TopicModeling:
    def __init__(self, id2word, corpus=None, filename=None):
        if corpus:
            self.corpus = corpus
        if filename:
            self.corpus = MmCorpus(filename)
        self.id2word = id2word

    def topicsLDA(self, num_topics=10, num_iterations=10000, num_words=10):
        num_workers = cpu_count()

        # LdaMulticore(corpus=None, num_topics=100, id2word=None, workers=None, chunksize=2000, passes=1, batch=False, alpha='symmetric', eta=None, decay=0.5, offset=1.0, eval_every=10, iterations=50, gamma_threshold=0.001)
        lsa = LdaMulticore(corpus=self.corpus, num_topics=num_topics, id2word=self.id2word, iterations=num_iterations,
                           workers=num_workers)

        # show_topics(num_topics=10, num_words=10, log=False, formatted=True)
        # For num_topics number of topics, return num_words most significant words (10 words per topic, by default).
        # The topics are returned as a list – a list of strings if formatted is True, or a list of (probability, word) 2-tuples if False.
        # If log is True, also output this result to log.
        # Unlike LSA, there is no natural ordering between the topics in LDA. The returned num_topics <= self.num_topics subset of all topics is therefore arbitrary and may change between two LDA training runs.

        return lsa.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)

    def topicsLSI(self, num_topics=10, num_words=10):
        # LsiModel(corpus=None, num_topics=200, id2word=None, chunksize=20000, decay=1.0, distributed=False, onepass=True, power_iters=2, extra_samples=100)
        lsi = LsiModel(corpus=self.corpus, num_topics=num_topics, id2word=self.id2word)

        # show_topics(num_topics=-1, num_words=10, log=False, formatted=True)
        # Return num_topics most significant topics (return all by default).
        # For each topic, show num_words most significant words (10 words by default).
        # The topics are returned as a list – a list of strings if formatted is True, or a list of (weight, word) 2-tuples if False.
        # If log is True, also output this result to log.

        return lsi.show_topics(num_words=num_words, formatted=False)

    def topicsHDP(self, num_topics=-1, topn=20):
        # HdpModel(corpus, id2word, max_chunks=None, max_time=None, chunksize=256, kappa=1.0, tau=64.0, K=15, T=150, alpha=1, gamma=1, eta=0.01, scale=1.0, var_converge=0.0001, outputdir=None)
        hdp = HdpModel(corpus=self.corpus, id2word=self.id2word)

        # show_topics(topics=20, topn=20, log=False, formatted=True)
        # Print the topN most probable words for topics number of topics. Set topics=-1 to print all topics.
        # Set formatted=True to return the topics as a list of strings, or False as lists of (weight, word) pairs.

        return hdp.show_topics(topics=num_topics, topn=topn, formatted=False)

# these are just tests
if __name__ == '__main__':
    mm = MarketMatrix(dbname='TwitterDB')
    # with query
    mm.build(query=True)
    # entire vocabulary
    # mm.build()
    id2word, id2tweetID, corpus = mm.buildCountMM()
    topic_model = TopicModeling(id2word=id2word, corpus=corpus)
    print 'LDA Count time:'
    for topic in topic_model.topicsLDA(num_topics=50):
        print topic
    print 'LSI Count time:'
    for topic in topic_model.topicsLSI():
        print topic
    print 'HDP Count time:'
    for topic in topic_model.topicsHDP():
        print topic