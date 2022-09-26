import pickle


def save_model(model, file_path):
    pickle.dump(model, open(file_path, 'wb'))


def load_model(file_path):
    return pickle.load(open(file_path, 'rb'))
