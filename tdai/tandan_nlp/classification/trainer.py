from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from .preprocessor import pre_processing


def get_train_data(sentences, labels):
    x_train, y_train = [], []
    for i, sentence in enumerate(sentences):
        x_train.append(pre_processing(sentence))
        y_train.append(labels[i])
    return x_train, y_train


def get_model(vectorizer=CountVectorizer(), transformer=TfidfTransformer(), classifier=MultinomialNB()):
    return Pipeline([('vectorizer', vectorizer),
                     ('transformer', transformer),
                     ('classifier', classifier)])


def training(model, x_train, y_train):
    model.fit(x_train, y_train)
    return model
