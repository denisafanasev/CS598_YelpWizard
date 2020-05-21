from services.rests_service import RestsService
import utils.ada as ada


class RestsPageController():

    rests_service = ""

    def __init__(self, _model_name, _active_dataset):
        """
        Constructor
        @params:
            _model_name     - Required  : name of active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.reload(_model_name, _active_dataset)

    def rest_number(self, _active_topic, _active_cousine):
        """
        Return number of rest
        @params:
            _model_name     - Required  : name of active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        return self.rests_service.get_rest_number(_active_topic, _active_cousine)

    def rests(self, _active_topic, _active_cousine):
        """
        Return a list of rest
        @params:
            _model_name     - Required  : name of active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        return self.rests_service.get_rests(_active_topic, _active_cousine)

    def reload(self, _model_name, _active_dataset):
        """
        Reload data for defined topic model and active dataset
        @params:
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.rests_service = RestsService(_model_name, _active_dataset)
