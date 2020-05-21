from models.data_service import DataService
import config


class DataManagerService():

    data_model = None

    def __init__(self, _active_dataset):
        self.data_model = DataService(_active_dataset)

    def get_datasets(self):
        return self.data_model.get_datasets()

    def save_dataset(self, _file):
        self.data_model.save_dataset(_file)
