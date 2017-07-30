# -*- Mode: Python; coding: utf-8 -*-

import numpy as np
import keras.models
from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
import sys
import keras.preprocessing.text
import os, csv
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from keras import backend as K
from keras.models import model_from_json
from keras.utils import np_utils
from keras.models import Sequential

# load json and create model
json_file = open('model2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(r'D:\App-SO\programmer\Perceptron\src\model2.h5')
print("Loaded model from disk")


text ="recebem mais doses da vacina contra febre amarela"
tokenizer = Tokenizer(num_words=400000)
tokenizer.fit_on_texts(text)
sequences = tokenizer.texts_to_sequences(text)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=1000)
print(data)


predict = loaded_model.predict(data, batch_size=1)
print(predict)
print(np.argmax(predict))




