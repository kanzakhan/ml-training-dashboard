'''
The experiment_manager contains utility functions that help to launch the
experiment thread, track experiment progress, and start the tensorboard process.
'''
import concurrent.futures
import subprocess
import json
import signal
import sys

from multiprocessing import Process, Queue

# relative paths within app
PROGRESS_DB_PATH = "utils/progress.db"
HYPER_PARAMS_PATH = "utils/default_hyper_params.json"

tensorboard_process = None
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# get progress written into file
def get_progress():
    return load_progress()

def load_progress():
    with open(PROGRESS_DB_PATH, "r") as read_file:
        return int(read_file.readline().strip('\n'))

# write the experiment progress to db
def write_progress(num):
    with open(PROGRESS_DB_PATH, "w") as write_file:
        write_file.write(str(num))

# Load default hyperparamter values from json
def get_default_params():
    with open(HYPER_PARAMS_PATH, "r") as read_file:
        return json.load(read_file)

# Check if params sent in http reuest are valid (positive)
def validate_form_data(request):

        # get form input from url query string  (e.g. ?max-steps=some-value)
        # convert numbers in string to int or float
        form = {
            "experiment_name": request.args.get('experiment-name'),
            "embedding_dim": int(request.args.get('embedding-dim')),
            "n_layers": int(request.args.get('n-layers')),
            "hidden_size": int(request.args.get('hidden-size')),
            "rnn_type": request.args.get('rnn-type').lower(),
            "rnn_dropout": float(request.args.get('rnn-dropout')),
            "embedding_dropout": float(request.args.get('embedding-dropout')),
            "max_steps": int(request.args.get('max-steps')),
            "iter_per_step": int(request.args.get('iter-per-step')),
        }

        if data_is_positive(form):
            return True, form
        else:
            return False, { "error": "ERROR: Integer values in form must be positive."}

# check that all int values in form are positive; float values positive by default
def data_is_positive(form):
    for key in form:
        if isinstance(form[key], int):
            if form[key] <= 0:
                 return False

    return True

# reset the experiment progress and start new experiment
def start_experiment(name,
                    max_steps,
                    iter_per_step,
                    embedding_dim,
                    n_layers,
                    rnn_type,
                    hidden_size,
                    rnn_dropout,
                    embedding_dropout):

    # execute call to run experiment asynchronously with the executor
    global executor
    from models.experiment import run_experiment

    # submit experiment job
    executor.submit(run_experiment,
                        name,
                        max_steps,
                        iter_per_step,
                        embedding_dim,
                        n_layers,
                        rnn_type,
                        hidden_size,
                        rnn_dropout,
                        embedding_dropout)
