import logging
import random
import numpy as np
from gensim.models import doc2vec
from gensim.models.doc2vec import Doc2Vec

from .model_builder import ModelBuilder
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class doc2VecBuilder(ModelBuilder):

    def __init__(self, corpus):
        self.corpus = corpus


    def initialize_model(self):
        logging.info("Building Doc2Vec vocabulary")
        self.model = doc2vec.Doc2Vec(min_count=1,  # Ignores all words with total frequency lower than this
                              window=10,
                              # The maximum distance between the current and predicted word within a sentence
                              vector_size=300,  # Dimensionality of the generated feature vectors
                              workers=5,  # Number of worker threads to train the model
                              alpha=0.025,  # The initial learning rate
                              min_alpha=0.00025,  # Learning rate will linearly drop to min_alpha as training progresses
                              dm=1)  # dm defines the training algorithm. If dm=1 means 'distributed memory' (PV-DM)
        # and dm =0 means 'distributed bag of words' (PV-DBOW)
        self.model.build_vocab(self.corpus)

    def train_model(self):
        logging.info("Training Doc2Vec model")
        # 10 epochs take around 10 minutes on my machine (i7), if you have more time/computational power make it 20
        for epoch in range(10):
            logging.info('Training iteration #{0}'.format(epoch))
            self.model.train(self.corpus, total_examples=self.model.corpus_count, epochs=self.model.epochs)
            # shuffle the corpus
            random.shuffle(self.corpus)
            # decrease the learning rate
            self.model.alpha -= 0.0002
            # fix the learning rate, no decay
            self.model.min_alpha = self.model.alpha

    def save_model(self):
        logging.info("Saving trained Doc2Vec model")
        self.model.save("./classifiers/d2v.model")

    def load_model(self):
        logging.info("Loading trained Doc2Vec model")
        d2v = Doc2Vec.load("./classifiers/d2v.model")
        self.model = d2v
        return d2v


