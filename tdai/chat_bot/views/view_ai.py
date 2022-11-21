import pickle

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression

from chat_bot.models import Sentence, Intent, IntentModel
from chat_bot.utils import intent_model_helper
from tandan_nlp.classification import trainer as clf_trainer, prediction as clf_prediction
from tandan_nlp.ner import prediction_bert as ner_prediction

@csrf_exempt
def test_nlp(request):
    if request.method == 'GET':
        return render(request, 'test_nlp/index.html')
    if request.method == 'POST':
        sentence = request.POST.get('sentence')
        text = sentence.strip()
        # predict intent
        intent_model = intent_model_helper.get_latest_model()
        reliability = clf_prediction.predict_proba_intent(text, intent_model)
        _intents = intent_model.classes_
        rs_intent = []
        for i, intent in enumerate(_intents):
            rs_intent.append({
                'intent': intent,
                'reliability': round(reliability[i] * 100, 2)
            })
        rs_intent = sorted(rs_intent, key=lambda x: x.get('reliability'), reverse=True)
        if len(rs_intent) > 4:
            rs_intent = rs_intent[:4]
            
        rs_entity = ner_prediction.predict_entity(text)

        data = {
            'status': 200,
            'sentence': text,
            'intents': rs_intent,
            'entities': rs_entity
        }
        return render(request, 'test_nlp/index.html', data)


@csrf_exempt
def speech_to_text(request):
    return render(request, 'speech_to_text.html')
