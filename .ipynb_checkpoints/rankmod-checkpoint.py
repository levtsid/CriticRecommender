import numpy as np
import scipy as sp
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os, re, importlib, requests, time, tempfile, pprint, glob, imageio
import PIL
from typing import Dict, Text
from IPython import display
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn
from random import randint

import collections
from typing import Dict, List, Optional, Text, Tuple

import tensorflow_ranking as tfr
import tensorflow_recommenders as tfrs



class RankingModel(tfrs.Model):

  def __init__(self, loss):
    super().__init__()
    embedding_dimension = 32

    # Compute embeddings for users.
    self.user_embeddings = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
        vocabulary=namemin),
      tf.keras.layers.Embedding(len(namemin) + 2, embedding_dimension)
    ])

    # Compute embeddings for movies.
    self.movie_embeddings = tf.keras.Sequential([
      tf.keras.layers.StringLookup(
        vocabulary=revmin),
      tf.keras.layers.Embedding(len(revmin) + 2, embedding_dimension)
    ])

    # Compute predictions.
    self.score_model = tf.keras.Sequential([
      # Learn multiple dense layers.
      tf.keras.layers.Dense(256, activation="relu"),
      tf.keras.layers.Dense(64, activation="relu"),
      # Make rating predictions in the final layer.
      tf.keras.layers.Dense(1)
    ])

    self.task = tfrs.tasks.Ranking(
      loss=loss,
      metrics=[
        tfr.keras.metrics.NDCGMetric(name="ndcg_metric"),
        tf.keras.metrics.RootMeanSquaredError()
      ]
    )

  def call(self, features):
    # We first convert the id features into embeddings.
    # User embeddings are a [batch_size, embedding_dim] tensor.
    user_embeddings = self.user_embeddings(features["user_id"])

    # Movie embeddings are a [batch_size, num_movies_in_list, embedding_dim]
    # tensor.
    movie_embeddings = self.movie_embeddings(features["movie_title"])

    # We want to concatenate user embeddings with movie emebeddings to pass
    # them into the ranking model. To do so, we need to reshape the user
    # embeddings to match the shape of movie embeddings.
    list_length = features["movie_title"].shape[1]
    user_embedding_repeated = tf.repeat(
        tf.expand_dims(user_embeddings, 1), [list_length], axis=1)

    # Once reshaped, we concatenate and pass into the dense layers to generate
    # predictions.
    concatenated_embeddings = tf.concat(
        [user_embedding_repeated, movie_embeddings], 2)

    return self.score_model(concatenated_embeddings)

  def compute_loss(self, features, training=False):
    labels = features.pop("user_rating")

    scores = self(features)

    return self.task(
        labels=labels,
        predictions=tf.squeeze(scores, axis=-1),
    )