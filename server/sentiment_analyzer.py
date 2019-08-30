# Uncomment and execute once - this is used to downgrade the pip version to one that doesn't cause an exception in keras
# https://github.com/tensorflow/tensorflow/issues/28102#issuecomment-487612628
#!pip install numpy==1.16.2

import logging
logging.getLogger('tensorflow').disabled = True

import warnings
# Importing numpy and Keras (specifically TensorFlow) causes printing of deprecation warnings.
# We suppress the warnings by filtering and by disabling the tensorflow logger and 
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import numpy as np
    import keras

from enum import Enum

MODEL_1_PATH = r"model_1.hdf5"
MODEL_2_PATH = r"model_2.hdf5"
MODEL_3_PATH = r"model_3.hdf5"
MODEL_4_PATH = r"model_4.hdf5"
MODEL_5_PATH = r"model_5.hdf5"

# Pre-loading models
models = []
print("Loading model 1")
models.append(keras.models.load_model(MODEL_1_PATH))
print("Loading model 2")
models.append(keras.models.load_model(MODEL_2_PATH))
print("Loading model 3")
models.append(keras.models.load_model(MODEL_3_PATH))
print("Loading model 4")
models.append(keras.models.load_model(MODEL_4_PATH))
print("Loading model 5")
models.append(keras.models.load_model(MODEL_5_PATH))

MAX_LEN = 1000
OOV_WORD_INDEX = 2

class Label(Enum):
    POSITIVE = 0
    NEGATIVE = 1

def predict_review_label(review, model):
    words = review.split()
    word_index = keras.datasets.imdb.get_word_index()
    my_index = []
    for word in words:
        if word in word_index:
            my_index.append(word_index[word])
        else:
            my_index.append(OOV_WORD_INDEX)
    seq = np.array(my_index)
    padded_seq = keras.preprocessing.sequence.pad_sequences([seq], maxlen=MAX_LEN, dtype='int32', padding='pre')
    return model.predict_classes(padded_seq)

def predict_review_prob(review, model):
    words = review.split()
    word_index = keras.datasets.imdb.get_word_index()
    my_index = []
    for word in words:
        if word in word_index:
            my_index.append(word_index[word])
        else:
            my_index.append(OOV_WORD_INDEX)
    seq = np.array(my_index)
    padded_seq = keras.preprocessing.sequence.pad_sequences([seq], maxlen=MAX_LEN, dtype='int32', padding='pre')
    return model.predict_proba(padded_seq)

def getProbAndLabel(review):
    print("\n======================================================\n")
    
    predicted_labels = []
    predicted_probs = []
    for i in range(len(models)):
        print("Testing model {0} out of {1}".format(i+1, len(models)))
        try:
            predicted_labels.append(predict_review_label(review, models[i])[0][0])
            prob = predict_review_prob(review, models[i])[0][0]
            # The probability is for the label 1, so we need to adjust it if the label is 0
            if predicted_labels[-1] == 0:
                prob = 1 - prob
            predicted_probs.append(prob)
            print("label: {}".format(Label(predicted_labels[-1]).name))
            print("prob: {}".format(predicted_probs[-1]))
        except Exception as e:
            print("Unknown word:")
            print(e)
            pass
    final_label = Label.POSITIVE \
        if predicted_labels.count(Label.POSITIVE.value) > predicted_labels.count(Label.NEGATIVE.value) \
        else Label.NEGATIVE
    print("Final label: {}".format(Label(final_label).name))
    
    # Calculate the average label probability, using only the probabilities of the
    # chosen label.
    final_prob = 0
    counted_probs = 0
    for i in range(len(predicted_probs)):
        if predicted_labels[i] == final_label.value:
            final_prob += predicted_probs[i]
            counted_probs += 1
    final_prob /= float(counted_probs)

    print("Final prob: {}".format(final_prob))

    reviewProbAndLabel = {'final_label' : Label(final_label).name, "final_prob" : final_prob}
    return reviewProbAndLabel

if __name__ == '__main__':
    # 1 -> good, 2 -> good, 3 -> bad, 4 -> bad, 5 -> bad, 6 -> good  
    reviews = [
    """Hobbs and Shaw is fresh and feels like a standalone. You really don't need to watch the other films to enjoy it, but if you want to learn the history off Hobbs and Shaw then feel free to go back and watch the last 3 installments. There is no Dominic Toretto and his crew. Fresh new story, characters, and theme. Vanessa Kirby shines as Hattie, Idris Elba shines as black superman, Hobbs and Shaw shines, Ezia Gonzalez shines as Madam M. I really love that they have put more focus into Hobbs and his daughter Samantha's relationship. I also love that they're teasing a romantic relationship between Luke Hobbs and Hattie Shaw which happens to be the sister of Owen and Deckard. Btw she kicks major behind. There are two BIG cameos in this film, a bunch of easter eggs, and a crazy fight sequence that takes place in Samoa, Hobbs homeland. It's a really good action-packed heartfelt film and I think you'd enjoy it. 8/10 The summer is almost over so sit back and enjoy Hobbs and Shaw for what it is.""",
    """Just saw it, Great movie with Great chemistry between Jason and the Rock. The movie was packed with a lot of action Great lines and Some wonderful suprises. A must see for the fast and furious fans!""",
    """No story. And Nothing new n too boring. Super Villain was super human but hob n shaw were like robots who cant get injured even. Its total money waste.""",
    """This is a seriously bad movie. I liked the look of the trailers but the movie itself was overlong and bad.""",
    """Its was just waste of time. Simple words. A display of pathetic movie, with all the hype created. Pity!""",
    """Great job from fast and furious must watch in cinema only to enjoy the sounds !!! Amazing night""",
    ]

    for review in reviews:
    #review = "Hobbs and Shaw is fresh and feels like a standalone. You really don't need to watch the other films to enjoy it, but if you want to learn the history off Hobbs and Shaw then feel free to go back and watch the last 3 installments. There is no Dominic Toretto and his crew. Fresh new story, characters, and theme. Vanessa Kirby shines as Hattie, Idris Elba shines as black superman, Hobbs and Shaw shines, Ezia Gonzalez shines as Madam M. I really love that they have put more focus into Hobbs and his daughter Samantha's relationship. I also love that they're teasing a romantic relationship between Luke Hobbs and Hattie Shaw which happens to be the sister of Owen and Deckard. Btw she kicks major behind. There are two BIG cameos in this film, a bunch of easter eggs, and a crazy fight sequence that takes place in Samoa, Hobbs homeland. It's a really good action-packed heartfelt film and I think you'd enjoy it. 8/10 The summer is almost over so sit back and enjoy Hobbs and Shaw for what it is."
        print(getProbAndLabel(review))
