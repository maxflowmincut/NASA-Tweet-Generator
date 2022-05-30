
import re
import numpy as np
import tensorflow as tf
from tensorflow import keras


def sample(preds, temperature=1.0):
    '''Samples an index from a probability array'''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_w_seed(sentence, diversity, model, input_size):
    '''Generates seed from model'''

    char_indices = {' ': 0, '!': 1, '"': 2, '#': 3, '$': 4, '%': 5, '&': 6, "'": 7, '(': 8, ')': 9, '*': 10,
                    '+': 11, ',': 12, '-': 13, '.': 14, '/': 15, '0': 16, '1': 17, '2': 18, '3': 19, '4': 20,
                    '5': 21, '6': 22, '7': 23, '8': 24, '9': 25, ':': 26, ';': 27, '=': 28, '?': 29, '@': 30,
                    '[': 31, ']': 32, '_': 33, 'a': 34, 'b': 35, 'c': 36, 'd': 37, 'e': 38, 'f': 39, 'g': 40,
                    'h': 41, 'i': 42, 'j': 43, 'k': 44, 'l': 45, 'm': 46, 'n': 47, 'o': 48, 'p': 49, 'q': 50,
                    'r': 51, 's': 52, 't': 53, 'u': 54, 'v': 55, 'w': 56, 'x': 57, 'y': 58, 'z': 59}

    indices_char = {v: k for k, v in char_indices.items()}

    generated = sentence

    for i in range(160-input_size):
        x_pred = np.zeros((1, input_size, 60))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

    return generated


def validate_seed(seed, input_size):
    if len(seed) < input_size:
        seed = seed + ((input_size-len(seed)) * " ")
    return seed[:input_size].lower()


def validate_text(text):
    return re.sub('\s+', ' ', text)


def generate(seed, diversity=0.4, path="src/model_display/model.h5", input_size=40):
    model = keras.models.load_model(path)
    seed = validate_seed(seed, input_size)
    text = generate_w_seed(seed, diversity, model, input_size)
    text = validate_text(text)
    return text
