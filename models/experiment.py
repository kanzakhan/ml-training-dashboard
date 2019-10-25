'''
This file contains run_experiment used to launch the RNN Text Classification
training. If no params are passed to run_experiment, then it will run with the
default values provided in utils/default_hyper_params.json.
'''
import torch
import json

from tqdm import tqdm

from flambe.logging import TrialLogging
from flambe.field import TextField, LabelField
from flambe.sampler import BaseSampler
from flambe.learn import Trainer
from flambe.metric import Accuracy
from flambe.nlp.classification import SSTDataset

from models.model import RNNTextClassifier
import utils.experiment_manager as em

DEFAULT_HYPER_PARAMS = em.get_default_params()
TENSORBOARD_DIR = './scratch/'

def run_experiment(name=DEFAULT_HYPER_PARAMS['experiment_name'],
                    max_steps=DEFAULT_HYPER_PARAMS['max_steps'],
                    iter_per_step=DEFAULT_HYPER_PARAMS['iter_per_step'],
                    embedding_dim=DEFAULT_HYPER_PARAMS['embedding_dim'],
                    n_layers=DEFAULT_HYPER_PARAMS['n_layers'],
                    rnn_type=DEFAULT_HYPER_PARAMS['rnn_type'],
                    hidden_size=DEFAULT_HYPER_PARAMS['hidden_size'],
                    rnn_dropout=DEFAULT_HYPER_PARAMS['rnn_dropout'],
                    embedding_dropout=DEFAULT_HYPER_PARAMS['embedding_dropout']
                ):
    # start off experiment progress at 0
    em.write_progress(0)
    print('*********')
    print(name)
    print(type(name))

    # Dataset
    dataset = SSTDataset(transform={'text': TextField(), 'label': LabelField()})

    # Model - takes params from front end GUI or from defaults in json
    model = RNNTextClassifier(vocab_size=dataset.text.vocab_size,
                              num_labels=dataset.label.vocab_size,
                              embedding_dim=embedding_dim,
                              n_layers=n_layers,
                              rnn_type=rnn_type,
                              hidden_size=hidden_size,
                              rnn_dropout=rnn_dropout,
                              embedding_dropout=embedding_dropout)

    # Trainer
    trainer = Trainer(dataset=dataset,
                      model=model,
                      train_sampler=BaseSampler(),
                      val_sampler=BaseSampler(),
                      loss_fn=torch.nn.NLLLoss(),
                      metric_fn=Accuracy(),
                      optimizer=torch.optim.Adam(params=model.trainable_params),
                      max_steps=max_steps,  # Total number of times to evaluate the model
                      iter_per_step=iter_per_step)  # Number of training iterations between steps

    # Run training
    current_iter_num = 0
    total_iters = max_steps * iter_per_step
    continue_ = True

    with TrialLogging(log_dir=TENSORBOARD_DIR+name,
                      verbose=False,
                      console_prefix=name,
                      capture_warnings=True):
        with tqdm(total=total_iters) as pbar:
            while continue_:
                continue_ = trainer.run()  # returns a boolean indicating if you should keep going
                # Update CLI progress bar
                pbar.update(iter_per_step)  # N iterations per step

                # Update progress data in DB to reflect updates on GUI
                current_iter_num += iter_per_step
                em.write_progress(int(current_iter_num / total_iters * 100))


if __name__ == '__main__':
    run_experiment()
