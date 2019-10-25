'''
App contains the Flask Web Server, url routing, and all of the API endpoints
'''
import json
from flask import Flask, request, render_template, jsonify
from utils.experiment_manager import get_progress, start_experiment, validate_form_data, get_default_params
import logging

# default values to show in GUI's experiment params form
DEFAULT_HYPER_PARAMS = get_default_params()

app = Flask(__name__)

# Application Routes:
@app.route('/')
def home():
    return render_template('index.html',
                            defaults=DEFAULT_HYPER_PARAMS,
                            experiment_progress=get_progress())

# REST API Endpoints:
# API endpoint for app's front end to retrieve experiment progress
@app.route('/progress-status')
def progress_status():
    return {"progress": get_progress()}, 200

# API endpoint for app's front end to send hyperparamters as query string
@app.route('/experiment-params', methods=['GET'])
def experiment_params():

    data_is_valid, form = validate_form_data(request)

    # send error back to user
    if not(data_is_valid):
        return jsonify(form), 416

    start_experiment(form['experiment_name'],
                        form['max_steps'],
                        form['iter_per_step'],
                        form['embedding_dim'],
                        form['n_layers'],
                        form['rnn_type'],
                        form['hidden_size'],
                        form['rnn_dropout'],
                        form['embedding_dropout'])

    return jsonify(form), 200


if __name__ == '__main__':
    # Supress API calls in terminal:
    log = logging.getLogger('werkzeug')
    log.disabled = True

    # before app launches, tensorboard starts from bash script
    print('ASAPP Challenge Project running at: http://localhost:5000/')
    print('Tensorboard running at http://localhost:6006')
    app.run(debug=True)
