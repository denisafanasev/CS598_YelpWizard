from models.data_service import DataService
import math
import pickle
import config
import random
import gensim.matutils as matutils
import utils.ada as ada


class CousinesService():

    data_service = None
    topics2cousines = []
    cuisine_matrix_ed = []
    cuisine_matrix_cs = []

    def model_load(self, _model_name, _active_dataset):
        """
        Load pre-trained model from disk
        @params:
            _model_name        - Required  : name of the topic mining model(Str)
            _active_dataset    - Required  : name of active dataset (Str)
        """

        # TODO: тут тоже надо бы проверить все ли файлы на месте (и исключения отработать)
        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2topics2cousines, 'rb') as f:
            _topics2cousines = pickle.load(f)

        return _topics2cousines

    def euclidean_distance(self, a, b):
        """
        Return euclidean distance between two vectors
        @params:
            a    - Required  : first vector (list of floats)
            b    - Required  : second vector (list of floats)
        """

        w = 0
        for i in range(0, len(a)):
            w = w + (a[i][1] - b[i][1]) * (a[i][1] - b[i][1])

        w = math.sqrt(w)
        return w

    def sim_matrix(self, _topics2cousines):
        """
        Return two similarities matrix
        @params:
            _topics2cousines    - Required  : list of topics vectors for list of cuisines (list of list of floats)
        """

        _cuisine_matrix_e = []
        _cuisine_matrix_c = []

        for i, doc_a in enumerate(_topics2cousines):

            doc_a = doc_a[1]

            sim_vecs_e = []
            sim_vecs_c = []

            for j, doc_b in enumerate(_topics2cousines):
                doc_b = doc_b[1]

                w_sum_cs = matutils.cossim(doc_a, doc_b)
                w_sum_ed = 1 - self.euclidean_distance(list(doc_a), list(doc_b))

                if w_sum_ed < 0:
                    w_sum_ed = -1 * w_sum_ed

                sim_vecs_e.append(w_sum_ed)
                sim_vecs_c.append(w_sum_cs)

            _cuisine_matrix_e.append([_topics2cousines[i][0], sim_vecs_e])
            _cuisine_matrix_c.append([_topics2cousines[i][0], sim_vecs_c])

        return _cuisine_matrix_e, _cuisine_matrix_c

    def __init__(self, _model_name, _active_dataset):
        """
        Constructor
        @params:
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.data_service = DataService(_active_dataset)
        self.topics2cousines = self.model_load(_model_name, _active_dataset)
        self.cuisine_matrix_ed, self.cuisine_matrix_cs  = self.sim_matrix(
            self.topics2cousines)

    def get_topic_for_cousine(self, _cousine):
        """
        Return topics vector for given cuisine
        @params:
            _cousine     - Required  : name of the cuisine (Str)
        """

        _max_w = 0
        _topic = 0

        for _vector in self.topics2cousines:
            if _vector[0] == _cousine:
                for w in enumerate(_vector[1]):
                    if _max_w < w[1][1]:
                        _max_w = w[1][1]
                        _topic = w[1][0]

        return _topic, _max_w

    def get_cousines(self, _active_topic=None, _active_cousine=None, active_sim_function=None):
        """
        Return a list of cuisines for topic
        @params:
            _active_topic        - Option  : name of the active topic (Str)
            _active_cousine      - Option  : name of active cuisine (Str)
            _active_sim_function - Option  : name of similarity function (Str)
        """

        # TODO: сделать рефакторинг, логику, связанную с представлением, перенести в контроллер
        _data = []

        i = random.randint(0, len(self.topics2cousines))

        if _active_cousine is not None:
            # найдем номер активной кухни по ее названию
            for i, _temp in enumerate(self.topics2cousines):
                if _temp[0] == _active_cousine:
                    break

        else:
            # найдем основную кухню для данного топика

            _max_i = 0
            _max_w = 0

            for i, _temp in enumerate(self.topics2cousines):
                _topic, _w = self.get_topic_for_cousine(_temp[0])

                if _topic == _active_topic:
                    if _max_w < _w:
                        _max_w = _w
                        _max_i = i

            i = _max_i

        # TODO: index of range bug
        if active_sim_function is not None:
            if active_sim_function == "sim_ed":
                _cousine_vec = self.cuisine_matrix_ed[i]
            else:
                _cousine_vec = self.cuisine_matrix_cs[i]
        else:
            _cousine_vec = self.cuisine_matrix_ed[i]

        for j, _cousine in enumerate(_cousine_vec[1]):

            if _active_cousine is not None:
                if i == j:
                    _count = 70000
                else:
                    _count = int(math.exp(_cousine * 10))
            else:
                _count = int(math.exp(_cousine * 10))

            _data.append(
                {"tag": self.topics2cousines[j][0], "count": _count})

        # оставляем только те кухни, для которых выбранные топик - самый доминирующий
        _data_filtered = []
        if _active_topic is not None:
            for _cousine in _data:
                _topic, _w = self.get_topic_for_cousine(_cousine['tag'])
                if _topic == _active_topic:
                    _data_filtered.append(_cousine)
        else:
            _data_filtered = _data

        return _data_filtered

    def get_cousine_number(self, _active_topic=None):
        """
        Return number of cuisines for topic
        @params:
            _active_topic     - Option  : name of the active topic (Str)
        """

        return len(self.get_cousines(_active_topic))
