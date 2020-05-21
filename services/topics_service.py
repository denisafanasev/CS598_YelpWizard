from gensim import corpora, models, similarities, matutils, parsing
from gensim.models import LdaModel
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
import config
import pickle

from models.data_service import DataService


class TopicsService():

    data_service = None
    model = gensim.models.basemodel.BaseTopicModel()

    def model_save(self, _model, _model_name, _active_dataset):
        """
        Save trained model to disk
        @params:
            _model          - Required  : model (gensim.models.LdaModel)
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        result = self.data_service.save_model(_model, _model_name, _active_dataset)

        return result

    def model_load(self, _model_name, _active_dataset):
        """
        Load pre-trained model from disk
        @params:
            _model_name        - Required  : name of the topic mining model(Str)
            _active_dataset    - Required  : name of active dataset (Str)
        """

        # TODO: тут надо проверять что созданы все нужные файлы
        # TODO: перенести загрузку в слой работы с данными
        try:
            self.model = models.LdaModel.load(
                config.path2data + _active_dataset + "." + _model_name + ".model")
            # self.model = models.LdaModel.load(config.path2data + "lda.model")
        except Exception as e:
            self.model = self.process_topics_mining(_active_dataset)
            self.model = models.LdaModel.load(
                config.path2data + _active_dataset + "." + _model_name + ".model")

        return True

    def __init__(self, _model_name, _active_dataset):
        """
        Constructor
        @params:
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.data_service = DataService(_active_dataset)
        self.model_load(_model_name, _active_dataset)

    def topic_mining(self, _active_dataset):
        """
        Internal function for process topic mining and sace trained models
        @params:
            _active_dataset - Required  : name of active dataset (Str)
        """

        # TODO: перенести сохранение в файлы в слой models

        print("topic minning start..")
        vectorizer = TfidfVectorizer(max_df=0.5, max_features=500,
                                     min_df=2, stop_words='english',
                                     use_idf=True)

        _cousines, _reviews = self.data_service.get_reviews_for_cousines()

        print("text uploaded")
        text = _reviews

        X = vectorizer.fit_transform(text)
        print("text transformed")

        # mapping from feature id to acutal word
        id2words = {}
        for i, word in enumerate(vectorizer.get_feature_names()):
            id2words[i] = word

        corpus = matutils.Sparse2Corpus(X, documents_columns=False)

        print("train LDA models")
        #####################################################################
        _model_name = "LDA10"
        self.modelLDA_10 = LdaModel(corpus, num_topics=10, id2word=id2words)
        self.model_save(self.modelLDA_10, _model_name, _active_dataset)

        _cousines2topics = self.modelLDA_10.get_document_topics(
            corpus, minimum_probability=0)
        _topics2cousines = []
        for i, _topics_weight in enumerate(_cousines2topics):
            _topics2cousines.append([_cousines[i], _topics_weight])
        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2topics2cousines, 'wb') as f:
            pickle.dump(_topics2cousines, f)

        _rests_topics = []
        _rests = self.data_service.get_rests()
        for _rest in _rests:

            _cousines = self.data_service.get_cousines_for_rest(_rest[0])

            _rest_vector = []
            for _rc in _cousines:
                for _c in _topics2cousines:
                    if _c[0] == _rc:
                        if not _rest_vector:
                            # _rest_vector = _c[1]
                            for _t, _w in _c[1]:
                                _rest_vector.append([_t, float(_w)])
                        else:
                            for _t, _w in _c[1]:
                                _rest_vector[_t][1] = (_rest_vector[_t][1] + float(_w)) / 2

            _rests_topics.append([_rest, _rest_vector, _cousines])

        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2rests2topics, 'wb') as f:
            pickle.dump(_rests_topics, f)

        #####################################################################
        _model_name = "LDA15"
        self.modelLDA_15 = LdaModel(corpus, num_topics=15, id2word=id2words)
        self.model_save(self.modelLDA_15, _model_name, _active_dataset)

        _cousines, _reviews = self.data_service.get_reviews_for_cousines()

        _cousines2topics = self.modelLDA_15.get_document_topics(
            corpus, minimum_probability=0)
        _topics2cousines = []
        for i, _topics_weight in enumerate(_cousines2topics):
            _topics2cousines.append([_cousines[i], _topics_weight])
        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2topics2cousines, 'wb') as f:
            pickle.dump(_topics2cousines, f)

        _rests_topics = []
        _rests = self.data_service.get_rests()
        for _rest in _rests:

            _cousines = self.data_service.get_cousines_for_rest(_rest[0])

            _rest_vector = []
            for _rc in _cousines:
                for _c in _topics2cousines:
                    if _c[0] == _rc:
                        if not _rest_vector:
                            # _rest_vector = _c[1]
                            for _t, _w in _c[1]:
                                _rest_vector.append([_t, float(_w)])
                        else:
                            for _t, _w in _c[1]:
                                _rest_vector[_t][1] = (
                                    _rest_vector[_t][1] + float(_w)) / 2

            _rests_topics.append([_rest, _rest_vector, _cousines])

        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2rests2topics, 'wb') as f:
            pickle.dump(_rests_topics, f)

        #####################################################################
        _model_name = "LDA20"
        self.modelLDA_20 = LdaModel(corpus, num_topics=20, id2word=id2words)
        self.model_save(self.modelLDA_20, _model_name, _active_dataset)

        _cousines, _reviews = self.data_service.get_reviews_for_cousines()

        _cousines2topics = self.modelLDA_20.get_document_topics(
            corpus, minimum_probability=0)
        _topics2cousines = []
        for i, _topics_weight in enumerate(_cousines2topics):
            _topics2cousines.append([_cousines[i], _topics_weight])
        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2topics2cousines, 'wb') as f:
            pickle.dump(_topics2cousines, f)

        _rests_topics = []
        _rests = self.data_service.get_rests()
        for _rest in _rests:

            _cousines = self.data_service.get_cousines_for_rest(_rest[0])

            _rest_vector = []
            for _rc in _cousines:
                for _c in _topics2cousines:
                    if _c[0] == _rc:
                        if not _rest_vector:
                            # _rest_vector = _c[1]
                            for _t, _w in _c[1]:
                                _rest_vector.append([_t, float(_w)])
                        else:
                            for _t, _w in _c[1]:
                                _rest_vector[_t][1] = (
                                    _rest_vector[_t][1] + float(_w)) / 2

            _rests_topics.append([_rest, _rest_vector, _cousines])

        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2rests2topics, 'wb') as f:
            pickle.dump(_rests_topics, f)

        ###################################################################

        print("TRAIN MODELS DONE")
        return self.modelLDA_10

    def get_topics(self, _num_words=10):
        """
        Return a list of topics
        @params:
            _num_words     - Option  : number of words for each topic to return (Int)
        """

        _topics = []
        for i, item in enumerate(self.model.show_topics(num_topics=20, num_words=_num_words, formatted=False)):
            _topic_words = []
            for term, weight in item[1]:
                _topic_words.append([term, weight])

            _topics.append([i, _topic_words])

        return _topics

    def process_topics_mining(self, _active_dataset):
        """
        Process topic mining and sace trained models
        @params:
            _active_dataset - Required  : name of active dataset (Str)
        """

        _result = self.topic_mining(_active_dataset)
        return _result

    def get_review_number(self):
        """
        Return a number of reviews in active dataset
        @params:
        """

        return self.data_service.get_review_number()
