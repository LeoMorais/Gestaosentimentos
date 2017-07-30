# -*- Mode: Python; coding: utf-8 -*-

from __future__ import print_function

import os, csv
import sys
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from keras import backend as K
from keras.models import model_from_json


BASE_DIR = (r'C:\Users\leonardo\Desktop\ProjetoDeep\Glove')
GLOVE_DIR = BASE_DIR + r'\glove.6B'
TEXT_DATA_DIR = BASE_DIR + r'\emotion'
MAX_SEQUENCE_LENGTH = 1000
#MAX_NB_WORDS = 20000
MAX_NB_WORDS = 400000
EMBEDDING_DIM = 300
VALIDATION_SPLIT = 0.2

# first, build index mapping words in the embeddings set
# to their embedding vector

print('Indexing word vectors.')
cont1 = 0
embeddings_index = {}
f = open(os.path.join(BASE_DIR, r'wiki.pt.vec'), encoding='utf8')
for line in f:
    values = line.split()
    word = values[0]
    try:
        coefs = np.asarray(values[1:], dtype='float32')
    except:
        pass
    embeddings_index[word] = coefs
    print(cont1)
    cont1 = cont1 + 1
f.close()

print('Found %s word vectors.' % len(embeddings_index))

# second, prepare text samples and their labels
print('Processing text dataset')


dic = {'Neutro': '1', 'Negativo': '2', 'Positivo': '3'}
cont = 0
texts = []  # list of text samples
labels_index = {}  # dictionary mapping label name to numeric id
labels = []  # list of label ids
with open(r'C:\Users\leonardo\Desktop\ProjetoDeep\Glove\positive2.csv', 'r', encoding='utf8', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar=' ')
    for linha in reader:
        print(cont)
        label= str(linha[1])
        label_id = dic[label]
        text = linha[0]
        texts.append(text)
        labels.append(label_id)
        cont = cont + 1
        
csvfile.close()
print('Found %s texts.' % len(texts))

# finally, vectorize the text samples into a 2D integer tensor
tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels = to_categorical(np.asarray(labels))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

# split the data into a training set and a validation set
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])

x_train = data[:-num_validation_samples]
y_train = labels[:-num_validation_samples]
x_val = data[-num_validation_samples:]
y_val = labels[-num_validation_samples:]

print('Preparing embedding matrix.')

# prepare embedding matrix
num_words = min(MAX_NB_WORDS, len(word_index))
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NB_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

# load pre-trained word embeddings into an Embedding layer
# note that we set trainable = False so as to keep the embeddings fixed
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

print('Training model.')

# train a 1D convnet with global maxpooling
sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
print("Sequence aqui = ",sequence_input)
print("Embeded aqui = ",embedded_sequences)
x = Conv1D(128, 5, activation='relu')(embedded_sequences)
x = MaxPooling1D(5)(x)
x = Conv1D(128, 5, activation='relu')(x)
x = MaxPooling1D(5)(x)
x = Conv1D(128, 5, activation='relu')(x)
x = MaxPooling1D(35)(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
#preds = Dense(len(labels_index), activation='softmax')(x)
preds = Dense(4, activation='softmax')(x)
print(preds)

model = Model(sequence_input, preds)
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])

model.fit(x_train, y_train,
          batch_size=15,
          epochs=25,
          validation_data=(x_val, y_val))

score = model.evaluate(x_val, y_val, verbose=0)
print('Teste loss:', score[0])
print('Teste accuracy:', score[1])

#Salvando modelo
model_json = model.to_json()
with open("model2.json","w") as json_file:
    json_file.write(model_json)
#serializae 
model.save_weights("model2.h5")

    
K.clear_session()
