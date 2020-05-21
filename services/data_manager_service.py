from models.data_service import DataService
import config


class DataManagerService():

    data_model = None

    def __init__(self, _active_dataset):
        """
        Constructor
        @params:
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.data_model = DataService(_active_dataset)

    def get_datasets(self):
        """
        Return a list of avalable datasets
        @params:
        """

        return self.data_model.get_datasets()

    def save_dataset(self, _file):
        """
        Save a new dataset to disk
        @params:
            _file     - Required  : file with new dataset (request.files)
        """

        self.data_model.save_dataset(_file)
