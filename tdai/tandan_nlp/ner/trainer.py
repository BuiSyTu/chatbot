from sklearn_crfsuite import CRF

from .feature_extractor import sent2features, sent2labels


def get_train_data(docs):
    x_train = [sent2features(s) for s in docs]
    y_train = [sent2labels(s) for s in docs]
    return x_train, y_train


def training(x_train, y_train):
    model = CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    model.fit(x_train, y_train)
    return model
