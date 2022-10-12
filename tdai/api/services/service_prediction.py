import numpy as np
import pickle

from chat_bot.models import IntentModel
from tandan_nlp.classification import prediction as clf_prediction
from tandan_nlp.ner import prediction_bert as ner_prediction

def classification_text(text):
    thres_scores = 0.05
    intent_model = get_latest_model()
    intents = intent_model.classes_
    scores_int = clf_prediction.predict_proba_intent(text, intent_model)
    max_scores_int = np.max(scores_int)

    if max_scores_int > thres_scores:
        intent = intents[np.argmax(scores_int)]
    else:
        return None
    return intent

def predict_entity(sentence):
    rs_entity = ner_prediction.predict_entity(sentence)
    return rs_entity

def get_latest_model():
    intent_model_dumps = IntentModel.objects.order_by('created_time')
    intent_model_dump = intent_model_dumps[len(intent_model_dumps) - 1]
    return pickle.loads(intent_model_dump.data)