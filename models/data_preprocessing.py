# system libs
import json

# additional libs
import pandas as pd
from gensim.parsing.preprocessing import strip_punctuation, remove_stopwords

# project libs
import config


class DataProcessor():

    dataset_name = ""

    def process_business_raw_data(self):

        categories = {}
        cat2rid = {}

        _business = []
        _cousine2business = []

        print("Rest data processing start...")

        with open(config.path2raw_buisness, 'r') as f:
            _lines = f.readlines()

            for line in _lines:

                business_json = json.loads(line)
                bjc = business_json['categories']

                if config.r in bjc:
                    if len(bjc) > 1:
                        restaurant_id = business_json['business_id']
                        stars = business_json['stars']
                        name = business_json['name']
                        review_count = business_json['review_count']
                        state = business_json['state']
                        address = business_json['full_address']

                        _business.append({'business_id': restaurant_id, 'name': name, 'stars': stars,
                                            'state': state, 'review_count': review_count})

                        for cat in bjc:
                            if cat == config.r:
                                continue

                            if cat in cat2rid:
                                cat2rid[cat].append(restaurant_id)
                            else:
                                cat2rid[cat] = [restaurant_id]

                            _cousine2business.append(
                                {'cousine': cat, 'business_id': restaurant_id})

            print("Saving restaurant data to CVS...")

            _business = pd.DataFrame(_business)
            _business.to_csv(config.path2data +
                             self.dataset_name + "." + config.path2business)

            _cousine2business = pd.DataFrame(_cousine2business)
            _cousine2business.to_csv(
                config.path2data + self.dataset_name + "." + config.path2cousines2business)

            # clearing from memory
            rest2rate = None
            _business = None
            _cousines = None
            _cousine2business = None
            _lines = None

            print("Rest data pre-processing DONE")

    def process_review_raw_data(self):

        print("Review data pre-processing start...")

        _reviews = []

        with open(config.path2datasets + self.dataset_name, 'r') as f:
            for line in f.readlines():
                review_json = json.loads(line)

                _business_id = review_json['business_id']
                _review_id = review_json['review_id']
                _stars = review_json['stars']
                _text = review_json['text']

                # remove punctuation
                _text = strip_punctuation(_text)
                _text = remove_stopwords(_text)
                _text = _text.lower()

                _reviews.append(
                    {'review_id': _review_id, 'business_id': _business_id, 'stars': _stars, 'text': _text})

        _reviews = pd.DataFrame(_reviews)
        _reviews.to_csv(config.path2data +
                        self.dataset_name + "." + config.path2reviews)
        _reviews = None

        print("Review data pre-processing DONE")

    def process_raw_data(self, _active_dataset):

        self.dataset_name = _active_dataset

        print("Starting data pre-processing...")

        self.process_business_raw_data()
        self.process_review_raw_data()

        print("Data pre-processing DONE")
