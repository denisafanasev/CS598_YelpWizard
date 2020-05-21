from models.data_service import DataService
import config
import pickle


class RestsService():

    rests2topics = []

    data_service = None

    def model_load(self, _model_name, _active_dataset):
        with open(config.path2data + _active_dataset + "." + _model_name + "_" + config.path2rests2topics, 'rb') as f:
            _topics2cousines = pickle.load(f)

        return _topics2cousines

    def __init__(self, _model_name, _active_dataset):
        self.data_service = DataService(_active_dataset)
        self.rests2topics = self.model_load(_model_name, _active_dataset)

    def find_max_topic(self, _vector):
        _max_i = 0
        _max_w = 0
        for _v in _vector:
            if _max_w < _v[1]:
                _max_w = _v[1]
                _max_i = _v[0]

        return _max_i, _max_w

    def get_rests(self, _active_topic, _active_cousine):
        _rests = []
        for _r in self.rests2topics:

            _to_add = True
            # проверим, какая тема является основной для ресторана
            if _active_topic is not None:
                _topic, _w = self.find_max_topic(_r[1])
                if _topic != _active_topic:
                    _to_add = False

            # проверим, есть ли у ресторана выбраная пользователем кухня
            if _active_cousine is not None:
                if _active_cousine not in _r[2]:
                    _to_add = False

            if _to_add:
                _rests.append([_r[0][3], _r[0][1], _r[0][2]])

        return _rests

    def get_rest_number(self, _active_topic, _active_cousine):
        return len(self.get_rests(_active_topic, _active_cousine))
