import json
from services.topics_service import TopicsService
import utils.ada as ada


class TopicsPageController():

    topic_service = None
    _active_topic = None

    def __init__(self, _model_name, _active_dataset):
        """
        Constructor
        @params:
            _model_name     - Required  : name of active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.reload(_model_name, _active_dataset)

    def reload(self, _model_name, _active_dataset):
        """
        Reload data for defined topic model and active dataset
        @params:
            _model_name     - Required  : name of the active topic model (Str)
            _active_dataset - Required  : name of active dataset (Str)
        """

        self.topic_service = TopicsService(_model_name, _active_dataset)

    def topics(self, _active_topic, _words_number):
        """
        Return a list of topics
        @params:
            _active_topic     - Required  : name of active topic (Str)
            _words_number     - Required  : number of words in topic to show (Int)
        """

        _data = []
        _topics = self.topic_service.get_topics(_words_number)

        for _topic in _topics:

            _topic_words = []
            for _word in _topic[1]:
                _value = int(_word[1] * 10000)

                if _active_topic is not None:
                    if ada.get_topic_name(_topic[0]) == _active_topic:
                        _topic_words.append({"name": _word[0], "value": _value, "color": "1"})
                    else:
                        _topic_words.append({"name": _word[0], "value": _value})
                else:
                    _topic_words.append({"name": _word[0], "value": _value})

            _data.append({'name': ada.get_topic_name(_topic[0]), "children": _topic_words})

        return _data

    def review_number(self):
        """
        Return number of reviews
        @params:
        """

        return self.topic_service.get_review_number()

    def process_topics_mining(self):
        """
        Return number of reviews
        @params:
        """

        result = self.topic_service.process_topics_mining()
        return result
