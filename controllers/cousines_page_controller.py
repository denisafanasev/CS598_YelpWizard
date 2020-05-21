import random
import math
from services.cousines_service import CousinesService
import utils.ada as ada


class CousinesPageController():

    cousines_service = ""

    def __init__(self, _model_name, _active_dataset):
        """
        Constructor
        @params:
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.reload(_model_name, _active_dataset)

    def cousine_number(self, _active_topic):
        """
        Return number of cuisines for defined topic
        @params:
            _active_dataset - Required  : name of active topic (Str)
        """

        return self.cousines_service.get_cousine_number(_active_topic)

    def cousines(self, _active_topic, _active_cousine, _active_sim_function):
        """
        Return a list of cuisines
        @params:
            _active_topic        - Required  : name of the active topic (Str)
            _active_cousine      - Required  : name of active cuisine (Str)
            _active_sim_function - Required  : name of similarity function (Str)
        """

        _data = []
        i, _data = self.cousines_service.get_cousines(
            _active_topic, _active_cousine, _active_sim_function)

        # преобразование списка кухнь для визуализации

        _data_to_show = []
        for j, _cousine in enumerate(_data):

            if _active_cousine is not None:
                if i == j:
                    _count = 70000
                else:
                    _count = int(math.exp(_cousine[1] * 10))
            else:
                _count = int(math.exp(_cousine[1] * 10))

            _data_to_show.append(
                {"tag": _cousine[0], "count": _count})

        return _data_to_show

    def reload(self, _model_name, _active_dataset):
        """
        Reload data for defined topic model and active dataset
        @params:
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.cousines_service = CousinesService(_model_name, _active_dataset)
