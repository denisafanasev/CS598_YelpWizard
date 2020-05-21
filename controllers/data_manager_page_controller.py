from services.data_manager_service import DataManagerService
import utils.ada as ada


class DataManagerPageController():

    data_manager_service = None

    def __init__(self, _active_dataset):
        """
        Constructor
        @params:
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.data_manager_service = DataManagerService(_active_dataset)

    def get_datasets(self):
        """
        Return a list of avalable datasets
        @params:
        """

        return self.data_manager_service.get_datasets()

    def upload_dataset(self, _file):
        """
        Save a new dataset file
        @params:
            _file     - Required  : file with new dataset (request.files)
        """

        data_manager_service.save_dataset(_file)
