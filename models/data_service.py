import json
import pickle
import random
import os.path
import config

from os import listdir
from os.path import isfile, join

import pandas as pd

from models.data_preprocessing import DataProcessor


class DataService():

    _busineses = []
    _reviews = []
    _cousines = []
    _cousines2business2reviews = []
    _dataset_name = ""

    def is_preprocessing_needed(self, _active_dataset):

        _is_all_files_existed = True

        if not os.path.isfile(config.path2data + _active_dataset + "." + config.path2business):
            _is_all_files_existed = False
        if not os.path.isfile(config.path2data + _active_dataset + "." + config.path2cousines2business):
            _is_all_files_existed = False
        if not os.path.isfile(config.path2data + _active_dataset + "." + config.path2reviews):
            _is_all_files_existed = False

        return not _is_all_files_existed

    def data_preprocessing(self, _active_dataset):
        _dp = DataProcessor()
        _dp.process_raw_data(_active_dataset)

    def load_data(self, _active_dataset):
        print("Loading business data...")
        self._busineses = pd.read_csv(config.path2data + _active_dataset + "." + config.path2business)

        print("Loading cousines data...")
        self._cousines2business2reviews = pd.read_csv(
            config.path2data + _active_dataset + "." + config.path2cousines2business)

        # we have to leave only data from existed business
        _business_ids = list(self._busineses['business_id'])
        self._cousines2business2reviews = self._cousines2business2reviews.loc[self._cousines2business2reviews['business_id'].isin(
            _business_ids)]

        self._cousines = list(set(self._cousines2business2reviews['cousine']))

        print("Loading reviews data...")
        self._reviews = pd.read_csv(
            config.path2data + _active_dataset + "." + config.path2reviews)
        self._reviews = self._reviews.loc[self._reviews['business_id'].isin(
            _business_ids)]

        # make cousines2review table
        self._cousines2business2reviews = self._cousines2business2reviews.merge(
            self._reviews, on='business_id', how='right')

        # теперь отфильтруем таблицу с ресторанами и оставим в ней только те, у которых есть review
        _business_ids = list(self._cousines2business2reviews['business_id'].unique())
        self._busineses = self._busineses.loc[self._busineses['business_id'].isin(
            _business_ids)]

        print("Loading data DONE")

    # singleton pattern implementation
    def __new__(cls, _active_dataset):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataService, cls).__new__(cls)
        return cls.instance

    def __init__(self, _active_dataset):
        print("Checking data files...")
        if self.is_preprocessing_needed(_active_dataset):
            self.data_preprocessing(_active_dataset)
        else:
            print("All data files OK")

        if self._dataset_name != _active_dataset:
            self._dataset_name = _active_dataset
            self.load_data(_active_dataset)

    def get_rest_number(self):
        return int(self._busineses.shape[0])

    def get_cousine_number(self):
        return len(self._cousines)

    def get_review_number(self):
        return int(self._reviews.shape[0])

    def get_reviews(self):
        return list(self._reviews['text'])

    def get_rests(self):
        _result = []

        for index, row in self._busineses.iterrows():
            _result.append(
                [row["business_id"], row["name"], row["stars"], row["state"]])

        return _result

    def get_reviews_for_cousines(self):
        _result_cousines = []
        _result_reviews = []

        for _cousine in self._cousines:
            _cousine_reviews = self._cousines2business2reviews.loc[self._cousines2business2reviews['cousine'].isin([_cousine])]
            _cousine_reviews = list(_cousine_reviews['text'])

            _t = []
            for _r in _cousine_reviews:
                if len(str(_r).strip()) == 0:
                    _r = "none"
                _t.append(str(_r))
            _cousine_reviews = _t

            _cousine_reviews = " ".join(_cousine_reviews)

            if len(_cousine_reviews.strip()) > 0:
                _result_cousines.append(_cousine)
                _result_reviews.append(_cousine_reviews)

        return _result_cousines, _result_reviews

    def get_cousines_for_rest(self, _rest_id):
        _cousines = []

        _cousines = self._cousines2business2reviews.loc[self._cousines2business2reviews['business_id'].isin([
            _rest_id])]

        _cousines = _cousines['cousine'].unique()

        _cousines = list(_cousines)

        return _cousines

    def get_datasets(self):
        onlyfiles = [f for f in listdir(config.path2datasets) if isfile(
            join(config.path2datasets, f))]

        _datasets = []
        for _file in onlyfiles:
            filename, file_extension = os.path.splitext(
                _file)

            if file_extension == ".json":
                _datasets.append(_file)

        return _datasets

    def save_dataset(self, _file):
        file = _file
        file.save(os.path.join(config.path2datasets, file.name))
