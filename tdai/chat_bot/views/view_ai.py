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


@csrf_exempt
def speech_to_text(request):
    return render(request, 'speech_to_text.html')
