import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


def clean_data(path, input_size):
    '''Cleans CSV file of tweets for our model'''
    # Load tweets
    df = pd.read_csv(path, sep='delimiter',
                     header=None, engine='python')

    # Make all tweets lowercase and then removes tweets with links or less than 75 characters
    tweets = df[0].str.lower()
    tweets = tweets.map(lambda s: ' '.join(
        [x for x in s.split() if 'http' not in x]))
    tweets = tweets[tweets.map(len) > 75]

    # Removes emojis from tweets and get list of valid characters
    chars = sorted(list(set(''.join(tweets))))
    for c in chars[60:]:  # Everything after 'z'
        tweets = tweets.str.replace(c, '', regex=True)
    chars = sorted(list(set(''.join(tweets))))
    char_indices = dict((c, i) for i, c in enumerate(chars))

    # Cut tweets in sequences of input size characters
    maxlen = input_size
    step = 1
    sentences = []
    next_chars = []
    for x in tweets:
        for i in range(0, len(x) - maxlen, step):
            sentences.append(x[i: i + maxlen])
            next_chars.append(x[i + maxlen])

    #  Vectorize
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=bool)
    y = np.zeros((len(sentences), len(chars)), dtype=bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1

    return chars, maxlen, x, y


def build_model(chars, maxlen):
    '''Builds LSTM Model'''
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, len(chars)), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(len(chars), activation='softmax'))

    optimizer = tf.keras.optimizers.Adam()
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    return model


def fit_model(model, x, y, epochs):
    '''Fits model'''
    model.fit(x, y,
              batch_size=128,
              epochs=epochs)
    return model


def main():
    chars, maxlen, x, y = clean_data(path="data/data.csv", input_size=40)
    model = build_model(chars, maxlen)
    model = fit_model(model, x, y, epochs=300)
    model.save('model.h5')


if __name__ == "__main__":
    main()
