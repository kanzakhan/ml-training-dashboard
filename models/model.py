"""
An RNNTextClassifier model.

IMPORTANT: You do not need to modify this code but you are
welcome to refer to it, especially regarding input types.

"""

from flambe.nlp.classification import TextClassifier
from flambe.nn import Embeddings, RNNEncoder, Embedder, SoftmaxLayer, LastPooling


class RNNTextClassifier(TextClassifier):
    """This class creates a typical text classifier architecture"""

    def __init__(self,
                 vocab_size: int,
                 num_labels: int,
                 embedding_dim: int = 300,
                 n_layers: int = 2,
                 rnn_type: str = 'sru',
                 hidden_size: int = 128,
                 rnn_dropout: float = 0.3,
                 embedding_dropout: float = 0.3):
        """Initialize the RNNTextClassifier.

        Parameters
        ----------
        vocab_size : int
            The number of tokens in the vocabulary
        num_labels : int
            The number of labels to classify over.
        embedding_dim : int, optional
            The embedding dimension, by default 300
        rnn_type: str, optional
            One of ['sru', 'lstm', 'gru']
        n_layers : int, optional
            The number of layers in the RNN, by default 2
        hidden_size : int, optional
            The hidden dimension of the RNN, by default 128
        rnn_dropout : float, optional
            Dropout probability for the rnn.
            Should be a number between 0 and 1, by default 0.3.
        embedding_dropout : float, optional
            Dropout probability for the embedding layer.
            Should be a number between 0 and 1, by default 0.3.

        """
        # DO NOT MODIFY
        embeddings = Embeddings(num_embeddings=vocab_size,
                                embedding_dim=embedding_dim)
        encoder = RNNEncoder(input_size=embedding_dim,
                             n_layers=n_layers,
                             hidden_size=hidden_size,
                             rnn_type=rnn_type,
                             dropout=rnn_dropout)
        embedder = Embedder(embedding=embeddings,
                            embedding_dropout=embedding_dropout,
                            encoder=encoder,
                            pooling=LastPooling())
        output_layer = SoftmaxLayer(input_size=hidden_size,
                                    output_size=num_labels)
        super().__init__(embedder=embedder, output_layer=output_layer)
