from flask import Flask, request, redirect, url_for, render_template
import logging
import config
import utils.ada as ada
import os

# import controllers for views
from controllers.topics_page_controller import TopicsPageController
from controllers.cousines_page_controller import CousinesPageController
from controllers.rests_page_controller import RestsPageController
from controllers.data_manager_page_controller import DataManagerPageController

app = Flask(__name__)
app.secret_key = 'super secret key'

app.debug = config.DEBUG
ALLOWED_EXTENSIONS = {'json'}


def get_model_name():
    _model_name = active_model + active_topics_number
    return _model_name


def set_active_topic(_value):

    global active_topic
    global active_topic_number

    active_topic = _value
    active_topic_number = ada.get_topic_number(active_topic)


def set_active_cousine(_value):

    global active_cousine
    active_cousine = _value


def set_active_dataset(_value):

    global active_dataset
    active_dataset = _value


def set_sim_function(_value):

    global active_sim_function
    active_sim_function = _value


def set_model(_model, _topics, _words):

    global active_model
    global active_topics_number
    global active_words_number

    active_model = _model
    active_topics_number = _topics
    active_words_number = _words

    set_active_topic(None)


def page_route(_source, _target):

    if _target == 'topics':
        set_active_topic(None)
        set_active_cousine(None)
    if _target == 'cousines':
        if _source == 'cousines' or _source == 'topics':
            set_active_cousine(None)
        return redirect(url_for('choose_cousine'))
    if _target == 'rests':
        return redirect(url_for('choose_rest'))

    return redirect(url_for('choose_topic'))


def reload_data(_model_name, active_dataset):
    global tpc
    global cpc
    global rpc

    tpc.reload(_model_name, active_dataset)
    cpc.reload(_model_name, active_dataset)
    rpc.reload(_model_name, active_dataset)


@app.route('/', methods=['GET', 'POST'])
def choose_topic():

    if request.method == 'POST':

        _action = request.form['action']
        _value = request.form['value']

        if _action == 'process':

            tpc.process_topics_mining()

            _model_name = get_model_name()
            reload_data(_model_name, active_dataset)

        if _action == 'set_active_topic':
            set_active_topic(_value)

        if _action == 'set_model':
            _model = _value
            _topics = request.form['topics']
            _words = request.form['words']
            set_model(_model, _topics, _words)

            reload_data(get_model_name(), active_dataset)

        if _action == 'goto':
            return page_route("topics", _value)

    return render_template('topics.html', view="topics", model=active_model, topics_number=active_topics_number, words_number=active_words_number,
                           topics_data=tpc.topics(active_topic, int(active_words_number)), rest_number=rpc.rest_number(active_topic_number, active_cousine), cousine_number=cpc.cousine_number(active_topic_number), review_number=tpc.review_number())


@app.route('/cousines', methods=['GET', 'POST'])
def choose_cousine():

    if request.method == 'POST':

        _action = request.form['action']
        _value = request.form['value']

        if _action == 'set_active_cousine':
            set_active_cousine(_value)

        if _action == 'set_sim_function':
            set_sim_function(_value)

        if _action == 'process':
            pass

        if _action == 'goto':
            return page_route("cousines", _value)

    return render_template('cousines.html', view="cousines", _sim_function=active_sim_function, cousines_data=cpc.cousines(active_topic_number, active_cousine, active_sim_function), rest_number=rpc.rest_number(active_topic_number, active_cousine), cousine_number=cpc.cousine_number(active_topic_number), review_number=tpc.review_number())

@app.route('/rests', methods=['GET', 'POST'])
def choose_rest():

    if request.method == 'POST':

        _action = request.form['action']
        _value = request.form['value']

        if _action == 'goto':
            return page_route("rests", _value)

    return render_template('rests.html', view="rests", _data=rpc.rests(active_topic_number, active_cousine), rest_number=rpc.rest_number(active_topic_number, active_cousine), cousine_number=cpc.cousine_number(active_topic_number), review_number=tpc.review_number())


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/data_manager', methods=['GET', 'POST'])
def choose_data():

    if request.method == 'POST':

        _action = request.form['action']

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                pass
            if file and allowed_file(file.filename):
                dpc.upload_dataset(file)
        else:
            _value = request.form['value']

            if _action == 'goto':
                return page_route("rests", _value)

            if _action == 'set_dataset':
                _model = _value
                set_active_dataset(_value)

                _model_name = get_model_name()
                reload_data(_model_name, active_dataset)

                return page_route("data_manager", "topics")

    return render_template('data_manager.html', view="datasets", _datasets=dpc.get_datasets(), _dataset_name=active_dataset, rest_number=rpc.rest_number(active_topic_number, active_cousine), cousine_number=cpc.cousine_number(active_topic_number), review_number=tpc.review_number())


# default values for initialization on the first run
active_cousine = None
active_topic = None
active_topic_number = None

active_sim_function = "sim_ed"

active_model = "LDA"
active_topics_number = "10"
active_words_number = "10"
active_dataset = "yelp_academic_dataset_review.json"

set_active_dataset(active_dataset)

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)

tpc = TopicsPageController(get_model_name(), active_dataset)
cpc = CousinesPageController(get_model_name(), active_dataset)
rpc = RestsPageController(get_model_name(), active_dataset)
dpc = DataManagerPageController(active_dataset)
