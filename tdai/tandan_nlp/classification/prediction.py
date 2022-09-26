from sklearn.metrics import accuracy_score

from .preprocessor import pre_processing


def accuracy_intent(model, texts, labels):
    predict = model.predict(texts)
    return accuracy_score(predict, labels)


def predict_proba_intent(text, model):
    text = pre_processing(text)
    text = [text]
    rs = model.predict_proba(text)
    return rs[0]


def predict_intent(text, model):
    text = pre_processing(text)
    text = [text]
    rs = model.predict(text)
    return rs[0]

