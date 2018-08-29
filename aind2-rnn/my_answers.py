import re
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation


def window_transform_series(series, window_size):
    '''
    Transform input series into a set of input/output pairs using the given
    window size

    :param series: numpy array of input series
    :param window_size: window size for transformation
    :return: tuple of the input of a shape (num. of samples, window_size)
             and the output of a shape (num. of samples). num_of_samples
             is equal to len(series) - window_size
    '''
    # containers for input/output pairs
    series_len = len(series)
    X = [series[i : i + window_size] for i in range(0, series_len - window_size)]
    y = [series[i] for i in range(window_size, series_len)]

    # reshape each
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y), 1)

    return X, y


def build_part1_RNN(window_size):
    '''
    Build RNN (using LSTM cell) to perform regression on time series input/output data

    :param windows_size: window size of the input
    :return: Keras model
    '''
    num_hidden_units = 5

    model = Sequential()
    model.add(LSTM(num_hidden_units, input_shape=(window_size, 1)))
    model.add(Dense(1))
   
    return model


def cleaned_text(text):
    '''
    Return the text input with only ascii lowercase and the punctuation given below included

    :param text: original text
    :return: cleaned text
    '''
    punctuation = ['!', ',', '.', ':', ';', '?']

    # make all lower case
    text = text.lower()

    # put all characters into unwanted characters
    unwanted_characters = set(text)
    unwanted_characters = ''.join(unwanted_characters)

    # remove punctuation from unwanted characters
    for char in unwanted_characters:
        if char in punctuation or char == ' ':
            unwanted_characters = unwanted_characters.replace(char, '')

    # remove letters and numbers from unwanted characters
    unwanted_characters = re.sub('[A-Za-z]+', '', unwanted_characters)

    # remove unwanted characters from the text
    for char in unwanted_characters:
        text = text.replace(char, '')
   
    return text


def window_transform_text(text, window_size, step_size):
    '''
    Transforms the input text and window size into a set of input/output
    pairs for use with our RNN model

    :param text: original text
    :param window_size: window size for transformation
    :param step_size: step size for the transformation
    :return: tuple of the input and output lists
    '''
    # containers for input/output pairs
    text_len = len(text)
    inputs = [text[i : i+window_size] for i in range(0, text_len - window_size, step_size)]
    outputs = [text[i] for i in range(window_size, text_len, step_size)]

    return inputs, outputs


def build_part2_RNN(window_size, num_chars):
    '''
    Build RNN (using LSTM cell) to predict a next character given the input text

    :param windows_size: window size of the input
    :param num_chars: number of unique characters in the training set
    :return: Keras model
    '''
    num_hidden_units = 200

    model = Sequential()
    model.add(LSTM(num_hidden_units, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))

    return model
